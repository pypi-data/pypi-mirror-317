"""
Type annotations for appconfig service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appconfig/type_defs/)

Usage::

    ```python
    from types_boto3_appconfig.type_defs import DeletionProtectionSettingsTypeDef

    data: DeletionProtectionSettingsTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import IO, Any, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ActionPointType,
    DeletionProtectionCheckType,
    DeploymentEventTypeType,
    DeploymentStateType,
    EnvironmentStateType,
    GrowthTypeType,
    ReplicateToType,
    TriggeredByType,
    ValidatorTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccountSettingsTypeDef",
    "ActionInvocationTypeDef",
    "ActionTypeDef",
    "ApplicationResponseTypeDef",
    "ApplicationTypeDef",
    "ApplicationsTypeDef",
    "AppliedExtensionTypeDef",
    "BlobTypeDef",
    "ConfigurationProfileSummaryTypeDef",
    "ConfigurationProfileTypeDef",
    "ConfigurationProfilesTypeDef",
    "ConfigurationTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateConfigurationProfileRequestRequestTypeDef",
    "CreateDeploymentStrategyRequestRequestTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "CreateExtensionAssociationRequestRequestTypeDef",
    "CreateExtensionRequestRequestTypeDef",
    "CreateHostedConfigurationVersionRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteConfigurationProfileRequestRequestTypeDef",
    "DeleteDeploymentStrategyRequestRequestTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeleteExtensionAssociationRequestRequestTypeDef",
    "DeleteExtensionRequestRequestTypeDef",
    "DeleteHostedConfigurationVersionRequestRequestTypeDef",
    "DeletionProtectionSettingsTypeDef",
    "DeploymentEventTypeDef",
    "DeploymentStrategiesTypeDef",
    "DeploymentStrategyResponseTypeDef",
    "DeploymentStrategyTypeDef",
    "DeploymentSummaryTypeDef",
    "DeploymentTypeDef",
    "DeploymentsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnvironmentResponseTypeDef",
    "EnvironmentTypeDef",
    "EnvironmentsTypeDef",
    "ExtensionAssociationSummaryTypeDef",
    "ExtensionAssociationTypeDef",
    "ExtensionAssociationsTypeDef",
    "ExtensionSummaryTypeDef",
    "ExtensionTypeDef",
    "ExtensionsTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetConfigurationProfileRequestRequestTypeDef",
    "GetConfigurationRequestRequestTypeDef",
    "GetDeploymentRequestRequestTypeDef",
    "GetDeploymentStrategyRequestRequestTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetExtensionAssociationRequestRequestTypeDef",
    "GetExtensionRequestRequestTypeDef",
    "GetHostedConfigurationVersionRequestRequestTypeDef",
    "HostedConfigurationVersionSummaryTypeDef",
    "HostedConfigurationVersionTypeDef",
    "HostedConfigurationVersionsTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListConfigurationProfilesRequestPaginateTypeDef",
    "ListConfigurationProfilesRequestRequestTypeDef",
    "ListDeploymentStrategiesRequestPaginateTypeDef",
    "ListDeploymentStrategiesRequestRequestTypeDef",
    "ListDeploymentsRequestPaginateTypeDef",
    "ListDeploymentsRequestRequestTypeDef",
    "ListEnvironmentsRequestPaginateTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListExtensionAssociationsRequestPaginateTypeDef",
    "ListExtensionAssociationsRequestRequestTypeDef",
    "ListExtensionsRequestPaginateTypeDef",
    "ListExtensionsRequestRequestTypeDef",
    "ListHostedConfigurationVersionsRequestPaginateTypeDef",
    "ListHostedConfigurationVersionsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MonitorTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterTypeDef",
    "ResourceTagsTypeDef",
    "ResponseMetadataTypeDef",
    "StartDeploymentRequestRequestTypeDef",
    "StopDeploymentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateConfigurationProfileRequestRequestTypeDef",
    "UpdateDeploymentStrategyRequestRequestTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "UpdateExtensionAssociationRequestRequestTypeDef",
    "UpdateExtensionRequestRequestTypeDef",
    "ValidateConfigurationRequestRequestTypeDef",
    "ValidatorTypeDef",
)


class DeletionProtectionSettingsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    ProtectionPeriodInMinutes: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ActionInvocationTypeDef(TypedDict):
    ExtensionIdentifier: NotRequired[str]
    ActionName: NotRequired[str]
    Uri: NotRequired[str]
    RoleArn: NotRequired[str]
    ErrorMessage: NotRequired[str]
    ErrorCode: NotRequired[str]
    InvocationId: NotRequired[str]


class ActionTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    Uri: NotRequired[str]
    RoleArn: NotRequired[str]


class ApplicationTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]


class AppliedExtensionTypeDef(TypedDict):
    ExtensionId: NotRequired[str]
    ExtensionAssociationId: NotRequired[str]
    VersionNumber: NotRequired[int]
    Parameters: NotRequired[dict[str, str]]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ConfigurationProfileSummaryTypeDef = TypedDict(
    "ConfigurationProfileSummaryTypeDef",
    {
        "ApplicationId": NotRequired[str],
        "Id": NotRequired[str],
        "Name": NotRequired[str],
        "LocationUri": NotRequired[str],
        "ValidatorTypes": NotRequired[list[ValidatorTypeType]],
        "Type": NotRequired[str],
    },
)
ValidatorTypeDef = TypedDict(
    "ValidatorTypeDef",
    {
        "Type": ValidatorTypeType,
        "Content": str,
    },
)


class CreateApplicationRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]


class CreateDeploymentStrategyRequestRequestTypeDef(TypedDict):
    Name: str
    DeploymentDurationInMinutes: int
    GrowthFactor: float
    Description: NotRequired[str]
    FinalBakeTimeInMinutes: NotRequired[int]
    GrowthType: NotRequired[GrowthTypeType]
    ReplicateTo: NotRequired[ReplicateToType]
    Tags: NotRequired[Mapping[str, str]]


class MonitorTypeDef(TypedDict):
    AlarmArn: str
    AlarmRoleArn: NotRequired[str]


class CreateExtensionAssociationRequestRequestTypeDef(TypedDict):
    ExtensionIdentifier: str
    ResourceIdentifier: str
    ExtensionVersionNumber: NotRequired[int]
    Parameters: NotRequired[Mapping[str, str]]
    Tags: NotRequired[Mapping[str, str]]


ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "Description": NotRequired[str],
        "Required": NotRequired[bool],
        "Dynamic": NotRequired[bool],
    },
)


class DeleteApplicationRequestRequestTypeDef(TypedDict):
    ApplicationId: str


class DeleteConfigurationProfileRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    DeletionProtectionCheck: NotRequired[DeletionProtectionCheckType]


class DeleteDeploymentStrategyRequestRequestTypeDef(TypedDict):
    DeploymentStrategyId: str


class DeleteEnvironmentRequestRequestTypeDef(TypedDict):
    EnvironmentId: str
    ApplicationId: str
    DeletionProtectionCheck: NotRequired[DeletionProtectionCheckType]


class DeleteExtensionAssociationRequestRequestTypeDef(TypedDict):
    ExtensionAssociationId: str


class DeleteExtensionRequestRequestTypeDef(TypedDict):
    ExtensionIdentifier: str
    VersionNumber: NotRequired[int]


class DeleteHostedConfigurationVersionRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    VersionNumber: int


class DeploymentStrategyTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    DeploymentDurationInMinutes: NotRequired[int]
    GrowthType: NotRequired[GrowthTypeType]
    GrowthFactor: NotRequired[float]
    FinalBakeTimeInMinutes: NotRequired[int]
    ReplicateTo: NotRequired[ReplicateToType]


class DeploymentSummaryTypeDef(TypedDict):
    DeploymentNumber: NotRequired[int]
    ConfigurationName: NotRequired[str]
    ConfigurationVersion: NotRequired[str]
    DeploymentDurationInMinutes: NotRequired[int]
    GrowthType: NotRequired[GrowthTypeType]
    GrowthFactor: NotRequired[float]
    FinalBakeTimeInMinutes: NotRequired[int]
    State: NotRequired[DeploymentStateType]
    PercentageComplete: NotRequired[float]
    StartedAt: NotRequired[datetime]
    CompletedAt: NotRequired[datetime]
    VersionLabel: NotRequired[str]


class ExtensionAssociationSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    ExtensionArn: NotRequired[str]
    ResourceArn: NotRequired[str]


class ExtensionSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    VersionNumber: NotRequired[int]
    Arn: NotRequired[str]
    Description: NotRequired[str]


class GetApplicationRequestRequestTypeDef(TypedDict):
    ApplicationId: str


class GetConfigurationProfileRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str


class GetConfigurationRequestRequestTypeDef(TypedDict):
    Application: str
    Environment: str
    Configuration: str
    ClientId: str
    ClientConfigurationVersion: NotRequired[str]


class GetDeploymentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EnvironmentId: str
    DeploymentNumber: int


class GetDeploymentStrategyRequestRequestTypeDef(TypedDict):
    DeploymentStrategyId: str


class GetEnvironmentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EnvironmentId: str


class GetExtensionAssociationRequestRequestTypeDef(TypedDict):
    ExtensionAssociationId: str


class GetExtensionRequestRequestTypeDef(TypedDict):
    ExtensionIdentifier: str
    VersionNumber: NotRequired[int]


class GetHostedConfigurationVersionRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    VersionNumber: int


class HostedConfigurationVersionSummaryTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    ConfigurationProfileId: NotRequired[str]
    VersionNumber: NotRequired[int]
    Description: NotRequired[str]
    ContentType: NotRequired[str]
    VersionLabel: NotRequired[str]
    KmsKeyArn: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListApplicationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


ListConfigurationProfilesRequestRequestTypeDef = TypedDict(
    "ListConfigurationProfilesRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "Type": NotRequired[str],
    },
)


class ListDeploymentStrategiesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDeploymentsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EnvironmentId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListEnvironmentsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListExtensionAssociationsRequestRequestTypeDef(TypedDict):
    ResourceIdentifier: NotRequired[str]
    ExtensionIdentifier: NotRequired[str]
    ExtensionVersionNumber: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListExtensionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Name: NotRequired[str]


class ListHostedConfigurationVersionsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    VersionLabel: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class StartDeploymentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EnvironmentId: str
    DeploymentStrategyId: str
    ConfigurationProfileId: str
    ConfigurationVersion: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    KmsKeyIdentifier: NotRequired[str]
    DynamicExtensionParameters: NotRequired[Mapping[str, str]]


class StopDeploymentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EnvironmentId: str
    DeploymentNumber: int
    AllowRevert: NotRequired[bool]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateApplicationRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    Name: NotRequired[str]
    Description: NotRequired[str]


class UpdateDeploymentStrategyRequestRequestTypeDef(TypedDict):
    DeploymentStrategyId: str
    Description: NotRequired[str]
    DeploymentDurationInMinutes: NotRequired[int]
    FinalBakeTimeInMinutes: NotRequired[int]
    GrowthFactor: NotRequired[float]
    GrowthType: NotRequired[GrowthTypeType]


class UpdateExtensionAssociationRequestRequestTypeDef(TypedDict):
    ExtensionAssociationId: str
    Parameters: NotRequired[Mapping[str, str]]


class ValidateConfigurationRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    ConfigurationVersion: str


class UpdateAccountSettingsRequestRequestTypeDef(TypedDict):
    DeletionProtection: NotRequired[DeletionProtectionSettingsTypeDef]


class AccountSettingsTypeDef(TypedDict):
    DeletionProtection: DeletionProtectionSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ApplicationResponseTypeDef(TypedDict):
    Id: str
    Name: str
    Description: str
    ResponseMetadata: ResponseMetadataTypeDef


class ConfigurationTypeDef(TypedDict):
    Content: StreamingBody
    ConfigurationVersion: str
    ContentType: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeploymentStrategyResponseTypeDef(TypedDict):
    Id: str
    Name: str
    Description: str
    DeploymentDurationInMinutes: int
    GrowthType: GrowthTypeType
    GrowthFactor: float
    FinalBakeTimeInMinutes: int
    ReplicateTo: ReplicateToType
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ExtensionAssociationTypeDef(TypedDict):
    Id: str
    ExtensionArn: str
    ResourceArn: str
    Arn: str
    Parameters: dict[str, str]
    ExtensionVersionNumber: int
    ResponseMetadata: ResponseMetadataTypeDef


class HostedConfigurationVersionTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    VersionNumber: int
    Description: str
    Content: StreamingBody
    ContentType: str
    VersionLabel: str
    KmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResourceTagsTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeploymentEventTypeDef(TypedDict):
    EventType: NotRequired[DeploymentEventTypeType]
    TriggeredBy: NotRequired[TriggeredByType]
    Description: NotRequired[str]
    ActionInvocations: NotRequired[list[ActionInvocationTypeDef]]
    OccurredAt: NotRequired[datetime]


class ApplicationsTypeDef(TypedDict):
    Items: list[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateHostedConfigurationVersionRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    Content: BlobTypeDef
    ContentType: str
    Description: NotRequired[str]
    LatestVersionNumber: NotRequired[int]
    VersionLabel: NotRequired[str]


class ConfigurationProfilesTypeDef(TypedDict):
    Items: list[ConfigurationProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


ConfigurationProfileTypeDef = TypedDict(
    "ConfigurationProfileTypeDef",
    {
        "ApplicationId": str,
        "Id": str,
        "Name": str,
        "Description": str,
        "LocationUri": str,
        "RetrievalRoleArn": str,
        "Validators": list[ValidatorTypeDef],
        "Type": str,
        "KmsKeyArn": str,
        "KmsKeyIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateConfigurationProfileRequestRequestTypeDef = TypedDict(
    "CreateConfigurationProfileRequestRequestTypeDef",
    {
        "ApplicationId": str,
        "Name": str,
        "LocationUri": str,
        "Description": NotRequired[str],
        "RetrievalRoleArn": NotRequired[str],
        "Validators": NotRequired[Sequence[ValidatorTypeDef]],
        "Tags": NotRequired[Mapping[str, str]],
        "Type": NotRequired[str],
        "KmsKeyIdentifier": NotRequired[str],
    },
)


class UpdateConfigurationProfileRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    RetrievalRoleArn: NotRequired[str]
    Validators: NotRequired[Sequence[ValidatorTypeDef]]
    KmsKeyIdentifier: NotRequired[str]


class CreateEnvironmentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    Name: str
    Description: NotRequired[str]
    Monitors: NotRequired[Sequence[MonitorTypeDef]]
    Tags: NotRequired[Mapping[str, str]]


class EnvironmentResponseTypeDef(TypedDict):
    ApplicationId: str
    Id: str
    Name: str
    Description: str
    State: EnvironmentStateType
    Monitors: list[MonitorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EnvironmentTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    State: NotRequired[EnvironmentStateType]
    Monitors: NotRequired[list[MonitorTypeDef]]


class UpdateEnvironmentRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    EnvironmentId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    Monitors: NotRequired[Sequence[MonitorTypeDef]]


class CreateExtensionRequestRequestTypeDef(TypedDict):
    Name: str
    Actions: Mapping[ActionPointType, Sequence[ActionTypeDef]]
    Description: NotRequired[str]
    Parameters: NotRequired[Mapping[str, ParameterTypeDef]]
    Tags: NotRequired[Mapping[str, str]]
    LatestVersionNumber: NotRequired[int]


class ExtensionTypeDef(TypedDict):
    Id: str
    Name: str
    VersionNumber: int
    Arn: str
    Description: str
    Actions: dict[ActionPointType, list[ActionTypeDef]]
    Parameters: dict[str, ParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateExtensionRequestRequestTypeDef(TypedDict):
    ExtensionIdentifier: str
    Description: NotRequired[str]
    Actions: NotRequired[Mapping[ActionPointType, Sequence[ActionTypeDef]]]
    Parameters: NotRequired[Mapping[str, ParameterTypeDef]]
    VersionNumber: NotRequired[int]


class DeploymentStrategiesTypeDef(TypedDict):
    Items: list[DeploymentStrategyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DeploymentsTypeDef(TypedDict):
    Items: list[DeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ExtensionAssociationsTypeDef(TypedDict):
    Items: list[ExtensionAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ExtensionsTypeDef(TypedDict):
    Items: list[ExtensionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class HostedConfigurationVersionsTypeDef(TypedDict):
    Items: list[HostedConfigurationVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListApplicationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListConfigurationProfilesRequestPaginateTypeDef = TypedDict(
    "ListConfigurationProfilesRequestPaginateTypeDef",
    {
        "ApplicationId": str,
        "Type": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListDeploymentStrategiesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeploymentsRequestPaginateTypeDef(TypedDict):
    ApplicationId: str
    EnvironmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentsRequestPaginateTypeDef(TypedDict):
    ApplicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExtensionAssociationsRequestPaginateTypeDef(TypedDict):
    ResourceIdentifier: NotRequired[str]
    ExtensionIdentifier: NotRequired[str]
    ExtensionVersionNumber: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExtensionsRequestPaginateTypeDef(TypedDict):
    Name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHostedConfigurationVersionsRequestPaginateTypeDef(TypedDict):
    ApplicationId: str
    ConfigurationProfileId: str
    VersionLabel: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DeploymentTypeDef(TypedDict):
    ApplicationId: str
    EnvironmentId: str
    DeploymentStrategyId: str
    ConfigurationProfileId: str
    DeploymentNumber: int
    ConfigurationName: str
    ConfigurationLocationUri: str
    ConfigurationVersion: str
    Description: str
    DeploymentDurationInMinutes: int
    GrowthType: GrowthTypeType
    GrowthFactor: float
    FinalBakeTimeInMinutes: int
    State: DeploymentStateType
    EventLog: list[DeploymentEventTypeDef]
    PercentageComplete: float
    StartedAt: datetime
    CompletedAt: datetime
    AppliedExtensions: list[AppliedExtensionTypeDef]
    KmsKeyArn: str
    KmsKeyIdentifier: str
    VersionLabel: str
    ResponseMetadata: ResponseMetadataTypeDef


class EnvironmentsTypeDef(TypedDict):
    Items: list[EnvironmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
