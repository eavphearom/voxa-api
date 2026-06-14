from __future__ import annotations

import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Generate a Laravel-style feature module."

    def add_arguments(self, parser) -> None:
        parser.add_argument("feature_name", type=str)

    def handle(self, *args, **options) -> None:
        class_name = self._normalize_class_name(options["feature_name"])
        if not class_name:
            raise CommandError("FeatureName is required")

        root = Path.cwd() / "app"
        context = {
            "class_name": class_name,
            "snake_name": self._to_snake_case(class_name),
            "plural_snake_name": f"{self._to_snake_case(class_name)}s",
        }

        self._create_feature_files(root, context)
        self._update_model_exports(root, class_name)
        self._update_repository_bindings(root, context)
        self._update_service_bindings(root, context)
        self._update_user_v1_routes(root, context)

        self.stdout.write(self.style.SUCCESS(f"{class_name} feature generated successfully."))

    def _create_feature_files(self, root: Path, context: dict[str, str]) -> None:
        class_name = context["class_name"]
        snake_name = context["snake_name"]
        files = {
            root / "Controllers" / f"{class_name}Controller.py": self._controller_template(context),
            root / "DTO" / f"{class_name}DTO.py": self._dto_template(context),
            root / "model" / f"{class_name}.py": self._model_template(context),
            root / "Repositories" / "Contracts" / f"{class_name}Repository.py": self._repository_contract_template(context),
            root / "Repositories" / f"{class_name}RepositoryImpl.py": self._repository_impl_template(context),
            root / "Services" / "Contracts" / f"{class_name}Service.py": self._service_contract_template(context),
            root / "Services" / f"{class_name}ServiceImpl.py": self._service_impl_template(context),
        }

        for path, content in files.items():
            self._write_file_if_missing(path, content)

    def _write_file_if_missing(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            self.stdout.write(self.style.WARNING(f"Skipped existing file: {path}"))
            return
        path.write_text(content, encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"Created: {path}"))

    def _update_model_exports(self, root: Path, class_name: str) -> None:
        path = root / "model" / "__init__.py"
        content = path.read_text(encoding="utf-8") if path.exists() else ""
        import_line = f"from .{class_name} import {class_name}"
        if import_line not in content:
            content = self._append_line(content, import_line)

        exports = self._extract_all_values(content)
        if class_name not in exports:
            exports.append(class_name)
        path.write_text(self._replace_or_append_all(content, exports), encoding="utf-8")

    def _update_repository_bindings(self, root: Path, context: dict[str, str]) -> None:
        class_name = context["class_name"]
        path = root / "config" / "binding" / "repositories.py"
        content = path.read_text(encoding="utf-8")
        imports = [
            f"from app.Repositories.Contracts.{class_name}Repository import {class_name}Repository",
            f"from app.Repositories.{class_name}RepositoryImpl import {class_name}RepositoryImpl",
        ]
        binding = f"    {class_name}Repository: {class_name}RepositoryImpl,"
        path.write_text(
            self._append_imports_and_dict_binding(content, "REPOSITORY_BINDINGS", imports, binding),
            encoding="utf-8",
        )

    def _update_service_bindings(self, root: Path, context: dict[str, str]) -> None:
        class_name = context["class_name"]
        path = root / "config" / "binding" / "services.py"
        content = path.read_text(encoding="utf-8")
        imports = [
            f"from app.Repositories.Contracts.{class_name}Repository import {class_name}Repository",
            f"from app.Services.Contracts.{class_name}Service import {class_name}Service",
            f"from app.Services.{class_name}ServiceImpl import {class_name}ServiceImpl",
        ]
        binding = (
            f"    {class_name}Service: lambda container: "
            f"{class_name}ServiceImpl(container.resolve({class_name}Repository)),"
        )
        path.write_text(
            self._append_imports_and_dict_binding(content, "SERVICE_BINDINGS", imports, binding),
            encoding="utf-8",
        )

    def _update_user_v1_routes(self, root: Path, context: dict[str, str]) -> None:
        class_name = context["class_name"]
        plural = context["plural_snake_name"]
        path = root / "Routes" / "user" / "v1.py"
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            content = path.read_text(encoding="utf-8")
        else:
            content = "from django.urls import path\n\n\nurlpatterns = []\n"

        import_line = f"from app.Controllers.{class_name}Controller import {class_name}Controller"
        if import_line not in content:
            content = self._prepend_import(content, import_line)

        marker = f"# {class_name} routes"
        if marker not in content:
            route_block = [
                f"    {marker}",
                f'    path("{plural}", {class_name}Controller.as_view(), name="{plural}-index"),',
                f'    path("{plural}/<int:id>", {class_name}Controller.as_view(), name="{plural}-show"),',
                f'    path("{plural}/create", {class_name}Controller.as_view(), name="{plural}-create"),',
                f'    path("{plural}/<int:id>/update", {class_name}Controller.as_view(), name="{plural}-update"),',
                f'    path("{plural}/<int:id>/delete", {class_name}Controller.as_view(), name="{plural}-delete"),',
                f"    # End {class_name} routes",
            ]
            content = self._append_urlpatterns_block(content, route_block)

        path.write_text(content, encoding="utf-8")

    def _append_urlpatterns_block(self, content: str, route_block: list[str]) -> str:
        if "urlpatterns" not in content:
            content = self._append_line(content, "urlpatterns = []")

        closing_index = content.rfind("]")
        block = "\n".join(route_block)
        if closing_index == -1:
            return self._append_line(content, block)

        prefix = content[:closing_index].rstrip()
        suffix = content[closing_index:]
        return f"{prefix}\n{block}\n{suffix.lstrip()}"

    def _append_imports_and_binding(self, content: str, imports: list[str], binding: str) -> str:
        for import_line in imports:
            if import_line not in content:
                content = self._prepend_import(content, import_line)
        if binding.strip() not in content:
            content = self._append_line(content, binding)
        return content

    def _append_imports_and_dict_binding(
        self,
        content: str,
        dict_name: str,
        imports: list[str],
        binding: str,
    ) -> str:
        for import_line in imports:
            if import_line not in content:
                content = self._prepend_import(content, import_line)

        if binding.strip() in content:
            return content

        if f"{dict_name} = {{" not in content:
            return self._append_line(content, f"{dict_name} = {{\n{binding}\n}}")

        closing_index = content.rfind("}")
        if closing_index == -1:
            return self._append_line(content, binding)

        prefix = content[:closing_index].rstrip()
        suffix = content[closing_index:]
        return f"{prefix}\n{binding}\n{suffix.lstrip()}"

    def _prepend_import(self, content: str, import_line: str) -> str:
        lines = content.splitlines()
        last_import_index = -1
        for index, line in enumerate(lines):
            if line.startswith("from ") or line.startswith("import "):
                last_import_index = index
        lines.insert(last_import_index + 1, import_line)
        return "\n".join(lines) + "\n"

    def _append_line(self, content: str, line: str) -> str:
        content = content.rstrip()
        if not content:
            return f"{line}\n"
        return f"{content}\n{line}\n"

    def _extract_all_values(self, content: str) -> list[str]:
        match = re.search(r"__all__\s*=\s*\[(.*?)\]", content, re.DOTALL)
        if not match:
            return []
        return re.findall(r"[\"']([^\"']+)[\"']", match.group(1))

    def _replace_or_append_all(self, content: str, exports: list[str]) -> str:
        exports = sorted(dict.fromkeys(exports))
        all_block = "__all__ = [\n" + "".join(f'    "{value}",\n' for value in exports) + "]"
        if re.search(r"__all__\s*=\s*\[.*?\]", content, re.DOTALL):
            return re.sub(r"__all__\s*=\s*\[.*?\]", all_block, content, flags=re.DOTALL)
        return self._append_line(content, all_block)

    def _normalize_class_name(self, raw_name: str) -> str:
        cleaned = re.sub(r"[^0-9a-zA-Z_]", "", raw_name.strip())
        return "".join(part[:1].upper() + part[1:] for part in re.split(r"[_\s]+", cleaned) if part)

    def _to_snake_case(self, value: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()

    def _controller_template(self, context: dict[str, str]) -> str:
        class_name = context["class_name"]
        return f'''from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.DTO.{class_name}DTO import {class_name}DTO
from app.Providers import container
from app.Services.Contracts.{class_name}Service import {class_name}Service


class {class_name}Controller(APIView):
    def get(self, request, id: int | None = None):
        service = container.resolve({class_name}Service)
        if id is None:
            return self.index(service)
        return self.show(service, id)

    def post(self, request):
        service = container.resolve({class_name}Service)
        return self.create(service, request)

    def put(self, request, id: int):
        service = container.resolve({class_name}Service)
        return self.update(service, request, id)

    def delete(self, request, id: int):
        service = container.resolve({class_name}Service)
        return self.delete_item(service, id)

    def index(self, service):
        return Response(service.get_all())

    def show(self, service, id: int):
        return Response(service.get_by_id(id))

    def create(self, service, request):
        dto = {class_name}DTO.from_request(request.data)
        return Response(service.create(dto), status=status.HTTP_201_CREATED)

    def update(self, service, request, id: int):
        dto = {class_name}DTO.from_request(request.data)
        return Response(service.update(id, dto))

    def delete_item(self, service, id: int):
        service.delete(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

    def _dto_template(self, context: dict[str, str]) -> str:
        class_name = context["class_name"]
        return f'''from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class {class_name}DTO:
    payload: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_request(cls, data) -> "{class_name}DTO":
        return cls(payload=dict(data))

    def to_dict(self) -> dict[str, Any]:
        return self.payload
'''

    def _model_template(self, context: dict[str, str]) -> str:
        class_name = context["class_name"]
        return f'''from django.db import models


class {class_name}(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "app"
        db_table = "{context["plural_snake_name"]}"

    def __str__(self) -> str:
        return self.name
'''

    def _repository_contract_template(self, context: dict[str, str]) -> str:
        class_name = context["class_name"]
        return f'''from app.Repositories.BaseRepository import BaseRepository


class {class_name}Repository(BaseRepository):
    pass
'''

    def _repository_impl_template(self, context: dict[str, str]) -> str:
        class_name = context["class_name"]
        return f'''from app.model import {class_name}
from app.Repositories.BaseRepositoryImpl import BaseRepositoryImpl
from app.Repositories.Contracts.{class_name}Repository import {class_name}Repository


class {class_name}RepositoryImpl(BaseRepositoryImpl, {class_name}Repository):
    model = {class_name}
'''

    def _service_contract_template(self, context: dict[str, str]) -> str:
        class_name = context["class_name"]
        return f'''from abc import ABC, abstractmethod
from typing import Any

from app.DTO.{class_name}DTO import {class_name}DTO


class {class_name}Service(ABC):
    @abstractmethod
    def get_all(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, object_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def create(self, dto: {class_name}DTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update(self, object_id: int, dto: {class_name}DTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, object_id: int) -> bool:
        raise NotImplementedError
'''

    def _service_impl_template(self, context: dict[str, str]) -> str:
        class_name = context["class_name"]
        return f'''from typing import Any

from app.DTO.{class_name}DTO import {class_name}DTO
from app.Exceptions import NotFoundException
from app.Repositories.Contracts.{class_name}Repository import {class_name}Repository
from app.Services.Contracts.{class_name}Service import {class_name}Service


class {class_name}ServiceImpl({class_name}Service):
    def __init__(self, repository: {class_name}Repository) -> None:
        self.repository = repository

    def get_all(self) -> list[dict[str, Any]]:
        return [self._to_dict(item) for item in self.repository.get_all()]

    def get_by_id(self, object_id: int) -> dict[str, Any]:
        instance = self.repository.get_by_id(object_id)
        if instance is None:
            raise NotFoundException("{class_name} not found")
        return self._to_dict(instance)

    def create(self, dto: {class_name}DTO) -> dict[str, Any]:
        return self._to_dict(self.repository.create(dto.to_dict()))

    def update(self, object_id: int, dto: {class_name}DTO) -> dict[str, Any]:
        instance = self.repository.update(object_id, dto.to_dict())
        if instance is None:
            raise NotFoundException("{class_name} not found")
        return self._to_dict(instance)

    def delete(self, object_id: int) -> bool:
        deleted = self.repository.delete(object_id)
        if not deleted:
            raise NotFoundException("{class_name} not found")
        return True

    def _to_dict(self, instance) -> dict[str, Any]:
        return {{
            "id": instance.id,
            "name": instance.name,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }}
'''

