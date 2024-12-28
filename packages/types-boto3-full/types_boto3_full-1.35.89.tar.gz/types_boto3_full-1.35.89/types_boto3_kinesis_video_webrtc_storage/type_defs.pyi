"""
Type annotations for kinesis-video-webrtc-storage service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kinesis_video_webrtc_storage/type_defs/)

Usage::

    ```python
    from types_boto3_kinesis_video_webrtc_storage.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "EmptyResponseMetadataTypeDef",
    "JoinStorageSessionAsViewerInputRequestTypeDef",
    "JoinStorageSessionInputRequestTypeDef",
    "ResponseMetadataTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class JoinStorageSessionAsViewerInputRequestTypeDef(TypedDict):
    channelArn: str
    clientId: str

class JoinStorageSessionInputRequestTypeDef(TypedDict):
    channelArn: str

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef
