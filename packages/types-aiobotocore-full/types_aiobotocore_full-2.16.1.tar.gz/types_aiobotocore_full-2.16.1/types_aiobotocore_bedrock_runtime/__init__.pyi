"""
Main interface for bedrock-runtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_runtime import (
        BedrockRuntimeClient,
        Client,
        ListAsyncInvokesPaginator,
    )

    session = get_session()
    async with session.create_client("bedrock-runtime") as client:
        client: BedrockRuntimeClient
        ...


    list_async_invokes_paginator: ListAsyncInvokesPaginator = client.get_paginator("list_async_invokes")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import BedrockRuntimeClient
from .paginator import ListAsyncInvokesPaginator

Client = BedrockRuntimeClient

__all__ = ("BedrockRuntimeClient", "Client", "ListAsyncInvokesPaginator")
