"""
Type annotations for appstream service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appstream/type_defs/)

Usage::

    ```python
    from types_boto3_appstream.type_defs import AccessEndpointTypeDef

    data: AccessEndpointTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    ActionType,
    AppBlockBuilderAttributeType,
    AppBlockBuilderStateType,
    AppBlockStateType,
    ApplicationAttributeType,
    AppVisibilityType,
    AuthenticationTypeType,
    CertificateBasedAuthStatusType,
    DynamicAppProvidersEnabledType,
    FleetAttributeType,
    FleetErrorCodeType,
    FleetStateType,
    FleetTypeType,
    ImageBuilderStateChangeReasonCodeType,
    ImageBuilderStateType,
    ImageSharedWithOthersType,
    ImageStateChangeReasonCodeType,
    ImageStateType,
    LatestAppstreamAgentVersionType,
    MessageActionType,
    PackagingTypeType,
    PermissionType,
    PlatformTypeType,
    PreferredProtocolType,
    SessionConnectionStateType,
    SessionStateType,
    StackAttributeType,
    StackErrorCodeType,
    StorageConnectorTypeType,
    StreamViewType,
    ThemeStateType,
    ThemeStylingType,
    UsageReportExecutionErrorCodeType,
    UserStackAssociationErrorCodeType,
    VisibilityTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessEndpointTypeDef",
    "AppBlockBuilderAppBlockAssociationTypeDef",
    "AppBlockBuilderStateChangeReasonTypeDef",
    "AppBlockBuilderTypeDef",
    "AppBlockTypeDef",
    "ApplicationFleetAssociationTypeDef",
    "ApplicationSettingsResponseTypeDef",
    "ApplicationSettingsTypeDef",
    "ApplicationTypeDef",
    "AssociateAppBlockBuilderAppBlockRequestRequestTypeDef",
    "AssociateAppBlockBuilderAppBlockResultTypeDef",
    "AssociateApplicationFleetRequestRequestTypeDef",
    "AssociateApplicationFleetResultTypeDef",
    "AssociateApplicationToEntitlementRequestRequestTypeDef",
    "AssociateFleetRequestRequestTypeDef",
    "BatchAssociateUserStackRequestRequestTypeDef",
    "BatchAssociateUserStackResultTypeDef",
    "BatchDisassociateUserStackRequestRequestTypeDef",
    "BatchDisassociateUserStackResultTypeDef",
    "CertificateBasedAuthPropertiesTypeDef",
    "ComputeCapacityStatusTypeDef",
    "ComputeCapacityTypeDef",
    "CopyImageRequestRequestTypeDef",
    "CopyImageResponseTypeDef",
    "CreateAppBlockBuilderRequestRequestTypeDef",
    "CreateAppBlockBuilderResultTypeDef",
    "CreateAppBlockBuilderStreamingURLRequestRequestTypeDef",
    "CreateAppBlockBuilderStreamingURLResultTypeDef",
    "CreateAppBlockRequestRequestTypeDef",
    "CreateAppBlockResultTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResultTypeDef",
    "CreateDirectoryConfigRequestRequestTypeDef",
    "CreateDirectoryConfigResultTypeDef",
    "CreateEntitlementRequestRequestTypeDef",
    "CreateEntitlementResultTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "CreateFleetResultTypeDef",
    "CreateImageBuilderRequestRequestTypeDef",
    "CreateImageBuilderResultTypeDef",
    "CreateImageBuilderStreamingURLRequestRequestTypeDef",
    "CreateImageBuilderStreamingURLResultTypeDef",
    "CreateStackRequestRequestTypeDef",
    "CreateStackResultTypeDef",
    "CreateStreamingURLRequestRequestTypeDef",
    "CreateStreamingURLResultTypeDef",
    "CreateThemeForStackRequestRequestTypeDef",
    "CreateThemeForStackResultTypeDef",
    "CreateUpdatedImageRequestRequestTypeDef",
    "CreateUpdatedImageResultTypeDef",
    "CreateUsageReportSubscriptionResultTypeDef",
    "CreateUserRequestRequestTypeDef",
    "DeleteAppBlockBuilderRequestRequestTypeDef",
    "DeleteAppBlockRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteDirectoryConfigRequestRequestTypeDef",
    "DeleteEntitlementRequestRequestTypeDef",
    "DeleteFleetRequestRequestTypeDef",
    "DeleteImageBuilderRequestRequestTypeDef",
    "DeleteImageBuilderResultTypeDef",
    "DeleteImagePermissionsRequestRequestTypeDef",
    "DeleteImageRequestRequestTypeDef",
    "DeleteImageResultTypeDef",
    "DeleteStackRequestRequestTypeDef",
    "DeleteThemeForStackRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeAppBlockBuilderAppBlockAssociationsRequestRequestTypeDef",
    "DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef",
    "DescribeAppBlockBuildersRequestRequestTypeDef",
    "DescribeAppBlockBuildersResultTypeDef",
    "DescribeAppBlocksRequestRequestTypeDef",
    "DescribeAppBlocksResultTypeDef",
    "DescribeApplicationFleetAssociationsRequestRequestTypeDef",
    "DescribeApplicationFleetAssociationsResultTypeDef",
    "DescribeApplicationsRequestRequestTypeDef",
    "DescribeApplicationsResultTypeDef",
    "DescribeDirectoryConfigsRequestPaginateTypeDef",
    "DescribeDirectoryConfigsRequestRequestTypeDef",
    "DescribeDirectoryConfigsResultTypeDef",
    "DescribeEntitlementsRequestRequestTypeDef",
    "DescribeEntitlementsResultTypeDef",
    "DescribeFleetsRequestPaginateTypeDef",
    "DescribeFleetsRequestRequestTypeDef",
    "DescribeFleetsRequestWaitTypeDef",
    "DescribeFleetsResultTypeDef",
    "DescribeImageBuildersRequestPaginateTypeDef",
    "DescribeImageBuildersRequestRequestTypeDef",
    "DescribeImageBuildersResultTypeDef",
    "DescribeImagePermissionsRequestRequestTypeDef",
    "DescribeImagePermissionsResultTypeDef",
    "DescribeImagesRequestPaginateTypeDef",
    "DescribeImagesRequestRequestTypeDef",
    "DescribeImagesResultTypeDef",
    "DescribeSessionsRequestPaginateTypeDef",
    "DescribeSessionsRequestRequestTypeDef",
    "DescribeSessionsResultTypeDef",
    "DescribeStacksRequestPaginateTypeDef",
    "DescribeStacksRequestRequestTypeDef",
    "DescribeStacksResultTypeDef",
    "DescribeThemeForStackRequestRequestTypeDef",
    "DescribeThemeForStackResultTypeDef",
    "DescribeUsageReportSubscriptionsRequestRequestTypeDef",
    "DescribeUsageReportSubscriptionsResultTypeDef",
    "DescribeUserStackAssociationsRequestPaginateTypeDef",
    "DescribeUserStackAssociationsRequestRequestTypeDef",
    "DescribeUserStackAssociationsResultTypeDef",
    "DescribeUsersRequestPaginateTypeDef",
    "DescribeUsersRequestRequestTypeDef",
    "DescribeUsersResultTypeDef",
    "DirectoryConfigTypeDef",
    "DisableUserRequestRequestTypeDef",
    "DisassociateAppBlockBuilderAppBlockRequestRequestTypeDef",
    "DisassociateApplicationFleetRequestRequestTypeDef",
    "DisassociateApplicationFromEntitlementRequestRequestTypeDef",
    "DisassociateFleetRequestRequestTypeDef",
    "DomainJoinInfoTypeDef",
    "EnableUserRequestRequestTypeDef",
    "EntitledApplicationTypeDef",
    "EntitlementAttributeTypeDef",
    "EntitlementTypeDef",
    "ErrorDetailsTypeDef",
    "ExpireSessionRequestRequestTypeDef",
    "FleetErrorTypeDef",
    "FleetTypeDef",
    "ImageBuilderStateChangeReasonTypeDef",
    "ImageBuilderTypeDef",
    "ImagePermissionsTypeDef",
    "ImageStateChangeReasonTypeDef",
    "ImageTypeDef",
    "LastReportGenerationExecutionErrorTypeDef",
    "ListAssociatedFleetsRequestPaginateTypeDef",
    "ListAssociatedFleetsRequestRequestTypeDef",
    "ListAssociatedFleetsResultTypeDef",
    "ListAssociatedStacksRequestPaginateTypeDef",
    "ListAssociatedStacksRequestRequestTypeDef",
    "ListAssociatedStacksResultTypeDef",
    "ListEntitledApplicationsRequestRequestTypeDef",
    "ListEntitledApplicationsResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NetworkAccessConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceErrorTypeDef",
    "ResponseMetadataTypeDef",
    "S3LocationTypeDef",
    "ScriptDetailsTypeDef",
    "ServiceAccountCredentialsTypeDef",
    "SessionTypeDef",
    "SharedImagePermissionsTypeDef",
    "StackErrorTypeDef",
    "StackTypeDef",
    "StartAppBlockBuilderRequestRequestTypeDef",
    "StartAppBlockBuilderResultTypeDef",
    "StartFleetRequestRequestTypeDef",
    "StartImageBuilderRequestRequestTypeDef",
    "StartImageBuilderResultTypeDef",
    "StopAppBlockBuilderRequestRequestTypeDef",
    "StopAppBlockBuilderResultTypeDef",
    "StopFleetRequestRequestTypeDef",
    "StopImageBuilderRequestRequestTypeDef",
    "StopImageBuilderResultTypeDef",
    "StorageConnectorOutputTypeDef",
    "StorageConnectorTypeDef",
    "StorageConnectorUnionTypeDef",
    "StreamingExperienceSettingsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ThemeFooterLinkTypeDef",
    "ThemeTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAppBlockBuilderRequestRequestTypeDef",
    "UpdateAppBlockBuilderResultTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateApplicationResultTypeDef",
    "UpdateDirectoryConfigRequestRequestTypeDef",
    "UpdateDirectoryConfigResultTypeDef",
    "UpdateEntitlementRequestRequestTypeDef",
    "UpdateEntitlementResultTypeDef",
    "UpdateFleetRequestRequestTypeDef",
    "UpdateFleetResultTypeDef",
    "UpdateImagePermissionsRequestRequestTypeDef",
    "UpdateStackRequestRequestTypeDef",
    "UpdateStackResultTypeDef",
    "UpdateThemeForStackRequestRequestTypeDef",
    "UpdateThemeForStackResultTypeDef",
    "UsageReportSubscriptionTypeDef",
    "UserSettingTypeDef",
    "UserStackAssociationErrorTypeDef",
    "UserStackAssociationTypeDef",
    "UserTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "WaiterConfigTypeDef",
)

class AccessEndpointTypeDef(TypedDict):
    EndpointType: Literal["STREAMING"]
    VpceId: NotRequired[str]

class AppBlockBuilderAppBlockAssociationTypeDef(TypedDict):
    AppBlockArn: str
    AppBlockBuilderName: str

class AppBlockBuilderStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[Literal["INTERNAL_ERROR"]]
    Message: NotRequired[str]

class ResourceErrorTypeDef(TypedDict):
    ErrorCode: NotRequired[FleetErrorCodeType]
    ErrorMessage: NotRequired[str]
    ErrorTimestamp: NotRequired[datetime]

class VpcConfigOutputTypeDef(TypedDict):
    SubnetIds: NotRequired[list[str]]
    SecurityGroupIds: NotRequired[list[str]]

class ErrorDetailsTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class S3LocationTypeDef(TypedDict):
    S3Bucket: str
    S3Key: NotRequired[str]

class ApplicationFleetAssociationTypeDef(TypedDict):
    FleetName: str
    ApplicationArn: str

class ApplicationSettingsResponseTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    SettingsGroup: NotRequired[str]
    S3BucketName: NotRequired[str]

class ApplicationSettingsTypeDef(TypedDict):
    Enabled: bool
    SettingsGroup: NotRequired[str]

class AssociateAppBlockBuilderAppBlockRequestRequestTypeDef(TypedDict):
    AppBlockArn: str
    AppBlockBuilderName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociateApplicationFleetRequestRequestTypeDef(TypedDict):
    FleetName: str
    ApplicationArn: str

class AssociateApplicationToEntitlementRequestRequestTypeDef(TypedDict):
    StackName: str
    EntitlementName: str
    ApplicationIdentifier: str

class AssociateFleetRequestRequestTypeDef(TypedDict):
    FleetName: str
    StackName: str

class UserStackAssociationTypeDef(TypedDict):
    StackName: str
    UserName: str
    AuthenticationType: AuthenticationTypeType
    SendEmailNotification: NotRequired[bool]

class CertificateBasedAuthPropertiesTypeDef(TypedDict):
    Status: NotRequired[CertificateBasedAuthStatusType]
    CertificateAuthorityArn: NotRequired[str]

class ComputeCapacityStatusTypeDef(TypedDict):
    Desired: int
    Running: NotRequired[int]
    InUse: NotRequired[int]
    Available: NotRequired[int]
    DesiredUserSessions: NotRequired[int]
    AvailableUserSessions: NotRequired[int]
    ActiveUserSessions: NotRequired[int]
    ActualUserSessions: NotRequired[int]

class ComputeCapacityTypeDef(TypedDict):
    DesiredInstances: NotRequired[int]
    DesiredSessions: NotRequired[int]

class CopyImageRequestRequestTypeDef(TypedDict):
    SourceImageName: str
    DestinationImageName: str
    DestinationRegion: str
    DestinationImageDescription: NotRequired[str]

class VpcConfigTypeDef(TypedDict):
    SubnetIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]

class CreateAppBlockBuilderStreamingURLRequestRequestTypeDef(TypedDict):
    AppBlockBuilderName: str
    Validity: NotRequired[int]

class ServiceAccountCredentialsTypeDef(TypedDict):
    AccountName: str
    AccountPassword: str

class EntitlementAttributeTypeDef(TypedDict):
    Name: str
    Value: str

class DomainJoinInfoTypeDef(TypedDict):
    DirectoryName: NotRequired[str]
    OrganizationalUnitDistinguishedName: NotRequired[str]

class CreateImageBuilderStreamingURLRequestRequestTypeDef(TypedDict):
    Name: str
    Validity: NotRequired[int]

class StreamingExperienceSettingsTypeDef(TypedDict):
    PreferredProtocol: NotRequired[PreferredProtocolType]

class UserSettingTypeDef(TypedDict):
    Action: ActionType
    Permission: PermissionType
    MaximumLength: NotRequired[int]

class CreateStreamingURLRequestRequestTypeDef(TypedDict):
    StackName: str
    FleetName: str
    UserId: str
    ApplicationId: NotRequired[str]
    Validity: NotRequired[int]
    SessionContext: NotRequired[str]

class ThemeFooterLinkTypeDef(TypedDict):
    DisplayName: NotRequired[str]
    FooterLinkURL: NotRequired[str]

class CreateUpdatedImageRequestRequestTypeDef(TypedDict):
    existingImageName: str
    newImageName: str
    newImageDescription: NotRequired[str]
    newImageDisplayName: NotRequired[str]
    newImageTags: NotRequired[Mapping[str, str]]
    dryRun: NotRequired[bool]

class CreateUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AuthenticationType: AuthenticationTypeType
    MessageAction: NotRequired[MessageActionType]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]

class DeleteAppBlockBuilderRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteAppBlockRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteDirectoryConfigRequestRequestTypeDef(TypedDict):
    DirectoryName: str

class DeleteEntitlementRequestRequestTypeDef(TypedDict):
    Name: str
    StackName: str

class DeleteFleetRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteImageBuilderRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteImagePermissionsRequestRequestTypeDef(TypedDict):
    Name: str
    SharedAccountId: str

class DeleteImageRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteStackRequestRequestTypeDef(TypedDict):
    Name: str

class DeleteThemeForStackRequestRequestTypeDef(TypedDict):
    StackName: str

class DeleteUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AuthenticationType: AuthenticationTypeType

class DescribeAppBlockBuilderAppBlockAssociationsRequestRequestTypeDef(TypedDict):
    AppBlockArn: NotRequired[str]
    AppBlockBuilderName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeAppBlockBuildersRequestRequestTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class DescribeAppBlocksRequestRequestTypeDef(TypedDict):
    Arns: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class DescribeApplicationFleetAssociationsRequestRequestTypeDef(TypedDict):
    FleetName: NotRequired[str]
    ApplicationArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeApplicationsRequestRequestTypeDef(TypedDict):
    Arns: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeDirectoryConfigsRequestRequestTypeDef(TypedDict):
    DirectoryNames: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeEntitlementsRequestRequestTypeDef(TypedDict):
    StackName: str
    Name: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class DescribeFleetsRequestRequestTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeImageBuildersRequestRequestTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeImagePermissionsRequestRequestTypeDef(TypedDict):
    Name: str
    MaxResults: NotRequired[int]
    SharedAwsAccountIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]

DescribeImagesRequestRequestTypeDef = TypedDict(
    "DescribeImagesRequestRequestTypeDef",
    {
        "Names": NotRequired[Sequence[str]],
        "Arns": NotRequired[Sequence[str]],
        "Type": NotRequired[VisibilityTypeType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

class DescribeSessionsRequestRequestTypeDef(TypedDict):
    StackName: str
    FleetName: str
    UserId: NotRequired[str]
    NextToken: NotRequired[str]
    Limit: NotRequired[int]
    AuthenticationType: NotRequired[AuthenticationTypeType]
    InstanceId: NotRequired[str]

class DescribeStacksRequestRequestTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]

class DescribeThemeForStackRequestRequestTypeDef(TypedDict):
    StackName: str

class DescribeUsageReportSubscriptionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeUserStackAssociationsRequestRequestTypeDef(TypedDict):
    StackName: NotRequired[str]
    UserName: NotRequired[str]
    AuthenticationType: NotRequired[AuthenticationTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeUsersRequestRequestTypeDef(TypedDict):
    AuthenticationType: AuthenticationTypeType
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class UserTypeDef(TypedDict):
    AuthenticationType: AuthenticationTypeType
    Arn: NotRequired[str]
    UserName: NotRequired[str]
    Enabled: NotRequired[bool]
    Status: NotRequired[str]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    CreatedTime: NotRequired[datetime]

class DisableUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AuthenticationType: AuthenticationTypeType

class DisassociateAppBlockBuilderAppBlockRequestRequestTypeDef(TypedDict):
    AppBlockArn: str
    AppBlockBuilderName: str

class DisassociateApplicationFleetRequestRequestTypeDef(TypedDict):
    FleetName: str
    ApplicationArn: str

class DisassociateApplicationFromEntitlementRequestRequestTypeDef(TypedDict):
    StackName: str
    EntitlementName: str
    ApplicationIdentifier: str

class DisassociateFleetRequestRequestTypeDef(TypedDict):
    FleetName: str
    StackName: str

class EnableUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AuthenticationType: AuthenticationTypeType

class EntitledApplicationTypeDef(TypedDict):
    ApplicationIdentifier: str

class ExpireSessionRequestRequestTypeDef(TypedDict):
    SessionId: str

class FleetErrorTypeDef(TypedDict):
    ErrorCode: NotRequired[FleetErrorCodeType]
    ErrorMessage: NotRequired[str]

class ImageBuilderStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[ImageBuilderStateChangeReasonCodeType]
    Message: NotRequired[str]

class NetworkAccessConfigurationTypeDef(TypedDict):
    EniPrivateIpAddress: NotRequired[str]
    EniId: NotRequired[str]

class ImagePermissionsTypeDef(TypedDict):
    allowFleet: NotRequired[bool]
    allowImageBuilder: NotRequired[bool]

class ImageStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[ImageStateChangeReasonCodeType]
    Message: NotRequired[str]

class LastReportGenerationExecutionErrorTypeDef(TypedDict):
    ErrorCode: NotRequired[UsageReportExecutionErrorCodeType]
    ErrorMessage: NotRequired[str]

class ListAssociatedFleetsRequestRequestTypeDef(TypedDict):
    StackName: str
    NextToken: NotRequired[str]

class ListAssociatedStacksRequestRequestTypeDef(TypedDict):
    FleetName: str
    NextToken: NotRequired[str]

class ListEntitledApplicationsRequestRequestTypeDef(TypedDict):
    StackName: str
    EntitlementName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class StackErrorTypeDef(TypedDict):
    ErrorCode: NotRequired[StackErrorCodeType]
    ErrorMessage: NotRequired[str]

class StorageConnectorOutputTypeDef(TypedDict):
    ConnectorType: StorageConnectorTypeType
    ResourceIdentifier: NotRequired[str]
    Domains: NotRequired[list[str]]

class StartAppBlockBuilderRequestRequestTypeDef(TypedDict):
    Name: str

class StartFleetRequestRequestTypeDef(TypedDict):
    Name: str

class StartImageBuilderRequestRequestTypeDef(TypedDict):
    Name: str
    AppstreamAgentVersion: NotRequired[str]

class StopAppBlockBuilderRequestRequestTypeDef(TypedDict):
    Name: str

class StopFleetRequestRequestTypeDef(TypedDict):
    Name: str

class StopImageBuilderRequestRequestTypeDef(TypedDict):
    Name: str

class StorageConnectorTypeDef(TypedDict):
    ConnectorType: StorageConnectorTypeType
    ResourceIdentifier: NotRequired[str]
    Domains: NotRequired[Sequence[str]]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class AppBlockBuilderTypeDef(TypedDict):
    Arn: str
    Name: str
    Platform: Literal["WINDOWS_SERVER_2019"]
    InstanceType: str
    VpcConfig: VpcConfigOutputTypeDef
    State: AppBlockBuilderStateType
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    EnableDefaultInternetAccess: NotRequired[bool]
    IamRoleArn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    AppBlockBuilderErrors: NotRequired[list[ResourceErrorTypeDef]]
    StateChangeReason: NotRequired[AppBlockBuilderStateChangeReasonTypeDef]
    AccessEndpoints: NotRequired[list[AccessEndpointTypeDef]]

class ApplicationTypeDef(TypedDict):
    Name: NotRequired[str]
    DisplayName: NotRequired[str]
    IconURL: NotRequired[str]
    LaunchPath: NotRequired[str]
    LaunchParameters: NotRequired[str]
    Enabled: NotRequired[bool]
    Metadata: NotRequired[dict[str, str]]
    WorkingDirectory: NotRequired[str]
    Description: NotRequired[str]
    Arn: NotRequired[str]
    AppBlockArn: NotRequired[str]
    IconS3Location: NotRequired[S3LocationTypeDef]
    Platforms: NotRequired[list[PlatformTypeType]]
    InstanceFamilies: NotRequired[list[str]]
    CreatedTime: NotRequired[datetime]

class CreateApplicationRequestRequestTypeDef(TypedDict):
    Name: str
    IconS3Location: S3LocationTypeDef
    LaunchPath: str
    Platforms: Sequence[PlatformTypeType]
    InstanceFamilies: Sequence[str]
    AppBlockArn: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    WorkingDirectory: NotRequired[str]
    LaunchParameters: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class ScriptDetailsTypeDef(TypedDict):
    ScriptS3Location: S3LocationTypeDef
    ExecutablePath: str
    TimeoutInSeconds: int
    ExecutableParameters: NotRequired[str]

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    Name: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    IconS3Location: NotRequired[S3LocationTypeDef]
    LaunchPath: NotRequired[str]
    WorkingDirectory: NotRequired[str]
    LaunchParameters: NotRequired[str]
    AppBlockArn: NotRequired[str]
    AttributesToDelete: NotRequired[Sequence[ApplicationAttributeType]]

class AssociateAppBlockBuilderAppBlockResultTypeDef(TypedDict):
    AppBlockBuilderAppBlockAssociation: AppBlockBuilderAppBlockAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateApplicationFleetResultTypeDef(TypedDict):
    ApplicationFleetAssociation: ApplicationFleetAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CopyImageResponseTypeDef(TypedDict):
    DestinationImageName: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAppBlockBuilderStreamingURLResultTypeDef(TypedDict):
    StreamingURL: str
    Expires: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateImageBuilderStreamingURLResultTypeDef(TypedDict):
    StreamingURL: str
    Expires: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateStreamingURLResultTypeDef(TypedDict):
    StreamingURL: str
    Expires: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateUsageReportSubscriptionResultTypeDef(TypedDict):
    S3BucketName: str
    Schedule: Literal["DAILY"]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef(TypedDict):
    AppBlockBuilderAppBlockAssociations: list[AppBlockBuilderAppBlockAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeApplicationFleetAssociationsResultTypeDef(TypedDict):
    ApplicationFleetAssociations: list[ApplicationFleetAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAssociatedFleetsResultTypeDef(TypedDict):
    Names: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListAssociatedStacksResultTypeDef(TypedDict):
    Names: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchAssociateUserStackRequestRequestTypeDef(TypedDict):
    UserStackAssociations: Sequence[UserStackAssociationTypeDef]

class BatchDisassociateUserStackRequestRequestTypeDef(TypedDict):
    UserStackAssociations: Sequence[UserStackAssociationTypeDef]

class DescribeUserStackAssociationsResultTypeDef(TypedDict):
    UserStackAssociations: list[UserStackAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UserStackAssociationErrorTypeDef(TypedDict):
    UserStackAssociation: NotRequired[UserStackAssociationTypeDef]
    ErrorCode: NotRequired[UserStackAssociationErrorCodeType]
    ErrorMessage: NotRequired[str]

class CreateAppBlockBuilderRequestRequestTypeDef(TypedDict):
    Name: str
    Platform: Literal["WINDOWS_SERVER_2019"]
    InstanceType: str
    VpcConfig: VpcConfigTypeDef
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    EnableDefaultInternetAccess: NotRequired[bool]
    IamRoleArn: NotRequired[str]
    AccessEndpoints: NotRequired[Sequence[AccessEndpointTypeDef]]

class UpdateAppBlockBuilderRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    Platform: NotRequired[PlatformTypeType]
    InstanceType: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    EnableDefaultInternetAccess: NotRequired[bool]
    IamRoleArn: NotRequired[str]
    AccessEndpoints: NotRequired[Sequence[AccessEndpointTypeDef]]
    AttributesToDelete: NotRequired[Sequence[AppBlockBuilderAttributeType]]

class CreateDirectoryConfigRequestRequestTypeDef(TypedDict):
    DirectoryName: str
    OrganizationalUnitDistinguishedNames: Sequence[str]
    ServiceAccountCredentials: NotRequired[ServiceAccountCredentialsTypeDef]
    CertificateBasedAuthProperties: NotRequired[CertificateBasedAuthPropertiesTypeDef]

class DirectoryConfigTypeDef(TypedDict):
    DirectoryName: str
    OrganizationalUnitDistinguishedNames: NotRequired[list[str]]
    ServiceAccountCredentials: NotRequired[ServiceAccountCredentialsTypeDef]
    CreatedTime: NotRequired[datetime]
    CertificateBasedAuthProperties: NotRequired[CertificateBasedAuthPropertiesTypeDef]

class UpdateDirectoryConfigRequestRequestTypeDef(TypedDict):
    DirectoryName: str
    OrganizationalUnitDistinguishedNames: NotRequired[Sequence[str]]
    ServiceAccountCredentials: NotRequired[ServiceAccountCredentialsTypeDef]
    CertificateBasedAuthProperties: NotRequired[CertificateBasedAuthPropertiesTypeDef]

class CreateEntitlementRequestRequestTypeDef(TypedDict):
    Name: str
    StackName: str
    AppVisibility: AppVisibilityType
    Attributes: Sequence[EntitlementAttributeTypeDef]
    Description: NotRequired[str]

class EntitlementTypeDef(TypedDict):
    Name: str
    StackName: str
    AppVisibility: AppVisibilityType
    Attributes: list[EntitlementAttributeTypeDef]
    Description: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class UpdateEntitlementRequestRequestTypeDef(TypedDict):
    Name: str
    StackName: str
    Description: NotRequired[str]
    AppVisibility: NotRequired[AppVisibilityType]
    Attributes: NotRequired[Sequence[EntitlementAttributeTypeDef]]

class CreateFleetRequestRequestTypeDef(TypedDict):
    Name: str
    InstanceType: str
    ImageName: NotRequired[str]
    ImageArn: NotRequired[str]
    FleetType: NotRequired[FleetTypeType]
    ComputeCapacity: NotRequired[ComputeCapacityTypeDef]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    MaxUserDurationInSeconds: NotRequired[int]
    DisconnectTimeoutInSeconds: NotRequired[int]
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    EnableDefaultInternetAccess: NotRequired[bool]
    DomainJoinInfo: NotRequired[DomainJoinInfoTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    IdleDisconnectTimeoutInSeconds: NotRequired[int]
    IamRoleArn: NotRequired[str]
    StreamView: NotRequired[StreamViewType]
    Platform: NotRequired[PlatformTypeType]
    MaxConcurrentSessions: NotRequired[int]
    UsbDeviceFilterStrings: NotRequired[Sequence[str]]
    SessionScriptS3Location: NotRequired[S3LocationTypeDef]
    MaxSessionsPerInstance: NotRequired[int]

class CreateImageBuilderRequestRequestTypeDef(TypedDict):
    Name: str
    InstanceType: str
    ImageName: NotRequired[str]
    ImageArn: NotRequired[str]
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    IamRoleArn: NotRequired[str]
    EnableDefaultInternetAccess: NotRequired[bool]
    DomainJoinInfo: NotRequired[DomainJoinInfoTypeDef]
    AppstreamAgentVersion: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    AccessEndpoints: NotRequired[Sequence[AccessEndpointTypeDef]]

class UpdateFleetRequestRequestTypeDef(TypedDict):
    ImageName: NotRequired[str]
    ImageArn: NotRequired[str]
    Name: NotRequired[str]
    InstanceType: NotRequired[str]
    ComputeCapacity: NotRequired[ComputeCapacityTypeDef]
    VpcConfig: NotRequired[VpcConfigTypeDef]
    MaxUserDurationInSeconds: NotRequired[int]
    DisconnectTimeoutInSeconds: NotRequired[int]
    DeleteVpcConfig: NotRequired[bool]
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    EnableDefaultInternetAccess: NotRequired[bool]
    DomainJoinInfo: NotRequired[DomainJoinInfoTypeDef]
    IdleDisconnectTimeoutInSeconds: NotRequired[int]
    AttributesToDelete: NotRequired[Sequence[FleetAttributeType]]
    IamRoleArn: NotRequired[str]
    StreamView: NotRequired[StreamViewType]
    Platform: NotRequired[PlatformTypeType]
    MaxConcurrentSessions: NotRequired[int]
    UsbDeviceFilterStrings: NotRequired[Sequence[str]]
    SessionScriptS3Location: NotRequired[S3LocationTypeDef]
    MaxSessionsPerInstance: NotRequired[int]

class CreateThemeForStackRequestRequestTypeDef(TypedDict):
    StackName: str
    TitleText: str
    ThemeStyling: ThemeStylingType
    OrganizationLogoS3Location: S3LocationTypeDef
    FaviconS3Location: S3LocationTypeDef
    FooterLinks: NotRequired[Sequence[ThemeFooterLinkTypeDef]]

class ThemeTypeDef(TypedDict):
    StackName: NotRequired[str]
    State: NotRequired[ThemeStateType]
    ThemeTitleText: NotRequired[str]
    ThemeStyling: NotRequired[ThemeStylingType]
    ThemeFooterLinks: NotRequired[list[ThemeFooterLinkTypeDef]]
    ThemeOrganizationLogoURL: NotRequired[str]
    ThemeFaviconURL: NotRequired[str]
    CreatedTime: NotRequired[datetime]

class UpdateThemeForStackRequestRequestTypeDef(TypedDict):
    StackName: str
    FooterLinks: NotRequired[Sequence[ThemeFooterLinkTypeDef]]
    TitleText: NotRequired[str]
    ThemeStyling: NotRequired[ThemeStylingType]
    OrganizationLogoS3Location: NotRequired[S3LocationTypeDef]
    FaviconS3Location: NotRequired[S3LocationTypeDef]
    State: NotRequired[ThemeStateType]
    AttributesToDelete: NotRequired[Sequence[Literal["FOOTER_LINKS"]]]

class DescribeDirectoryConfigsRequestPaginateTypeDef(TypedDict):
    DirectoryNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeFleetsRequestPaginateTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeImageBuildersRequestPaginateTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

DescribeImagesRequestPaginateTypeDef = TypedDict(
    "DescribeImagesRequestPaginateTypeDef",
    {
        "Names": NotRequired[Sequence[str]],
        "Arns": NotRequired[Sequence[str]],
        "Type": NotRequired[VisibilityTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class DescribeSessionsRequestPaginateTypeDef(TypedDict):
    StackName: str
    FleetName: str
    UserId: NotRequired[str]
    AuthenticationType: NotRequired[AuthenticationTypeType]
    InstanceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeStacksRequestPaginateTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeUserStackAssociationsRequestPaginateTypeDef(TypedDict):
    StackName: NotRequired[str]
    UserName: NotRequired[str]
    AuthenticationType: NotRequired[AuthenticationTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeUsersRequestPaginateTypeDef(TypedDict):
    AuthenticationType: AuthenticationTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssociatedFleetsRequestPaginateTypeDef(TypedDict):
    StackName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssociatedStacksRequestPaginateTypeDef(TypedDict):
    FleetName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeFleetsRequestWaitTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeUsersResultTypeDef(TypedDict):
    Users: list[UserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEntitledApplicationsResultTypeDef(TypedDict):
    EntitledApplications: list[EntitledApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class FleetTypeDef(TypedDict):
    Arn: str
    Name: str
    InstanceType: str
    ComputeCapacityStatus: ComputeCapacityStatusTypeDef
    State: FleetStateType
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    ImageName: NotRequired[str]
    ImageArn: NotRequired[str]
    FleetType: NotRequired[FleetTypeType]
    MaxUserDurationInSeconds: NotRequired[int]
    DisconnectTimeoutInSeconds: NotRequired[int]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    CreatedTime: NotRequired[datetime]
    FleetErrors: NotRequired[list[FleetErrorTypeDef]]
    EnableDefaultInternetAccess: NotRequired[bool]
    DomainJoinInfo: NotRequired[DomainJoinInfoTypeDef]
    IdleDisconnectTimeoutInSeconds: NotRequired[int]
    IamRoleArn: NotRequired[str]
    StreamView: NotRequired[StreamViewType]
    Platform: NotRequired[PlatformTypeType]
    MaxConcurrentSessions: NotRequired[int]
    UsbDeviceFilterStrings: NotRequired[list[str]]
    SessionScriptS3Location: NotRequired[S3LocationTypeDef]
    MaxSessionsPerInstance: NotRequired[int]

class ImageBuilderTypeDef(TypedDict):
    Name: str
    Arn: NotRequired[str]
    ImageArn: NotRequired[str]
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    InstanceType: NotRequired[str]
    Platform: NotRequired[PlatformTypeType]
    IamRoleArn: NotRequired[str]
    State: NotRequired[ImageBuilderStateType]
    StateChangeReason: NotRequired[ImageBuilderStateChangeReasonTypeDef]
    CreatedTime: NotRequired[datetime]
    EnableDefaultInternetAccess: NotRequired[bool]
    DomainJoinInfo: NotRequired[DomainJoinInfoTypeDef]
    NetworkAccessConfiguration: NotRequired[NetworkAccessConfigurationTypeDef]
    ImageBuilderErrors: NotRequired[list[ResourceErrorTypeDef]]
    AppstreamAgentVersion: NotRequired[str]
    AccessEndpoints: NotRequired[list[AccessEndpointTypeDef]]
    LatestAppstreamAgentVersion: NotRequired[LatestAppstreamAgentVersionType]

class SessionTypeDef(TypedDict):
    Id: str
    UserId: str
    StackName: str
    FleetName: str
    State: SessionStateType
    ConnectionState: NotRequired[SessionConnectionStateType]
    StartTime: NotRequired[datetime]
    MaxExpirationTime: NotRequired[datetime]
    AuthenticationType: NotRequired[AuthenticationTypeType]
    NetworkAccessConfiguration: NotRequired[NetworkAccessConfigurationTypeDef]
    InstanceId: NotRequired[str]

class SharedImagePermissionsTypeDef(TypedDict):
    sharedAccountId: str
    imagePermissions: ImagePermissionsTypeDef

class UpdateImagePermissionsRequestRequestTypeDef(TypedDict):
    Name: str
    SharedAccountId: str
    ImagePermissions: ImagePermissionsTypeDef

class UsageReportSubscriptionTypeDef(TypedDict):
    S3BucketName: NotRequired[str]
    Schedule: NotRequired[Literal["DAILY"]]
    LastGeneratedReportDate: NotRequired[datetime]
    SubscriptionErrors: NotRequired[list[LastReportGenerationExecutionErrorTypeDef]]

class StackTypeDef(TypedDict):
    Name: str
    Arn: NotRequired[str]
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    StorageConnectors: NotRequired[list[StorageConnectorOutputTypeDef]]
    RedirectURL: NotRequired[str]
    FeedbackURL: NotRequired[str]
    StackErrors: NotRequired[list[StackErrorTypeDef]]
    UserSettings: NotRequired[list[UserSettingTypeDef]]
    ApplicationSettings: NotRequired[ApplicationSettingsResponseTypeDef]
    AccessEndpoints: NotRequired[list[AccessEndpointTypeDef]]
    EmbedHostDomains: NotRequired[list[str]]
    StreamingExperienceSettings: NotRequired[StreamingExperienceSettingsTypeDef]

StorageConnectorUnionTypeDef = Union[StorageConnectorTypeDef, StorageConnectorOutputTypeDef]

class UpdateStackRequestRequestTypeDef(TypedDict):
    Name: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    StorageConnectors: NotRequired[Sequence[StorageConnectorTypeDef]]
    DeleteStorageConnectors: NotRequired[bool]
    RedirectURL: NotRequired[str]
    FeedbackURL: NotRequired[str]
    AttributesToDelete: NotRequired[Sequence[StackAttributeType]]
    UserSettings: NotRequired[Sequence[UserSettingTypeDef]]
    ApplicationSettings: NotRequired[ApplicationSettingsTypeDef]
    AccessEndpoints: NotRequired[Sequence[AccessEndpointTypeDef]]
    EmbedHostDomains: NotRequired[Sequence[str]]
    StreamingExperienceSettings: NotRequired[StreamingExperienceSettingsTypeDef]

class CreateAppBlockBuilderResultTypeDef(TypedDict):
    AppBlockBuilder: AppBlockBuilderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAppBlockBuildersResultTypeDef(TypedDict):
    AppBlockBuilders: list[AppBlockBuilderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartAppBlockBuilderResultTypeDef(TypedDict):
    AppBlockBuilder: AppBlockBuilderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopAppBlockBuilderResultTypeDef(TypedDict):
    AppBlockBuilder: AppBlockBuilderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAppBlockBuilderResultTypeDef(TypedDict):
    AppBlockBuilder: AppBlockBuilderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApplicationResultTypeDef(TypedDict):
    Application: ApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeApplicationsResultTypeDef(TypedDict):
    Applications: list[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ImageTypeDef(TypedDict):
    Name: str
    Arn: NotRequired[str]
    BaseImageArn: NotRequired[str]
    DisplayName: NotRequired[str]
    State: NotRequired[ImageStateType]
    Visibility: NotRequired[VisibilityTypeType]
    ImageBuilderSupported: NotRequired[bool]
    ImageBuilderName: NotRequired[str]
    Platform: NotRequired[PlatformTypeType]
    Description: NotRequired[str]
    StateChangeReason: NotRequired[ImageStateChangeReasonTypeDef]
    Applications: NotRequired[list[ApplicationTypeDef]]
    CreatedTime: NotRequired[datetime]
    PublicBaseImageReleasedDate: NotRequired[datetime]
    AppstreamAgentVersion: NotRequired[str]
    ImagePermissions: NotRequired[ImagePermissionsTypeDef]
    ImageErrors: NotRequired[list[ResourceErrorTypeDef]]
    LatestAppstreamAgentVersion: NotRequired[LatestAppstreamAgentVersionType]
    SupportedInstanceFamilies: NotRequired[list[str]]
    DynamicAppProvidersEnabled: NotRequired[DynamicAppProvidersEnabledType]
    ImageSharedWithOthers: NotRequired[ImageSharedWithOthersType]

class UpdateApplicationResultTypeDef(TypedDict):
    Application: ApplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AppBlockTypeDef(TypedDict):
    Name: str
    Arn: str
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    SourceS3Location: NotRequired[S3LocationTypeDef]
    SetupScriptDetails: NotRequired[ScriptDetailsTypeDef]
    CreatedTime: NotRequired[datetime]
    PostSetupScriptDetails: NotRequired[ScriptDetailsTypeDef]
    PackagingType: NotRequired[PackagingTypeType]
    State: NotRequired[AppBlockStateType]
    AppBlockErrors: NotRequired[list[ErrorDetailsTypeDef]]

class CreateAppBlockRequestRequestTypeDef(TypedDict):
    Name: str
    SourceS3Location: S3LocationTypeDef
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    SetupScriptDetails: NotRequired[ScriptDetailsTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    PostSetupScriptDetails: NotRequired[ScriptDetailsTypeDef]
    PackagingType: NotRequired[PackagingTypeType]

class BatchAssociateUserStackResultTypeDef(TypedDict):
    errors: list[UserStackAssociationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDisassociateUserStackResultTypeDef(TypedDict):
    errors: list[UserStackAssociationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDirectoryConfigResultTypeDef(TypedDict):
    DirectoryConfig: DirectoryConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDirectoryConfigsResultTypeDef(TypedDict):
    DirectoryConfigs: list[DirectoryConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateDirectoryConfigResultTypeDef(TypedDict):
    DirectoryConfig: DirectoryConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEntitlementResultTypeDef(TypedDict):
    Entitlement: EntitlementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeEntitlementsResultTypeDef(TypedDict):
    Entitlements: list[EntitlementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateEntitlementResultTypeDef(TypedDict):
    Entitlement: EntitlementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateThemeForStackResultTypeDef(TypedDict):
    Theme: ThemeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeThemeForStackResultTypeDef(TypedDict):
    Theme: ThemeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateThemeForStackResultTypeDef(TypedDict):
    Theme: ThemeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFleetResultTypeDef(TypedDict):
    Fleet: FleetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeFleetsResultTypeDef(TypedDict):
    Fleets: list[FleetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateFleetResultTypeDef(TypedDict):
    Fleet: FleetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateImageBuilderResultTypeDef(TypedDict):
    ImageBuilder: ImageBuilderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteImageBuilderResultTypeDef(TypedDict):
    ImageBuilder: ImageBuilderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeImageBuildersResultTypeDef(TypedDict):
    ImageBuilders: list[ImageBuilderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartImageBuilderResultTypeDef(TypedDict):
    ImageBuilder: ImageBuilderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopImageBuilderResultTypeDef(TypedDict):
    ImageBuilder: ImageBuilderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSessionsResultTypeDef(TypedDict):
    Sessions: list[SessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeImagePermissionsResultTypeDef(TypedDict):
    Name: str
    SharedImagePermissionsList: list[SharedImagePermissionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeUsageReportSubscriptionsResultTypeDef(TypedDict):
    UsageReportSubscriptions: list[UsageReportSubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateStackResultTypeDef(TypedDict):
    Stack: StackTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeStacksResultTypeDef(TypedDict):
    Stacks: list[StackTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateStackResultTypeDef(TypedDict):
    Stack: StackTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateStackRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    StorageConnectors: NotRequired[Sequence[StorageConnectorUnionTypeDef]]
    RedirectURL: NotRequired[str]
    FeedbackURL: NotRequired[str]
    UserSettings: NotRequired[Sequence[UserSettingTypeDef]]
    ApplicationSettings: NotRequired[ApplicationSettingsTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    AccessEndpoints: NotRequired[Sequence[AccessEndpointTypeDef]]
    EmbedHostDomains: NotRequired[Sequence[str]]
    StreamingExperienceSettings: NotRequired[StreamingExperienceSettingsTypeDef]

class CreateUpdatedImageResultTypeDef(TypedDict):
    image: ImageTypeDef
    canUpdateImage: bool
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteImageResultTypeDef(TypedDict):
    Image: ImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeImagesResultTypeDef(TypedDict):
    Images: list[ImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateAppBlockResultTypeDef(TypedDict):
    AppBlock: AppBlockTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAppBlocksResultTypeDef(TypedDict):
    AppBlocks: list[AppBlockTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
