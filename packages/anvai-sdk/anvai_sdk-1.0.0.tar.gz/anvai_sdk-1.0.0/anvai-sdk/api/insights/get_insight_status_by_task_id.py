from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_insight_status_by_task_id_response_200 import GetInsightStatusByTaskIdResponse200
from ...types import Response


def _get_kwargs(
    task_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/ingest/public/v1/api/collections/task/{task_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetInsightStatusByTaskIdResponse200]:
    if response.status_code == 200:
        response_200 = GetInsightStatusByTaskIdResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetInsightStatusByTaskIdResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    task_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[GetInsightStatusByTaskIdResponse200]:
    """Get Insight Task Status

     Retrieve the status of a previously executed insight task.

    Args:
        task_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetInsightStatusByTaskIdResponse200]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    task_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[GetInsightStatusByTaskIdResponse200]:
    """Get Insight Task Status

     Retrieve the status of a previously executed insight task.

    Args:
        task_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetInsightStatusByTaskIdResponse200
    """

    return sync_detailed(
        task_id=task_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    task_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[GetInsightStatusByTaskIdResponse200]:
    """Get Insight Task Status

     Retrieve the status of a previously executed insight task.

    Args:
        task_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetInsightStatusByTaskIdResponse200]
    """

    kwargs = _get_kwargs(
        task_id=task_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[GetInsightStatusByTaskIdResponse200]:
    """Get Insight Task Status

     Retrieve the status of a previously executed insight task.

    Args:
        task_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetInsightStatusByTaskIdResponse200
    """

    return (
        await asyncio_detailed(
            task_id=task_id,
            client=client,
        )
    ).parsed
