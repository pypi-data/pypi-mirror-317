"""
Type annotations for arc-zonal-shift service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_arc_zonal_shift/type_defs/)

Usage::

    ```python
    from types_boto3_arc_zonal_shift.type_defs import AutoshiftInResourceTypeDef

    data: AutoshiftInResourceTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence

from .literals import (
    AppliedStatusType,
    AutoshiftAppliedStatusType,
    AutoshiftExecutionStatusType,
    AutoshiftObserverNotificationStatusType,
    PracticeRunOutcomeType,
    ZonalAutoshiftStatusType,
    ZonalShiftStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AutoshiftInResourceTypeDef",
    "AutoshiftSummaryTypeDef",
    "CancelZonalShiftRequestRequestTypeDef",
    "ControlConditionTypeDef",
    "CreatePracticeRunConfigurationRequestRequestTypeDef",
    "CreatePracticeRunConfigurationResponseTypeDef",
    "DeletePracticeRunConfigurationRequestRequestTypeDef",
    "DeletePracticeRunConfigurationResponseTypeDef",
    "GetAutoshiftObserverNotificationStatusResponseTypeDef",
    "GetManagedResourceRequestRequestTypeDef",
    "GetManagedResourceResponseTypeDef",
    "ListAutoshiftsRequestPaginateTypeDef",
    "ListAutoshiftsRequestRequestTypeDef",
    "ListAutoshiftsResponseTypeDef",
    "ListManagedResourcesRequestPaginateTypeDef",
    "ListManagedResourcesRequestRequestTypeDef",
    "ListManagedResourcesResponseTypeDef",
    "ListZonalShiftsRequestPaginateTypeDef",
    "ListZonalShiftsRequestRequestTypeDef",
    "ListZonalShiftsResponseTypeDef",
    "ManagedResourceSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PracticeRunConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "StartZonalShiftRequestRequestTypeDef",
    "UpdateAutoshiftObserverNotificationStatusRequestRequestTypeDef",
    "UpdateAutoshiftObserverNotificationStatusResponseTypeDef",
    "UpdatePracticeRunConfigurationRequestRequestTypeDef",
    "UpdatePracticeRunConfigurationResponseTypeDef",
    "UpdateZonalAutoshiftConfigurationRequestRequestTypeDef",
    "UpdateZonalAutoshiftConfigurationResponseTypeDef",
    "UpdateZonalShiftRequestRequestTypeDef",
    "ZonalShiftInResourceTypeDef",
    "ZonalShiftSummaryTypeDef",
    "ZonalShiftTypeDef",
)


class AutoshiftInResourceTypeDef(TypedDict):
    appliedStatus: AutoshiftAppliedStatusType
    awayFrom: str
    startTime: datetime


class AutoshiftSummaryTypeDef(TypedDict):
    awayFrom: str
    endTime: datetime
    startTime: datetime
    status: AutoshiftExecutionStatusType


class CancelZonalShiftRequestRequestTypeDef(TypedDict):
    zonalShiftId: str


ControlConditionTypeDef = TypedDict(
    "ControlConditionTypeDef",
    {
        "alarmIdentifier": str,
        "type": Literal["CLOUDWATCH"],
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeletePracticeRunConfigurationRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str


class GetManagedResourceRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str


class ZonalShiftInResourceTypeDef(TypedDict):
    appliedStatus: AppliedStatusType
    awayFrom: str
    comment: str
    expiryTime: datetime
    resourceIdentifier: str
    startTime: datetime
    zonalShiftId: str
    practiceRunOutcome: NotRequired[PracticeRunOutcomeType]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAutoshiftsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[AutoshiftExecutionStatusType]


class ListManagedResourcesRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListZonalShiftsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    resourceIdentifier: NotRequired[str]
    status: NotRequired[ZonalShiftStatusType]


class ZonalShiftSummaryTypeDef(TypedDict):
    awayFrom: str
    comment: str
    expiryTime: datetime
    resourceIdentifier: str
    startTime: datetime
    status: ZonalShiftStatusType
    zonalShiftId: str
    practiceRunOutcome: NotRequired[PracticeRunOutcomeType]


class StartZonalShiftRequestRequestTypeDef(TypedDict):
    awayFrom: str
    comment: str
    expiresIn: str
    resourceIdentifier: str


class UpdateAutoshiftObserverNotificationStatusRequestRequestTypeDef(TypedDict):
    status: AutoshiftObserverNotificationStatusType


class UpdateZonalAutoshiftConfigurationRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str
    zonalAutoshiftStatus: ZonalAutoshiftStatusType


class UpdateZonalShiftRequestRequestTypeDef(TypedDict):
    zonalShiftId: str
    comment: NotRequired[str]
    expiresIn: NotRequired[str]


class CreatePracticeRunConfigurationRequestRequestTypeDef(TypedDict):
    outcomeAlarms: Sequence[ControlConditionTypeDef]
    resourceIdentifier: str
    blockedDates: NotRequired[Sequence[str]]
    blockedWindows: NotRequired[Sequence[str]]
    blockingAlarms: NotRequired[Sequence[ControlConditionTypeDef]]


class PracticeRunConfigurationTypeDef(TypedDict):
    outcomeAlarms: list[ControlConditionTypeDef]
    blockedDates: NotRequired[list[str]]
    blockedWindows: NotRequired[list[str]]
    blockingAlarms: NotRequired[list[ControlConditionTypeDef]]


class UpdatePracticeRunConfigurationRequestRequestTypeDef(TypedDict):
    resourceIdentifier: str
    blockedDates: NotRequired[Sequence[str]]
    blockedWindows: NotRequired[Sequence[str]]
    blockingAlarms: NotRequired[Sequence[ControlConditionTypeDef]]
    outcomeAlarms: NotRequired[Sequence[ControlConditionTypeDef]]


class DeletePracticeRunConfigurationResponseTypeDef(TypedDict):
    arn: str
    name: str
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetAutoshiftObserverNotificationStatusResponseTypeDef(TypedDict):
    status: AutoshiftObserverNotificationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ListAutoshiftsResponseTypeDef(TypedDict):
    items: list[AutoshiftSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateAutoshiftObserverNotificationStatusResponseTypeDef(TypedDict):
    status: AutoshiftObserverNotificationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateZonalAutoshiftConfigurationResponseTypeDef(TypedDict):
    resourceIdentifier: str
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ZonalShiftTypeDef(TypedDict):
    awayFrom: str
    comment: str
    expiryTime: datetime
    resourceIdentifier: str
    startTime: datetime
    status: ZonalShiftStatusType
    zonalShiftId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ManagedResourceSummaryTypeDef(TypedDict):
    availabilityZones: list[str]
    appliedWeights: NotRequired[dict[str, float]]
    arn: NotRequired[str]
    autoshifts: NotRequired[list[AutoshiftInResourceTypeDef]]
    name: NotRequired[str]
    practiceRunStatus: NotRequired[ZonalAutoshiftStatusType]
    zonalAutoshiftStatus: NotRequired[ZonalAutoshiftStatusType]
    zonalShifts: NotRequired[list[ZonalShiftInResourceTypeDef]]


class ListAutoshiftsRequestPaginateTypeDef(TypedDict):
    status: NotRequired[AutoshiftExecutionStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedResourcesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListZonalShiftsRequestPaginateTypeDef(TypedDict):
    resourceIdentifier: NotRequired[str]
    status: NotRequired[ZonalShiftStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListZonalShiftsResponseTypeDef(TypedDict):
    items: list[ZonalShiftSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreatePracticeRunConfigurationResponseTypeDef(TypedDict):
    arn: str
    name: str
    practiceRunConfiguration: PracticeRunConfigurationTypeDef
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetManagedResourceResponseTypeDef(TypedDict):
    appliedWeights: dict[str, float]
    arn: str
    autoshifts: list[AutoshiftInResourceTypeDef]
    name: str
    practiceRunConfiguration: PracticeRunConfigurationTypeDef
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    zonalShifts: list[ZonalShiftInResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePracticeRunConfigurationResponseTypeDef(TypedDict):
    arn: str
    name: str
    practiceRunConfiguration: PracticeRunConfigurationTypeDef
    zonalAutoshiftStatus: ZonalAutoshiftStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ListManagedResourcesResponseTypeDef(TypedDict):
    items: list[ManagedResourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
