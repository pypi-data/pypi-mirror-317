from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_summary_response_200 import GetSummaryResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    collection_id: int,
    file: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["collection_id"] = collection_id

    params["file"] = file

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/v1/api/collection/summary",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetSummaryResponse200]:
    if response.status_code == 200:
        response_200 = GetSummaryResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetSummaryResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    collection_id: int,
    file: Union[Unset, str] = UNSET,
) -> Response[GetSummaryResponse200]:
    """Summary

     Generate a summary for a collection file.

    Args:
        collection_id (int):
        file (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetSummaryResponse200]
    """

    kwargs = _get_kwargs(
        collection_id=collection_id,
        file=file,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    collection_id: int,
    file: Union[Unset, str] = UNSET,
) -> Optional[GetSummaryResponse200]:
    """Summary

     Generate a summary for a collection file.

    Args:
        collection_id (int):
        file (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetSummaryResponse200
    """

    return sync_detailed(
        client=client,
        collection_id=collection_id,
        file=file,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    collection_id: int,
    file: Union[Unset, str] = UNSET,
) -> Response[GetSummaryResponse200]:
    """Summary

     Generate a summary for a collection file.

    Args:
        collection_id (int):
        file (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetSummaryResponse200]
    """

    kwargs = _get_kwargs(
        collection_id=collection_id,
        file=file,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    collection_id: int,
    file: Union[Unset, str] = UNSET,
) -> Optional[GetSummaryResponse200]:
    """Summary

     Generate a summary for a collection file.

    Args:
        collection_id (int):
        file (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetSummaryResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            collection_id=collection_id,
            file=file,
        )
    ).parsed
