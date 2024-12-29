"""
Type annotations for codeguru-security service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/type_defs/)

Usage::

    ```python
    from types_boto3_codeguru_security.type_defs import FindingMetricsValuePerSeverityTypeDef

    data: FindingMetricsValuePerSeverityTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    AnalysisTypeType,
    ErrorCodeType,
    ScanStateType,
    ScanTypeType,
    SeverityType,
    StatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AccountFindingsMetricTypeDef",
    "BatchGetFindingsErrorTypeDef",
    "BatchGetFindingsRequestRequestTypeDef",
    "BatchGetFindingsResponseTypeDef",
    "CategoryWithFindingNumTypeDef",
    "CodeLineTypeDef",
    "CreateScanRequestRequestTypeDef",
    "CreateScanResponseTypeDef",
    "CreateUploadUrlRequestRequestTypeDef",
    "CreateUploadUrlResponseTypeDef",
    "EncryptionConfigTypeDef",
    "FilePathTypeDef",
    "FindingIdentifierTypeDef",
    "FindingMetricsValuePerSeverityTypeDef",
    "FindingTypeDef",
    "GetAccountConfigurationResponseTypeDef",
    "GetFindingsRequestPaginateTypeDef",
    "GetFindingsRequestRequestTypeDef",
    "GetFindingsResponseTypeDef",
    "GetMetricsSummaryRequestRequestTypeDef",
    "GetMetricsSummaryResponseTypeDef",
    "GetScanRequestRequestTypeDef",
    "GetScanResponseTypeDef",
    "ListFindingsMetricsRequestPaginateTypeDef",
    "ListFindingsMetricsRequestRequestTypeDef",
    "ListFindingsMetricsResponseTypeDef",
    "ListScansRequestPaginateTypeDef",
    "ListScansRequestRequestTypeDef",
    "ListScansResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MetricsSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "RecommendationTypeDef",
    "RemediationTypeDef",
    "ResourceIdTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ScanNameWithFindingNumTypeDef",
    "ScanSummaryTypeDef",
    "SuggestedFixTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccountConfigurationRequestRequestTypeDef",
    "UpdateAccountConfigurationResponseTypeDef",
    "VulnerabilityTypeDef",
)

class FindingMetricsValuePerSeverityTypeDef(TypedDict):
    critical: NotRequired[float]
    high: NotRequired[float]
    info: NotRequired[float]
    low: NotRequired[float]
    medium: NotRequired[float]

class BatchGetFindingsErrorTypeDef(TypedDict):
    errorCode: ErrorCodeType
    findingId: str
    message: str
    scanName: str

class FindingIdentifierTypeDef(TypedDict):
    findingId: str
    scanName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CategoryWithFindingNumTypeDef(TypedDict):
    categoryName: NotRequired[str]
    findingNumber: NotRequired[int]

class CodeLineTypeDef(TypedDict):
    content: NotRequired[str]
    number: NotRequired[int]

class ResourceIdTypeDef(TypedDict):
    codeArtifactId: NotRequired[str]

class CreateUploadUrlRequestRequestTypeDef(TypedDict):
    scanName: str

class EncryptionConfigTypeDef(TypedDict):
    kmsKeyArn: NotRequired[str]

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "id": NotRequired[str],
        "subResourceId": NotRequired[str],
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetFindingsRequestRequestTypeDef(TypedDict):
    scanName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[StatusType]

TimestampTypeDef = Union[datetime, str]

class GetScanRequestRequestTypeDef(TypedDict):
    scanName: str
    runId: NotRequired[str]

class ListScansRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ScanSummaryTypeDef(TypedDict):
    createdAt: datetime
    runId: str
    scanName: str
    scanState: ScanStateType
    scanNameArn: NotRequired[str]
    updatedAt: NotRequired[datetime]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ScanNameWithFindingNumTypeDef(TypedDict):
    findingNumber: NotRequired[int]
    scanName: NotRequired[str]

class RecommendationTypeDef(TypedDict):
    text: NotRequired[str]
    url: NotRequired[str]

class SuggestedFixTypeDef(TypedDict):
    code: NotRequired[str]
    description: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class AccountFindingsMetricTypeDef(TypedDict):
    closedFindings: NotRequired[FindingMetricsValuePerSeverityTypeDef]
    date: NotRequired[datetime]
    meanTimeToClose: NotRequired[FindingMetricsValuePerSeverityTypeDef]
    newFindings: NotRequired[FindingMetricsValuePerSeverityTypeDef]
    openFindings: NotRequired[FindingMetricsValuePerSeverityTypeDef]

class BatchGetFindingsRequestRequestTypeDef(TypedDict):
    findingIdentifiers: Sequence[FindingIdentifierTypeDef]

class CreateUploadUrlResponseTypeDef(TypedDict):
    codeArtifactId: str
    requestHeaders: dict[str, str]
    s3Url: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetScanResponseTypeDef(TypedDict):
    analysisType: AnalysisTypeType
    createdAt: datetime
    errorMessage: str
    numberOfRevisions: int
    runId: str
    scanName: str
    scanNameArn: str
    scanState: ScanStateType
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class FilePathTypeDef(TypedDict):
    codeSnippet: NotRequired[list[CodeLineTypeDef]]
    endLine: NotRequired[int]
    name: NotRequired[str]
    path: NotRequired[str]
    startLine: NotRequired[int]

class CreateScanRequestRequestTypeDef(TypedDict):
    resourceId: ResourceIdTypeDef
    scanName: str
    analysisType: NotRequired[AnalysisTypeType]
    clientToken: NotRequired[str]
    scanType: NotRequired[ScanTypeType]
    tags: NotRequired[Mapping[str, str]]

class CreateScanResponseTypeDef(TypedDict):
    resourceId: ResourceIdTypeDef
    runId: str
    scanName: str
    scanNameArn: str
    scanState: ScanStateType
    ResponseMetadata: ResponseMetadataTypeDef

class GetAccountConfigurationResponseTypeDef(TypedDict):
    encryptionConfig: EncryptionConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAccountConfigurationRequestRequestTypeDef(TypedDict):
    encryptionConfig: EncryptionConfigTypeDef

class UpdateAccountConfigurationResponseTypeDef(TypedDict):
    encryptionConfig: EncryptionConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetFindingsRequestPaginateTypeDef(TypedDict):
    scanName: str
    status: NotRequired[StatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListScansRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetMetricsSummaryRequestRequestTypeDef(TypedDict):
    date: TimestampTypeDef

class ListFindingsMetricsRequestPaginateTypeDef(TypedDict):
    endDate: TimestampTypeDef
    startDate: TimestampTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFindingsMetricsRequestRequestTypeDef(TypedDict):
    endDate: TimestampTypeDef
    startDate: TimestampTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListScansResponseTypeDef(TypedDict):
    summaries: list[ScanSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MetricsSummaryTypeDef(TypedDict):
    categoriesWithMostFindings: NotRequired[list[CategoryWithFindingNumTypeDef]]
    date: NotRequired[datetime]
    openFindings: NotRequired[FindingMetricsValuePerSeverityTypeDef]
    scansWithMostOpenCriticalFindings: NotRequired[list[ScanNameWithFindingNumTypeDef]]
    scansWithMostOpenFindings: NotRequired[list[ScanNameWithFindingNumTypeDef]]

class RemediationTypeDef(TypedDict):
    recommendation: NotRequired[RecommendationTypeDef]
    suggestedFixes: NotRequired[list[SuggestedFixTypeDef]]

class ListFindingsMetricsResponseTypeDef(TypedDict):
    findingsMetrics: list[AccountFindingsMetricTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

VulnerabilityTypeDef = TypedDict(
    "VulnerabilityTypeDef",
    {
        "filePath": NotRequired[FilePathTypeDef],
        "id": NotRequired[str],
        "itemCount": NotRequired[int],
        "referenceUrls": NotRequired[list[str]],
        "relatedVulnerabilities": NotRequired[list[str]],
    },
)

class GetMetricsSummaryResponseTypeDef(TypedDict):
    metricsSummary: MetricsSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

FindingTypeDef = TypedDict(
    "FindingTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "detectorId": NotRequired[str],
        "detectorName": NotRequired[str],
        "detectorTags": NotRequired[list[str]],
        "generatorId": NotRequired[str],
        "id": NotRequired[str],
        "remediation": NotRequired[RemediationTypeDef],
        "resource": NotRequired[ResourceTypeDef],
        "ruleId": NotRequired[str],
        "severity": NotRequired[SeverityType],
        "status": NotRequired[StatusType],
        "title": NotRequired[str],
        "type": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "vulnerability": NotRequired[VulnerabilityTypeDef],
    },
)

class BatchGetFindingsResponseTypeDef(TypedDict):
    failedFindings: list[BatchGetFindingsErrorTypeDef]
    findings: list[FindingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetFindingsResponseTypeDef(TypedDict):
    findings: list[FindingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
