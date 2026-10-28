from collections.abc import Callable
from typing import Protocol, ClassVar, Any
from uuid import UUID
import json
from pathlib import Path


class RoleRepository(Protocol):
    def is_assigned(self, role: Role, user: User) -> bool: ...
    def assign(self, role: Role, user: User) -> None: ...
    def unassign(self, role: Role, user: User) -> None: ...


class InMemoryRoleRepository(RoleRepository):
    def __init__(self) -> None:
        self._links: list[tuple[UUID, UUID]] = []

    def is_assigned(self, role: Role, user: User) -> bool:
        return (role.id, user.id) in self._links

    def assign(self, role: Role, user: User) -> None:
        self._links.append((role.id, user.id))

    def unassign(self, role: Role, user: User) -> None:
        self._links.remove((role.id, user.id))


class SqlRoleRepository(RoleRepository):
    def __init__(self, connection_string: str):
        self._connection_string = connection_string

    def is_assigned(self, role: Role, user: User) -> bool:
        raise NotImplementedError
    
    def assign(self, role: Role, user: User) -> None:
        raise NotImplementedError
    
    def unassign(self, role: Role, user: User) -> None:
        raise NotImplementedError


class FileRoleRepository(RoleRepository):
    def __init__(self, path: str | Path) -> None:
        if not str(path).strip():
            raise ValueError("path must not be empty")

        self._path = Path(path)

    def _read(self) -> list[tuple[UUID, UUID]]:
        try:
            with self._path.open(encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []

        return [
            (UUID(role_id), UUID(user_id))
            for role_id, user_id in data
        ]

    def _write(self, links: list[tuple[UUID, UUID]]) -> None:
        data = [
            (str(role_id), str(user_id))
            for role_id, user_id in links
        ]

        with self._path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def is_assigned(self, role: Role, user: User) -> bool:
        return (role.id, user.id) in self._read()

    def assign(self, role: Role, user: User) -> None:
        links = self._read()
        links.append((role.id, user.id))
        self._write(links)

    def unassign(self, role: Role, user: User) -> None:
        links = self._read()
        link = (role.id, user.id)

        if link in links:
            links.remove(link)
            self._write(links)
    

class RoleRepositoryFactory:
    _registry: ClassVar[dict[str, Callable[..., RoleRepository]]] = {}

    @classmethod
    def register(cls, kind: str, constructor: Callable[..., RoleRepository]) -> None:
        if kind in cls._registry:
            return

        cls._registry[kind] = constructor

    @classmethod
    def create(cls, kind: str, **kwargs: Any) -> RoleRepository:
        if kind not in cls._registry:
            raise ValueError(f"RoleRepositoryFactory entry for kind '{kind}' not found")

        return cls._registry[kind](**kwargs)


RoleRepositoryFactory.register("memory", InMemoryRoleRepository)
RoleRepositoryFactory.register("sql", SqlRoleRepository)
RoleRepositoryFactory.register("file", FileRoleRepository)
