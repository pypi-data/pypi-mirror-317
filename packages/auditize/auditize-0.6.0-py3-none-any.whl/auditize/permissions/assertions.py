from dataclasses import dataclass
from functools import partial
from typing import Callable
from uuid import UUID

from auditize.permissions.models import Permissions

__all__ = (
    "PermissionAssertion",
    "can_read_logs_from_repo",
    "can_read_logs_from_all_repos",
    "can_read_logs_from_any_repo",
    "can_write_logs_to_repo",
    "can_write_logs_to_all_repos",
    "can_read_repo",
    "can_write_repo",
    "can_read_user",
    "can_write_user",
    "can_read_apikey",
    "can_write_apikey",
    "permissions_and",
    "permissions_or",
)

PermissionAssertion = Callable[[Permissions], bool]


def can_read_logs_from_all_repos() -> PermissionAssertion:
    def func(perms: Permissions) -> bool:
        return bool(perms.is_superadmin or perms.logs.read)

    return func


def can_read_logs_from_repo(
    repo_id: UUID, *, on_all_entities=False
) -> PermissionAssertion:
    def func(perms: Permissions) -> bool:
        if perms.is_superadmin or perms.logs.read:
            return True

        repo_perms = perms.logs.get_repo_permissions(repo_id)
        if on_all_entities:
            return bool(repo_perms.read)
        else:
            return bool(repo_perms.read or repo_perms.readable_entities)

    return func


def can_read_logs_from_any_repo() -> PermissionAssertion:
    def func(perms: Permissions) -> bool:
        if perms.is_superadmin or perms.logs.read:
            return True

        return any(repo.read or repo.readable_entities for repo in perms.logs.repos)

    return func


def can_write_logs_to_all_repos() -> PermissionAssertion:
    def func(perms: Permissions) -> bool:
        return bool(perms.is_superadmin or perms.logs.write)

    return func


def can_write_logs_to_repo(repo_id: UUID) -> PermissionAssertion:
    def func(perms: Permissions) -> bool:
        if perms.is_superadmin or perms.logs.write:
            return True

        repo_perms = perms.logs.get_repo_permissions(repo_id)
        return bool(repo_perms.write)

    return func


@dataclass
class EntityPermissionAssertion:
    permission_type: str  # "read" or "write"
    entity_type: str  # "repos", "users" or "apikeys"

    def __call__(self, perms: Permissions) -> bool:
        if perms.is_superadmin:
            return True

        if self.entity_type == "repos":
            entity_perms = perms.management.repos
        elif self.entity_type == "users":
            entity_perms = perms.management.users
        elif self.entity_type == "apikeys":
            entity_perms = perms.management.apikeys
        else:
            raise Exception(
                f"Invalid entity type: {self.entity_type}"
            )  # pragma: no cover, cannot happen

        if self.permission_type == "read":
            return bool(entity_perms.read)
        if self.permission_type == "write":
            return bool(entity_perms.write)

        raise Exception(
            f"Invalid entity permission type: {self.permission_type}"
        )  # pragma: no cover, cannot happen


can_read_repo = partial(
    EntityPermissionAssertion, permission_type="read", entity_type="repos"
)
can_write_repo = partial(
    EntityPermissionAssertion, permission_type="write", entity_type="repos"
)
can_read_user = partial(
    EntityPermissionAssertion, permission_type="read", entity_type="users"
)
can_write_user = partial(
    EntityPermissionAssertion, permission_type="write", entity_type="users"
)
can_read_apikey = partial(
    EntityPermissionAssertion, permission_type="read", entity_type="apikeys"
)
can_write_apikey = partial(
    EntityPermissionAssertion, permission_type="write", entity_type="apikeys"
)


def permissions_and(*assertions: PermissionAssertion) -> PermissionAssertion:
    def func(perms: Permissions) -> bool:
        return all(assertion(perms) for assertion in assertions)

    return func


def permissions_or(*assertions: PermissionAssertion) -> PermissionAssertion:
    def func(perms: Permissions) -> bool:
        return any(assertion(perms) for assertion in assertions)

    return func
