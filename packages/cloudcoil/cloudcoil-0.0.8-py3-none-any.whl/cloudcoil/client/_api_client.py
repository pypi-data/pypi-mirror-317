from typing import Generic, Type, TypeVar

import httpx

from cloudcoil.client._resource import Resource
from cloudcoil.client.errors import APIError, ResourceAlreadyExists, ResourceNotFound

T = TypeVar("T", bound="Resource")


class _BaseAPIClient(Generic[T]):
    def __init__(
        self,
        api_version: str,
        kind: Type[T],
        resource: str,
        default_namespace: str,
        namespaced: bool,
    ) -> None:
        self.api_version = api_version
        self.kind = kind
        self.resource = resource
        self.default_namespace = default_namespace
        self.namespaced = namespaced

    def _build_url(self, namespace: str | None = None, name: str | None = None) -> str:
        api_base = f"/api/{self.api_version}"
        if "/" in self.api_version:
            api_base = f"/apis/{self.api_version}"
        if not (name and namespace):
            return f"{api_base}/{self.resource}"
        if not namespace:
            raise ValueError("namespace must be provided when name is provided")
        if self.namespaced:
            return f"{api_base}/namespaces/{namespace}/{self.resource}/{name}"
        return f"{api_base}/{self.resource}/{name}"

    def _handle_get_response(self, response: httpx.Response, namespace: str, name: str) -> T:
        if response.status_code == 404:
            raise ResourceNotFound(
                f"Resource kind='{self.kind.__name__}', {namespace=}, {name=} not found"
            )
        return self.kind.model_validate_json(response.content)  # type: ignore

    def _handle_create_response(self, response: httpx.Response) -> T:
        if response.status_code == 409:
            raise ResourceAlreadyExists(response.json()["details"])
        if response.status_code != 201:
            raise APIError(response.json())
        return self.kind.model_validate_json(response.content)  # type: ignore


class APIClient(_BaseAPIClient[T]):
    def __init__(
        self,
        api_version: str,
        kind: Type[T],
        resource: str,
        default_namespace: str,
        namespaced: bool,
        client: httpx.Client,
    ) -> None:
        super().__init__(api_version, kind, resource, default_namespace, namespaced)
        self._client = client

    def get(self, name: str, namespace: str | None = None) -> T:
        namespace = namespace or self.default_namespace
        url = self._build_url(name=name, namespace=namespace)
        response = self._client.get(url)
        return self._handle_get_response(response, namespace, name)

    def create(self, body: T, namespace: str | None = None) -> T:
        if not (body.metadata):
            raise ValueError(f"metadata must be set for {body=}")
        namespace = namespace or body.metadata.namespace or self.default_namespace
        url = self._build_url(namespace=namespace)
        response = self._client.post(url, json=body.model_dump(mode="json", by_alias=True))
        return self._handle_create_response(response)

    def delete(self, name: str, namespace: str | None = None) -> T:
        namespace = namespace or self.default_namespace
        url = self._build_url(name=name, namespace=namespace)
        response = self._client.delete(url)
        return self._handle_get_response(response, namespace, name)

    def remove(self, body: T) -> T:
        if not (body.metadata and body.metadata.name):
            raise ValueError(f"metadata.name must be set for {body=}")
        namespace = body.metadata.namespace or self.default_namespace
        name = body.metadata.name
        return self.delete(name, namespace)


class AsyncAPIClient(_BaseAPIClient[T]):
    def __init__(
        self,
        api_version: str,
        kind: Type[T],
        resource: str,
        default_namespace: str,
        namespaced: bool,
        client: httpx.AsyncClient,
    ) -> None:
        super().__init__(api_version, kind, resource, default_namespace, namespaced)
        self._client = client

    async def get(self, name: str, namespace: str | None = None) -> T:
        namespace = namespace or self.default_namespace
        url = self._build_url(name=name, namespace=namespace)
        response = await self._client.get(url)
        return self._handle_get_response(response, namespace, name)

    async def create(self, body: T, namespace: str | None = None) -> T:
        if not (body.metadata):
            raise ValueError(f"metadata.name must be set for {body=}")
        namespace = namespace or body.metadata.namespace or self.default_namespace
        url = self._build_url(namespace=namespace)
        response = await self._client.post(url, json=body.model_dump(mode="json", by_alias=True))
        return self._handle_create_response(response)

    async def delete(self, name: str, namespace: str | None = None) -> T:
        namespace = namespace or self.default_namespace
        url = self._build_url(name=name, namespace=namespace)
        response = await self._client.delete(url)
        return self._handle_get_response(response, namespace, name)

    async def remove(self, body: T) -> T:
        if not (body.metadata and body.metadata.name):
            raise ValueError(f"metadata.name must be set for {body=}")
        namespace = body.metadata.namespace or self.default_namespace
        name = body.metadata.name
        return await self.delete(name, namespace)
