"""
Type annotations for outposts service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_outposts/type_defs/)

Usage::

    ```python
    from types_boto3_outposts.type_defs import AddressTypeDef

    data: AddressTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence

from .literals import (
    AddressTypeType,
    AssetStateType,
    AWSServiceNameType,
    CapacityTaskFailureTypeType,
    CapacityTaskStatusType,
    CatalogItemClassType,
    CatalogItemStatusType,
    ComputeAssetStateType,
    FiberOpticCableTypeType,
    LineItemStatusType,
    MaximumSupportedWeightLbsType,
    OpticalStandardType,
    OrderStatusType,
    OrderTypeType,
    PaymentOptionType,
    PaymentTermType,
    PowerConnectorType,
    PowerDrawKvaType,
    PowerFeedDropType,
    PowerPhaseType,
    ShipmentCarrierType,
    SupportedHardwareTypeType,
    SupportedStorageEnumType,
    TaskActionOnBlockingInstancesType,
    UplinkCountType,
    UplinkGbpsType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AddressTypeDef",
    "AssetInfoTypeDef",
    "AssetInstanceTypeCapacityTypeDef",
    "AssetInstanceTypeDef",
    "AssetLocationTypeDef",
    "BlockingInstanceTypeDef",
    "CancelCapacityTaskInputRequestTypeDef",
    "CancelOrderInputRequestTypeDef",
    "CapacityTaskFailureTypeDef",
    "CapacityTaskSummaryTypeDef",
    "CatalogItemTypeDef",
    "ComputeAttributesTypeDef",
    "ConnectionDetailsTypeDef",
    "CreateOrderInputRequestTypeDef",
    "CreateOrderOutputTypeDef",
    "CreateOutpostInputRequestTypeDef",
    "CreateOutpostOutputTypeDef",
    "CreateSiteInputRequestTypeDef",
    "CreateSiteOutputTypeDef",
    "DeleteOutpostInputRequestTypeDef",
    "DeleteSiteInputRequestTypeDef",
    "EC2CapacityTypeDef",
    "GetCapacityTaskInputRequestTypeDef",
    "GetCapacityTaskOutputTypeDef",
    "GetCatalogItemInputRequestTypeDef",
    "GetCatalogItemOutputTypeDef",
    "GetConnectionRequestRequestTypeDef",
    "GetConnectionResponseTypeDef",
    "GetOrderInputRequestTypeDef",
    "GetOrderOutputTypeDef",
    "GetOutpostInputRequestTypeDef",
    "GetOutpostInstanceTypesInputPaginateTypeDef",
    "GetOutpostInstanceTypesInputRequestTypeDef",
    "GetOutpostInstanceTypesOutputTypeDef",
    "GetOutpostOutputTypeDef",
    "GetOutpostSupportedInstanceTypesInputPaginateTypeDef",
    "GetOutpostSupportedInstanceTypesInputRequestTypeDef",
    "GetOutpostSupportedInstanceTypesOutputTypeDef",
    "GetSiteAddressInputRequestTypeDef",
    "GetSiteAddressOutputTypeDef",
    "GetSiteInputRequestTypeDef",
    "GetSiteOutputTypeDef",
    "InstanceTypeCapacityTypeDef",
    "InstanceTypeItemTypeDef",
    "InstancesToExcludeOutputTypeDef",
    "InstancesToExcludeTypeDef",
    "LineItemAssetInformationTypeDef",
    "LineItemRequestTypeDef",
    "LineItemTypeDef",
    "ListAssetInstancesInputPaginateTypeDef",
    "ListAssetInstancesInputRequestTypeDef",
    "ListAssetInstancesOutputTypeDef",
    "ListAssetsInputPaginateTypeDef",
    "ListAssetsInputRequestTypeDef",
    "ListAssetsOutputTypeDef",
    "ListBlockingInstancesForCapacityTaskInputPaginateTypeDef",
    "ListBlockingInstancesForCapacityTaskInputRequestTypeDef",
    "ListBlockingInstancesForCapacityTaskOutputTypeDef",
    "ListCapacityTasksInputPaginateTypeDef",
    "ListCapacityTasksInputRequestTypeDef",
    "ListCapacityTasksOutputTypeDef",
    "ListCatalogItemsInputPaginateTypeDef",
    "ListCatalogItemsInputRequestTypeDef",
    "ListCatalogItemsOutputTypeDef",
    "ListOrdersInputPaginateTypeDef",
    "ListOrdersInputRequestTypeDef",
    "ListOrdersOutputTypeDef",
    "ListOutpostsInputPaginateTypeDef",
    "ListOutpostsInputRequestTypeDef",
    "ListOutpostsOutputTypeDef",
    "ListSitesInputPaginateTypeDef",
    "ListSitesInputRequestTypeDef",
    "ListSitesOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OrderSummaryTypeDef",
    "OrderTypeDef",
    "OutpostTypeDef",
    "PaginatorConfigTypeDef",
    "RackPhysicalPropertiesTypeDef",
    "ResponseMetadataTypeDef",
    "ShipmentInformationTypeDef",
    "SiteTypeDef",
    "StartCapacityTaskInputRequestTypeDef",
    "StartCapacityTaskOutputTypeDef",
    "StartConnectionRequestRequestTypeDef",
    "StartConnectionResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateOutpostInputRequestTypeDef",
    "UpdateOutpostOutputTypeDef",
    "UpdateSiteAddressInputRequestTypeDef",
    "UpdateSiteAddressOutputTypeDef",
    "UpdateSiteInputRequestTypeDef",
    "UpdateSiteOutputTypeDef",
    "UpdateSiteRackPhysicalPropertiesInputRequestTypeDef",
    "UpdateSiteRackPhysicalPropertiesOutputTypeDef",
)

class AddressTypeDef(TypedDict):
    AddressLine1: str
    City: str
    StateOrRegion: str
    PostalCode: str
    CountryCode: str
    ContactName: NotRequired[str]
    ContactPhoneNumber: NotRequired[str]
    AddressLine2: NotRequired[str]
    AddressLine3: NotRequired[str]
    DistrictOrCounty: NotRequired[str]
    Municipality: NotRequired[str]

class AssetLocationTypeDef(TypedDict):
    RackElevation: NotRequired[float]

class AssetInstanceTypeCapacityTypeDef(TypedDict):
    InstanceType: str
    Count: int

class AssetInstanceTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    InstanceType: NotRequired[str]
    AssetId: NotRequired[str]
    AccountId: NotRequired[str]
    AwsServiceName: NotRequired[AWSServiceNameType]

class BlockingInstanceTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    AccountId: NotRequired[str]
    AwsServiceName: NotRequired[AWSServiceNameType]

class CancelCapacityTaskInputRequestTypeDef(TypedDict):
    CapacityTaskId: str
    OutpostIdentifier: str

class CancelOrderInputRequestTypeDef(TypedDict):
    OrderId: str

CapacityTaskFailureTypeDef = TypedDict(
    "CapacityTaskFailureTypeDef",
    {
        "Reason": str,
        "Type": NotRequired[CapacityTaskFailureTypeType],
    },
)

class CapacityTaskSummaryTypeDef(TypedDict):
    CapacityTaskId: NotRequired[str]
    OutpostId: NotRequired[str]
    OrderId: NotRequired[str]
    CapacityTaskStatus: NotRequired[CapacityTaskStatusType]
    CreationDate: NotRequired[datetime]
    CompletionDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]

class EC2CapacityTypeDef(TypedDict):
    Family: NotRequired[str]
    MaxSize: NotRequired[str]
    Quantity: NotRequired[str]

class ConnectionDetailsTypeDef(TypedDict):
    ClientPublicKey: NotRequired[str]
    ServerPublicKey: NotRequired[str]
    ServerEndpoint: NotRequired[str]
    ClientTunnelAddress: NotRequired[str]
    ServerTunnelAddress: NotRequired[str]
    AllowedIps: NotRequired[list[str]]

class LineItemRequestTypeDef(TypedDict):
    CatalogItemId: NotRequired[str]
    Quantity: NotRequired[int]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateOutpostInputRequestTypeDef(TypedDict):
    Name: str
    SiteId: str
    Description: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    SupportedHardwareType: NotRequired[SupportedHardwareTypeType]

class OutpostTypeDef(TypedDict):
    OutpostId: NotRequired[str]
    OwnerId: NotRequired[str]
    OutpostArn: NotRequired[str]
    SiteId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    LifeCycleStatus: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    Tags: NotRequired[dict[str, str]]
    SiteArn: NotRequired[str]
    SupportedHardwareType: NotRequired[SupportedHardwareTypeType]

class RackPhysicalPropertiesTypeDef(TypedDict):
    PowerDrawKva: NotRequired[PowerDrawKvaType]
    PowerPhase: NotRequired[PowerPhaseType]
    PowerConnector: NotRequired[PowerConnectorType]
    PowerFeedDrop: NotRequired[PowerFeedDropType]
    UplinkGbps: NotRequired[UplinkGbpsType]
    UplinkCount: NotRequired[UplinkCountType]
    FiberOpticCableType: NotRequired[FiberOpticCableTypeType]
    OpticalStandard: NotRequired[OpticalStandardType]
    MaximumSupportedWeightLbs: NotRequired[MaximumSupportedWeightLbsType]

class DeleteOutpostInputRequestTypeDef(TypedDict):
    OutpostId: str

class DeleteSiteInputRequestTypeDef(TypedDict):
    SiteId: str

class GetCapacityTaskInputRequestTypeDef(TypedDict):
    CapacityTaskId: str
    OutpostIdentifier: str

class InstanceTypeCapacityTypeDef(TypedDict):
    InstanceType: str
    Count: int

class InstancesToExcludeOutputTypeDef(TypedDict):
    Instances: NotRequired[list[str]]
    AccountIds: NotRequired[list[str]]
    Services: NotRequired[list[AWSServiceNameType]]

class GetCatalogItemInputRequestTypeDef(TypedDict):
    CatalogItemId: str

class GetConnectionRequestRequestTypeDef(TypedDict):
    ConnectionId: str

class GetOrderInputRequestTypeDef(TypedDict):
    OrderId: str

class GetOutpostInputRequestTypeDef(TypedDict):
    OutpostId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetOutpostInstanceTypesInputRequestTypeDef(TypedDict):
    OutpostId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class InstanceTypeItemTypeDef(TypedDict):
    InstanceType: NotRequired[str]
    VCPUs: NotRequired[int]

class GetOutpostSupportedInstanceTypesInputRequestTypeDef(TypedDict):
    OutpostIdentifier: str
    OrderId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetSiteAddressInputRequestTypeDef(TypedDict):
    SiteId: str
    AddressType: AddressTypeType

class GetSiteInputRequestTypeDef(TypedDict):
    SiteId: str

class InstancesToExcludeTypeDef(TypedDict):
    Instances: NotRequired[Sequence[str]]
    AccountIds: NotRequired[Sequence[str]]
    Services: NotRequired[Sequence[AWSServiceNameType]]

class LineItemAssetInformationTypeDef(TypedDict):
    AssetId: NotRequired[str]
    MacAddressList: NotRequired[list[str]]

class ShipmentInformationTypeDef(TypedDict):
    ShipmentTrackingNumber: NotRequired[str]
    ShipmentCarrier: NotRequired[ShipmentCarrierType]

class ListAssetInstancesInputRequestTypeDef(TypedDict):
    OutpostIdentifier: str
    AssetIdFilter: NotRequired[Sequence[str]]
    InstanceTypeFilter: NotRequired[Sequence[str]]
    AccountIdFilter: NotRequired[Sequence[str]]
    AwsServiceFilter: NotRequired[Sequence[AWSServiceNameType]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAssetsInputRequestTypeDef(TypedDict):
    OutpostIdentifier: str
    HostIdFilter: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    StatusFilter: NotRequired[Sequence[AssetStateType]]

class ListBlockingInstancesForCapacityTaskInputRequestTypeDef(TypedDict):
    OutpostIdentifier: str
    CapacityTaskId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCapacityTasksInputRequestTypeDef(TypedDict):
    OutpostIdentifierFilter: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    CapacityTaskStatusFilter: NotRequired[Sequence[CapacityTaskStatusType]]

class ListCatalogItemsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ItemClassFilter: NotRequired[Sequence[CatalogItemClassType]]
    SupportedStorageFilter: NotRequired[Sequence[SupportedStorageEnumType]]
    EC2FamilyFilter: NotRequired[Sequence[str]]

class ListOrdersInputRequestTypeDef(TypedDict):
    OutpostIdentifierFilter: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class OrderSummaryTypeDef(TypedDict):
    OutpostId: NotRequired[str]
    OrderId: NotRequired[str]
    OrderType: NotRequired[OrderTypeType]
    Status: NotRequired[OrderStatusType]
    LineItemCountsByStatus: NotRequired[dict[LineItemStatusType, int]]
    OrderSubmissionDate: NotRequired[datetime]
    OrderFulfilledDate: NotRequired[datetime]

class ListOutpostsInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    LifeCycleStatusFilter: NotRequired[Sequence[str]]
    AvailabilityZoneFilter: NotRequired[Sequence[str]]
    AvailabilityZoneIdFilter: NotRequired[Sequence[str]]

class ListSitesInputRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    OperatingAddressCountryCodeFilter: NotRequired[Sequence[str]]
    OperatingAddressStateOrRegionFilter: NotRequired[Sequence[str]]
    OperatingAddressCityFilter: NotRequired[Sequence[str]]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class StartConnectionRequestRequestTypeDef(TypedDict):
    AssetId: str
    ClientPublicKey: str
    NetworkInterfaceDeviceIndex: int
    DeviceSerialNumber: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateOutpostInputRequestTypeDef(TypedDict):
    OutpostId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    SupportedHardwareType: NotRequired[SupportedHardwareTypeType]

class UpdateSiteInputRequestTypeDef(TypedDict):
    SiteId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    Notes: NotRequired[str]

class UpdateSiteRackPhysicalPropertiesInputRequestTypeDef(TypedDict):
    SiteId: str
    PowerDrawKva: NotRequired[PowerDrawKvaType]
    PowerPhase: NotRequired[PowerPhaseType]
    PowerConnector: NotRequired[PowerConnectorType]
    PowerFeedDrop: NotRequired[PowerFeedDropType]
    UplinkGbps: NotRequired[UplinkGbpsType]
    UplinkCount: NotRequired[UplinkCountType]
    FiberOpticCableType: NotRequired[FiberOpticCableTypeType]
    OpticalStandard: NotRequired[OpticalStandardType]
    MaximumSupportedWeightLbs: NotRequired[MaximumSupportedWeightLbsType]

class UpdateSiteAddressInputRequestTypeDef(TypedDict):
    SiteId: str
    AddressType: AddressTypeType
    Address: AddressTypeDef

class ComputeAttributesTypeDef(TypedDict):
    HostId: NotRequired[str]
    State: NotRequired[ComputeAssetStateType]
    InstanceFamilies: NotRequired[list[str]]
    InstanceTypeCapacities: NotRequired[list[AssetInstanceTypeCapacityTypeDef]]
    MaxVcpus: NotRequired[int]

class CatalogItemTypeDef(TypedDict):
    CatalogItemId: NotRequired[str]
    ItemStatus: NotRequired[CatalogItemStatusType]
    EC2Capacities: NotRequired[list[EC2CapacityTypeDef]]
    PowerKva: NotRequired[float]
    WeightLbs: NotRequired[int]
    SupportedUplinkGbps: NotRequired[list[int]]
    SupportedStorage: NotRequired[list[SupportedStorageEnumType]]

class CreateOrderInputRequestTypeDef(TypedDict):
    OutpostIdentifier: str
    LineItems: Sequence[LineItemRequestTypeDef]
    PaymentOption: PaymentOptionType
    PaymentTerm: NotRequired[PaymentTermType]

class GetConnectionResponseTypeDef(TypedDict):
    ConnectionId: str
    ConnectionDetails: ConnectionDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSiteAddressOutputTypeDef(TypedDict):
    SiteId: str
    AddressType: AddressTypeType
    Address: AddressTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssetInstancesOutputTypeDef(TypedDict):
    AssetInstances: list[AssetInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListBlockingInstancesForCapacityTaskOutputTypeDef(TypedDict):
    BlockingInstances: list[BlockingInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCapacityTasksOutputTypeDef(TypedDict):
    CapacityTasks: list[CapacityTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartConnectionResponseTypeDef(TypedDict):
    ConnectionId: str
    UnderlayIpAddress: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSiteAddressOutputTypeDef(TypedDict):
    AddressType: AddressTypeType
    Address: AddressTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOutpostOutputTypeDef(TypedDict):
    Outpost: OutpostTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetOutpostOutputTypeDef(TypedDict):
    Outpost: OutpostTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListOutpostsOutputTypeDef(TypedDict):
    Outposts: list[OutpostTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateOutpostOutputTypeDef(TypedDict):
    Outpost: OutpostTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSiteInputRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    Notes: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    OperatingAddress: NotRequired[AddressTypeDef]
    ShippingAddress: NotRequired[AddressTypeDef]
    RackPhysicalProperties: NotRequired[RackPhysicalPropertiesTypeDef]

class SiteTypeDef(TypedDict):
    SiteId: NotRequired[str]
    AccountId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[dict[str, str]]
    SiteArn: NotRequired[str]
    Notes: NotRequired[str]
    OperatingAddressCountryCode: NotRequired[str]
    OperatingAddressStateOrRegion: NotRequired[str]
    OperatingAddressCity: NotRequired[str]
    RackPhysicalProperties: NotRequired[RackPhysicalPropertiesTypeDef]

class GetCapacityTaskOutputTypeDef(TypedDict):
    CapacityTaskId: str
    OutpostId: str
    OrderId: str
    RequestedInstancePools: list[InstanceTypeCapacityTypeDef]
    InstancesToExclude: InstancesToExcludeOutputTypeDef
    DryRun: bool
    CapacityTaskStatus: CapacityTaskStatusType
    Failed: CapacityTaskFailureTypeDef
    CreationDate: datetime
    CompletionDate: datetime
    LastModifiedDate: datetime
    TaskActionOnBlockingInstances: TaskActionOnBlockingInstancesType
    ResponseMetadata: ResponseMetadataTypeDef

class StartCapacityTaskOutputTypeDef(TypedDict):
    CapacityTaskId: str
    OutpostId: str
    OrderId: str
    RequestedInstancePools: list[InstanceTypeCapacityTypeDef]
    InstancesToExclude: InstancesToExcludeOutputTypeDef
    DryRun: bool
    CapacityTaskStatus: CapacityTaskStatusType
    Failed: CapacityTaskFailureTypeDef
    CreationDate: datetime
    CompletionDate: datetime
    LastModifiedDate: datetime
    TaskActionOnBlockingInstances: TaskActionOnBlockingInstancesType
    ResponseMetadata: ResponseMetadataTypeDef

class GetOutpostInstanceTypesInputPaginateTypeDef(TypedDict):
    OutpostId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetOutpostSupportedInstanceTypesInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    OrderId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssetInstancesInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    AssetIdFilter: NotRequired[Sequence[str]]
    InstanceTypeFilter: NotRequired[Sequence[str]]
    AccountIdFilter: NotRequired[Sequence[str]]
    AwsServiceFilter: NotRequired[Sequence[AWSServiceNameType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssetsInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    HostIdFilter: NotRequired[Sequence[str]]
    StatusFilter: NotRequired[Sequence[AssetStateType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBlockingInstancesForCapacityTaskInputPaginateTypeDef(TypedDict):
    OutpostIdentifier: str
    CapacityTaskId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCapacityTasksInputPaginateTypeDef(TypedDict):
    OutpostIdentifierFilter: NotRequired[str]
    CapacityTaskStatusFilter: NotRequired[Sequence[CapacityTaskStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCatalogItemsInputPaginateTypeDef(TypedDict):
    ItemClassFilter: NotRequired[Sequence[CatalogItemClassType]]
    SupportedStorageFilter: NotRequired[Sequence[SupportedStorageEnumType]]
    EC2FamilyFilter: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrdersInputPaginateTypeDef(TypedDict):
    OutpostIdentifierFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOutpostsInputPaginateTypeDef(TypedDict):
    LifeCycleStatusFilter: NotRequired[Sequence[str]]
    AvailabilityZoneFilter: NotRequired[Sequence[str]]
    AvailabilityZoneIdFilter: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSitesInputPaginateTypeDef(TypedDict):
    OperatingAddressCountryCodeFilter: NotRequired[Sequence[str]]
    OperatingAddressStateOrRegionFilter: NotRequired[Sequence[str]]
    OperatingAddressCityFilter: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetOutpostInstanceTypesOutputTypeDef(TypedDict):
    InstanceTypes: list[InstanceTypeItemTypeDef]
    OutpostId: str
    OutpostArn: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetOutpostSupportedInstanceTypesOutputTypeDef(TypedDict):
    InstanceTypes: list[InstanceTypeItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class StartCapacityTaskInputRequestTypeDef(TypedDict):
    OutpostIdentifier: str
    InstancePools: Sequence[InstanceTypeCapacityTypeDef]
    OrderId: NotRequired[str]
    InstancesToExclude: NotRequired[InstancesToExcludeTypeDef]
    DryRun: NotRequired[bool]
    TaskActionOnBlockingInstances: NotRequired[TaskActionOnBlockingInstancesType]

class LineItemTypeDef(TypedDict):
    CatalogItemId: NotRequired[str]
    LineItemId: NotRequired[str]
    Quantity: NotRequired[int]
    Status: NotRequired[LineItemStatusType]
    ShipmentInformation: NotRequired[ShipmentInformationTypeDef]
    AssetInformationList: NotRequired[list[LineItemAssetInformationTypeDef]]
    PreviousLineItemId: NotRequired[str]
    PreviousOrderId: NotRequired[str]

class ListOrdersOutputTypeDef(TypedDict):
    Orders: list[OrderSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class AssetInfoTypeDef(TypedDict):
    AssetId: NotRequired[str]
    RackId: NotRequired[str]
    AssetType: NotRequired[Literal["COMPUTE"]]
    ComputeAttributes: NotRequired[ComputeAttributesTypeDef]
    AssetLocation: NotRequired[AssetLocationTypeDef]

class GetCatalogItemOutputTypeDef(TypedDict):
    CatalogItem: CatalogItemTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCatalogItemsOutputTypeDef(TypedDict):
    CatalogItems: list[CatalogItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateSiteOutputTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetSiteOutputTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListSitesOutputTypeDef(TypedDict):
    Sites: list[SiteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateSiteOutputTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSiteRackPhysicalPropertiesOutputTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class OrderTypeDef(TypedDict):
    OutpostId: NotRequired[str]
    OrderId: NotRequired[str]
    Status: NotRequired[OrderStatusType]
    LineItems: NotRequired[list[LineItemTypeDef]]
    PaymentOption: NotRequired[PaymentOptionType]
    OrderSubmissionDate: NotRequired[datetime]
    OrderFulfilledDate: NotRequired[datetime]
    PaymentTerm: NotRequired[PaymentTermType]
    OrderType: NotRequired[OrderTypeType]

class ListAssetsOutputTypeDef(TypedDict):
    Assets: list[AssetInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateOrderOutputTypeDef(TypedDict):
    Order: OrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetOrderOutputTypeDef(TypedDict):
    Order: OrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
