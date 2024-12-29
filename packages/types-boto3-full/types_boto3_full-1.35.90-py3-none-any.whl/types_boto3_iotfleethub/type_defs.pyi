"""
Type annotations for iotfleethub service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotfleethub/type_defs/)

Usage::

    ```python
    from types_boto3_iotfleethub.type_defs import ApplicationSummaryTypeDef

    data: ApplicationSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Mapping, Sequence

from .literals import ApplicationStateType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ApplicationSummaryTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DescribeApplicationRequestRequestTypeDef",
    "DescribeApplicationResponseTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
)

class ApplicationSummaryTypeDef(TypedDict):
    applicationId: str
    applicationName: str
    applicationUrl: str
    applicationDescription: NotRequired[str]
    applicationCreationDate: NotRequired[int]
    applicationLastUpdateDate: NotRequired[int]
    applicationState: NotRequired[ApplicationStateType]

class CreateApplicationRequestRequestTypeDef(TypedDict):
    applicationName: str
    roleArn: str
    applicationDescription: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str
    clientToken: NotRequired[str]

class DescribeApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListApplicationsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    applicationId: str
    applicationName: NotRequired[str]
    applicationDescription: NotRequired[str]
    clientToken: NotRequired[str]

class CreateApplicationResponseTypeDef(TypedDict):
    applicationId: str
    applicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeApplicationResponseTypeDef(TypedDict):
    applicationId: str
    applicationArn: str
    applicationName: str
    applicationDescription: str
    applicationUrl: str
    applicationState: ApplicationStateType
    applicationCreationDate: int
    applicationLastUpdateDate: int
    roleArn: str
    ssoClientId: str
    errorMessage: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationsResponseTypeDef(TypedDict):
    applicationSummaries: list[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
