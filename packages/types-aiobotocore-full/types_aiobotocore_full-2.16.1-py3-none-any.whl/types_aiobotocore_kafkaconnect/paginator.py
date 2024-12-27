"""
Type annotations for kafkaconnect service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kafkaconnect.client import KafkaConnectClient
    from types_aiobotocore_kafkaconnect.paginator import (
        ListConnectorsPaginator,
        ListCustomPluginsPaginator,
        ListWorkerConfigurationsPaginator,
    )

    session = get_session()
    with session.create_client("kafkaconnect") as client:
        client: KafkaConnectClient

        list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
        list_custom_plugins_paginator: ListCustomPluginsPaginator = client.get_paginator("list_custom_plugins")
        list_worker_configurations_paginator: ListWorkerConfigurationsPaginator = client.get_paginator("list_worker_configurations")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListConnectorsRequestPaginateTypeDef,
    ListConnectorsResponseTypeDef,
    ListCustomPluginsRequestPaginateTypeDef,
    ListCustomPluginsResponseTypeDef,
    ListWorkerConfigurationsRequestPaginateTypeDef,
    ListWorkerConfigurationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListConnectorsPaginator",
    "ListCustomPluginsPaginator",
    "ListWorkerConfigurationsPaginator",
)


if TYPE_CHECKING:
    _ListConnectorsPaginatorBase = AioPaginator[ListConnectorsResponseTypeDef]
else:
    _ListConnectorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectorsPaginator(_ListConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/paginator/ListConnectors.html#KafkaConnect.Paginator.ListConnectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listconnectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/paginator/ListConnectors.html#KafkaConnect.Paginator.ListConnectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listconnectorspaginator)
        """


if TYPE_CHECKING:
    _ListCustomPluginsPaginatorBase = AioPaginator[ListCustomPluginsResponseTypeDef]
else:
    _ListCustomPluginsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomPluginsPaginator(_ListCustomPluginsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/paginator/ListCustomPlugins.html#KafkaConnect.Paginator.ListCustomPlugins)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listcustompluginspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomPluginsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/paginator/ListCustomPlugins.html#KafkaConnect.Paginator.ListCustomPlugins.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listcustompluginspaginator)
        """


if TYPE_CHECKING:
    _ListWorkerConfigurationsPaginatorBase = AioPaginator[ListWorkerConfigurationsResponseTypeDef]
else:
    _ListWorkerConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkerConfigurationsPaginator(_ListWorkerConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/paginator/ListWorkerConfigurations.html#KafkaConnect.Paginator.ListWorkerConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listworkerconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkerConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkerConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect/paginator/ListWorkerConfigurations.html#KafkaConnect.Paginator.ListWorkerConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listworkerconfigurationspaginator)
        """
