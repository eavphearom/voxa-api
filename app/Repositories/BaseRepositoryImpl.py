from typing import Any

from django.core.paginator import Paginator

from app.Repositories.Contracts.BaseRepository import BaseRepository


class BaseRepositoryImpl(BaseRepository):
    model = None

    def get_model(self):
        if self.model is None:
            raise NotImplementedError("Repository model must be defined")
        return self.model

    def get_all(self):
        return self.get_model().objects.all()

    def get_by_id(self, object_id: int):
        return self.get_model().objects.filter(id=object_id).first()

    def create(self, data: dict[str, Any]):
        return self.get_model().objects.create(**data)

    def update(self, object_id: int, data: dict[str, Any]):
        instance = self.get_by_id(object_id)
        if instance is None:
            return None
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, object_id: int) -> bool:
        instance = self.get_by_id(object_id)
        if instance is None:
            return False
        instance.delete()
        return True

    def paginate(self, page: int = 1, per_page: int = 10):
        paginator = Paginator(self.get_all(), per_page)
        return paginator.get_page(page)
