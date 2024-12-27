"""
Type annotations for devicefarm service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_devicefarm/type_defs/)

Usage::

    ```python
    from types_boto3_devicefarm.type_defs import TrialMinutesTypeDef

    data: TrialMinutesTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    ArtifactCategoryType,
    ArtifactTypeType,
    BillingMethodType,
    DeviceAttributeType,
    DeviceAvailabilityType,
    DeviceFilterAttributeType,
    DeviceFormFactorType,
    DevicePlatformType,
    DevicePoolTypeType,
    ExecutionResultCodeType,
    ExecutionResultType,
    ExecutionStatusType,
    InstanceStatusType,
    InteractionModeType,
    NetworkProfileTypeType,
    OfferingTransactionTypeType,
    RuleOperatorType,
    SampleTypeType,
    TestGridSessionArtifactCategoryType,
    TestGridSessionArtifactTypeType,
    TestGridSessionStatusType,
    TestTypeType,
    UploadCategoryType,
    UploadStatusType,
    UploadTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountSettingsTypeDef",
    "ArtifactTypeDef",
    "CPUTypeDef",
    "CountersTypeDef",
    "CreateDevicePoolRequestRequestTypeDef",
    "CreateDevicePoolResultTypeDef",
    "CreateInstanceProfileRequestRequestTypeDef",
    "CreateInstanceProfileResultTypeDef",
    "CreateNetworkProfileRequestRequestTypeDef",
    "CreateNetworkProfileResultTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResultTypeDef",
    "CreateRemoteAccessSessionConfigurationTypeDef",
    "CreateRemoteAccessSessionRequestRequestTypeDef",
    "CreateRemoteAccessSessionResultTypeDef",
    "CreateTestGridProjectRequestRequestTypeDef",
    "CreateTestGridProjectResultTypeDef",
    "CreateTestGridUrlRequestRequestTypeDef",
    "CreateTestGridUrlResultTypeDef",
    "CreateUploadRequestRequestTypeDef",
    "CreateUploadResultTypeDef",
    "CreateVPCEConfigurationRequestRequestTypeDef",
    "CreateVPCEConfigurationResultTypeDef",
    "CustomerArtifactPathsOutputTypeDef",
    "CustomerArtifactPathsTypeDef",
    "CustomerArtifactPathsUnionTypeDef",
    "DeleteDevicePoolRequestRequestTypeDef",
    "DeleteInstanceProfileRequestRequestTypeDef",
    "DeleteNetworkProfileRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteRemoteAccessSessionRequestRequestTypeDef",
    "DeleteRunRequestRequestTypeDef",
    "DeleteTestGridProjectRequestRequestTypeDef",
    "DeleteUploadRequestRequestTypeDef",
    "DeleteVPCEConfigurationRequestRequestTypeDef",
    "DeviceFilterOutputTypeDef",
    "DeviceFilterTypeDef",
    "DeviceFilterUnionTypeDef",
    "DeviceInstanceTypeDef",
    "DeviceMinutesTypeDef",
    "DevicePoolCompatibilityResultTypeDef",
    "DevicePoolTypeDef",
    "DeviceSelectionConfigurationTypeDef",
    "DeviceSelectionResultTypeDef",
    "DeviceTypeDef",
    "ExecutionConfigurationTypeDef",
    "GetAccountSettingsResultTypeDef",
    "GetDeviceInstanceRequestRequestTypeDef",
    "GetDeviceInstanceResultTypeDef",
    "GetDevicePoolCompatibilityRequestRequestTypeDef",
    "GetDevicePoolCompatibilityResultTypeDef",
    "GetDevicePoolRequestRequestTypeDef",
    "GetDevicePoolResultTypeDef",
    "GetDeviceRequestRequestTypeDef",
    "GetDeviceResultTypeDef",
    "GetInstanceProfileRequestRequestTypeDef",
    "GetInstanceProfileResultTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetJobResultTypeDef",
    "GetNetworkProfileRequestRequestTypeDef",
    "GetNetworkProfileResultTypeDef",
    "GetOfferingStatusRequestPaginateTypeDef",
    "GetOfferingStatusRequestRequestTypeDef",
    "GetOfferingStatusResultTypeDef",
    "GetProjectRequestRequestTypeDef",
    "GetProjectResultTypeDef",
    "GetRemoteAccessSessionRequestRequestTypeDef",
    "GetRemoteAccessSessionResultTypeDef",
    "GetRunRequestRequestTypeDef",
    "GetRunResultTypeDef",
    "GetSuiteRequestRequestTypeDef",
    "GetSuiteResultTypeDef",
    "GetTestGridProjectRequestRequestTypeDef",
    "GetTestGridProjectResultTypeDef",
    "GetTestGridSessionRequestRequestTypeDef",
    "GetTestGridSessionResultTypeDef",
    "GetTestRequestRequestTypeDef",
    "GetTestResultTypeDef",
    "GetUploadRequestRequestTypeDef",
    "GetUploadResultTypeDef",
    "GetVPCEConfigurationRequestRequestTypeDef",
    "GetVPCEConfigurationResultTypeDef",
    "IncompatibilityMessageTypeDef",
    "InstallToRemoteAccessSessionRequestRequestTypeDef",
    "InstallToRemoteAccessSessionResultTypeDef",
    "InstanceProfileTypeDef",
    "JobTypeDef",
    "ListArtifactsRequestPaginateTypeDef",
    "ListArtifactsRequestRequestTypeDef",
    "ListArtifactsResultTypeDef",
    "ListDeviceInstancesRequestPaginateTypeDef",
    "ListDeviceInstancesRequestRequestTypeDef",
    "ListDeviceInstancesResultTypeDef",
    "ListDevicePoolsRequestPaginateTypeDef",
    "ListDevicePoolsRequestRequestTypeDef",
    "ListDevicePoolsResultTypeDef",
    "ListDevicesRequestPaginateTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "ListDevicesResultTypeDef",
    "ListInstanceProfilesRequestPaginateTypeDef",
    "ListInstanceProfilesRequestRequestTypeDef",
    "ListInstanceProfilesResultTypeDef",
    "ListJobsRequestPaginateTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListJobsResultTypeDef",
    "ListNetworkProfilesRequestPaginateTypeDef",
    "ListNetworkProfilesRequestRequestTypeDef",
    "ListNetworkProfilesResultTypeDef",
    "ListOfferingPromotionsRequestPaginateTypeDef",
    "ListOfferingPromotionsRequestRequestTypeDef",
    "ListOfferingPromotionsResultTypeDef",
    "ListOfferingTransactionsRequestPaginateTypeDef",
    "ListOfferingTransactionsRequestRequestTypeDef",
    "ListOfferingTransactionsResultTypeDef",
    "ListOfferingsRequestPaginateTypeDef",
    "ListOfferingsRequestRequestTypeDef",
    "ListOfferingsResultTypeDef",
    "ListProjectsRequestPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResultTypeDef",
    "ListRemoteAccessSessionsRequestPaginateTypeDef",
    "ListRemoteAccessSessionsRequestRequestTypeDef",
    "ListRemoteAccessSessionsResultTypeDef",
    "ListRunsRequestPaginateTypeDef",
    "ListRunsRequestRequestTypeDef",
    "ListRunsResultTypeDef",
    "ListSamplesRequestPaginateTypeDef",
    "ListSamplesRequestRequestTypeDef",
    "ListSamplesResultTypeDef",
    "ListSuitesRequestPaginateTypeDef",
    "ListSuitesRequestRequestTypeDef",
    "ListSuitesResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTestGridProjectsRequestRequestTypeDef",
    "ListTestGridProjectsResultTypeDef",
    "ListTestGridSessionActionsRequestRequestTypeDef",
    "ListTestGridSessionActionsResultTypeDef",
    "ListTestGridSessionArtifactsRequestRequestTypeDef",
    "ListTestGridSessionArtifactsResultTypeDef",
    "ListTestGridSessionsRequestRequestTypeDef",
    "ListTestGridSessionsResultTypeDef",
    "ListTestsRequestPaginateTypeDef",
    "ListTestsRequestRequestTypeDef",
    "ListTestsResultTypeDef",
    "ListUniqueProblemsRequestPaginateTypeDef",
    "ListUniqueProblemsRequestRequestTypeDef",
    "ListUniqueProblemsResultTypeDef",
    "ListUploadsRequestPaginateTypeDef",
    "ListUploadsRequestRequestTypeDef",
    "ListUploadsResultTypeDef",
    "ListVPCEConfigurationsRequestPaginateTypeDef",
    "ListVPCEConfigurationsRequestRequestTypeDef",
    "ListVPCEConfigurationsResultTypeDef",
    "LocationTypeDef",
    "MonetaryAmountTypeDef",
    "NetworkProfileTypeDef",
    "OfferingPromotionTypeDef",
    "OfferingStatusTypeDef",
    "OfferingTransactionTypeDef",
    "OfferingTypeDef",
    "PaginatorConfigTypeDef",
    "ProblemDetailTypeDef",
    "ProblemTypeDef",
    "ProjectTypeDef",
    "PurchaseOfferingRequestRequestTypeDef",
    "PurchaseOfferingResultTypeDef",
    "RadiosTypeDef",
    "RecurringChargeTypeDef",
    "RemoteAccessSessionTypeDef",
    "RenewOfferingRequestRequestTypeDef",
    "RenewOfferingResultTypeDef",
    "ResolutionTypeDef",
    "ResponseMetadataTypeDef",
    "RuleTypeDef",
    "RunTypeDef",
    "SampleTypeDef",
    "ScheduleRunConfigurationTypeDef",
    "ScheduleRunRequestRequestTypeDef",
    "ScheduleRunResultTypeDef",
    "ScheduleRunTestTypeDef",
    "StopJobRequestRequestTypeDef",
    "StopJobResultTypeDef",
    "StopRemoteAccessSessionRequestRequestTypeDef",
    "StopRemoteAccessSessionResultTypeDef",
    "StopRunRequestRequestTypeDef",
    "StopRunResultTypeDef",
    "SuiteTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TestGridProjectTypeDef",
    "TestGridSessionActionTypeDef",
    "TestGridSessionArtifactTypeDef",
    "TestGridSessionTypeDef",
    "TestGridVpcConfigOutputTypeDef",
    "TestGridVpcConfigTypeDef",
    "TestTypeDef",
    "TimestampTypeDef",
    "TrialMinutesTypeDef",
    "UniqueProblemTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDeviceInstanceRequestRequestTypeDef",
    "UpdateDeviceInstanceResultTypeDef",
    "UpdateDevicePoolRequestRequestTypeDef",
    "UpdateDevicePoolResultTypeDef",
    "UpdateInstanceProfileRequestRequestTypeDef",
    "UpdateInstanceProfileResultTypeDef",
    "UpdateNetworkProfileRequestRequestTypeDef",
    "UpdateNetworkProfileResultTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateProjectResultTypeDef",
    "UpdateTestGridProjectRequestRequestTypeDef",
    "UpdateTestGridProjectResultTypeDef",
    "UpdateUploadRequestRequestTypeDef",
    "UpdateUploadResultTypeDef",
    "UpdateVPCEConfigurationRequestRequestTypeDef",
    "UpdateVPCEConfigurationResultTypeDef",
    "UploadTypeDef",
    "VPCEConfigurationTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
)


class TrialMinutesTypeDef(TypedDict):
    total: NotRequired[float]
    remaining: NotRequired[float]


ArtifactTypeDef = TypedDict(
    "ArtifactTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[ArtifactTypeType],
        "extension": NotRequired[str],
        "url": NotRequired[str],
    },
)


class CPUTypeDef(TypedDict):
    frequency: NotRequired[str]
    architecture: NotRequired[str]
    clock: NotRequired[float]


class CountersTypeDef(TypedDict):
    total: NotRequired[int]
    passed: NotRequired[int]
    failed: NotRequired[int]
    warned: NotRequired[int]
    errored: NotRequired[int]
    stopped: NotRequired[int]
    skipped: NotRequired[int]


RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "attribute": NotRequired[DeviceAttributeType],
        "operator": NotRequired[RuleOperatorType],
        "value": NotRequired[str],
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateInstanceProfileRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    packageCleanup: NotRequired[bool]
    excludeAppPackagesFromCleanup: NotRequired[Sequence[str]]
    rebootAfterUse: NotRequired[bool]


class InstanceProfileTypeDef(TypedDict):
    arn: NotRequired[str]
    packageCleanup: NotRequired[bool]
    excludeAppPackagesFromCleanup: NotRequired[list[str]]
    rebootAfterUse: NotRequired[bool]
    name: NotRequired[str]
    description: NotRequired[str]


CreateNetworkProfileRequestRequestTypeDef = TypedDict(
    "CreateNetworkProfileRequestRequestTypeDef",
    {
        "projectArn": str,
        "name": str,
        "description": NotRequired[str],
        "type": NotRequired[NetworkProfileTypeType],
        "uplinkBandwidthBits": NotRequired[int],
        "downlinkBandwidthBits": NotRequired[int],
        "uplinkDelayMs": NotRequired[int],
        "downlinkDelayMs": NotRequired[int],
        "uplinkJitterMs": NotRequired[int],
        "downlinkJitterMs": NotRequired[int],
        "uplinkLossPercent": NotRequired[int],
        "downlinkLossPercent": NotRequired[int],
    },
)
NetworkProfileTypeDef = TypedDict(
    "NetworkProfileTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "type": NotRequired[NetworkProfileTypeType],
        "uplinkBandwidthBits": NotRequired[int],
        "downlinkBandwidthBits": NotRequired[int],
        "uplinkDelayMs": NotRequired[int],
        "downlinkDelayMs": NotRequired[int],
        "uplinkJitterMs": NotRequired[int],
        "downlinkJitterMs": NotRequired[int],
        "uplinkLossPercent": NotRequired[int],
        "downlinkLossPercent": NotRequired[int],
    },
)


class VpcConfigTypeDef(TypedDict):
    securityGroupIds: Sequence[str]
    subnetIds: Sequence[str]
    vpcId: str


class CreateRemoteAccessSessionConfigurationTypeDef(TypedDict):
    billingMethod: NotRequired[BillingMethodType]
    vpceConfigurationArns: NotRequired[Sequence[str]]


class TestGridVpcConfigTypeDef(TypedDict):
    securityGroupIds: Sequence[str]
    subnetIds: Sequence[str]
    vpcId: str


class CreateTestGridUrlRequestRequestTypeDef(TypedDict):
    projectArn: str
    expiresInSeconds: int


CreateUploadRequestRequestTypeDef = TypedDict(
    "CreateUploadRequestRequestTypeDef",
    {
        "projectArn": str,
        "name": str,
        "type": UploadTypeType,
        "contentType": NotRequired[str],
    },
)
UploadTypeDef = TypedDict(
    "UploadTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "created": NotRequired[datetime],
        "type": NotRequired[UploadTypeType],
        "status": NotRequired[UploadStatusType],
        "url": NotRequired[str],
        "metadata": NotRequired[str],
        "contentType": NotRequired[str],
        "message": NotRequired[str],
        "category": NotRequired[UploadCategoryType],
    },
)


class CreateVPCEConfigurationRequestRequestTypeDef(TypedDict):
    vpceConfigurationName: str
    vpceServiceName: str
    serviceDnsName: str
    vpceConfigurationDescription: NotRequired[str]


class VPCEConfigurationTypeDef(TypedDict):
    arn: NotRequired[str]
    vpceConfigurationName: NotRequired[str]
    vpceServiceName: NotRequired[str]
    serviceDnsName: NotRequired[str]
    vpceConfigurationDescription: NotRequired[str]


class CustomerArtifactPathsOutputTypeDef(TypedDict):
    iosPaths: NotRequired[list[str]]
    androidPaths: NotRequired[list[str]]
    deviceHostPaths: NotRequired[list[str]]


class CustomerArtifactPathsTypeDef(TypedDict):
    iosPaths: NotRequired[Sequence[str]]
    androidPaths: NotRequired[Sequence[str]]
    deviceHostPaths: NotRequired[Sequence[str]]


class DeleteDevicePoolRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteInstanceProfileRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteNetworkProfileRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteProjectRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteRemoteAccessSessionRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteRunRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteTestGridProjectRequestRequestTypeDef(TypedDict):
    projectArn: str


class DeleteUploadRequestRequestTypeDef(TypedDict):
    arn: str


class DeleteVPCEConfigurationRequestRequestTypeDef(TypedDict):
    arn: str


DeviceFilterOutputTypeDef = TypedDict(
    "DeviceFilterOutputTypeDef",
    {
        "attribute": DeviceFilterAttributeType,
        "operator": RuleOperatorType,
        "values": list[str],
    },
)
DeviceFilterTypeDef = TypedDict(
    "DeviceFilterTypeDef",
    {
        "attribute": DeviceFilterAttributeType,
        "operator": RuleOperatorType,
        "values": Sequence[str],
    },
)


class DeviceMinutesTypeDef(TypedDict):
    total: NotRequired[float]
    metered: NotRequired[float]
    unmetered: NotRequired[float]


IncompatibilityMessageTypeDef = TypedDict(
    "IncompatibilityMessageTypeDef",
    {
        "message": NotRequired[str],
        "type": NotRequired[DeviceAttributeType],
    },
)


class ResolutionTypeDef(TypedDict):
    width: NotRequired[int]
    height: NotRequired[int]


class ExecutionConfigurationTypeDef(TypedDict):
    jobTimeoutMinutes: NotRequired[int]
    accountsCleanup: NotRequired[bool]
    appPackagesCleanup: NotRequired[bool]
    videoCapture: NotRequired[bool]
    skipAppResign: NotRequired[bool]


class GetDeviceInstanceRequestRequestTypeDef(TypedDict):
    arn: str


ScheduleRunTestTypeDef = TypedDict(
    "ScheduleRunTestTypeDef",
    {
        "type": TestTypeType,
        "testPackageArn": NotRequired[str],
        "testSpecArn": NotRequired[str],
        "filter": NotRequired[str],
        "parameters": NotRequired[Mapping[str, str]],
    },
)


class GetDevicePoolRequestRequestTypeDef(TypedDict):
    arn: str


class GetDeviceRequestRequestTypeDef(TypedDict):
    arn: str


class GetInstanceProfileRequestRequestTypeDef(TypedDict):
    arn: str


class GetJobRequestRequestTypeDef(TypedDict):
    arn: str


class GetNetworkProfileRequestRequestTypeDef(TypedDict):
    arn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetOfferingStatusRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]


class GetProjectRequestRequestTypeDef(TypedDict):
    arn: str


class GetRemoteAccessSessionRequestRequestTypeDef(TypedDict):
    arn: str


class GetRunRequestRequestTypeDef(TypedDict):
    arn: str


class GetSuiteRequestRequestTypeDef(TypedDict):
    arn: str


class GetTestGridProjectRequestRequestTypeDef(TypedDict):
    projectArn: str


class GetTestGridSessionRequestRequestTypeDef(TypedDict):
    projectArn: NotRequired[str]
    sessionId: NotRequired[str]
    sessionArn: NotRequired[str]


class TestGridSessionTypeDef(TypedDict):
    arn: NotRequired[str]
    status: NotRequired[TestGridSessionStatusType]
    created: NotRequired[datetime]
    ended: NotRequired[datetime]
    billingMinutes: NotRequired[float]
    seleniumProperties: NotRequired[str]


class GetTestRequestRequestTypeDef(TypedDict):
    arn: str


class GetUploadRequestRequestTypeDef(TypedDict):
    arn: str


class GetVPCEConfigurationRequestRequestTypeDef(TypedDict):
    arn: str


class InstallToRemoteAccessSessionRequestRequestTypeDef(TypedDict):
    remoteAccessSessionArn: str
    appArn: str


ListArtifactsRequestRequestTypeDef = TypedDict(
    "ListArtifactsRequestRequestTypeDef",
    {
        "arn": str,
        "type": ArtifactCategoryType,
        "nextToken": NotRequired[str],
    },
)


class ListDeviceInstancesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ListDevicePoolsRequestRequestTypeDef = TypedDict(
    "ListDevicePoolsRequestRequestTypeDef",
    {
        "arn": str,
        "type": NotRequired[DevicePoolTypeType],
        "nextToken": NotRequired[str],
    },
)


class ListInstanceProfilesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListJobsRequestRequestTypeDef(TypedDict):
    arn: str
    nextToken: NotRequired[str]


ListNetworkProfilesRequestRequestTypeDef = TypedDict(
    "ListNetworkProfilesRequestRequestTypeDef",
    {
        "arn": str,
        "type": NotRequired[NetworkProfileTypeType],
        "nextToken": NotRequired[str],
    },
)


class ListOfferingPromotionsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]


OfferingPromotionTypeDef = TypedDict(
    "OfferingPromotionTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
    },
)


class ListOfferingTransactionsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]


class ListOfferingsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]


class ListProjectsRequestRequestTypeDef(TypedDict):
    arn: NotRequired[str]
    nextToken: NotRequired[str]


class ListRemoteAccessSessionsRequestRequestTypeDef(TypedDict):
    arn: str
    nextToken: NotRequired[str]


class ListRunsRequestRequestTypeDef(TypedDict):
    arn: str
    nextToken: NotRequired[str]


class ListSamplesRequestRequestTypeDef(TypedDict):
    arn: str
    nextToken: NotRequired[str]


SampleTypeDef = TypedDict(
    "SampleTypeDef",
    {
        "arn": NotRequired[str],
        "type": NotRequired[SampleTypeType],
        "url": NotRequired[str],
    },
)


class ListSuitesRequestRequestTypeDef(TypedDict):
    arn: str
    nextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ListTestGridProjectsRequestRequestTypeDef(TypedDict):
    maxResult: NotRequired[int]
    nextToken: NotRequired[str]


class ListTestGridSessionActionsRequestRequestTypeDef(TypedDict):
    sessionArn: str
    maxResult: NotRequired[int]
    nextToken: NotRequired[str]


class TestGridSessionActionTypeDef(TypedDict):
    action: NotRequired[str]
    started: NotRequired[datetime]
    duration: NotRequired[int]
    statusCode: NotRequired[str]
    requestMethod: NotRequired[str]


ListTestGridSessionArtifactsRequestRequestTypeDef = TypedDict(
    "ListTestGridSessionArtifactsRequestRequestTypeDef",
    {
        "sessionArn": str,
        "type": NotRequired[TestGridSessionArtifactCategoryType],
        "maxResult": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
TestGridSessionArtifactTypeDef = TypedDict(
    "TestGridSessionArtifactTypeDef",
    {
        "filename": NotRequired[str],
        "type": NotRequired[TestGridSessionArtifactTypeType],
        "url": NotRequired[str],
    },
)
TimestampTypeDef = Union[datetime, str]


class ListTestsRequestRequestTypeDef(TypedDict):
    arn: str
    nextToken: NotRequired[str]


class ListUniqueProblemsRequestRequestTypeDef(TypedDict):
    arn: str
    nextToken: NotRequired[str]


ListUploadsRequestRequestTypeDef = TypedDict(
    "ListUploadsRequestRequestTypeDef",
    {
        "arn": str,
        "type": NotRequired[UploadTypeType],
        "nextToken": NotRequired[str],
    },
)


class ListVPCEConfigurationsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class LocationTypeDef(TypedDict):
    latitude: float
    longitude: float


class MonetaryAmountTypeDef(TypedDict):
    amount: NotRequired[float]
    currencyCode: NotRequired[Literal["USD"]]


class ProblemDetailTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]


class VpcConfigOutputTypeDef(TypedDict):
    securityGroupIds: list[str]
    subnetIds: list[str]
    vpcId: str


class PurchaseOfferingRequestRequestTypeDef(TypedDict):
    offeringId: str
    quantity: int
    offeringPromotionId: NotRequired[str]


class RadiosTypeDef(TypedDict):
    wifi: NotRequired[bool]
    bluetooth: NotRequired[bool]
    nfc: NotRequired[bool]
    gps: NotRequired[bool]


class RenewOfferingRequestRequestTypeDef(TypedDict):
    offeringId: str
    quantity: int


class StopJobRequestRequestTypeDef(TypedDict):
    arn: str


class StopRemoteAccessSessionRequestRequestTypeDef(TypedDict):
    arn: str


class StopRunRequestRequestTypeDef(TypedDict):
    arn: str


class TestGridVpcConfigOutputTypeDef(TypedDict):
    securityGroupIds: list[str]
    subnetIds: list[str]
    vpcId: str


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateDeviceInstanceRequestRequestTypeDef(TypedDict):
    arn: str
    profileArn: NotRequired[str]
    labels: NotRequired[Sequence[str]]


class UpdateInstanceProfileRequestRequestTypeDef(TypedDict):
    arn: str
    name: NotRequired[str]
    description: NotRequired[str]
    packageCleanup: NotRequired[bool]
    excludeAppPackagesFromCleanup: NotRequired[Sequence[str]]
    rebootAfterUse: NotRequired[bool]


UpdateNetworkProfileRequestRequestTypeDef = TypedDict(
    "UpdateNetworkProfileRequestRequestTypeDef",
    {
        "arn": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "type": NotRequired[NetworkProfileTypeType],
        "uplinkBandwidthBits": NotRequired[int],
        "downlinkBandwidthBits": NotRequired[int],
        "uplinkDelayMs": NotRequired[int],
        "downlinkDelayMs": NotRequired[int],
        "uplinkJitterMs": NotRequired[int],
        "downlinkJitterMs": NotRequired[int],
        "uplinkLossPercent": NotRequired[int],
        "downlinkLossPercent": NotRequired[int],
    },
)


class UpdateUploadRequestRequestTypeDef(TypedDict):
    arn: str
    name: NotRequired[str]
    contentType: NotRequired[str]
    editContent: NotRequired[bool]


class UpdateVPCEConfigurationRequestRequestTypeDef(TypedDict):
    arn: str
    vpceConfigurationName: NotRequired[str]
    vpceServiceName: NotRequired[str]
    serviceDnsName: NotRequired[str]
    vpceConfigurationDescription: NotRequired[str]


class AccountSettingsTypeDef(TypedDict):
    awsAccountNumber: NotRequired[str]
    unmeteredDevices: NotRequired[dict[DevicePlatformType, int]]
    unmeteredRemoteAccessDevices: NotRequired[dict[DevicePlatformType, int]]
    maxJobTimeoutMinutes: NotRequired[int]
    trialMinutes: NotRequired[TrialMinutesTypeDef]
    maxSlots: NotRequired[dict[str, int]]
    defaultJobTimeoutMinutes: NotRequired[int]
    skipAppResign: NotRequired[bool]


class CreateDevicePoolRequestRequestTypeDef(TypedDict):
    projectArn: str
    name: str
    rules: Sequence[RuleTypeDef]
    description: NotRequired[str]
    maxDevices: NotRequired[int]


DevicePoolTypeDef = TypedDict(
    "DevicePoolTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "description": NotRequired[str],
        "type": NotRequired[DevicePoolTypeType],
        "rules": NotRequired[list[RuleTypeDef]],
        "maxDevices": NotRequired[int],
    },
)


class UpdateDevicePoolRequestRequestTypeDef(TypedDict):
    arn: str
    name: NotRequired[str]
    description: NotRequired[str]
    rules: NotRequired[Sequence[RuleTypeDef]]
    maxDevices: NotRequired[int]
    clearMaxDevices: NotRequired[bool]


class CreateTestGridUrlResultTypeDef(TypedDict):
    url: str
    expires: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListArtifactsResultTypeDef(TypedDict):
    artifacts: list[ArtifactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateInstanceProfileResultTypeDef(TypedDict):
    instanceProfile: InstanceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeviceInstanceTypeDef(TypedDict):
    arn: NotRequired[str]
    deviceArn: NotRequired[str]
    labels: NotRequired[list[str]]
    status: NotRequired[InstanceStatusType]
    udid: NotRequired[str]
    instanceProfile: NotRequired[InstanceProfileTypeDef]


class GetInstanceProfileResultTypeDef(TypedDict):
    instanceProfile: InstanceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListInstanceProfilesResultTypeDef(TypedDict):
    instanceProfiles: list[InstanceProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateInstanceProfileResultTypeDef(TypedDict):
    instanceProfile: InstanceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNetworkProfileResultTypeDef(TypedDict):
    networkProfile: NetworkProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNetworkProfileResultTypeDef(TypedDict):
    networkProfile: NetworkProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListNetworkProfilesResultTypeDef(TypedDict):
    networkProfiles: list[NetworkProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateNetworkProfileResultTypeDef(TypedDict):
    networkProfile: NetworkProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProjectRequestRequestTypeDef(TypedDict):
    name: str
    defaultJobTimeoutMinutes: NotRequired[int]
    vpcConfig: NotRequired[VpcConfigTypeDef]


class UpdateProjectRequestRequestTypeDef(TypedDict):
    arn: str
    name: NotRequired[str]
    defaultJobTimeoutMinutes: NotRequired[int]
    vpcConfig: NotRequired[VpcConfigTypeDef]


class CreateRemoteAccessSessionRequestRequestTypeDef(TypedDict):
    projectArn: str
    deviceArn: str
    instanceArn: NotRequired[str]
    sshPublicKey: NotRequired[str]
    remoteDebugEnabled: NotRequired[bool]
    remoteRecordEnabled: NotRequired[bool]
    remoteRecordAppArn: NotRequired[str]
    name: NotRequired[str]
    clientId: NotRequired[str]
    configuration: NotRequired[CreateRemoteAccessSessionConfigurationTypeDef]
    interactionMode: NotRequired[InteractionModeType]
    skipAppResign: NotRequired[bool]


class CreateTestGridProjectRequestRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    vpcConfig: NotRequired[TestGridVpcConfigTypeDef]


class UpdateTestGridProjectRequestRequestTypeDef(TypedDict):
    projectArn: str
    name: NotRequired[str]
    description: NotRequired[str]
    vpcConfig: NotRequired[TestGridVpcConfigTypeDef]


class CreateUploadResultTypeDef(TypedDict):
    upload: UploadTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetUploadResultTypeDef(TypedDict):
    upload: UploadTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InstallToRemoteAccessSessionResultTypeDef(TypedDict):
    appUpload: UploadTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListUploadsResultTypeDef(TypedDict):
    uploads: list[UploadTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateUploadResultTypeDef(TypedDict):
    upload: UploadTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVPCEConfigurationResultTypeDef(TypedDict):
    vpceConfiguration: VPCEConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetVPCEConfigurationResultTypeDef(TypedDict):
    vpceConfiguration: VPCEConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListVPCEConfigurationsResultTypeDef(TypedDict):
    vpceConfigurations: list[VPCEConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateVPCEConfigurationResultTypeDef(TypedDict):
    vpceConfiguration: VPCEConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CustomerArtifactPathsUnionTypeDef = Union[
    CustomerArtifactPathsTypeDef, CustomerArtifactPathsOutputTypeDef
]


class DeviceSelectionResultTypeDef(TypedDict):
    filters: NotRequired[list[DeviceFilterOutputTypeDef]]
    matchedDevicesCount: NotRequired[int]
    maxDevices: NotRequired[int]


DeviceFilterUnionTypeDef = Union[DeviceFilterTypeDef, DeviceFilterOutputTypeDef]
SuiteTypeDef = TypedDict(
    "SuiteTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[TestTypeType],
        "created": NotRequired[datetime],
        "status": NotRequired[ExecutionStatusType],
        "result": NotRequired[ExecutionResultType],
        "started": NotRequired[datetime],
        "stopped": NotRequired[datetime],
        "counters": NotRequired[CountersTypeDef],
        "message": NotRequired[str],
        "deviceMinutes": NotRequired[DeviceMinutesTypeDef],
    },
)
TestTypeDef = TypedDict(
    "TestTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[TestTypeType],
        "created": NotRequired[datetime],
        "status": NotRequired[ExecutionStatusType],
        "result": NotRequired[ExecutionResultType],
        "started": NotRequired[datetime],
        "stopped": NotRequired[datetime],
        "counters": NotRequired[CountersTypeDef],
        "message": NotRequired[str],
        "deviceMinutes": NotRequired[DeviceMinutesTypeDef],
    },
)


class GetOfferingStatusRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListArtifactsRequestPaginateTypeDef = TypedDict(
    "ListArtifactsRequestPaginateTypeDef",
    {
        "arn": str,
        "type": ArtifactCategoryType,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListDeviceInstancesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListDevicePoolsRequestPaginateTypeDef = TypedDict(
    "ListDevicePoolsRequestPaginateTypeDef",
    {
        "arn": str,
        "type": NotRequired[DevicePoolTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListDevicesRequestPaginateTypeDef(TypedDict):
    arn: NotRequired[str]
    filters: NotRequired[Sequence[DeviceFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInstanceProfilesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobsRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListNetworkProfilesRequestPaginateTypeDef = TypedDict(
    "ListNetworkProfilesRequestPaginateTypeDef",
    {
        "arn": str,
        "type": NotRequired[NetworkProfileTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListOfferingPromotionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOfferingTransactionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOfferingsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectsRequestPaginateTypeDef(TypedDict):
    arn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRemoteAccessSessionsRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRunsRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSamplesRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSuitesRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTestsRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUniqueProblemsRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListUploadsRequestPaginateTypeDef = TypedDict(
    "ListUploadsRequestPaginateTypeDef",
    {
        "arn": str,
        "type": NotRequired[UploadTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListVPCEConfigurationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTestGridSessionResultTypeDef(TypedDict):
    testGridSession: TestGridSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTestGridSessionsResultTypeDef(TypedDict):
    testGridSessions: list[TestGridSessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListOfferingPromotionsResultTypeDef(TypedDict):
    offeringPromotions: list[OfferingPromotionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSamplesResultTypeDef(TypedDict):
    samples: list[SampleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class ListTestGridSessionActionsResultTypeDef(TypedDict):
    actions: list[TestGridSessionActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTestGridSessionArtifactsResultTypeDef(TypedDict):
    artifacts: list[TestGridSessionArtifactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTestGridSessionsRequestRequestTypeDef(TypedDict):
    projectArn: str
    status: NotRequired[TestGridSessionStatusType]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    endTimeAfter: NotRequired[TimestampTypeDef]
    endTimeBefore: NotRequired[TimestampTypeDef]
    maxResult: NotRequired[int]
    nextToken: NotRequired[str]


class RecurringChargeTypeDef(TypedDict):
    cost: NotRequired[MonetaryAmountTypeDef]
    frequency: NotRequired[Literal["MONTHLY"]]


class ProjectTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    defaultJobTimeoutMinutes: NotRequired[int]
    created: NotRequired[datetime]
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]


class TestGridProjectTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    vpcConfig: NotRequired[TestGridVpcConfigOutputTypeDef]
    created: NotRequired[datetime]


class GetAccountSettingsResultTypeDef(TypedDict):
    accountSettings: AccountSettingsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDevicePoolResultTypeDef(TypedDict):
    devicePool: DevicePoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDevicePoolResultTypeDef(TypedDict):
    devicePool: DevicePoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDevicePoolsResultTypeDef(TypedDict):
    devicePools: list[DevicePoolTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateDevicePoolResultTypeDef(TypedDict):
    devicePool: DevicePoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeviceTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    manufacturer: NotRequired[str]
    model: NotRequired[str]
    modelId: NotRequired[str]
    formFactor: NotRequired[DeviceFormFactorType]
    platform: NotRequired[DevicePlatformType]
    os: NotRequired[str]
    cpu: NotRequired[CPUTypeDef]
    resolution: NotRequired[ResolutionTypeDef]
    heapSize: NotRequired[int]
    memory: NotRequired[int]
    image: NotRequired[str]
    carrier: NotRequired[str]
    radio: NotRequired[str]
    remoteAccessEnabled: NotRequired[bool]
    remoteDebugEnabled: NotRequired[bool]
    fleetType: NotRequired[str]
    fleetName: NotRequired[str]
    instances: NotRequired[list[DeviceInstanceTypeDef]]
    availability: NotRequired[DeviceAvailabilityType]


class GetDeviceInstanceResultTypeDef(TypedDict):
    deviceInstance: DeviceInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDeviceInstancesResultTypeDef(TypedDict):
    deviceInstances: list[DeviceInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateDeviceInstanceResultTypeDef(TypedDict):
    deviceInstance: DeviceInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ScheduleRunConfigurationTypeDef(TypedDict):
    extraDataPackageArn: NotRequired[str]
    networkProfileArn: NotRequired[str]
    locale: NotRequired[str]
    location: NotRequired[LocationTypeDef]
    vpceConfigurationArns: NotRequired[Sequence[str]]
    customerArtifactPaths: NotRequired[CustomerArtifactPathsUnionTypeDef]
    radios: NotRequired[RadiosTypeDef]
    auxiliaryApps: NotRequired[Sequence[str]]
    billingMethod: NotRequired[BillingMethodType]


RunTypeDef = TypedDict(
    "RunTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[TestTypeType],
        "platform": NotRequired[DevicePlatformType],
        "created": NotRequired[datetime],
        "status": NotRequired[ExecutionStatusType],
        "result": NotRequired[ExecutionResultType],
        "started": NotRequired[datetime],
        "stopped": NotRequired[datetime],
        "counters": NotRequired[CountersTypeDef],
        "message": NotRequired[str],
        "totalJobs": NotRequired[int],
        "completedJobs": NotRequired[int],
        "billingMethod": NotRequired[BillingMethodType],
        "deviceMinutes": NotRequired[DeviceMinutesTypeDef],
        "networkProfile": NotRequired[NetworkProfileTypeDef],
        "parsingResultUrl": NotRequired[str],
        "resultCode": NotRequired[ExecutionResultCodeType],
        "seed": NotRequired[int],
        "appUpload": NotRequired[str],
        "eventCount": NotRequired[int],
        "jobTimeoutMinutes": NotRequired[int],
        "devicePoolArn": NotRequired[str],
        "locale": NotRequired[str],
        "radios": NotRequired[RadiosTypeDef],
        "location": NotRequired[LocationTypeDef],
        "customerArtifactPaths": NotRequired[CustomerArtifactPathsOutputTypeDef],
        "webUrl": NotRequired[str],
        "skipAppResign": NotRequired[bool],
        "testSpecArn": NotRequired[str],
        "deviceSelectionResult": NotRequired[DeviceSelectionResultTypeDef],
        "vpcConfig": NotRequired[VpcConfigOutputTypeDef],
    },
)


class DeviceSelectionConfigurationTypeDef(TypedDict):
    filters: Sequence[DeviceFilterUnionTypeDef]
    maxDevices: int


class ListDevicesRequestRequestTypeDef(TypedDict):
    arn: NotRequired[str]
    nextToken: NotRequired[str]
    filters: NotRequired[Sequence[DeviceFilterUnionTypeDef]]


class GetSuiteResultTypeDef(TypedDict):
    suite: SuiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListSuitesResultTypeDef(TypedDict):
    suites: list[SuiteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetTestResultTypeDef(TypedDict):
    test: TestTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTestsResultTypeDef(TypedDict):
    tests: list[TestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


OfferingTypeDef = TypedDict(
    "OfferingTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
        "type": NotRequired[Literal["RECURRING"]],
        "platform": NotRequired[DevicePlatformType],
        "recurringCharges": NotRequired[list[RecurringChargeTypeDef]],
    },
)


class CreateProjectResultTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetProjectResultTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListProjectsResultTypeDef(TypedDict):
    projects: list[ProjectTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateProjectResultTypeDef(TypedDict):
    project: ProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTestGridProjectResultTypeDef(TypedDict):
    testGridProject: TestGridProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTestGridProjectResultTypeDef(TypedDict):
    testGridProject: TestGridProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTestGridProjectsResultTypeDef(TypedDict):
    testGridProjects: list[TestGridProjectTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateTestGridProjectResultTypeDef(TypedDict):
    testGridProject: TestGridProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DevicePoolCompatibilityResultTypeDef(TypedDict):
    device: NotRequired[DeviceTypeDef]
    compatible: NotRequired[bool]
    incompatibilityMessages: NotRequired[list[IncompatibilityMessageTypeDef]]


class GetDeviceResultTypeDef(TypedDict):
    device: DeviceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "arn": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[TestTypeType],
        "created": NotRequired[datetime],
        "status": NotRequired[ExecutionStatusType],
        "result": NotRequired[ExecutionResultType],
        "started": NotRequired[datetime],
        "stopped": NotRequired[datetime],
        "counters": NotRequired[CountersTypeDef],
        "message": NotRequired[str],
        "device": NotRequired[DeviceTypeDef],
        "instanceArn": NotRequired[str],
        "deviceMinutes": NotRequired[DeviceMinutesTypeDef],
        "videoEndpoint": NotRequired[str],
        "videoCapture": NotRequired[bool],
    },
)


class ListDevicesResultTypeDef(TypedDict):
    devices: list[DeviceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ProblemTypeDef(TypedDict):
    run: NotRequired[ProblemDetailTypeDef]
    job: NotRequired[ProblemDetailTypeDef]
    suite: NotRequired[ProblemDetailTypeDef]
    test: NotRequired[ProblemDetailTypeDef]
    device: NotRequired[DeviceTypeDef]
    result: NotRequired[ExecutionResultType]
    message: NotRequired[str]


class RemoteAccessSessionTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    created: NotRequired[datetime]
    status: NotRequired[ExecutionStatusType]
    result: NotRequired[ExecutionResultType]
    message: NotRequired[str]
    started: NotRequired[datetime]
    stopped: NotRequired[datetime]
    device: NotRequired[DeviceTypeDef]
    instanceArn: NotRequired[str]
    remoteDebugEnabled: NotRequired[bool]
    remoteRecordEnabled: NotRequired[bool]
    remoteRecordAppArn: NotRequired[str]
    hostAddress: NotRequired[str]
    clientId: NotRequired[str]
    billingMethod: NotRequired[BillingMethodType]
    deviceMinutes: NotRequired[DeviceMinutesTypeDef]
    endpoint: NotRequired[str]
    deviceUdid: NotRequired[str]
    interactionMode: NotRequired[InteractionModeType]
    skipAppResign: NotRequired[bool]
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]


class GetDevicePoolCompatibilityRequestRequestTypeDef(TypedDict):
    devicePoolArn: str
    appArn: NotRequired[str]
    testType: NotRequired[TestTypeType]
    test: NotRequired[ScheduleRunTestTypeDef]
    configuration: NotRequired[ScheduleRunConfigurationTypeDef]


class GetRunResultTypeDef(TypedDict):
    run: RunTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListRunsResultTypeDef(TypedDict):
    runs: list[RunTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ScheduleRunResultTypeDef(TypedDict):
    run: RunTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopRunResultTypeDef(TypedDict):
    run: RunTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ScheduleRunRequestRequestTypeDef(TypedDict):
    projectArn: str
    test: ScheduleRunTestTypeDef
    appArn: NotRequired[str]
    devicePoolArn: NotRequired[str]
    deviceSelectionConfiguration: NotRequired[DeviceSelectionConfigurationTypeDef]
    name: NotRequired[str]
    configuration: NotRequired[ScheduleRunConfigurationTypeDef]
    executionConfiguration: NotRequired[ExecutionConfigurationTypeDef]


class ListOfferingsResultTypeDef(TypedDict):
    offerings: list[OfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


OfferingStatusTypeDef = TypedDict(
    "OfferingStatusTypeDef",
    {
        "type": NotRequired[OfferingTransactionTypeType],
        "offering": NotRequired[OfferingTypeDef],
        "quantity": NotRequired[int],
        "effectiveOn": NotRequired[datetime],
    },
)


class GetDevicePoolCompatibilityResultTypeDef(TypedDict):
    compatibleDevices: list[DevicePoolCompatibilityResultTypeDef]
    incompatibleDevices: list[DevicePoolCompatibilityResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetJobResultTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListJobsResultTypeDef(TypedDict):
    jobs: list[JobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StopJobResultTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UniqueProblemTypeDef(TypedDict):
    message: NotRequired[str]
    problems: NotRequired[list[ProblemTypeDef]]


class CreateRemoteAccessSessionResultTypeDef(TypedDict):
    remoteAccessSession: RemoteAccessSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetRemoteAccessSessionResultTypeDef(TypedDict):
    remoteAccessSession: RemoteAccessSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListRemoteAccessSessionsResultTypeDef(TypedDict):
    remoteAccessSessions: list[RemoteAccessSessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StopRemoteAccessSessionResultTypeDef(TypedDict):
    remoteAccessSession: RemoteAccessSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetOfferingStatusResultTypeDef(TypedDict):
    current: dict[str, OfferingStatusTypeDef]
    nextPeriod: dict[str, OfferingStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class OfferingTransactionTypeDef(TypedDict):
    offeringStatus: NotRequired[OfferingStatusTypeDef]
    transactionId: NotRequired[str]
    offeringPromotionId: NotRequired[str]
    createdOn: NotRequired[datetime]
    cost: NotRequired[MonetaryAmountTypeDef]


class ListUniqueProblemsResultTypeDef(TypedDict):
    uniqueProblems: dict[ExecutionResultType, list[UniqueProblemTypeDef]]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListOfferingTransactionsResultTypeDef(TypedDict):
    offeringTransactions: list[OfferingTransactionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PurchaseOfferingResultTypeDef(TypedDict):
    offeringTransaction: OfferingTransactionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RenewOfferingResultTypeDef(TypedDict):
    offeringTransaction: OfferingTransactionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
