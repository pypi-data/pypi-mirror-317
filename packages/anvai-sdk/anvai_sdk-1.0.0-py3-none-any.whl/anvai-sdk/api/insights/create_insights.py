from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_insights_body import CreateInsightsBody
from ...models.create_insights_response_200 import CreateInsightsResponse200
from ...types import Response


def _get_kwargs(
    collection_id: int,
    *,
    body: CreateInsightsBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/ingest/public/v1/api/collections/{collection_id}/create-insights",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CreateInsightsResponse200]:
    if response.status_code == 200:
        response_200 = CreateInsightsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CreateInsightsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    collection_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateInsightsBody,
) -> Response[CreateInsightsResponse200]:
    """Run Insights

     Execute specific tasks on a collection.

    Args:
        collection_id (int):
        body (CreateInsightsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateInsightsResponse200]
    """

    kwargs = _get_kwargs(
        collection_id=collection_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateInsightsBody,
) -> Optional[CreateInsightsResponse200]:
    """Run Insights

     Execute specific tasks on a collection.

    Args:
        collection_id (int):
        body (CreateInsightsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateInsightsResponse200
    """

    return sync_detailed(
        collection_id=collection_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    collection_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateInsightsBody,
) -> Response[CreateInsightsResponse200]:
    """Run Insights

     Execute specific tasks on a collection.

    Args:
        collection_id (int):
        body (CreateInsightsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateInsightsResponse200]
    """

    kwargs = _get_kwargs(
        collection_id=collection_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection_id: int,
    *,
    client: AuthenticatedClient,
    body: CreateInsightsBody,
) -> Optional[CreateInsightsResponse200]:
    """Run Insights

     Execute specific tasks on a collection.

    Args:
        collection_id (int):
        body (CreateInsightsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateInsightsResponse200
    """

    return (
        await asyncio_detailed(
            collection_id=collection_id,
            client=client,
            body=body,
        )
    ).parsed
