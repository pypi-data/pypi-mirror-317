"""
Type annotations for controlcatalog service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_controlcatalog/type_defs/)

Usage::

    ```python
    from types_boto3_controlcatalog.type_defs import AssociatedDomainSummaryTypeDef

    data: AssociatedDomainSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence

from .literals import ControlBehaviorType, ControlScopeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AssociatedDomainSummaryTypeDef",
    "AssociatedObjectiveSummaryTypeDef",
    "CommonControlFilterTypeDef",
    "CommonControlSummaryTypeDef",
    "ControlParameterTypeDef",
    "ControlSummaryTypeDef",
    "DomainResourceFilterTypeDef",
    "DomainSummaryTypeDef",
    "GetControlRequestRequestTypeDef",
    "GetControlResponseTypeDef",
    "ImplementationDetailsTypeDef",
    "ListCommonControlsRequestPaginateTypeDef",
    "ListCommonControlsRequestRequestTypeDef",
    "ListCommonControlsResponseTypeDef",
    "ListControlsRequestPaginateTypeDef",
    "ListControlsRequestRequestTypeDef",
    "ListControlsResponseTypeDef",
    "ListDomainsRequestPaginateTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "ListObjectivesRequestPaginateTypeDef",
    "ListObjectivesRequestRequestTypeDef",
    "ListObjectivesResponseTypeDef",
    "ObjectiveFilterTypeDef",
    "ObjectiveResourceFilterTypeDef",
    "ObjectiveSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "RegionConfigurationTypeDef",
    "ResponseMetadataTypeDef",
)


class AssociatedDomainSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class AssociatedObjectiveSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class ObjectiveResourceFilterTypeDef(TypedDict):
    Arn: NotRequired[str]


class ControlParameterTypeDef(TypedDict):
    Name: str


class ControlSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str


class DomainResourceFilterTypeDef(TypedDict):
    Arn: NotRequired[str]


class DomainSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    CreateTime: datetime
    LastUpdateTime: datetime


class GetControlRequestRequestTypeDef(TypedDict):
    ControlArn: str


ImplementationDetailsTypeDef = TypedDict(
    "ImplementationDetailsTypeDef",
    {
        "Type": str,
    },
)


class RegionConfigurationTypeDef(TypedDict):
    Scope: ControlScopeType
    DeployableRegions: NotRequired[list[str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListControlsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDomainsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ObjectiveSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    Domain: AssociatedDomainSummaryTypeDef
    CreateTime: datetime
    LastUpdateTime: datetime


class CommonControlSummaryTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    Domain: AssociatedDomainSummaryTypeDef
    Objective: AssociatedObjectiveSummaryTypeDef
    CreateTime: datetime
    LastUpdateTime: datetime


class CommonControlFilterTypeDef(TypedDict):
    Objectives: NotRequired[Sequence[ObjectiveResourceFilterTypeDef]]


class ObjectiveFilterTypeDef(TypedDict):
    Domains: NotRequired[Sequence[DomainResourceFilterTypeDef]]


class GetControlResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    Behavior: ControlBehaviorType
    RegionConfiguration: RegionConfigurationTypeDef
    Implementation: ImplementationDetailsTypeDef
    Parameters: list[ControlParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListControlsResponseTypeDef(TypedDict):
    Controls: list[ControlSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDomainsResponseTypeDef(TypedDict):
    Domains: list[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListControlsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListObjectivesResponseTypeDef(TypedDict):
    Objectives: list[ObjectiveSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCommonControlsResponseTypeDef(TypedDict):
    CommonControls: list[CommonControlSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListCommonControlsRequestPaginateTypeDef(TypedDict):
    CommonControlFilter: NotRequired[CommonControlFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCommonControlsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    CommonControlFilter: NotRequired[CommonControlFilterTypeDef]


class ListObjectivesRequestPaginateTypeDef(TypedDict):
    ObjectiveFilter: NotRequired[ObjectiveFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListObjectivesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ObjectiveFilter: NotRequired[ObjectiveFilterTypeDef]
