from __future__ import annotations

from typing import Dict, List, Tuple

import base64
from io import BytesIO
from typing import Any

from app.DTO.ChatDTO import ChatMessageCreateDTO
from app.DTO.ChatMessageAttachmentDTO import ChatMessageAttachmentDTO
from app.Exceptions import ValidationException
from app.Services.Contracts.ChatAttachmentContentService import ChatAttachmentContentService


class ChatAttachmentContentServiceImpl(ChatAttachmentContentService):
    TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".xml", ".html", ".log", ".py", ".js", ".ts", ".css"}

    def build_gemini_input(self, dto: ChatMessageCreateDTO) -> Tuple[str, List[Dict[str, Any]]]:
        prompt = dto.message or "Analyze the attached file."
        text_sections = []
        inline_parts = []

        for attachment in dto.attachments:
            file_bytes = self._read_uploaded_file(attachment)

            if self._is_pdf(attachment):
                text_sections.append(self._extract_pdf_text(attachment.file_name, file_bytes))
                continue

            if self._is_text(attachment):
                text_sections.append(self._extract_text_file(attachment.file_name, file_bytes))
                continue

            if self._is_inline_media(attachment):
                inline_parts.append(self._build_inline_part(attachment, file_bytes))
                text_sections.append(f"{attachment.file_name}: attached {attachment.attachment_type.value} file.")
                continue

            text_sections.append(
                f"{attachment.file_name}: attached file. Content extraction is not supported for this file type."
            )

        if text_sections:
            prompt = f"{prompt}\n\n" + "\n\n".join(text_sections)

        return prompt, inline_parts

    def _read_uploaded_file(self, attachment: ChatMessageAttachmentDTO) -> bytes:
        uploaded_file = attachment.uploaded_file
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        file_bytes = uploaded_file.read()
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        return file_bytes

    def _is_pdf(self, attachment: ChatMessageAttachmentDTO) -> bool:
        return attachment.content_type == "application/pdf" or attachment.extension == ".pdf"

    def _is_text(self, attachment: ChatMessageAttachmentDTO) -> bool:
        return attachment.content_type.startswith("text/") or attachment.extension in self.TEXT_EXTENSIONS

    def _is_inline_media(self, attachment: ChatMessageAttachmentDTO) -> bool:
        return (
            attachment.content_type.startswith("image/")
            or attachment.content_type.startswith("audio/")
            or attachment.content_type.startswith("video/")
        )

    def _extract_pdf_text(self, file_name: str, file_bytes: bytes) -> str:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ValidationException("pypdf is required to analyze PDF attachments") from exc

        reader = PdfReader(BytesIO(file_bytes))
        page_text = [page.extract_text() or "" for page in reader.pages]
        extracted_text = "\n".join(page_text).strip()
        if not extracted_text:
            return f"{file_name} Content:\nNo extractable PDF text was found."
        return f"{file_name} Content:\n{extracted_text}"

    def _extract_text_file(self, file_name: str, file_bytes: bytes) -> str:
        for encoding in ("utf-8", "utf-16", "latin-1"):
            try:
                text = file_bytes.decode(encoding).strip()
                return f"{file_name} Content:\n{text}"
            except UnicodeDecodeError:
                continue
        return f"{file_name} Content:\nUnable to decode text content."

    def _build_inline_part(self, attachment: ChatMessageAttachmentDTO, file_bytes: bytes) -> Dict[str, Any]:
        return {
            "inline_data": {
                "mime_type": attachment.content_type,
                "data": base64.b64encode(file_bytes).decode("ascii"),
            }
        }
