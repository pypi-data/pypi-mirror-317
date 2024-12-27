"""
Main interface for observabilityadmin service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_observabilityadmin import (
        Client,
        CloudWatchObservabilityAdminServiceClient,
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
    )

    session = get_session()
    async with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient
        ...


    list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
    list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import CloudWatchObservabilityAdminServiceClient
from .paginator import ListResourceTelemetryForOrganizationPaginator, ListResourceTelemetryPaginator

Client = CloudWatchObservabilityAdminServiceClient

__all__ = (
    "Client",
    "CloudWatchObservabilityAdminServiceClient",
    "ListResourceTelemetryForOrganizationPaginator",
    "ListResourceTelemetryPaginator",
)
