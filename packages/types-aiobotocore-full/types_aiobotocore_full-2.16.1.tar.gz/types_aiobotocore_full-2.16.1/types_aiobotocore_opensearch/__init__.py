"""
Main interface for opensearch service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opensearch import (
        Client,
        ListApplicationsPaginator,
        OpenSearchServiceClient,
    )

    session = get_session()
    async with session.create_client("opensearch") as client:
        client: OpenSearchServiceClient
        ...


    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import OpenSearchServiceClient
from .paginator import ListApplicationsPaginator

Client = OpenSearchServiceClient


__all__ = ("Client", "ListApplicationsPaginator", "OpenSearchServiceClient")
