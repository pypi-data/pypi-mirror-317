"""
Main interface for sesv2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sesv2 import (
        Client,
        ListMultiRegionEndpointsPaginator,
        SESV2Client,
    )

    session = get_session()
    async with session.create_client("sesv2") as client:
        client: SESV2Client
        ...


    list_multi_region_endpoints_paginator: ListMultiRegionEndpointsPaginator = client.get_paginator("list_multi_region_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SESV2Client
from .paginator import ListMultiRegionEndpointsPaginator

Client = SESV2Client


__all__ = ("Client", "ListMultiRegionEndpointsPaginator", "SESV2Client")
