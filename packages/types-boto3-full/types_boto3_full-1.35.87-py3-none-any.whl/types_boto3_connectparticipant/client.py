"""
Type annotations for connectparticipant service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_connectparticipant.client import ConnectParticipantClient

    session = Session()
    client: ConnectParticipantClient = session.client("connectparticipant")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CancelParticipantAuthenticationRequestRequestTypeDef,
    CompleteAttachmentUploadRequestRequestTypeDef,
    CreateParticipantConnectionRequestRequestTypeDef,
    CreateParticipantConnectionResponseTypeDef,
    DescribeViewRequestRequestTypeDef,
    DescribeViewResponseTypeDef,
    DisconnectParticipantRequestRequestTypeDef,
    GetAttachmentRequestRequestTypeDef,
    GetAttachmentResponseTypeDef,
    GetAuthenticationUrlRequestRequestTypeDef,
    GetAuthenticationUrlResponseTypeDef,
    GetTranscriptRequestRequestTypeDef,
    GetTranscriptResponseTypeDef,
    SendEventRequestRequestTypeDef,
    SendEventResponseTypeDef,
    SendMessageRequestRequestTypeDef,
    SendMessageResponseTypeDef,
    StartAttachmentUploadRequestRequestTypeDef,
    StartAttachmentUploadResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ConnectParticipantClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class ConnectParticipantClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectParticipantClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#generate_presigned_url)
        """

    def cancel_participant_authentication(
        self, **kwargs: Unpack[CancelParticipantAuthenticationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Cancels the authentication session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/cancel_participant_authentication.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#cancel_participant_authentication)
        """

    def complete_attachment_upload(
        self, **kwargs: Unpack[CompleteAttachmentUploadRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Allows you to confirm that the attachment has been uploaded using the
        pre-signed URL provided in StartAttachmentUpload API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/complete_attachment_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#complete_attachment_upload)
        """

    def create_participant_connection(
        self, **kwargs: Unpack[CreateParticipantConnectionRequestRequestTypeDef]
    ) -> CreateParticipantConnectionResponseTypeDef:
        """
        Creates the participant's connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/create_participant_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#create_participant_connection)
        """

    def describe_view(
        self, **kwargs: Unpack[DescribeViewRequestRequestTypeDef]
    ) -> DescribeViewResponseTypeDef:
        """
        Retrieves the view for the specified view token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/describe_view.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#describe_view)
        """

    def disconnect_participant(
        self, **kwargs: Unpack[DisconnectParticipantRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disconnects a participant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/disconnect_participant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#disconnect_participant)
        """

    def get_attachment(
        self, **kwargs: Unpack[GetAttachmentRequestRequestTypeDef]
    ) -> GetAttachmentResponseTypeDef:
        """
        Provides a pre-signed URL for download of a completed attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/get_attachment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#get_attachment)
        """

    def get_authentication_url(
        self, **kwargs: Unpack[GetAuthenticationUrlRequestRequestTypeDef]
    ) -> GetAuthenticationUrlResponseTypeDef:
        """
        Retrieves the AuthenticationUrl for the current authentication session for the
        AuthenticateCustomer flow block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/get_authentication_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#get_authentication_url)
        """

    def get_transcript(
        self, **kwargs: Unpack[GetTranscriptRequestRequestTypeDef]
    ) -> GetTranscriptResponseTypeDef:
        """
        Retrieves a transcript of the session, including details about any attachments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/get_transcript.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#get_transcript)
        """

    def send_event(
        self, **kwargs: Unpack[SendEventRequestRequestTypeDef]
    ) -> SendEventResponseTypeDef:
        """
        The
        <code>application/vnd.amazonaws.connect.event.connection.acknowledged</code>
        ContentType will no longer be supported starting December 31, 2024.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/send_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#send_event)
        """

    def send_message(
        self, **kwargs: Unpack[SendMessageRequestRequestTypeDef]
    ) -> SendMessageResponseTypeDef:
        """
        Sends a message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/send_message.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#send_message)
        """

    def start_attachment_upload(
        self, **kwargs: Unpack[StartAttachmentUploadRequestRequestTypeDef]
    ) -> StartAttachmentUploadResponseTypeDef:
        """
        Provides a pre-signed Amazon S3 URL in response for uploading the file directly
        to S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/start_attachment_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectparticipant/client/#start_attachment_upload)
        """
