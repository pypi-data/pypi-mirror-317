"""
Type annotations for geo-maps service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_geo_maps.client import LocationServiceMapsV2Client

    session = get_session()
    async with session.create_client("geo-maps") as client:
        client: LocationServiceMapsV2Client
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, Mapping

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    GetGlyphsRequestRequestTypeDef,
    GetGlyphsResponseTypeDef,
    GetSpritesRequestRequestTypeDef,
    GetSpritesResponseTypeDef,
    GetStaticMapRequestRequestTypeDef,
    GetStaticMapResponseTypeDef,
    GetStyleDescriptorRequestRequestTypeDef,
    GetStyleDescriptorResponseTypeDef,
    GetTileRequestRequestTypeDef,
    GetTileResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("LocationServiceMapsV2Client",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class LocationServiceMapsV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServiceMapsV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/#generate_presigned_url)
        """

    async def get_glyphs(
        self, **kwargs: Unpack[GetGlyphsRequestRequestTypeDef]
    ) -> GetGlyphsResponseTypeDef:
        """
        Returns the map's glyphs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps/client/get_glyphs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/#get_glyphs)
        """

    async def get_sprites(
        self, **kwargs: Unpack[GetSpritesRequestRequestTypeDef]
    ) -> GetSpritesResponseTypeDef:
        """
        Returns the map's sprites.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps/client/get_sprites.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/#get_sprites)
        """

    async def get_static_map(
        self, **kwargs: Unpack[GetStaticMapRequestRequestTypeDef]
    ) -> GetStaticMapResponseTypeDef:
        """
        Provides high-quality static map images with customizable options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps/client/get_static_map.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/#get_static_map)
        """

    async def get_style_descriptor(
        self, **kwargs: Unpack[GetStyleDescriptorRequestRequestTypeDef]
    ) -> GetStyleDescriptorResponseTypeDef:
        """
        Returns information about the style.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps/client/get_style_descriptor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/#get_style_descriptor)
        """

    async def get_tile(
        self, **kwargs: Unpack[GetTileRequestRequestTypeDef]
    ) -> GetTileResponseTypeDef:
        """
        Returns a tile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps/client/get_tile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/#get_tile)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/geo-maps.html#LocationServiceMapsV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_geo_maps/client/)
        """
