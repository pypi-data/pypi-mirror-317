"""
Type annotations for dsql service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dsql/type_defs/)

Usage::

    ```python
    from types_boto3_dsql.type_defs import ClusterSummaryTypeDef

    data: ClusterSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence

from .literals import ClusterStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ClusterSummaryTypeDef",
    "CreateClusterInputRequestTypeDef",
    "CreateClusterOutputTypeDef",
    "CreateMultiRegionClustersInputRequestTypeDef",
    "CreateMultiRegionClustersOutputTypeDef",
    "DeleteClusterInputRequestTypeDef",
    "DeleteClusterOutputTypeDef",
    "DeleteMultiRegionClustersInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetClusterInputRequestTypeDef",
    "GetClusterInputWaitTypeDef",
    "GetClusterOutputTypeDef",
    "LinkedClusterPropertiesTypeDef",
    "ListClustersInputPaginateTypeDef",
    "ListClustersInputRequestTypeDef",
    "ListClustersOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateClusterInputRequestTypeDef",
    "UpdateClusterOutputTypeDef",
    "WaiterConfigTypeDef",
)


class ClusterSummaryTypeDef(TypedDict):
    identifier: str
    arn: str


class CreateClusterInputRequestTypeDef(TypedDict):
    deletionProtectionEnabled: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class LinkedClusterPropertiesTypeDef(TypedDict):
    deletionProtectionEnabled: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class DeleteClusterInputRequestTypeDef(TypedDict):
    identifier: str
    clientToken: NotRequired[str]


class DeleteMultiRegionClustersInputRequestTypeDef(TypedDict):
    linkedClusterArns: Sequence[str]
    clientToken: NotRequired[str]


class GetClusterInputRequestTypeDef(TypedDict):
    identifier: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListClustersInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateClusterInputRequestTypeDef(TypedDict):
    identifier: str
    deletionProtectionEnabled: NotRequired[bool]
    clientToken: NotRequired[str]


class CreateClusterOutputTypeDef(TypedDict):
    identifier: str
    arn: str
    status: ClusterStatusType
    creationTime: datetime
    deletionProtectionEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMultiRegionClustersOutputTypeDef(TypedDict):
    linkedClusterArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterOutputTypeDef(TypedDict):
    identifier: str
    arn: str
    status: ClusterStatusType
    creationTime: datetime
    deletionProtectionEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetClusterOutputTypeDef(TypedDict):
    identifier: str
    arn: str
    status: ClusterStatusType
    creationTime: datetime
    deletionProtectionEnabled: bool
    witnessRegion: str
    linkedClusterArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListClustersOutputTypeDef(TypedDict):
    clusters: list[ClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterOutputTypeDef(TypedDict):
    identifier: str
    arn: str
    status: ClusterStatusType
    creationTime: datetime
    deletionProtectionEnabled: bool
    witnessRegion: str
    linkedClusterArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMultiRegionClustersInputRequestTypeDef(TypedDict):
    linkedRegionList: Sequence[str]
    witnessRegion: str
    clusterProperties: NotRequired[Mapping[str, LinkedClusterPropertiesTypeDef]]
    clientToken: NotRequired[str]


class GetClusterInputWaitTypeDef(TypedDict):
    identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ListClustersInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
