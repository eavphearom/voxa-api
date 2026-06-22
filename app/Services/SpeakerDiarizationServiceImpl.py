from __future__ import annotations

from typing import List

import logging

import numpy as np
import torch
from django.conf import settings

from app.DTO.MeetingTranscriptionDTO import SpeakerTurnDTO
from app.Services.Contracts.SpeakerDiarizationService import SpeakerDiarizationService


logger = logging.getLogger(__name__)


class SpeakerDiarizationServiceImpl(SpeakerDiarizationService):
    SAMPLE_RATE = 16000

    def diarize(self, file_path: str) -> List[SpeakerTurnDTO]:
        if not settings.PYANNOTE_AUTH_TOKEN:
            logger.warning("PYANNOTE_AUTH_TOKEN is not configured; using single-speaker transcript")
            return []

        try:
            from pyannote.audio import Pipeline

            pipeline = Pipeline.from_pretrained(
                settings.PYANNOTE_MODEL,
                token=settings.PYANNOTE_AUTH_TOKEN,
            )
            if pipeline is None:
                return []
            waveform = self._load_waveform(file_path)
            output = pipeline({"waveform": waveform, "sample_rate": self.SAMPLE_RATE})
            annotation = getattr(output, "speaker_diarization", output)
            return [
                SpeakerTurnDTO(
                    start=float(turn.start),
                    end=float(turn.end),
                    speaker=str(speaker),
                )
                for turn, _, speaker in annotation.itertracks(yield_label=True)
            ]
        except Exception as exc:
            logger.exception("Speaker diarization failed: %s", exc)
            return []

    def _load_waveform(self, file_path: str) -> torch.Tensor:
        # faster-whisper uses PyAV, whose bundled FFmpeg libraries avoid relying
        # on a system ffmpeg executable and produce the mono 16 kHz waveform
        # expected by the Pyannote pipeline.
        from faster_whisper.audio import decode_audio

        samples = np.asarray(
            decode_audio(file_path, sampling_rate=self.SAMPLE_RATE),
            dtype=np.float32,
        )
        if samples.size == 0:
            raise ValueError("Decoded audio is empty")
        return torch.from_numpy(samples).unsqueeze(0)
