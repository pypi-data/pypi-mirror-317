"""
Type annotations for budgets service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_budgets/type_defs/)

Usage::

    ```python
    from types_boto3_budgets.type_defs import ActionThresholdTypeDef

    data: ActionThresholdTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    ActionStatusType,
    ActionSubTypeType,
    ActionTypeType,
    ApprovalModelType,
    AutoAdjustTypeType,
    BudgetTypeType,
    ComparisonOperatorType,
    EventTypeType,
    ExecutionTypeType,
    NotificationStateType,
    NotificationTypeType,
    SubscriptionTypeType,
    ThresholdTypeType,
    TimeUnitType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ActionHistoryDetailsTypeDef",
    "ActionHistoryTypeDef",
    "ActionThresholdTypeDef",
    "ActionTypeDef",
    "AutoAdjustDataOutputTypeDef",
    "AutoAdjustDataTypeDef",
    "AutoAdjustDataUnionTypeDef",
    "BudgetNotificationsForAccountTypeDef",
    "BudgetOutputTypeDef",
    "BudgetPerformanceHistoryTypeDef",
    "BudgetTypeDef",
    "BudgetedAndActualAmountsTypeDef",
    "CalculatedSpendTypeDef",
    "CostTypesTypeDef",
    "CreateBudgetActionRequestRequestTypeDef",
    "CreateBudgetActionResponseTypeDef",
    "CreateBudgetRequestRequestTypeDef",
    "CreateNotificationRequestRequestTypeDef",
    "CreateSubscriberRequestRequestTypeDef",
    "DefinitionOutputTypeDef",
    "DefinitionTypeDef",
    "DeleteBudgetActionRequestRequestTypeDef",
    "DeleteBudgetActionResponseTypeDef",
    "DeleteBudgetRequestRequestTypeDef",
    "DeleteNotificationRequestRequestTypeDef",
    "DeleteSubscriberRequestRequestTypeDef",
    "DescribeBudgetActionHistoriesRequestPaginateTypeDef",
    "DescribeBudgetActionHistoriesRequestRequestTypeDef",
    "DescribeBudgetActionHistoriesResponseTypeDef",
    "DescribeBudgetActionRequestRequestTypeDef",
    "DescribeBudgetActionResponseTypeDef",
    "DescribeBudgetActionsForAccountRequestPaginateTypeDef",
    "DescribeBudgetActionsForAccountRequestRequestTypeDef",
    "DescribeBudgetActionsForAccountResponseTypeDef",
    "DescribeBudgetActionsForBudgetRequestPaginateTypeDef",
    "DescribeBudgetActionsForBudgetRequestRequestTypeDef",
    "DescribeBudgetActionsForBudgetResponseTypeDef",
    "DescribeBudgetNotificationsForAccountRequestPaginateTypeDef",
    "DescribeBudgetNotificationsForAccountRequestRequestTypeDef",
    "DescribeBudgetNotificationsForAccountResponseTypeDef",
    "DescribeBudgetPerformanceHistoryRequestPaginateTypeDef",
    "DescribeBudgetPerformanceHistoryRequestRequestTypeDef",
    "DescribeBudgetPerformanceHistoryResponseTypeDef",
    "DescribeBudgetRequestRequestTypeDef",
    "DescribeBudgetResponseTypeDef",
    "DescribeBudgetsRequestPaginateTypeDef",
    "DescribeBudgetsRequestRequestTypeDef",
    "DescribeBudgetsResponseTypeDef",
    "DescribeNotificationsForBudgetRequestPaginateTypeDef",
    "DescribeNotificationsForBudgetRequestRequestTypeDef",
    "DescribeNotificationsForBudgetResponseTypeDef",
    "DescribeSubscribersForNotificationRequestPaginateTypeDef",
    "DescribeSubscribersForNotificationRequestRequestTypeDef",
    "DescribeSubscribersForNotificationResponseTypeDef",
    "ExecuteBudgetActionRequestRequestTypeDef",
    "ExecuteBudgetActionResponseTypeDef",
    "HistoricalOptionsTypeDef",
    "IamActionDefinitionOutputTypeDef",
    "IamActionDefinitionTypeDef",
    "IamActionDefinitionUnionTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NotificationTypeDef",
    "NotificationWithSubscribersTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "ScpActionDefinitionOutputTypeDef",
    "ScpActionDefinitionTypeDef",
    "ScpActionDefinitionUnionTypeDef",
    "SpendTypeDef",
    "SsmActionDefinitionOutputTypeDef",
    "SsmActionDefinitionTypeDef",
    "SsmActionDefinitionUnionTypeDef",
    "SubscriberTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimePeriodOutputTypeDef",
    "TimePeriodTypeDef",
    "TimePeriodUnionTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBudgetActionRequestRequestTypeDef",
    "UpdateBudgetActionResponseTypeDef",
    "UpdateBudgetRequestRequestTypeDef",
    "UpdateNotificationRequestRequestTypeDef",
    "UpdateSubscriberRequestRequestTypeDef",
)

class ActionThresholdTypeDef(TypedDict):
    ActionThresholdValue: float
    ActionThresholdType: ThresholdTypeType

class SubscriberTypeDef(TypedDict):
    SubscriptionType: SubscriptionTypeType
    Address: str

class HistoricalOptionsTypeDef(TypedDict):
    BudgetAdjustmentPeriod: int
    LookBackAvailablePeriods: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class NotificationTypeDef(TypedDict):
    NotificationType: NotificationTypeType
    ComparisonOperator: ComparisonOperatorType
    Threshold: float
    ThresholdType: NotRequired[ThresholdTypeType]
    NotificationState: NotRequired[NotificationStateType]

class CostTypesTypeDef(TypedDict):
    IncludeTax: NotRequired[bool]
    IncludeSubscription: NotRequired[bool]
    UseBlended: NotRequired[bool]
    IncludeRefund: NotRequired[bool]
    IncludeCredit: NotRequired[bool]
    IncludeUpfront: NotRequired[bool]
    IncludeRecurring: NotRequired[bool]
    IncludeOtherSubscription: NotRequired[bool]
    IncludeSupport: NotRequired[bool]
    IncludeDiscount: NotRequired[bool]
    UseAmortized: NotRequired[bool]

class SpendTypeDef(TypedDict):
    Amount: str
    Unit: str

class TimePeriodOutputTypeDef(TypedDict):
    Start: NotRequired[datetime]
    End: NotRequired[datetime]

class ResourceTagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class IamActionDefinitionOutputTypeDef(TypedDict):
    PolicyArn: str
    Roles: NotRequired[list[str]]
    Groups: NotRequired[list[str]]
    Users: NotRequired[list[str]]

class ScpActionDefinitionOutputTypeDef(TypedDict):
    PolicyId: str
    TargetIds: list[str]

class SsmActionDefinitionOutputTypeDef(TypedDict):
    ActionSubType: ActionSubTypeType
    Region: str
    InstanceIds: list[str]

class DeleteBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str

class DeleteBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str

class DescribeBudgetActionsForAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeBudgetActionsForBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeBudgetNotificationsForAccountRequestRequestTypeDef(TypedDict):
    AccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str

class DescribeBudgetsRequestRequestTypeDef(TypedDict):
    AccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeNotificationsForBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ExecuteBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    ExecutionType: ExecutionTypeType

class IamActionDefinitionTypeDef(TypedDict):
    PolicyArn: str
    Roles: NotRequired[Sequence[str]]
    Groups: NotRequired[Sequence[str]]
    Users: NotRequired[Sequence[str]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str

class ScpActionDefinitionTypeDef(TypedDict):
    PolicyId: str
    TargetIds: Sequence[str]

class SsmActionDefinitionTypeDef(TypedDict):
    ActionSubType: ActionSubTypeType
    Region: str
    InstanceIds: Sequence[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    ResourceTagKeys: Sequence[str]

class AutoAdjustDataOutputTypeDef(TypedDict):
    AutoAdjustType: AutoAdjustTypeType
    HistoricalOptions: NotRequired[HistoricalOptionsTypeDef]
    LastAutoAdjustTime: NotRequired[datetime]

class AutoAdjustDataTypeDef(TypedDict):
    AutoAdjustType: AutoAdjustTypeType
    HistoricalOptions: NotRequired[HistoricalOptionsTypeDef]
    LastAutoAdjustTime: NotRequired[TimestampTypeDef]

class TimePeriodTypeDef(TypedDict):
    Start: NotRequired[TimestampTypeDef]
    End: NotRequired[TimestampTypeDef]

class BudgetNotificationsForAccountTypeDef(TypedDict):
    Notifications: NotRequired[list[NotificationTypeDef]]
    BudgetName: NotRequired[str]

class CreateNotificationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    Subscribers: Sequence[SubscriberTypeDef]

class CreateSubscriberRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    Subscriber: SubscriberTypeDef

class DeleteNotificationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef

class DeleteSubscriberRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    Subscriber: SubscriberTypeDef

class DescribeSubscribersForNotificationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class NotificationWithSubscribersTypeDef(TypedDict):
    Notification: NotificationTypeDef
    Subscribers: Sequence[SubscriberTypeDef]

class UpdateNotificationRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    OldNotification: NotificationTypeDef
    NewNotification: NotificationTypeDef

class UpdateSubscriberRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    OldSubscriber: SubscriberTypeDef
    NewSubscriber: SubscriberTypeDef

class CalculatedSpendTypeDef(TypedDict):
    ActualSpend: SpendTypeDef
    ForecastedSpend: NotRequired[SpendTypeDef]

class BudgetedAndActualAmountsTypeDef(TypedDict):
    BudgetedAmount: NotRequired[SpendTypeDef]
    ActualAmount: NotRequired[SpendTypeDef]
    TimePeriod: NotRequired[TimePeriodOutputTypeDef]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    ResourceTags: Sequence[ResourceTagTypeDef]

class CreateBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNotificationsForBudgetResponseTypeDef(TypedDict):
    Notifications: list[NotificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeSubscribersForNotificationResponseTypeDef(TypedDict):
    Subscribers: list[SubscriberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ExecuteBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    ExecutionType: ExecutionTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceTags: list[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DefinitionOutputTypeDef(TypedDict):
    IamActionDefinition: NotRequired[IamActionDefinitionOutputTypeDef]
    ScpActionDefinition: NotRequired[ScpActionDefinitionOutputTypeDef]
    SsmActionDefinition: NotRequired[SsmActionDefinitionOutputTypeDef]

class DescribeBudgetActionsForAccountRequestPaginateTypeDef(TypedDict):
    AccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetActionsForBudgetRequestPaginateTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetNotificationsForAccountRequestPaginateTypeDef(TypedDict):
    AccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetsRequestPaginateTypeDef(TypedDict):
    AccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeNotificationsForBudgetRequestPaginateTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeSubscribersForNotificationRequestPaginateTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Notification: NotificationTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

IamActionDefinitionUnionTypeDef = Union[
    IamActionDefinitionTypeDef, IamActionDefinitionOutputTypeDef
]
ScpActionDefinitionUnionTypeDef = Union[
    ScpActionDefinitionTypeDef, ScpActionDefinitionOutputTypeDef
]
SsmActionDefinitionUnionTypeDef = Union[
    SsmActionDefinitionTypeDef, SsmActionDefinitionOutputTypeDef
]
AutoAdjustDataUnionTypeDef = Union[AutoAdjustDataTypeDef, AutoAdjustDataOutputTypeDef]

class DescribeBudgetActionHistoriesRequestPaginateTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    TimePeriod: NotRequired[TimePeriodTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetActionHistoriesRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    TimePeriod: NotRequired[TimePeriodTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeBudgetPerformanceHistoryRequestPaginateTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    TimePeriod: NotRequired[TimePeriodTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeBudgetPerformanceHistoryRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    TimePeriod: NotRequired[TimePeriodTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

TimePeriodUnionTypeDef = Union[TimePeriodTypeDef, TimePeriodOutputTypeDef]

class DescribeBudgetNotificationsForAccountResponseTypeDef(TypedDict):
    BudgetNotificationsForAccount: list[BudgetNotificationsForAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class BudgetOutputTypeDef(TypedDict):
    BudgetName: str
    TimeUnit: TimeUnitType
    BudgetType: BudgetTypeType
    BudgetLimit: NotRequired[SpendTypeDef]
    PlannedBudgetLimits: NotRequired[dict[str, SpendTypeDef]]
    CostFilters: NotRequired[dict[str, list[str]]]
    CostTypes: NotRequired[CostTypesTypeDef]
    TimePeriod: NotRequired[TimePeriodOutputTypeDef]
    CalculatedSpend: NotRequired[CalculatedSpendTypeDef]
    LastUpdatedTime: NotRequired[datetime]
    AutoAdjustData: NotRequired[AutoAdjustDataOutputTypeDef]

class BudgetPerformanceHistoryTypeDef(TypedDict):
    BudgetName: NotRequired[str]
    BudgetType: NotRequired[BudgetTypeType]
    CostFilters: NotRequired[dict[str, list[str]]]
    CostTypes: NotRequired[CostTypesTypeDef]
    TimeUnit: NotRequired[TimeUnitType]
    BudgetedAndActualAmountsList: NotRequired[list[BudgetedAndActualAmountsTypeDef]]

class ActionTypeDef(TypedDict):
    ActionId: str
    BudgetName: str
    NotificationType: NotificationTypeType
    ActionType: ActionTypeType
    ActionThreshold: ActionThresholdTypeDef
    Definition: DefinitionOutputTypeDef
    ExecutionRoleArn: str
    ApprovalModel: ApprovalModelType
    Status: ActionStatusType
    Subscribers: list[SubscriberTypeDef]

class DefinitionTypeDef(TypedDict):
    IamActionDefinition: NotRequired[IamActionDefinitionUnionTypeDef]
    ScpActionDefinition: NotRequired[ScpActionDefinitionUnionTypeDef]
    SsmActionDefinition: NotRequired[SsmActionDefinitionUnionTypeDef]

class BudgetTypeDef(TypedDict):
    BudgetName: str
    TimeUnit: TimeUnitType
    BudgetType: BudgetTypeType
    BudgetLimit: NotRequired[SpendTypeDef]
    PlannedBudgetLimits: NotRequired[Mapping[str, SpendTypeDef]]
    CostFilters: NotRequired[Mapping[str, Sequence[str]]]
    CostTypes: NotRequired[CostTypesTypeDef]
    TimePeriod: NotRequired[TimePeriodUnionTypeDef]
    CalculatedSpend: NotRequired[CalculatedSpendTypeDef]
    LastUpdatedTime: NotRequired[TimestampTypeDef]
    AutoAdjustData: NotRequired[AutoAdjustDataUnionTypeDef]

class DescribeBudgetResponseTypeDef(TypedDict):
    Budget: BudgetOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBudgetsResponseTypeDef(TypedDict):
    Budgets: list[BudgetOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeBudgetPerformanceHistoryResponseTypeDef(TypedDict):
    BudgetPerformanceHistory: BudgetPerformanceHistoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ActionHistoryDetailsTypeDef(TypedDict):
    Message: str
    Action: ActionTypeDef

class DeleteBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Action: ActionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    Action: ActionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBudgetActionsForAccountResponseTypeDef(TypedDict):
    Actions: list[ActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeBudgetActionsForBudgetResponseTypeDef(TypedDict):
    Actions: list[ActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateBudgetActionResponseTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    OldAction: ActionTypeDef
    NewAction: ActionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    NotificationType: NotificationTypeType
    ActionType: ActionTypeType
    ActionThreshold: ActionThresholdTypeDef
    Definition: DefinitionTypeDef
    ExecutionRoleArn: str
    ApprovalModel: ApprovalModelType
    Subscribers: Sequence[SubscriberTypeDef]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class UpdateBudgetActionRequestRequestTypeDef(TypedDict):
    AccountId: str
    BudgetName: str
    ActionId: str
    NotificationType: NotRequired[NotificationTypeType]
    ActionThreshold: NotRequired[ActionThresholdTypeDef]
    Definition: NotRequired[DefinitionTypeDef]
    ExecutionRoleArn: NotRequired[str]
    ApprovalModel: NotRequired[ApprovalModelType]
    Subscribers: NotRequired[Sequence[SubscriberTypeDef]]

class CreateBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    Budget: BudgetTypeDef
    NotificationsWithSubscribers: NotRequired[Sequence[NotificationWithSubscribersTypeDef]]
    ResourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class UpdateBudgetRequestRequestTypeDef(TypedDict):
    AccountId: str
    NewBudget: BudgetTypeDef

class ActionHistoryTypeDef(TypedDict):
    Timestamp: datetime
    Status: ActionStatusType
    EventType: EventTypeType
    ActionHistoryDetails: ActionHistoryDetailsTypeDef

class DescribeBudgetActionHistoriesResponseTypeDef(TypedDict):
    ActionHistories: list[ActionHistoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
