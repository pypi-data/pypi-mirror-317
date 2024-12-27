"""
Type annotations for privatenetworks service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_privatenetworks/type_defs/)

Usage::

    ```python
    from types_boto3_privatenetworks.type_defs import AcknowledgeOrderReceiptRequestRequestTypeDef

    data: AcknowledgeOrderReceiptRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    AcknowledgmentStatusType,
    CommitmentLengthType,
    DeviceIdentifierFilterKeysType,
    DeviceIdentifierStatusType,
    ElevationReferenceType,
    HealthStatusType,
    NetworkResourceDefinitionTypeType,
    NetworkResourceFilterKeysType,
    NetworkResourceStatusType,
    NetworkSiteStatusType,
    NetworkStatusType,
    OrderFilterKeysType,
    UpdateTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcknowledgeOrderReceiptRequestRequestTypeDef",
    "AcknowledgeOrderReceiptResponseTypeDef",
    "ActivateDeviceIdentifierRequestRequestTypeDef",
    "ActivateDeviceIdentifierResponseTypeDef",
    "ActivateNetworkSiteRequestRequestTypeDef",
    "ActivateNetworkSiteResponseTypeDef",
    "AddressTypeDef",
    "CommitmentConfigurationTypeDef",
    "CommitmentInformationTypeDef",
    "ConfigureAccessPointRequestRequestTypeDef",
    "ConfigureAccessPointResponseTypeDef",
    "CreateNetworkRequestRequestTypeDef",
    "CreateNetworkResponseTypeDef",
    "CreateNetworkSiteRequestRequestTypeDef",
    "CreateNetworkSiteResponseTypeDef",
    "DeactivateDeviceIdentifierRequestRequestTypeDef",
    "DeactivateDeviceIdentifierResponseTypeDef",
    "DeleteNetworkRequestRequestTypeDef",
    "DeleteNetworkResponseTypeDef",
    "DeleteNetworkSiteRequestRequestTypeDef",
    "DeleteNetworkSiteResponseTypeDef",
    "DeviceIdentifierTypeDef",
    "GetDeviceIdentifierRequestRequestTypeDef",
    "GetDeviceIdentifierResponseTypeDef",
    "GetNetworkRequestRequestTypeDef",
    "GetNetworkResourceRequestRequestTypeDef",
    "GetNetworkResourceResponseTypeDef",
    "GetNetworkResponseTypeDef",
    "GetNetworkSiteRequestRequestTypeDef",
    "GetNetworkSiteResponseTypeDef",
    "GetOrderRequestRequestTypeDef",
    "GetOrderResponseTypeDef",
    "ListDeviceIdentifiersRequestPaginateTypeDef",
    "ListDeviceIdentifiersRequestRequestTypeDef",
    "ListDeviceIdentifiersResponseTypeDef",
    "ListNetworkResourcesRequestPaginateTypeDef",
    "ListNetworkResourcesRequestRequestTypeDef",
    "ListNetworkResourcesResponseTypeDef",
    "ListNetworkSitesRequestPaginateTypeDef",
    "ListNetworkSitesRequestRequestTypeDef",
    "ListNetworkSitesResponseTypeDef",
    "ListNetworksRequestPaginateTypeDef",
    "ListNetworksRequestRequestTypeDef",
    "ListNetworksResponseTypeDef",
    "ListOrdersRequestPaginateTypeDef",
    "ListOrdersRequestRequestTypeDef",
    "ListOrdersResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NameValuePairTypeDef",
    "NetworkResourceDefinitionOutputTypeDef",
    "NetworkResourceDefinitionTypeDef",
    "NetworkResourceDefinitionUnionTypeDef",
    "NetworkResourceTypeDef",
    "NetworkSiteTypeDef",
    "NetworkTypeDef",
    "OrderTypeDef",
    "OrderedResourceDefinitionTypeDef",
    "PaginatorConfigTypeDef",
    "PingResponseTypeDef",
    "PositionTypeDef",
    "ResponseMetadataTypeDef",
    "ReturnInformationTypeDef",
    "SitePlanOutputTypeDef",
    "SitePlanTypeDef",
    "StartNetworkResourceUpdateRequestRequestTypeDef",
    "StartNetworkResourceUpdateResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TrackingInformationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateNetworkSitePlanRequestRequestTypeDef",
    "UpdateNetworkSiteRequestRequestTypeDef",
    "UpdateNetworkSiteResponseTypeDef",
)

class AcknowledgeOrderReceiptRequestRequestTypeDef(TypedDict):
    orderArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ActivateDeviceIdentifierRequestRequestTypeDef(TypedDict):
    deviceIdentifierArn: str
    clientToken: NotRequired[str]

class DeviceIdentifierTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    deviceIdentifierArn: NotRequired[str]
    iccid: NotRequired[str]
    imsi: NotRequired[str]
    networkArn: NotRequired[str]
    orderArn: NotRequired[str]
    status: NotRequired[DeviceIdentifierStatusType]
    trafficGroupArn: NotRequired[str]
    vendor: NotRequired[str]

class AddressTypeDef(TypedDict):
    city: str
    country: str
    name: str
    postalCode: str
    stateOrProvince: str
    street1: str
    company: NotRequired[str]
    emailAddress: NotRequired[str]
    phoneNumber: NotRequired[str]
    street2: NotRequired[str]
    street3: NotRequired[str]

class CommitmentConfigurationTypeDef(TypedDict):
    automaticRenewal: bool
    commitmentLength: CommitmentLengthType

class PositionTypeDef(TypedDict):
    elevation: NotRequired[float]
    elevationReference: NotRequired[ElevationReferenceType]
    elevationUnit: NotRequired[Literal["FEET"]]
    latitude: NotRequired[float]
    longitude: NotRequired[float]

class CreateNetworkRequestRequestTypeDef(TypedDict):
    networkName: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class NetworkTypeDef(TypedDict):
    networkArn: str
    networkName: str
    status: NetworkStatusType
    createdAt: NotRequired[datetime]
    description: NotRequired[str]
    statusReason: NotRequired[str]

class DeactivateDeviceIdentifierRequestRequestTypeDef(TypedDict):
    deviceIdentifierArn: str
    clientToken: NotRequired[str]

class DeleteNetworkRequestRequestTypeDef(TypedDict):
    networkArn: str
    clientToken: NotRequired[str]

class DeleteNetworkSiteRequestRequestTypeDef(TypedDict):
    networkSiteArn: str
    clientToken: NotRequired[str]

class GetDeviceIdentifierRequestRequestTypeDef(TypedDict):
    deviceIdentifierArn: str

class GetNetworkRequestRequestTypeDef(TypedDict):
    networkArn: str

class GetNetworkResourceRequestRequestTypeDef(TypedDict):
    networkResourceArn: str

class GetNetworkSiteRequestRequestTypeDef(TypedDict):
    networkSiteArn: str

class GetOrderRequestRequestTypeDef(TypedDict):
    orderArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDeviceIdentifiersRequestRequestTypeDef(TypedDict):
    networkArn: str
    filters: NotRequired[Mapping[DeviceIdentifierFilterKeysType, Sequence[str]]]
    maxResults: NotRequired[int]
    startToken: NotRequired[str]

class ListNetworkResourcesRequestRequestTypeDef(TypedDict):
    networkArn: str
    filters: NotRequired[Mapping[NetworkResourceFilterKeysType, Sequence[str]]]
    maxResults: NotRequired[int]
    startToken: NotRequired[str]

class ListNetworkSitesRequestRequestTypeDef(TypedDict):
    networkArn: str
    filters: NotRequired[Mapping[Literal["STATUS"], Sequence[str]]]
    maxResults: NotRequired[int]
    startToken: NotRequired[str]

class ListNetworksRequestRequestTypeDef(TypedDict):
    filters: NotRequired[Mapping[Literal["STATUS"], Sequence[str]]]
    maxResults: NotRequired[int]
    startToken: NotRequired[str]

class ListOrdersRequestRequestTypeDef(TypedDict):
    networkArn: str
    filters: NotRequired[Mapping[OrderFilterKeysType, Sequence[str]]]
    maxResults: NotRequired[int]
    startToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class NameValuePairTypeDef(TypedDict):
    name: str
    value: NotRequired[str]

class TrackingInformationTypeDef(TypedDict):
    trackingNumber: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateNetworkSiteRequestRequestTypeDef(TypedDict):
    networkSiteArn: str
    clientToken: NotRequired[str]
    description: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PingResponseTypeDef(TypedDict):
    status: str
    ResponseMetadata: ResponseMetadataTypeDef

class ActivateDeviceIdentifierResponseTypeDef(TypedDict):
    deviceIdentifier: DeviceIdentifierTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeactivateDeviceIdentifierResponseTypeDef(TypedDict):
    deviceIdentifier: DeviceIdentifierTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeviceIdentifierResponseTypeDef(TypedDict):
    deviceIdentifier: DeviceIdentifierTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListDeviceIdentifiersResponseTypeDef(TypedDict):
    deviceIdentifiers: list[DeviceIdentifierTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ReturnInformationTypeDef(TypedDict):
    replacementOrderArn: NotRequired[str]
    returnReason: NotRequired[str]
    shippingAddress: NotRequired[AddressTypeDef]
    shippingLabel: NotRequired[str]

class ActivateNetworkSiteRequestRequestTypeDef(TypedDict):
    networkSiteArn: str
    shippingAddress: AddressTypeDef
    clientToken: NotRequired[str]
    commitmentConfiguration: NotRequired[CommitmentConfigurationTypeDef]

class CommitmentInformationTypeDef(TypedDict):
    commitmentConfiguration: CommitmentConfigurationTypeDef
    expiresOn: NotRequired[datetime]
    startAt: NotRequired[datetime]

OrderedResourceDefinitionTypeDef = TypedDict(
    "OrderedResourceDefinitionTypeDef",
    {
        "count": int,
        "type": NetworkResourceDefinitionTypeType,
        "commitmentConfiguration": NotRequired[CommitmentConfigurationTypeDef],
    },
)

class StartNetworkResourceUpdateRequestRequestTypeDef(TypedDict):
    networkResourceArn: str
    updateType: UpdateTypeType
    commitmentConfiguration: NotRequired[CommitmentConfigurationTypeDef]
    returnReason: NotRequired[str]
    shippingAddress: NotRequired[AddressTypeDef]

class ConfigureAccessPointRequestRequestTypeDef(TypedDict):
    accessPointArn: str
    cpiSecretKey: NotRequired[str]
    cpiUserId: NotRequired[str]
    cpiUserPassword: NotRequired[str]
    cpiUsername: NotRequired[str]
    position: NotRequired[PositionTypeDef]

class CreateNetworkResponseTypeDef(TypedDict):
    network: NetworkTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNetworkResponseTypeDef(TypedDict):
    network: NetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetNetworkResponseTypeDef(TypedDict):
    network: NetworkTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListNetworksResponseTypeDef(TypedDict):
    networks: list[NetworkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDeviceIdentifiersRequestPaginateTypeDef(TypedDict):
    networkArn: str
    filters: NotRequired[Mapping[DeviceIdentifierFilterKeysType, Sequence[str]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworkResourcesRequestPaginateTypeDef(TypedDict):
    networkArn: str
    filters: NotRequired[Mapping[NetworkResourceFilterKeysType, Sequence[str]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworkSitesRequestPaginateTypeDef(TypedDict):
    networkArn: str
    filters: NotRequired[Mapping[Literal["STATUS"], Sequence[str]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworksRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[Mapping[Literal["STATUS"], Sequence[str]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOrdersRequestPaginateTypeDef(TypedDict):
    networkArn: str
    filters: NotRequired[Mapping[OrderFilterKeysType, Sequence[str]]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

NetworkResourceDefinitionOutputTypeDef = TypedDict(
    "NetworkResourceDefinitionOutputTypeDef",
    {
        "count": int,
        "type": NetworkResourceDefinitionTypeType,
        "options": NotRequired[list[NameValuePairTypeDef]],
    },
)
NetworkResourceDefinitionTypeDef = TypedDict(
    "NetworkResourceDefinitionTypeDef",
    {
        "count": int,
        "type": NetworkResourceDefinitionTypeType,
        "options": NotRequired[Sequence[NameValuePairTypeDef]],
    },
)
NetworkResourceTypeDef = TypedDict(
    "NetworkResourceTypeDef",
    {
        "attributes": NotRequired[list[NameValuePairTypeDef]],
        "commitmentInformation": NotRequired[CommitmentInformationTypeDef],
        "createdAt": NotRequired[datetime],
        "description": NotRequired[str],
        "health": NotRequired[HealthStatusType],
        "model": NotRequired[str],
        "networkArn": NotRequired[str],
        "networkResourceArn": NotRequired[str],
        "networkSiteArn": NotRequired[str],
        "orderArn": NotRequired[str],
        "position": NotRequired[PositionTypeDef],
        "returnInformation": NotRequired[ReturnInformationTypeDef],
        "serialNumber": NotRequired[str],
        "status": NotRequired[NetworkResourceStatusType],
        "statusReason": NotRequired[str],
        "type": NotRequired[Literal["RADIO_UNIT"]],
        "vendor": NotRequired[str],
    },
)

class OrderTypeDef(TypedDict):
    acknowledgmentStatus: NotRequired[AcknowledgmentStatusType]
    createdAt: NotRequired[datetime]
    networkArn: NotRequired[str]
    networkSiteArn: NotRequired[str]
    orderArn: NotRequired[str]
    orderedResources: NotRequired[list[OrderedResourceDefinitionTypeDef]]
    shippingAddress: NotRequired[AddressTypeDef]
    trackingInformation: NotRequired[list[TrackingInformationTypeDef]]

class SitePlanOutputTypeDef(TypedDict):
    options: NotRequired[list[NameValuePairTypeDef]]
    resourceDefinitions: NotRequired[list[NetworkResourceDefinitionOutputTypeDef]]

NetworkResourceDefinitionUnionTypeDef = Union[
    NetworkResourceDefinitionTypeDef, NetworkResourceDefinitionOutputTypeDef
]

class ConfigureAccessPointResponseTypeDef(TypedDict):
    accessPoint: NetworkResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetNetworkResourceResponseTypeDef(TypedDict):
    networkResource: NetworkResourceTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListNetworkResourcesResponseTypeDef(TypedDict):
    networkResources: list[NetworkResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class StartNetworkResourceUpdateResponseTypeDef(TypedDict):
    networkResource: NetworkResourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AcknowledgeOrderReceiptResponseTypeDef(TypedDict):
    order: OrderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetOrderResponseTypeDef(TypedDict):
    order: OrderTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListOrdersResponseTypeDef(TypedDict):
    orders: list[OrderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class NetworkSiteTypeDef(TypedDict):
    networkArn: str
    networkSiteArn: str
    networkSiteName: str
    status: NetworkSiteStatusType
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    createdAt: NotRequired[datetime]
    currentPlan: NotRequired[SitePlanOutputTypeDef]
    description: NotRequired[str]
    pendingPlan: NotRequired[SitePlanOutputTypeDef]
    statusReason: NotRequired[str]

class SitePlanTypeDef(TypedDict):
    options: NotRequired[Sequence[NameValuePairTypeDef]]
    resourceDefinitions: NotRequired[Sequence[NetworkResourceDefinitionUnionTypeDef]]

class ActivateNetworkSiteResponseTypeDef(TypedDict):
    networkSite: NetworkSiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNetworkSiteResponseTypeDef(TypedDict):
    networkSite: NetworkSiteTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNetworkSiteResponseTypeDef(TypedDict):
    networkSite: NetworkSiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetNetworkSiteResponseTypeDef(TypedDict):
    networkSite: NetworkSiteTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListNetworkSitesResponseTypeDef(TypedDict):
    networkSites: list[NetworkSiteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateNetworkSiteResponseTypeDef(TypedDict):
    networkSite: NetworkSiteTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateNetworkSiteRequestRequestTypeDef(TypedDict):
    networkArn: str
    networkSiteName: str
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    pendingPlan: NotRequired[SitePlanTypeDef]
    tags: NotRequired[Mapping[str, str]]

class UpdateNetworkSitePlanRequestRequestTypeDef(TypedDict):
    networkSiteArn: str
    pendingPlan: SitePlanTypeDef
    clientToken: NotRequired[str]
