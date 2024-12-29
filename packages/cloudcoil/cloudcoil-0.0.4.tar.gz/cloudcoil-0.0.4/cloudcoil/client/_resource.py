import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from pydantic import BaseModel, ConfigDict

from cloudcoil.client._context import context


class RootModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )


class Resource(RootModel):
    @classmethod
    def gvk(cls):
        fields = cls.model_fields
        if "api_version" not in fields:
            raise ValueError(f"Resource {cls} does not have an api_version field")
        if "kind" not in fields:
            raise ValueError(f"Resource {cls} does not have a kind field")
        api_version = fields["api_version"].default
        kind = fields["kind"].default
        return api_version, kind

    @classmethod
    def get(cls, name: str, namespace: str | None = None) -> Self:
        client_set = context.active_client_set
        return client_set.client_for(cls, sync=True).get(name, namespace)

    @classmethod
    async def async_get(cls, name: str, namespace: str | None = None) -> Self:
        client_set = context.active_client_set
        return await client_set.client_for(cls, sync=False).get(name, namespace)

    def create(self, namespace: str | None = None) -> Self:
        client_set = context.active_client_set
        return client_set.client_for(self.__class__, sync=True).create(self, namespace=namespace)

    async def async_create(self, namespace: str | None = None) -> Self:
        client_set = context.active_client_set
        return await client_set.client_for(self.__class__, sync=False).create(
            self, namespace=namespace
        )

    @classmethod
    def delete(cls, name: str, namespace: str | None = None) -> Self:
        client_set = context.active_client_set
        return client_set.client_for(cls, sync=True).delete(name, namespace)

    @classmethod
    async def async_delete(cls, name: str, namespace: str | None = None) -> Self:
        client_set = context.active_client_set
        return await client_set.client_for(cls, sync=False).delete(name, namespace)

    def remove(self) -> Self:
        client_set = context.active_client_set
        return client_set.client_for(self.__class__, sync=True).remove(self)

    async def async_remove(self) -> Self:
        client_set = context.active_client_set
        return await client_set.client_for(self.__class__, sync=False).remove(self)
