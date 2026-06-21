from celery import shared_task


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
)
def process_meeting_transcription(self, meeting_id: int, user_id: int) -> None:
    from app.Providers import container
    from app.Services.Contracts.MeetingProcessingService import MeetingProcessingService

    container.resolve(MeetingProcessingService).process(meeting_id, user_id)
