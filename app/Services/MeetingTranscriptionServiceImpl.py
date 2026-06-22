from __future__ import annotations

from typing import Dict

import logging

from django.conf import settings

from app.DTO.MeetingTranscriptionDTO import MeetingTranscriptionResultDTO, TranscriptionSegmentDTO
from app.Exceptions import ApplicationException
from app.Services.Contracts.MeetingTranscriptionService import MeetingTranscriptionService
from app.Services.Contracts.SpeakerDiarizationService import SpeakerDiarizationService


logger = logging.getLogger(__name__)


class MeetingTranscriptionServiceImpl(MeetingTranscriptionService):
    _model = None

    def __init__(self, diarization_service: SpeakerDiarizationService) -> None:
        self.diarization_service = diarization_service

    def transcribe(self, file_path: str, language: str | None = None) -> MeetingTranscriptionResultDTO:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise ApplicationException("faster-whisper is not installed") from exc

        model = self._get_model(WhisperModel)
        segments, info = self._run_transcription(model, file_path, language, vad_filter=True)
        if not segments:
            logger.warning(
                "No speech survived VAD for %s; retrying transcription without VAD",
                file_path,
            )
            segments, info = self._run_transcription(model, file_path, language, vad_filter=False)
        if not segments:
            raise ApplicationException("No transcript text was generated")

        logger.info(
            "Faster-Whisper transcribed %s: language=%s probability=%s duration=%s segments=%s",
            file_path,
            getattr(info, "language", None),
            getattr(info, "language_probability", None),
            getattr(info, "duration", None),
            len(segments),
        )

        speaker_turns = self.diarization_service.diarize(file_path)
        transcript = self._format_speaker_transcript(segments, speaker_turns)
        return MeetingTranscriptionResultDTO(
            text=transcript,
            language=getattr(info, "language", None),
            duration=float(getattr(info, "duration", 0.0) or 0.0) or None,
            segments=segments,
        )

    def _run_transcription(self, model, file_path: str, language: str | None, vad_filter: bool):
        requested_language = self._normalize_language(language)
        raw_segments, info = model.transcribe(
            file_path,
            language=requested_language,
            vad_filter=vad_filter,
        )
        segments = [
            TranscriptionSegmentDTO(
                start=float(segment.start),
                end=float(segment.end),
                text=segment.text.strip(),
            )
            for segment in raw_segments
            if segment.text.strip()
        ]
        return segments, info

    @staticmethod
    def _normalize_language(language: str | None) -> str | None:
        normalized = (language or "").strip().lower()
        return normalized or None

    def transcribe_live_chunk(self, file_path: str, language: str | None = None) -> MeetingTranscriptionResultDTO:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise ApplicationException("faster-whisper is not installed") from exc
        model = self._get_model(WhisperModel)
        raw_segments, info = model.transcribe(
            file_path,
            language=self._normalize_language(language),
            vad_filter=True,
        )
        segments = [
            TranscriptionSegmentDTO(float(segment.start), float(segment.end), segment.text.strip())
            for segment in raw_segments
            if segment.text.strip()
        ]
        text = " ".join(segment.text for segment in segments).strip()
        return MeetingTranscriptionResultDTO(
            text=text,
            language=getattr(info, "language", None),
            duration=float(getattr(info, "duration", 0.0) or 0.0) or None,
            segments=segments,
        )

    def _get_model(self, model_class):
        if self.__class__._model is None:
            self.__class__._model = model_class(
                settings.FASTER_WHISPER_MODEL_SIZE,
                device=settings.FASTER_WHISPER_DEVICE,
                compute_type=settings.FASTER_WHISPER_COMPUTE_TYPE,
            )
        return self.__class__._model

    def _format_speaker_transcript(self, segments, speaker_turns) -> str:
        labels: Dict[str, str] = {}
        lines = []
        previous_label = None

        for segment in segments:
            raw_speaker = self._speaker_for_segment(segment, speaker_turns)
            if raw_speaker not in labels:
                labels[raw_speaker] = f"Speaker {len(labels) + 1}"
            label = labels[raw_speaker]
            if label == previous_label:
                lines[-1] = f"{lines[-1]} {segment.text}"
            else:
                lines.append(f"{label}:\n{segment.text}")
                previous_label = label
        return "\n\n".join(lines)

    def _speaker_for_segment(self, segment, speaker_turns) -> str:
        if not speaker_turns:
            return "SPEAKER_00"
        overlaps = [
            (max(0.0, min(segment.end, turn.end) - max(segment.start, turn.start)), turn.speaker)
            for turn in speaker_turns
        ]
        return max(overlaps, key=lambda item: item[0])[1]
