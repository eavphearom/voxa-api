from django.db import models

from app.model.BaseModel import BaseModel
from app.model.Folder import Folder
from app.model.Meeting import Meeting


class FolderMeeting(BaseModel):
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="meeting_links",
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="folder_links",
    )

    class Meta:
        app_label = "app"
        db_table = "folder_meetings"
        constraints = [
            models.UniqueConstraint(
                fields=["folder", "meeting"],
                name="unique_folder_meeting",
            ),
        ]
