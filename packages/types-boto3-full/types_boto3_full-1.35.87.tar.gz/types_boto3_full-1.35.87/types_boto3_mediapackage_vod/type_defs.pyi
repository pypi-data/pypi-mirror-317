"""
Type annotations for mediapackage-vod service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mediapackage_vod/type_defs/)

Usage::

    ```python
    from types_boto3_mediapackage_vod.type_defs import AssetShallowTypeDef

    data: AssetShallowTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Mapping, Sequence, Union

from .literals import (
    AdMarkersType,
    EncryptionMethodType,
    ManifestLayoutType,
    PresetSpeke20AudioType,
    PresetSpeke20VideoType,
    ProfileType,
    ScteMarkersSourceType,
    SegmentTemplateFormatType,
    StreamOrderType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AssetShallowTypeDef",
    "AuthorizationTypeDef",
    "CmafEncryptionOutputTypeDef",
    "CmafEncryptionTypeDef",
    "CmafEncryptionUnionTypeDef",
    "CmafPackageOutputTypeDef",
    "CmafPackageTypeDef",
    "ConfigureLogsRequestRequestTypeDef",
    "ConfigureLogsResponseTypeDef",
    "CreateAssetRequestRequestTypeDef",
    "CreateAssetResponseTypeDef",
    "CreatePackagingConfigurationRequestRequestTypeDef",
    "CreatePackagingConfigurationResponseTypeDef",
    "CreatePackagingGroupRequestRequestTypeDef",
    "CreatePackagingGroupResponseTypeDef",
    "DashEncryptionOutputTypeDef",
    "DashEncryptionTypeDef",
    "DashEncryptionUnionTypeDef",
    "DashManifestTypeDef",
    "DashPackageOutputTypeDef",
    "DashPackageTypeDef",
    "DeleteAssetRequestRequestTypeDef",
    "DeletePackagingConfigurationRequestRequestTypeDef",
    "DeletePackagingGroupRequestRequestTypeDef",
    "DescribeAssetRequestRequestTypeDef",
    "DescribeAssetResponseTypeDef",
    "DescribePackagingConfigurationRequestRequestTypeDef",
    "DescribePackagingConfigurationResponseTypeDef",
    "DescribePackagingGroupRequestRequestTypeDef",
    "DescribePackagingGroupResponseTypeDef",
    "EgressAccessLogsTypeDef",
    "EgressEndpointTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionContractConfigurationTypeDef",
    "HlsEncryptionOutputTypeDef",
    "HlsEncryptionTypeDef",
    "HlsEncryptionUnionTypeDef",
    "HlsManifestTypeDef",
    "HlsPackageOutputTypeDef",
    "HlsPackageTypeDef",
    "ListAssetsRequestPaginateTypeDef",
    "ListAssetsRequestRequestTypeDef",
    "ListAssetsResponseTypeDef",
    "ListPackagingConfigurationsRequestPaginateTypeDef",
    "ListPackagingConfigurationsRequestRequestTypeDef",
    "ListPackagingConfigurationsResponseTypeDef",
    "ListPackagingGroupsRequestPaginateTypeDef",
    "ListPackagingGroupsRequestRequestTypeDef",
    "ListPackagingGroupsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MssEncryptionOutputTypeDef",
    "MssEncryptionTypeDef",
    "MssEncryptionUnionTypeDef",
    "MssManifestTypeDef",
    "MssPackageOutputTypeDef",
    "MssPackageTypeDef",
    "PackagingConfigurationTypeDef",
    "PackagingGroupTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SpekeKeyProviderOutputTypeDef",
    "SpekeKeyProviderTypeDef",
    "SpekeKeyProviderUnionTypeDef",
    "StreamSelectionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePackagingGroupRequestRequestTypeDef",
    "UpdatePackagingGroupResponseTypeDef",
)

class AssetShallowTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedAt: NotRequired[str]
    Id: NotRequired[str]
    PackagingGroupId: NotRequired[str]
    ResourceId: NotRequired[str]
    SourceArn: NotRequired[str]
    SourceRoleArn: NotRequired[str]
    Tags: NotRequired[dict[str, str]]

class AuthorizationTypeDef(TypedDict):
    CdnIdentifierSecret: str
    SecretsRoleArn: str

class EgressAccessLogsTypeDef(TypedDict):
    LogGroupName: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateAssetRequestRequestTypeDef(TypedDict):
    Id: str
    PackagingGroupId: str
    SourceArn: str
    SourceRoleArn: str
    ResourceId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class EgressEndpointTypeDef(TypedDict):
    PackagingConfigurationId: NotRequired[str]
    Status: NotRequired[str]
    Url: NotRequired[str]

class StreamSelectionTypeDef(TypedDict):
    MaxVideoBitsPerSecond: NotRequired[int]
    MinVideoBitsPerSecond: NotRequired[int]
    StreamOrder: NotRequired[StreamOrderType]

class DeleteAssetRequestRequestTypeDef(TypedDict):
    Id: str

class DeletePackagingConfigurationRequestRequestTypeDef(TypedDict):
    Id: str

class DeletePackagingGroupRequestRequestTypeDef(TypedDict):
    Id: str

class DescribeAssetRequestRequestTypeDef(TypedDict):
    Id: str

class DescribePackagingConfigurationRequestRequestTypeDef(TypedDict):
    Id: str

class DescribePackagingGroupRequestRequestTypeDef(TypedDict):
    Id: str

class EncryptionContractConfigurationTypeDef(TypedDict):
    PresetSpeke20Audio: PresetSpeke20AudioType
    PresetSpeke20Video: PresetSpeke20VideoType

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAssetsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    PackagingGroupId: NotRequired[str]

class ListPackagingConfigurationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    PackagingGroupId: NotRequired[str]

class ListPackagingGroupsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdatePackagingGroupRequestRequestTypeDef(TypedDict):
    Id: str
    Authorization: NotRequired[AuthorizationTypeDef]

class ConfigureLogsRequestRequestTypeDef(TypedDict):
    Id: str
    EgressAccessLogs: NotRequired[EgressAccessLogsTypeDef]

class CreatePackagingGroupRequestRequestTypeDef(TypedDict):
    Id: str
    Authorization: NotRequired[AuthorizationTypeDef]
    EgressAccessLogs: NotRequired[EgressAccessLogsTypeDef]
    Tags: NotRequired[Mapping[str, str]]

class PackagingGroupTypeDef(TypedDict):
    ApproximateAssetCount: NotRequired[int]
    Arn: NotRequired[str]
    Authorization: NotRequired[AuthorizationTypeDef]
    CreatedAt: NotRequired[str]
    DomainName: NotRequired[str]
    EgressAccessLogs: NotRequired[EgressAccessLogsTypeDef]
    Id: NotRequired[str]
    Tags: NotRequired[dict[str, str]]

class ConfigureLogsResponseTypeDef(TypedDict):
    Arn: str
    Authorization: AuthorizationTypeDef
    CreatedAt: str
    DomainName: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    Id: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePackagingGroupResponseTypeDef(TypedDict):
    Arn: str
    Authorization: AuthorizationTypeDef
    CreatedAt: str
    DomainName: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    Id: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePackagingGroupResponseTypeDef(TypedDict):
    ApproximateAssetCount: int
    Arn: str
    Authorization: AuthorizationTypeDef
    CreatedAt: str
    DomainName: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    Id: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssetsResponseTypeDef(TypedDict):
    Assets: list[AssetShallowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePackagingGroupResponseTypeDef(TypedDict):
    ApproximateAssetCount: int
    Arn: str
    Authorization: AuthorizationTypeDef
    CreatedAt: str
    DomainName: str
    EgressAccessLogs: EgressAccessLogsTypeDef
    Id: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAssetResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: str
    EgressEndpoints: list[EgressEndpointTypeDef]
    Id: str
    PackagingGroupId: str
    ResourceId: str
    SourceArn: str
    SourceRoleArn: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAssetResponseTypeDef(TypedDict):
    Arn: str
    CreatedAt: str
    EgressEndpoints: list[EgressEndpointTypeDef]
    Id: str
    PackagingGroupId: str
    ResourceId: str
    SourceArn: str
    SourceRoleArn: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DashManifestTypeDef(TypedDict):
    ManifestLayout: NotRequired[ManifestLayoutType]
    ManifestName: NotRequired[str]
    MinBufferTimeSeconds: NotRequired[int]
    Profile: NotRequired[ProfileType]
    ScteMarkersSource: NotRequired[ScteMarkersSourceType]
    StreamSelection: NotRequired[StreamSelectionTypeDef]

class HlsManifestTypeDef(TypedDict):
    AdMarkers: NotRequired[AdMarkersType]
    IncludeIframeOnlyStream: NotRequired[bool]
    ManifestName: NotRequired[str]
    ProgramDateTimeIntervalSeconds: NotRequired[int]
    RepeatExtXKey: NotRequired[bool]
    StreamSelection: NotRequired[StreamSelectionTypeDef]

class MssManifestTypeDef(TypedDict):
    ManifestName: NotRequired[str]
    StreamSelection: NotRequired[StreamSelectionTypeDef]

class SpekeKeyProviderOutputTypeDef(TypedDict):
    RoleArn: str
    SystemIds: list[str]
    Url: str
    EncryptionContractConfiguration: NotRequired[EncryptionContractConfigurationTypeDef]

class SpekeKeyProviderTypeDef(TypedDict):
    RoleArn: str
    SystemIds: Sequence[str]
    Url: str
    EncryptionContractConfiguration: NotRequired[EncryptionContractConfigurationTypeDef]

class ListAssetsRequestPaginateTypeDef(TypedDict):
    PackagingGroupId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPackagingConfigurationsRequestPaginateTypeDef(TypedDict):
    PackagingGroupId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPackagingGroupsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPackagingGroupsResponseTypeDef(TypedDict):
    PackagingGroups: list[PackagingGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CmafEncryptionOutputTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef
    ConstantInitializationVector: NotRequired[str]

class DashEncryptionOutputTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef

class HlsEncryptionOutputTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef
    ConstantInitializationVector: NotRequired[str]
    EncryptionMethod: NotRequired[EncryptionMethodType]

class MssEncryptionOutputTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderOutputTypeDef

SpekeKeyProviderUnionTypeDef = Union[SpekeKeyProviderTypeDef, SpekeKeyProviderOutputTypeDef]

class CmafPackageOutputTypeDef(TypedDict):
    HlsManifests: list[HlsManifestTypeDef]
    Encryption: NotRequired[CmafEncryptionOutputTypeDef]
    IncludeEncoderConfigurationInSegments: NotRequired[bool]
    SegmentDurationSeconds: NotRequired[int]

class DashPackageOutputTypeDef(TypedDict):
    DashManifests: list[DashManifestTypeDef]
    Encryption: NotRequired[DashEncryptionOutputTypeDef]
    IncludeEncoderConfigurationInSegments: NotRequired[bool]
    IncludeIframeOnlyStream: NotRequired[bool]
    PeriodTriggers: NotRequired[list[Literal["ADS"]]]
    SegmentDurationSeconds: NotRequired[int]
    SegmentTemplateFormat: NotRequired[SegmentTemplateFormatType]

class HlsPackageOutputTypeDef(TypedDict):
    HlsManifests: list[HlsManifestTypeDef]
    Encryption: NotRequired[HlsEncryptionOutputTypeDef]
    IncludeDvbSubtitles: NotRequired[bool]
    SegmentDurationSeconds: NotRequired[int]
    UseAudioRenditionGroup: NotRequired[bool]

class MssPackageOutputTypeDef(TypedDict):
    MssManifests: list[MssManifestTypeDef]
    Encryption: NotRequired[MssEncryptionOutputTypeDef]
    SegmentDurationSeconds: NotRequired[int]

class CmafEncryptionTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef
    ConstantInitializationVector: NotRequired[str]

class DashEncryptionTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef

class HlsEncryptionTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef
    ConstantInitializationVector: NotRequired[str]
    EncryptionMethod: NotRequired[EncryptionMethodType]

class MssEncryptionTypeDef(TypedDict):
    SpekeKeyProvider: SpekeKeyProviderUnionTypeDef

class CreatePackagingConfigurationResponseTypeDef(TypedDict):
    Arn: str
    CmafPackage: CmafPackageOutputTypeDef
    CreatedAt: str
    DashPackage: DashPackageOutputTypeDef
    HlsPackage: HlsPackageOutputTypeDef
    Id: str
    MssPackage: MssPackageOutputTypeDef
    PackagingGroupId: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePackagingConfigurationResponseTypeDef(TypedDict):
    Arn: str
    CmafPackage: CmafPackageOutputTypeDef
    CreatedAt: str
    DashPackage: DashPackageOutputTypeDef
    HlsPackage: HlsPackageOutputTypeDef
    Id: str
    MssPackage: MssPackageOutputTypeDef
    PackagingGroupId: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PackagingConfigurationTypeDef(TypedDict):
    Arn: NotRequired[str]
    CmafPackage: NotRequired[CmafPackageOutputTypeDef]
    CreatedAt: NotRequired[str]
    DashPackage: NotRequired[DashPackageOutputTypeDef]
    HlsPackage: NotRequired[HlsPackageOutputTypeDef]
    Id: NotRequired[str]
    MssPackage: NotRequired[MssPackageOutputTypeDef]
    PackagingGroupId: NotRequired[str]
    Tags: NotRequired[dict[str, str]]

CmafEncryptionUnionTypeDef = Union[CmafEncryptionTypeDef, CmafEncryptionOutputTypeDef]
DashEncryptionUnionTypeDef = Union[DashEncryptionTypeDef, DashEncryptionOutputTypeDef]
HlsEncryptionUnionTypeDef = Union[HlsEncryptionTypeDef, HlsEncryptionOutputTypeDef]
MssEncryptionUnionTypeDef = Union[MssEncryptionTypeDef, MssEncryptionOutputTypeDef]

class ListPackagingConfigurationsResponseTypeDef(TypedDict):
    PackagingConfigurations: list[PackagingConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CmafPackageTypeDef(TypedDict):
    HlsManifests: Sequence[HlsManifestTypeDef]
    Encryption: NotRequired[CmafEncryptionUnionTypeDef]
    IncludeEncoderConfigurationInSegments: NotRequired[bool]
    SegmentDurationSeconds: NotRequired[int]

class DashPackageTypeDef(TypedDict):
    DashManifests: Sequence[DashManifestTypeDef]
    Encryption: NotRequired[DashEncryptionUnionTypeDef]
    IncludeEncoderConfigurationInSegments: NotRequired[bool]
    IncludeIframeOnlyStream: NotRequired[bool]
    PeriodTriggers: NotRequired[Sequence[Literal["ADS"]]]
    SegmentDurationSeconds: NotRequired[int]
    SegmentTemplateFormat: NotRequired[SegmentTemplateFormatType]

class HlsPackageTypeDef(TypedDict):
    HlsManifests: Sequence[HlsManifestTypeDef]
    Encryption: NotRequired[HlsEncryptionUnionTypeDef]
    IncludeDvbSubtitles: NotRequired[bool]
    SegmentDurationSeconds: NotRequired[int]
    UseAudioRenditionGroup: NotRequired[bool]

class MssPackageTypeDef(TypedDict):
    MssManifests: Sequence[MssManifestTypeDef]
    Encryption: NotRequired[MssEncryptionUnionTypeDef]
    SegmentDurationSeconds: NotRequired[int]

class CreatePackagingConfigurationRequestRequestTypeDef(TypedDict):
    Id: str
    PackagingGroupId: str
    CmafPackage: NotRequired[CmafPackageTypeDef]
    DashPackage: NotRequired[DashPackageTypeDef]
    HlsPackage: NotRequired[HlsPackageTypeDef]
    MssPackage: NotRequired[MssPackageTypeDef]
    Tags: NotRequired[Mapping[str, str]]
