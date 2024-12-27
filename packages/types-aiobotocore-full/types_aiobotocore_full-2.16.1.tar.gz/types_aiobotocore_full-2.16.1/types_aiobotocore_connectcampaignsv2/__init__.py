"""
Main interface for connectcampaignsv2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectcampaignsv2 import (
        Client,
        ConnectCampaignServiceV2Client,
        ListCampaignsPaginator,
        ListConnectInstanceIntegrationsPaginator,
    )

    session = get_session()
    async with session.create_client("connectcampaignsv2") as client:
        client: ConnectCampaignServiceV2Client
        ...


    list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
    list_connect_instance_integrations_paginator: ListConnectInstanceIntegrationsPaginator = client.get_paginator("list_connect_instance_integrations")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ConnectCampaignServiceV2Client
from .paginator import ListCampaignsPaginator, ListConnectInstanceIntegrationsPaginator

Client = ConnectCampaignServiceV2Client


__all__ = (
    "Client",
    "ConnectCampaignServiceV2Client",
    "ListCampaignsPaginator",
    "ListConnectInstanceIntegrationsPaginator",
)
