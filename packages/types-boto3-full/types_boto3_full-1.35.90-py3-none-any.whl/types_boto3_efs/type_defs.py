"""
Type annotations for efs service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_efs/type_defs/)

Usage::

    ```python
    from types_boto3_efs.type_defs import PosixUserOutputTypeDef

    data: PosixUserOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence

from .literals import (
    DeletionModeType,
    LifeCycleStateType,
    PerformanceModeType,
    ReplicationOverwriteProtectionType,
    ReplicationStatusType,
    ResourceIdTypeType,
    ResourceType,
    StatusType,
    ThroughputModeType,
    TransitionToArchiveRulesType,
    TransitionToIARulesType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessPointDescriptionResponseTypeDef",
    "AccessPointDescriptionTypeDef",
    "BackupPolicyDescriptionTypeDef",
    "BackupPolicyTypeDef",
    "CreateAccessPointRequestRequestTypeDef",
    "CreateFileSystemRequestRequestTypeDef",
    "CreateMountTargetRequestRequestTypeDef",
    "CreateReplicationConfigurationRequestRequestTypeDef",
    "CreateTagsRequestRequestTypeDef",
    "CreationInfoTypeDef",
    "DeleteAccessPointRequestRequestTypeDef",
    "DeleteFileSystemPolicyRequestRequestTypeDef",
    "DeleteFileSystemRequestRequestTypeDef",
    "DeleteMountTargetRequestRequestTypeDef",
    "DeleteReplicationConfigurationRequestRequestTypeDef",
    "DeleteTagsRequestRequestTypeDef",
    "DescribeAccessPointsRequestPaginateTypeDef",
    "DescribeAccessPointsRequestRequestTypeDef",
    "DescribeAccessPointsResponseTypeDef",
    "DescribeAccountPreferencesRequestRequestTypeDef",
    "DescribeAccountPreferencesResponseTypeDef",
    "DescribeBackupPolicyRequestRequestTypeDef",
    "DescribeFileSystemPolicyRequestRequestTypeDef",
    "DescribeFileSystemsRequestPaginateTypeDef",
    "DescribeFileSystemsRequestRequestTypeDef",
    "DescribeFileSystemsResponseTypeDef",
    "DescribeLifecycleConfigurationRequestRequestTypeDef",
    "DescribeMountTargetSecurityGroupsRequestRequestTypeDef",
    "DescribeMountTargetSecurityGroupsResponseTypeDef",
    "DescribeMountTargetsRequestPaginateTypeDef",
    "DescribeMountTargetsRequestRequestTypeDef",
    "DescribeMountTargetsResponseTypeDef",
    "DescribeReplicationConfigurationsRequestPaginateTypeDef",
    "DescribeReplicationConfigurationsRequestRequestTypeDef",
    "DescribeReplicationConfigurationsResponseTypeDef",
    "DescribeTagsRequestPaginateTypeDef",
    "DescribeTagsRequestRequestTypeDef",
    "DescribeTagsResponseTypeDef",
    "DestinationToCreateTypeDef",
    "DestinationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FileSystemDescriptionResponseTypeDef",
    "FileSystemDescriptionTypeDef",
    "FileSystemPolicyDescriptionTypeDef",
    "FileSystemProtectionDescriptionResponseTypeDef",
    "FileSystemProtectionDescriptionTypeDef",
    "FileSystemSizeTypeDef",
    "LifecycleConfigurationDescriptionTypeDef",
    "LifecyclePolicyTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ModifyMountTargetSecurityGroupsRequestRequestTypeDef",
    "MountTargetDescriptionResponseTypeDef",
    "MountTargetDescriptionTypeDef",
    "PaginatorConfigTypeDef",
    "PosixUserOutputTypeDef",
    "PosixUserTypeDef",
    "PutAccountPreferencesRequestRequestTypeDef",
    "PutAccountPreferencesResponseTypeDef",
    "PutBackupPolicyRequestRequestTypeDef",
    "PutFileSystemPolicyRequestRequestTypeDef",
    "PutLifecycleConfigurationRequestRequestTypeDef",
    "ReplicationConfigurationDescriptionResponseTypeDef",
    "ReplicationConfigurationDescriptionTypeDef",
    "ResourceIdPreferenceTypeDef",
    "ResponseMetadataTypeDef",
    "RootDirectoryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFileSystemProtectionRequestRequestTypeDef",
    "UpdateFileSystemRequestRequestTypeDef",
)


class PosixUserOutputTypeDef(TypedDict):
    Uid: int
    Gid: int
    SecondaryGids: NotRequired[list[int]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class BackupPolicyTypeDef(TypedDict):
    Status: StatusType


class PosixUserTypeDef(TypedDict):
    Uid: int
    Gid: int
    SecondaryGids: NotRequired[Sequence[int]]


class CreateMountTargetRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    SubnetId: str
    IpAddress: NotRequired[str]
    SecurityGroups: NotRequired[Sequence[str]]


class DestinationToCreateTypeDef(TypedDict):
    Region: NotRequired[str]
    AvailabilityZoneName: NotRequired[str]
    KmsKeyId: NotRequired[str]
    FileSystemId: NotRequired[str]
    RoleArn: NotRequired[str]


class CreationInfoTypeDef(TypedDict):
    OwnerUid: int
    OwnerGid: int
    Permissions: str


class DeleteAccessPointRequestRequestTypeDef(TypedDict):
    AccessPointId: str


class DeleteFileSystemPolicyRequestRequestTypeDef(TypedDict):
    FileSystemId: str


class DeleteFileSystemRequestRequestTypeDef(TypedDict):
    FileSystemId: str


class DeleteMountTargetRequestRequestTypeDef(TypedDict):
    MountTargetId: str


class DeleteReplicationConfigurationRequestRequestTypeDef(TypedDict):
    SourceFileSystemId: str
    DeletionMode: NotRequired[DeletionModeType]


class DeleteTagsRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    TagKeys: Sequence[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeAccessPointsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccessPointId: NotRequired[str]
    FileSystemId: NotRequired[str]


class DescribeAccountPreferencesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ResourceIdPreferenceTypeDef(TypedDict):
    ResourceIdType: NotRequired[ResourceIdTypeType]
    Resources: NotRequired[list[ResourceType]]


class DescribeBackupPolicyRequestRequestTypeDef(TypedDict):
    FileSystemId: str


class DescribeFileSystemPolicyRequestRequestTypeDef(TypedDict):
    FileSystemId: str


class DescribeFileSystemsRequestRequestTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    Marker: NotRequired[str]
    CreationToken: NotRequired[str]
    FileSystemId: NotRequired[str]


class DescribeLifecycleConfigurationRequestRequestTypeDef(TypedDict):
    FileSystemId: str


class DescribeMountTargetSecurityGroupsRequestRequestTypeDef(TypedDict):
    MountTargetId: str


class DescribeMountTargetsRequestRequestTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    Marker: NotRequired[str]
    FileSystemId: NotRequired[str]
    MountTargetId: NotRequired[str]
    AccessPointId: NotRequired[str]


class MountTargetDescriptionTypeDef(TypedDict):
    MountTargetId: str
    FileSystemId: str
    SubnetId: str
    LifeCycleState: LifeCycleStateType
    OwnerId: NotRequired[str]
    IpAddress: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    AvailabilityZoneName: NotRequired[str]
    VpcId: NotRequired[str]


class DescribeReplicationConfigurationsRequestRequestTypeDef(TypedDict):
    FileSystemId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeTagsRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    MaxItems: NotRequired[int]
    Marker: NotRequired[str]


class DestinationTypeDef(TypedDict):
    Status: ReplicationStatusType
    FileSystemId: str
    Region: str
    LastReplicatedTimestamp: NotRequired[datetime]
    OwnerId: NotRequired[str]
    StatusMessage: NotRequired[str]
    RoleArn: NotRequired[str]


class FileSystemProtectionDescriptionTypeDef(TypedDict):
    ReplicationOverwriteProtection: NotRequired[ReplicationOverwriteProtectionType]


class FileSystemSizeTypeDef(TypedDict):
    Value: int
    Timestamp: NotRequired[datetime]
    ValueInIA: NotRequired[int]
    ValueInStandard: NotRequired[int]
    ValueInArchive: NotRequired[int]


class LifecyclePolicyTypeDef(TypedDict):
    TransitionToIA: NotRequired[TransitionToIARulesType]
    TransitionToPrimaryStorageClass: NotRequired[Literal["AFTER_1_ACCESS"]]
    TransitionToArchive: NotRequired[TransitionToArchiveRulesType]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ModifyMountTargetSecurityGroupsRequestRequestTypeDef(TypedDict):
    MountTargetId: str
    SecurityGroups: NotRequired[Sequence[str]]


class PutAccountPreferencesRequestRequestTypeDef(TypedDict):
    ResourceIdType: ResourceIdTypeType


class PutFileSystemPolicyRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    Policy: str
    BypassPolicyLockoutSafetyCheck: NotRequired[bool]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    TagKeys: Sequence[str]


class UpdateFileSystemProtectionRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    ReplicationOverwriteProtection: NotRequired[ReplicationOverwriteProtectionType]


class UpdateFileSystemRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    ThroughputMode: NotRequired[ThroughputModeType]
    ProvisionedThroughputInMibps: NotRequired[float]


class DescribeMountTargetSecurityGroupsResponseTypeDef(TypedDict):
    SecurityGroups: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class FileSystemPolicyDescriptionTypeDef(TypedDict):
    FileSystemId: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class FileSystemProtectionDescriptionResponseTypeDef(TypedDict):
    ReplicationOverwriteProtection: ReplicationOverwriteProtectionType
    ResponseMetadata: ResponseMetadataTypeDef


class MountTargetDescriptionResponseTypeDef(TypedDict):
    OwnerId: str
    MountTargetId: str
    FileSystemId: str
    SubnetId: str
    LifeCycleState: LifeCycleStateType
    IpAddress: str
    NetworkInterfaceId: str
    AvailabilityZoneId: str
    AvailabilityZoneName: str
    VpcId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFileSystemRequestRequestTypeDef(TypedDict):
    CreationToken: str
    PerformanceMode: NotRequired[PerformanceModeType]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    ThroughputMode: NotRequired[ThroughputModeType]
    ProvisionedThroughputInMibps: NotRequired[float]
    AvailabilityZoneName: NotRequired[str]
    Backup: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTagsRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    Tags: Sequence[TagTypeDef]


class DescribeTagsResponseTypeDef(TypedDict):
    Marker: str
    Tags: list[TagTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceId: str
    Tags: Sequence[TagTypeDef]


class BackupPolicyDescriptionTypeDef(TypedDict):
    BackupPolicy: BackupPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutBackupPolicyRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    BackupPolicy: BackupPolicyTypeDef


class CreateReplicationConfigurationRequestRequestTypeDef(TypedDict):
    SourceFileSystemId: str
    Destinations: Sequence[DestinationToCreateTypeDef]


class RootDirectoryTypeDef(TypedDict):
    Path: NotRequired[str]
    CreationInfo: NotRequired[CreationInfoTypeDef]


class DescribeAccessPointsRequestPaginateTypeDef(TypedDict):
    AccessPointId: NotRequired[str]
    FileSystemId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFileSystemsRequestPaginateTypeDef(TypedDict):
    CreationToken: NotRequired[str]
    FileSystemId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMountTargetsRequestPaginateTypeDef(TypedDict):
    FileSystemId: NotRequired[str]
    MountTargetId: NotRequired[str]
    AccessPointId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplicationConfigurationsRequestPaginateTypeDef(TypedDict):
    FileSystemId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTagsRequestPaginateTypeDef(TypedDict):
    FileSystemId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAccountPreferencesResponseTypeDef(TypedDict):
    ResourceIdPreference: ResourceIdPreferenceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutAccountPreferencesResponseTypeDef(TypedDict):
    ResourceIdPreference: ResourceIdPreferenceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMountTargetsResponseTypeDef(TypedDict):
    Marker: str
    MountTargets: list[MountTargetDescriptionTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReplicationConfigurationDescriptionResponseTypeDef(TypedDict):
    SourceFileSystemId: str
    SourceFileSystemRegion: str
    SourceFileSystemArn: str
    OriginalSourceFileSystemArn: str
    CreationTime: datetime
    Destinations: list[DestinationTypeDef]
    SourceFileSystemOwnerId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReplicationConfigurationDescriptionTypeDef(TypedDict):
    SourceFileSystemId: str
    SourceFileSystemRegion: str
    SourceFileSystemArn: str
    OriginalSourceFileSystemArn: str
    CreationTime: datetime
    Destinations: list[DestinationTypeDef]
    SourceFileSystemOwnerId: NotRequired[str]


class FileSystemDescriptionResponseTypeDef(TypedDict):
    OwnerId: str
    CreationToken: str
    FileSystemId: str
    FileSystemArn: str
    CreationTime: datetime
    LifeCycleState: LifeCycleStateType
    Name: str
    NumberOfMountTargets: int
    SizeInBytes: FileSystemSizeTypeDef
    PerformanceMode: PerformanceModeType
    Encrypted: bool
    KmsKeyId: str
    ThroughputMode: ThroughputModeType
    ProvisionedThroughputInMibps: float
    AvailabilityZoneName: str
    AvailabilityZoneId: str
    Tags: list[TagTypeDef]
    FileSystemProtection: FileSystemProtectionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FileSystemDescriptionTypeDef(TypedDict):
    OwnerId: str
    CreationToken: str
    FileSystemId: str
    CreationTime: datetime
    LifeCycleState: LifeCycleStateType
    NumberOfMountTargets: int
    SizeInBytes: FileSystemSizeTypeDef
    PerformanceMode: PerformanceModeType
    Tags: list[TagTypeDef]
    FileSystemArn: NotRequired[str]
    Name: NotRequired[str]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    ThroughputMode: NotRequired[ThroughputModeType]
    ProvisionedThroughputInMibps: NotRequired[float]
    AvailabilityZoneName: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    FileSystemProtection: NotRequired[FileSystemProtectionDescriptionTypeDef]


class LifecycleConfigurationDescriptionTypeDef(TypedDict):
    LifecyclePolicies: list[LifecyclePolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutLifecycleConfigurationRequestRequestTypeDef(TypedDict):
    FileSystemId: str
    LifecyclePolicies: Sequence[LifecyclePolicyTypeDef]


class AccessPointDescriptionResponseTypeDef(TypedDict):
    ClientToken: str
    Name: str
    Tags: list[TagTypeDef]
    AccessPointId: str
    AccessPointArn: str
    FileSystemId: str
    PosixUser: PosixUserOutputTypeDef
    RootDirectory: RootDirectoryTypeDef
    OwnerId: str
    LifeCycleState: LifeCycleStateType
    ResponseMetadata: ResponseMetadataTypeDef


class AccessPointDescriptionTypeDef(TypedDict):
    ClientToken: NotRequired[str]
    Name: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    AccessPointId: NotRequired[str]
    AccessPointArn: NotRequired[str]
    FileSystemId: NotRequired[str]
    PosixUser: NotRequired[PosixUserOutputTypeDef]
    RootDirectory: NotRequired[RootDirectoryTypeDef]
    OwnerId: NotRequired[str]
    LifeCycleState: NotRequired[LifeCycleStateType]


class CreateAccessPointRequestRequestTypeDef(TypedDict):
    ClientToken: str
    FileSystemId: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    PosixUser: NotRequired[PosixUserTypeDef]
    RootDirectory: NotRequired[RootDirectoryTypeDef]


class DescribeReplicationConfigurationsResponseTypeDef(TypedDict):
    Replications: list[ReplicationConfigurationDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeFileSystemsResponseTypeDef(TypedDict):
    Marker: str
    FileSystems: list[FileSystemDescriptionTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccessPointsResponseTypeDef(TypedDict):
    AccessPoints: list[AccessPointDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
