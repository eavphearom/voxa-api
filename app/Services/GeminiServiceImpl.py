import json
import logging
import time
from typing import Any
from urllib import error, request

from django.conf import settings

from app.Exceptions import ApplicationException
from app.Services.Contracts.GeminiService import GeminiService


logger = logging.getLogger(__name__)


class GeminiServiceImpl(GeminiService):
    RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
    RETRY_DELAYS_SECONDS = (1, 2, 4)
    MARKDOWN_SYSTEM_INSTRUCTION = """
You are a professional assistant. Always answer in clean GitHub-flavored Markdown.

Formatting rules:
- Preserve Markdown syntax as Markdown. Do not escape headings, bullets, tables, links, or code fences.
- Use Markdown headings for sections when helpful.
- Use bullet points for grouped details.
- Use numbered lists for step-by-step instructions.
- Use Markdown tables for tabular comparisons.
- Wrap every source code example in triple backticks with a language identifier.
- Keep answers readable, structured, and concise.

Code block example:
```python
print("Hello World")
```
""".strip()

    def generate_response(self, message: str, history: list[dict[str, Any]] | None = None) -> str:
        if not settings.GEMINI_API_KEY:
            raise ApplicationException("GEMINI_API_KEY is not configured")

        payload = self._build_payload(message, history or [])
        response_data = self._request_available_model(payload)
        return self._extract_text(response_data)

    def _request_available_model(self, payload: dict[str, Any]) -> dict[str, Any]:
        models = [settings.GEMINI_MODEL, *settings.GEMINI_FALLBACK_MODELS]
        last_error = "Gemini API request failed"
        for model in dict.fromkeys(models):
            try:
                return self._request_with_retries(model, payload)
            except ApplicationException as exc:
                last_error = str(exc)
                logger.warning("Gemini model %s failed: %s", model, exc)

        raise ApplicationException(last_error)

    def _request_with_retries(self, model: str, payload: dict[str, Any]) -> dict[str, Any]:
        last_error = "Gemini API request failed"
        for attempt in range(len(self.RETRY_DELAYS_SECONDS) + 1):
            try:
                return self._request_model(model, payload)
            except error.HTTPError as exc:
                last_error = self._format_http_error(exc)
                if exc.code not in self.RETRY_STATUS_CODES or attempt == len(self.RETRY_DELAYS_SECONDS):
                    break
                delay = self.RETRY_DELAYS_SECONDS[attempt]
                logger.warning("%s. Retrying in %s second(s).", last_error, delay)
                time.sleep(delay)
            except error.URLError:
                last_error = "Gemini API is unavailable"
                if attempt == len(self.RETRY_DELAYS_SECONDS):
                    break
                delay = self.RETRY_DELAYS_SECONDS[attempt]
                logger.warning("%s. Retrying in %s second(s).", last_error, delay)
                time.sleep(delay)

        raise ApplicationException(last_error)

    def _request_model(self, model: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={settings.GEMINI_API_KEY}"
        )

        api_request = request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with request.urlopen(api_request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    def _format_http_error(self, exc: error.HTTPError) -> str:
        try:
            error_data = json.loads(exc.read().decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return f"Gemini API request failed with status {exc.code}"

        message = error_data.get("error", {}).get("message")
        if message:
            return f"Gemini API request failed: {message}"
        return f"Gemini API request failed with status {exc.code}"

    def _build_payload(self, message: str, history: list[dict[str, Any]]) -> dict[str, Any]:
        contents = []
        for item in history[-20:]:
            role = "model" if item.get("role") == "assistant" else "user"
            text = str(item.get("content", "")).strip()
            if not text:
                continue
            if not contents and role != "user":
                continue
            if contents and contents[-1]["role"] == role:
                contents[-1]["parts"][0]["text"] = (
                    f"{contents[-1]['parts'][0]['text']}\n\n{text}"
                )
                continue
            contents.append(
                {
                    "role": role,
                    "parts": [{"text": text}],
                }
            )

        if contents and contents[-1]["role"] == "user":
            contents.pop()
        contents.append({"role": "user", "parts": [{"text": message}]})
        return {
            "systemInstruction": {
                "parts": [{"text": self.MARKDOWN_SYSTEM_INSTRUCTION}],
            },
            "contents": contents,
        }

    def _extract_text(self, response_data: dict[str, Any]) -> str:
        candidates = response_data.get("candidates", [])
        if not candidates:
            raise ApplicationException("Gemini API returned no response")

        parts = candidates[0].get("content", {}).get("parts", [])
        text_parts = [part.get("text", "") for part in parts if part.get("text")]
        response_text = "\n".join(text_parts)
        if not response_text.strip():
            raise ApplicationException("Gemini API returned an empty response")
        return response_text
