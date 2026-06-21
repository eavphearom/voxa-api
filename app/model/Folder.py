from django.db import models

from app.model.BaseModel import BaseModel


class Folder(BaseModel):
    user_id = models.BigIntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "app"
        db_table = "folders"

    def __str__(self) -> str:
        return self.name
