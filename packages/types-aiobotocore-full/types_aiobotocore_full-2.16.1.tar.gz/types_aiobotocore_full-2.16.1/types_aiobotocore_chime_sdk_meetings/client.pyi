"""
Type annotations for chime-sdk-meetings service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_meetings.client import ChimeSDKMeetingsClient

    session = get_session()
    async with session.create_client("chime-sdk-meetings") as client:
        client: ChimeSDKMeetingsClient
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
    BatchCreateAttendeeRequestRequestTypeDef,
    BatchCreateAttendeeResponseTypeDef,
    BatchUpdateAttendeeCapabilitiesExceptRequestRequestTypeDef,
    CreateAttendeeRequestRequestTypeDef,
    CreateAttendeeResponseTypeDef,
    CreateMeetingRequestRequestTypeDef,
    CreateMeetingResponseTypeDef,
    CreateMeetingWithAttendeesRequestRequestTypeDef,
    CreateMeetingWithAttendeesResponseTypeDef,
    DeleteAttendeeRequestRequestTypeDef,
    DeleteMeetingRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAttendeeRequestRequestTypeDef,
    GetAttendeeResponseTypeDef,
    GetMeetingRequestRequestTypeDef,
    GetMeetingResponseTypeDef,
    ListAttendeesRequestRequestTypeDef,
    ListAttendeesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartMeetingTranscriptionRequestRequestTypeDef,
    StopMeetingTranscriptionRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAttendeeCapabilitiesRequestRequestTypeDef,
    UpdateAttendeeCapabilitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("ChimeSDKMeetingsClient",)

class Exceptions(BaseClientExceptions):
    BadRequestException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    ForbiddenException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    NotFoundException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceFailureException: type[BotocoreClientError]
    ServiceUnavailableException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TooManyTagsException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    UnprocessableEntityException: type[BotocoreClientError]

class ChimeSDKMeetingsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKMeetingsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#generate_presigned_url)
        """

    async def batch_create_attendee(
        self, **kwargs: Unpack[BatchCreateAttendeeRequestRequestTypeDef]
    ) -> BatchCreateAttendeeResponseTypeDef:
        """
        Creates up to 100 attendees for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/batch_create_attendee.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#batch_create_attendee)
        """

    async def batch_update_attendee_capabilities_except(
        self, **kwargs: Unpack[BatchUpdateAttendeeCapabilitiesExceptRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates <code>AttendeeCapabilities</code> except the capabilities listed in an
        <code>ExcludedAttendeeIds</code> table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/batch_update_attendee_capabilities_except.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#batch_update_attendee_capabilities_except)
        """

    async def create_attendee(
        self, **kwargs: Unpack[CreateAttendeeRequestRequestTypeDef]
    ) -> CreateAttendeeResponseTypeDef:
        """
        Creates a new attendee for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/create_attendee.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#create_attendee)
        """

    async def create_meeting(
        self, **kwargs: Unpack[CreateMeetingRequestRequestTypeDef]
    ) -> CreateMeetingResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region with no
        initial attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/create_meeting.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#create_meeting)
        """

    async def create_meeting_with_attendees(
        self, **kwargs: Unpack[CreateMeetingWithAttendeesRequestRequestTypeDef]
    ) -> CreateMeetingWithAttendeesResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region, with
        attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/create_meeting_with_attendees.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#create_meeting_with_attendees)
        """

    async def delete_attendee(
        self, **kwargs: Unpack[DeleteAttendeeRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an attendee from the specified Amazon Chime SDK meeting and deletes
        their <code>JoinToken</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/delete_attendee.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#delete_attendee)
        """

    async def delete_meeting(
        self, **kwargs: Unpack[DeleteMeetingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/delete_meeting.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#delete_meeting)
        """

    async def get_attendee(
        self, **kwargs: Unpack[GetAttendeeRequestRequestTypeDef]
    ) -> GetAttendeeResponseTypeDef:
        """
        Gets the Amazon Chime SDK attendee details for a specified meeting ID and
        attendee ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/get_attendee.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#get_attendee)
        """

    async def get_meeting(
        self, **kwargs: Unpack[GetMeetingRequestRequestTypeDef]
    ) -> GetMeetingResponseTypeDef:
        """
        Gets the Amazon Chime SDK meeting details for the specified meeting ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/get_meeting.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#get_meeting)
        """

    async def list_attendees(
        self, **kwargs: Unpack[ListAttendeesRequestRequestTypeDef]
    ) -> ListAttendeesResponseTypeDef:
        """
        Lists the attendees for the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/list_attendees.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#list_attendees)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags available for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#list_tags_for_resource)
        """

    async def start_meeting_transcription(
        self, **kwargs: Unpack[StartMeetingTranscriptionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts transcription for the specified <code>meetingId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/start_meeting_transcription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#start_meeting_transcription)
        """

    async def stop_meeting_transcription(
        self, **kwargs: Unpack[StopMeetingTranscriptionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops transcription for the specified <code>meetingId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/stop_meeting_transcription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#stop_meeting_transcription)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        The resource that supports tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes the specified tags from the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#untag_resource)
        """

    async def update_attendee_capabilities(
        self, **kwargs: Unpack[UpdateAttendeeCapabilitiesRequestRequestTypeDef]
    ) -> UpdateAttendeeCapabilitiesResponseTypeDef:
        """
        The capabilities that you want to update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings/client/update_attendee_capabilities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#update_attendee_capabilities)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/)
        """
