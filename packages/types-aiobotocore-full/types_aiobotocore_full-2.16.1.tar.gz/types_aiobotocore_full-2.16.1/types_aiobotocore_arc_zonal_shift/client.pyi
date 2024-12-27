"""
Type annotations for arc-zonal-shift service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_arc_zonal_shift.client import ARCZonalShiftClient

    session = get_session()
    async with session.create_client("arc-zonal-shift") as client:
        client: ARCZonalShiftClient
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, Mapping, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListAutoshiftsPaginator,
    ListManagedResourcesPaginator,
    ListZonalShiftsPaginator,
)
from .type_defs import (
    CancelZonalShiftRequestRequestTypeDef,
    CreatePracticeRunConfigurationRequestRequestTypeDef,
    CreatePracticeRunConfigurationResponseTypeDef,
    DeletePracticeRunConfigurationRequestRequestTypeDef,
    DeletePracticeRunConfigurationResponseTypeDef,
    GetAutoshiftObserverNotificationStatusResponseTypeDef,
    GetManagedResourceRequestRequestTypeDef,
    GetManagedResourceResponseTypeDef,
    ListAutoshiftsRequestRequestTypeDef,
    ListAutoshiftsResponseTypeDef,
    ListManagedResourcesRequestRequestTypeDef,
    ListManagedResourcesResponseTypeDef,
    ListZonalShiftsRequestRequestTypeDef,
    ListZonalShiftsResponseTypeDef,
    StartZonalShiftRequestRequestTypeDef,
    UpdateAutoshiftObserverNotificationStatusRequestRequestTypeDef,
    UpdateAutoshiftObserverNotificationStatusResponseTypeDef,
    UpdatePracticeRunConfigurationRequestRequestTypeDef,
    UpdatePracticeRunConfigurationResponseTypeDef,
    UpdateZonalAutoshiftConfigurationRequestRequestTypeDef,
    UpdateZonalAutoshiftConfigurationResponseTypeDef,
    UpdateZonalShiftRequestRequestTypeDef,
    ZonalShiftTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("ARCZonalShiftClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class ARCZonalShiftClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ARCZonalShiftClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#generate_presigned_url)
        """

    async def cancel_zonal_shift(
        self, **kwargs: Unpack[CancelZonalShiftRequestRequestTypeDef]
    ) -> ZonalShiftTypeDef:
        """
        Cancel a zonal shift in Amazon Route 53 Application Recovery Controller.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/cancel_zonal_shift.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#cancel_zonal_shift)
        """

    async def create_practice_run_configuration(
        self, **kwargs: Unpack[CreatePracticeRunConfigurationRequestRequestTypeDef]
    ) -> CreatePracticeRunConfigurationResponseTypeDef:
        """
        A practice run configuration for zonal autoshift is required when you enable
        zonal autoshift.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/create_practice_run_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#create_practice_run_configuration)
        """

    async def delete_practice_run_configuration(
        self, **kwargs: Unpack[DeletePracticeRunConfigurationRequestRequestTypeDef]
    ) -> DeletePracticeRunConfigurationResponseTypeDef:
        """
        Deletes the practice run configuration for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/delete_practice_run_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#delete_practice_run_configuration)
        """

    async def get_autoshift_observer_notification_status(
        self,
    ) -> GetAutoshiftObserverNotificationStatusResponseTypeDef:
        """
        Returns the status of autoshift observer notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/get_autoshift_observer_notification_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#get_autoshift_observer_notification_status)
        """

    async def get_managed_resource(
        self, **kwargs: Unpack[GetManagedResourceRequestRequestTypeDef]
    ) -> GetManagedResourceResponseTypeDef:
        """
        Get information about a resource that's been registered for zonal shifts with
        Amazon Route 53 Application Recovery Controller in this Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/get_managed_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#get_managed_resource)
        """

    async def list_autoshifts(
        self, **kwargs: Unpack[ListAutoshiftsRequestRequestTypeDef]
    ) -> ListAutoshiftsResponseTypeDef:
        """
        Returns a list of autoshifts for an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/list_autoshifts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#list_autoshifts)
        """

    async def list_managed_resources(
        self, **kwargs: Unpack[ListManagedResourcesRequestRequestTypeDef]
    ) -> ListManagedResourcesResponseTypeDef:
        """
        Lists all the resources in your Amazon Web Services account in this Amazon Web
        Services Region that are managed for zonal shifts in Amazon Route 53
        Application Recovery Controller, and information about them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/list_managed_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#list_managed_resources)
        """

    async def list_zonal_shifts(
        self, **kwargs: Unpack[ListZonalShiftsRequestRequestTypeDef]
    ) -> ListZonalShiftsResponseTypeDef:
        """
        Lists all active and completed zonal shifts in Amazon Route 53 Application
        Recovery Controller in your Amazon Web Services account in this Amazon Web
        Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/list_zonal_shifts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#list_zonal_shifts)
        """

    async def start_zonal_shift(
        self, **kwargs: Unpack[StartZonalShiftRequestRequestTypeDef]
    ) -> ZonalShiftTypeDef:
        """
        You start a zonal shift to temporarily move load balancer traffic away from an
        Availability Zone in an Amazon Web Services Region, to help your application
        recover immediately, for example, from a developer's bad code deployment or
        from an Amazon Web Services infrastructure failure in a single Av...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/start_zonal_shift.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#start_zonal_shift)
        """

    async def update_autoshift_observer_notification_status(
        self, **kwargs: Unpack[UpdateAutoshiftObserverNotificationStatusRequestRequestTypeDef]
    ) -> UpdateAutoshiftObserverNotificationStatusResponseTypeDef:
        """
        Update the status of autoshift observer notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/update_autoshift_observer_notification_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#update_autoshift_observer_notification_status)
        """

    async def update_practice_run_configuration(
        self, **kwargs: Unpack[UpdatePracticeRunConfigurationRequestRequestTypeDef]
    ) -> UpdatePracticeRunConfigurationResponseTypeDef:
        """
        Update a practice run configuration to change one or more of the following:
        add, change, or remove the blocking alarm; change the outcome alarm; or add,
        change, or remove blocking dates or time windows.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/update_practice_run_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#update_practice_run_configuration)
        """

    async def update_zonal_autoshift_configuration(
        self, **kwargs: Unpack[UpdateZonalAutoshiftConfigurationRequestRequestTypeDef]
    ) -> UpdateZonalAutoshiftConfigurationResponseTypeDef:
        """
        The zonal autoshift configuration for a resource includes the practice run
        configuration and the status for running autoshifts, zonal autoshift status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/update_zonal_autoshift_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#update_zonal_autoshift_configuration)
        """

    async def update_zonal_shift(
        self, **kwargs: Unpack[UpdateZonalShiftRequestRequestTypeDef]
    ) -> ZonalShiftTypeDef:
        """
        Update an active zonal shift in Amazon Route 53 Application Recovery Controller
        in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/update_zonal_shift.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#update_zonal_shift)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_autoshifts"]
    ) -> ListAutoshiftsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_resources"]
    ) -> ListManagedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_zonal_shifts"]
    ) -> ListZonalShiftsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_zonal_shift/client/)
        """
