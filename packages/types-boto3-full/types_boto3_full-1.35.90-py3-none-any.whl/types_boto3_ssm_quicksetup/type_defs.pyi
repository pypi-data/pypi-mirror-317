"""
Type annotations for ssm-quicksetup service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_quicksetup/type_defs/)

Usage::

    ```python
    from types_boto3_ssm_quicksetup.type_defs import ConfigurationDefinitionInputTypeDef

    data: ConfigurationDefinitionInputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence

from .literals import StatusType, StatusTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ConfigurationDefinitionInputTypeDef",
    "ConfigurationDefinitionSummaryTypeDef",
    "ConfigurationDefinitionTypeDef",
    "ConfigurationManagerSummaryTypeDef",
    "ConfigurationSummaryTypeDef",
    "CreateConfigurationManagerInputRequestTypeDef",
    "CreateConfigurationManagerOutputTypeDef",
    "DeleteConfigurationManagerInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FilterTypeDef",
    "GetConfigurationInputRequestTypeDef",
    "GetConfigurationManagerInputRequestTypeDef",
    "GetConfigurationManagerOutputTypeDef",
    "GetConfigurationOutputTypeDef",
    "GetServiceSettingsOutputTypeDef",
    "ListConfigurationManagersInputPaginateTypeDef",
    "ListConfigurationManagersInputRequestTypeDef",
    "ListConfigurationManagersOutputTypeDef",
    "ListConfigurationsInputPaginateTypeDef",
    "ListConfigurationsInputRequestTypeDef",
    "ListConfigurationsOutputTypeDef",
    "ListQuickSetupTypesOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "QuickSetupTypeOutputTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceSettingsTypeDef",
    "StatusSummaryTypeDef",
    "TagEntryTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateConfigurationDefinitionInputRequestTypeDef",
    "UpdateConfigurationManagerInputRequestTypeDef",
    "UpdateServiceSettingsInputRequestTypeDef",
)

ConfigurationDefinitionInputTypeDef = TypedDict(
    "ConfigurationDefinitionInputTypeDef",
    {
        "Parameters": Mapping[str, str],
        "Type": str,
        "LocalDeploymentAdministrationRoleArn": NotRequired[str],
        "LocalDeploymentExecutionRoleName": NotRequired[str],
        "TypeVersion": NotRequired[str],
    },
)
ConfigurationDefinitionSummaryTypeDef = TypedDict(
    "ConfigurationDefinitionSummaryTypeDef",
    {
        "FirstClassParameters": NotRequired[dict[str, str]],
        "Id": NotRequired[str],
        "Type": NotRequired[str],
        "TypeVersion": NotRequired[str],
    },
)
ConfigurationDefinitionTypeDef = TypedDict(
    "ConfigurationDefinitionTypeDef",
    {
        "Parameters": dict[str, str],
        "Type": str,
        "Id": NotRequired[str],
        "LocalDeploymentAdministrationRoleArn": NotRequired[str],
        "LocalDeploymentExecutionRoleName": NotRequired[str],
        "TypeVersion": NotRequired[str],
    },
)
StatusSummaryTypeDef = TypedDict(
    "StatusSummaryTypeDef",
    {
        "LastUpdatedAt": datetime,
        "StatusType": StatusTypeType,
        "Status": NotRequired[StatusType],
        "StatusDetails": NotRequired[dict[str, str]],
        "StatusMessage": NotRequired[str],
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteConfigurationManagerInputRequestTypeDef(TypedDict):
    ManagerArn: str

class FilterTypeDef(TypedDict):
    Key: str
    Values: Sequence[str]

class GetConfigurationInputRequestTypeDef(TypedDict):
    ConfigurationId: str

class GetConfigurationManagerInputRequestTypeDef(TypedDict):
    ManagerArn: str

class ServiceSettingsTypeDef(TypedDict):
    ExplorerEnablingRoleArn: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

QuickSetupTypeOutputTypeDef = TypedDict(
    "QuickSetupTypeOutputTypeDef",
    {
        "LatestVersion": NotRequired[str],
        "Type": NotRequired[str],
    },
)

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class TagEntryTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateConfigurationDefinitionInputRequestTypeDef(TypedDict):
    Id: str
    ManagerArn: str
    LocalDeploymentAdministrationRoleArn: NotRequired[str]
    LocalDeploymentExecutionRoleName: NotRequired[str]
    Parameters: NotRequired[Mapping[str, str]]
    TypeVersion: NotRequired[str]

class UpdateConfigurationManagerInputRequestTypeDef(TypedDict):
    ManagerArn: str
    Description: NotRequired[str]
    Name: NotRequired[str]

class UpdateServiceSettingsInputRequestTypeDef(TypedDict):
    ExplorerEnablingRoleArn: NotRequired[str]

class CreateConfigurationManagerInputRequestTypeDef(TypedDict):
    ConfigurationDefinitions: Sequence[ConfigurationDefinitionInputTypeDef]
    Description: NotRequired[str]
    Name: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class ConfigurationManagerSummaryTypeDef(TypedDict):
    ManagerArn: str
    ConfigurationDefinitionSummaries: NotRequired[list[ConfigurationDefinitionSummaryTypeDef]]
    Description: NotRequired[str]
    Name: NotRequired[str]
    StatusSummaries: NotRequired[list[StatusSummaryTypeDef]]

ConfigurationSummaryTypeDef = TypedDict(
    "ConfigurationSummaryTypeDef",
    {
        "Account": NotRequired[str],
        "ConfigurationDefinitionId": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "FirstClassParameters": NotRequired[dict[str, str]],
        "Id": NotRequired[str],
        "ManagerArn": NotRequired[str],
        "Region": NotRequired[str],
        "StatusSummaries": NotRequired[list[StatusSummaryTypeDef]],
        "Type": NotRequired[str],
        "TypeVersion": NotRequired[str],
    },
)

class CreateConfigurationManagerOutputTypeDef(TypedDict):
    ManagerArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfigurationManagerOutputTypeDef(TypedDict):
    ConfigurationDefinitions: list[ConfigurationDefinitionTypeDef]
    CreatedAt: datetime
    Description: str
    LastModifiedAt: datetime
    ManagerArn: str
    Name: str
    StatusSummaries: list[StatusSummaryTypeDef]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

GetConfigurationOutputTypeDef = TypedDict(
    "GetConfigurationOutputTypeDef",
    {
        "Account": str,
        "ConfigurationDefinitionId": str,
        "CreatedAt": datetime,
        "Id": str,
        "LastModifiedAt": datetime,
        "ManagerArn": str,
        "Parameters": dict[str, str],
        "Region": str,
        "StatusSummaries": list[StatusSummaryTypeDef],
        "Type": str,
        "TypeVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListConfigurationManagersInputRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxItems: NotRequired[int]
    StartingToken: NotRequired[str]

class ListConfigurationsInputRequestTypeDef(TypedDict):
    ConfigurationDefinitionId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ManagerArn: NotRequired[str]
    MaxItems: NotRequired[int]
    StartingToken: NotRequired[str]

class GetServiceSettingsOutputTypeDef(TypedDict):
    ServiceSettings: ServiceSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationManagersInputPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfigurationsInputPaginateTypeDef(TypedDict):
    ConfigurationDefinitionId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ManagerArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQuickSetupTypesOutputTypeDef(TypedDict):
    QuickSetupTypeList: list[QuickSetupTypeOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListConfigurationManagersOutputTypeDef(TypedDict):
    ConfigurationManagersList: list[ConfigurationManagerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListConfigurationsOutputTypeDef(TypedDict):
    ConfigurationsList: list[ConfigurationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
