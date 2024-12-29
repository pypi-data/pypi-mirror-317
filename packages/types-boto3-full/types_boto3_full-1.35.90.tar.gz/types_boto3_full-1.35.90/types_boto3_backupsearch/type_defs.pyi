"""
Type annotations for backupsearch service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_backupsearch/type_defs/)

Usage::

    ```python
    from types_boto3_backupsearch.type_defs import BackupCreationTimeFilterOutputTypeDef

    data: BackupCreationTimeFilterOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    ExportJobStatusType,
    LongConditionOperatorType,
    ResourceTypeType,
    SearchJobStateType,
    StringConditionOperatorType,
    TimeConditionOperatorType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BackupCreationTimeFilterOutputTypeDef",
    "BackupCreationTimeFilterTypeDef",
    "BackupCreationTimeFilterUnionTypeDef",
    "CurrentSearchProgressTypeDef",
    "EBSItemFilterOutputTypeDef",
    "EBSItemFilterTypeDef",
    "EBSItemFilterUnionTypeDef",
    "EBSResultItemTypeDef",
    "ExportJobSummaryTypeDef",
    "ExportSpecificationTypeDef",
    "GetSearchJobInputRequestTypeDef",
    "GetSearchJobOutputTypeDef",
    "GetSearchResultExportJobInputRequestTypeDef",
    "GetSearchResultExportJobOutputTypeDef",
    "ItemFiltersOutputTypeDef",
    "ItemFiltersTypeDef",
    "ListSearchJobBackupsInputPaginateTypeDef",
    "ListSearchJobBackupsInputRequestTypeDef",
    "ListSearchJobBackupsOutputTypeDef",
    "ListSearchJobResultsInputPaginateTypeDef",
    "ListSearchJobResultsInputRequestTypeDef",
    "ListSearchJobResultsOutputTypeDef",
    "ListSearchJobsInputPaginateTypeDef",
    "ListSearchJobsInputRequestTypeDef",
    "ListSearchJobsOutputTypeDef",
    "ListSearchResultExportJobsInputPaginateTypeDef",
    "ListSearchResultExportJobsInputRequestTypeDef",
    "ListSearchResultExportJobsOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LongConditionTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "ResultItemTypeDef",
    "S3ExportSpecificationTypeDef",
    "S3ItemFilterOutputTypeDef",
    "S3ItemFilterTypeDef",
    "S3ItemFilterUnionTypeDef",
    "S3ResultItemTypeDef",
    "SearchJobBackupsResultTypeDef",
    "SearchJobSummaryTypeDef",
    "SearchScopeOutputTypeDef",
    "SearchScopeSummaryTypeDef",
    "SearchScopeTypeDef",
    "StartSearchJobInputRequestTypeDef",
    "StartSearchJobOutputTypeDef",
    "StartSearchResultExportJobInputRequestTypeDef",
    "StartSearchResultExportJobOutputTypeDef",
    "StopSearchJobInputRequestTypeDef",
    "StringConditionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimeConditionOutputTypeDef",
    "TimeConditionTypeDef",
    "TimeConditionUnionTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
)

class BackupCreationTimeFilterOutputTypeDef(TypedDict):
    CreatedAfter: NotRequired[datetime]
    CreatedBefore: NotRequired[datetime]

TimestampTypeDef = Union[datetime, str]

class CurrentSearchProgressTypeDef(TypedDict):
    RecoveryPointsScannedCount: NotRequired[int]
    ItemsScannedCount: NotRequired[int]
    ItemsMatchedCount: NotRequired[int]

class LongConditionTypeDef(TypedDict):
    Value: int
    Operator: NotRequired[LongConditionOperatorType]

class StringConditionTypeDef(TypedDict):
    Value: str
    Operator: NotRequired[StringConditionOperatorType]

class TimeConditionOutputTypeDef(TypedDict):
    Value: datetime
    Operator: NotRequired[TimeConditionOperatorType]

class EBSResultItemTypeDef(TypedDict):
    BackupResourceArn: NotRequired[str]
    SourceResourceArn: NotRequired[str]
    BackupVaultName: NotRequired[str]
    FileSystemIdentifier: NotRequired[str]
    FilePath: NotRequired[str]
    FileSize: NotRequired[int]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class ExportJobSummaryTypeDef(TypedDict):
    ExportJobIdentifier: str
    ExportJobArn: NotRequired[str]
    Status: NotRequired[ExportJobStatusType]
    CreationTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    StatusMessage: NotRequired[str]
    SearchJobArn: NotRequired[str]

class S3ExportSpecificationTypeDef(TypedDict):
    DestinationBucket: str
    DestinationPrefix: NotRequired[str]

class GetSearchJobInputRequestTypeDef(TypedDict):
    SearchJobIdentifier: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class SearchScopeSummaryTypeDef(TypedDict):
    TotalRecoveryPointsToScanCount: NotRequired[int]
    TotalItemsToScanCount: NotRequired[int]

class GetSearchResultExportJobInputRequestTypeDef(TypedDict):
    ExportJobIdentifier: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListSearchJobBackupsInputRequestTypeDef(TypedDict):
    SearchJobIdentifier: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class SearchJobBackupsResultTypeDef(TypedDict):
    Status: NotRequired[SearchJobStateType]
    StatusMessage: NotRequired[str]
    ResourceType: NotRequired[ResourceTypeType]
    BackupResourceArn: NotRequired[str]
    SourceResourceArn: NotRequired[str]
    IndexCreationTime: NotRequired[datetime]
    BackupCreationTime: NotRequired[datetime]

class ListSearchJobResultsInputRequestTypeDef(TypedDict):
    SearchJobIdentifier: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListSearchJobsInputRequestTypeDef(TypedDict):
    ByStatus: NotRequired[SearchJobStateType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListSearchResultExportJobsInputRequestTypeDef(TypedDict):
    Status: NotRequired[ExportJobStatusType]
    SearchJobIdentifier: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class S3ResultItemTypeDef(TypedDict):
    BackupResourceArn: NotRequired[str]
    SourceResourceArn: NotRequired[str]
    BackupVaultName: NotRequired[str]
    ObjectKey: NotRequired[str]
    ObjectSize: NotRequired[int]
    CreationTime: NotRequired[datetime]
    ETag: NotRequired[str]
    VersionId: NotRequired[str]

class StopSearchJobInputRequestTypeDef(TypedDict):
    SearchJobIdentifier: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class SearchScopeOutputTypeDef(TypedDict):
    BackupResourceTypes: list[ResourceTypeType]
    BackupResourceCreationTime: NotRequired[BackupCreationTimeFilterOutputTypeDef]
    SourceResourceArns: NotRequired[list[str]]
    BackupResourceArns: NotRequired[list[str]]
    BackupResourceTags: NotRequired[dict[str, str]]

class BackupCreationTimeFilterTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]

class TimeConditionTypeDef(TypedDict):
    Value: TimestampTypeDef
    Operator: NotRequired[TimeConditionOperatorType]

class EBSItemFilterOutputTypeDef(TypedDict):
    FilePaths: NotRequired[list[StringConditionTypeDef]]
    Sizes: NotRequired[list[LongConditionTypeDef]]
    CreationTimes: NotRequired[list[TimeConditionOutputTypeDef]]
    LastModificationTimes: NotRequired[list[TimeConditionOutputTypeDef]]

class S3ItemFilterOutputTypeDef(TypedDict):
    ObjectKeys: NotRequired[list[StringConditionTypeDef]]
    Sizes: NotRequired[list[LongConditionTypeDef]]
    CreationTimes: NotRequired[list[TimeConditionOutputTypeDef]]
    VersionIds: NotRequired[list[StringConditionTypeDef]]
    ETags: NotRequired[list[StringConditionTypeDef]]

class ExportSpecificationTypeDef(TypedDict):
    s3ExportSpecification: NotRequired[S3ExportSpecificationTypeDef]

class ListSearchResultExportJobsOutputTypeDef(TypedDict):
    ExportJobs: list[ExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartSearchJobOutputTypeDef(TypedDict):
    SearchJobArn: str
    CreationTime: datetime
    SearchJobIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartSearchResultExportJobOutputTypeDef(TypedDict):
    ExportJobArn: str
    ExportJobIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class SearchJobSummaryTypeDef(TypedDict):
    SearchJobIdentifier: NotRequired[str]
    SearchJobArn: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[SearchJobStateType]
    CreationTime: NotRequired[datetime]
    CompletionTime: NotRequired[datetime]
    SearchScopeSummary: NotRequired[SearchScopeSummaryTypeDef]
    StatusMessage: NotRequired[str]

class ListSearchJobBackupsInputPaginateTypeDef(TypedDict):
    SearchJobIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSearchJobResultsInputPaginateTypeDef(TypedDict):
    SearchJobIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSearchJobsInputPaginateTypeDef(TypedDict):
    ByStatus: NotRequired[SearchJobStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSearchResultExportJobsInputPaginateTypeDef(TypedDict):
    Status: NotRequired[ExportJobStatusType]
    SearchJobIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSearchJobBackupsOutputTypeDef(TypedDict):
    Results: list[SearchJobBackupsResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ResultItemTypeDef(TypedDict):
    S3ResultItem: NotRequired[S3ResultItemTypeDef]
    EBSResultItem: NotRequired[EBSResultItemTypeDef]

BackupCreationTimeFilterUnionTypeDef = Union[
    BackupCreationTimeFilterTypeDef, BackupCreationTimeFilterOutputTypeDef
]

class S3ItemFilterTypeDef(TypedDict):
    ObjectKeys: NotRequired[Sequence[StringConditionTypeDef]]
    Sizes: NotRequired[Sequence[LongConditionTypeDef]]
    CreationTimes: NotRequired[Sequence[TimeConditionTypeDef]]
    VersionIds: NotRequired[Sequence[StringConditionTypeDef]]
    ETags: NotRequired[Sequence[StringConditionTypeDef]]

TimeConditionUnionTypeDef = Union[TimeConditionTypeDef, TimeConditionOutputTypeDef]

class ItemFiltersOutputTypeDef(TypedDict):
    S3ItemFilters: NotRequired[list[S3ItemFilterOutputTypeDef]]
    EBSItemFilters: NotRequired[list[EBSItemFilterOutputTypeDef]]

class GetSearchResultExportJobOutputTypeDef(TypedDict):
    ExportJobIdentifier: str
    ExportJobArn: str
    Status: ExportJobStatusType
    CreationTime: datetime
    CompletionTime: datetime
    StatusMessage: str
    ExportSpecification: ExportSpecificationTypeDef
    SearchJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartSearchResultExportJobInputRequestTypeDef(TypedDict):
    SearchJobIdentifier: str
    ExportSpecification: ExportSpecificationTypeDef
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    RoleArn: NotRequired[str]

class ListSearchJobsOutputTypeDef(TypedDict):
    SearchJobs: list[SearchJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSearchJobResultsOutputTypeDef(TypedDict):
    Results: list[ResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SearchScopeTypeDef(TypedDict):
    BackupResourceTypes: Sequence[ResourceTypeType]
    BackupResourceCreationTime: NotRequired[BackupCreationTimeFilterUnionTypeDef]
    SourceResourceArns: NotRequired[Sequence[str]]
    BackupResourceArns: NotRequired[Sequence[str]]
    BackupResourceTags: NotRequired[Mapping[str, str]]

S3ItemFilterUnionTypeDef = Union[S3ItemFilterTypeDef, S3ItemFilterOutputTypeDef]

class EBSItemFilterTypeDef(TypedDict):
    FilePaths: NotRequired[Sequence[StringConditionTypeDef]]
    Sizes: NotRequired[Sequence[LongConditionTypeDef]]
    CreationTimes: NotRequired[Sequence[TimeConditionUnionTypeDef]]
    LastModificationTimes: NotRequired[Sequence[TimeConditionTypeDef]]

class GetSearchJobOutputTypeDef(TypedDict):
    Name: str
    SearchScopeSummary: SearchScopeSummaryTypeDef
    CurrentSearchProgress: CurrentSearchProgressTypeDef
    StatusMessage: str
    EncryptionKeyArn: str
    CompletionTime: datetime
    Status: SearchJobStateType
    SearchScope: SearchScopeOutputTypeDef
    ItemFilters: ItemFiltersOutputTypeDef
    CreationTime: datetime
    SearchJobIdentifier: str
    SearchJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

EBSItemFilterUnionTypeDef = Union[EBSItemFilterTypeDef, EBSItemFilterOutputTypeDef]

class ItemFiltersTypeDef(TypedDict):
    S3ItemFilters: NotRequired[Sequence[S3ItemFilterUnionTypeDef]]
    EBSItemFilters: NotRequired[Sequence[EBSItemFilterUnionTypeDef]]

class StartSearchJobInputRequestTypeDef(TypedDict):
    SearchScope: SearchScopeTypeDef
    Tags: NotRequired[Mapping[str, str]]
    Name: NotRequired[str]
    EncryptionKeyArn: NotRequired[str]
    ClientToken: NotRequired[str]
    ItemFilters: NotRequired[ItemFiltersTypeDef]
