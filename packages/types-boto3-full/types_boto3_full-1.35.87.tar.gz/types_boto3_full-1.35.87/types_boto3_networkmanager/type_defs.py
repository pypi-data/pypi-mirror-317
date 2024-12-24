"""
Type annotations for networkmanager service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_networkmanager/type_defs/)

Usage::

    ```python
    from types_boto3_networkmanager.type_defs import AWSLocationTypeDef

    data: AWSLocationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence

from .literals import (
    AttachmentErrorCodeType,
    AttachmentStateType,
    AttachmentTypeType,
    ChangeActionType,
    ChangeSetStateType,
    ChangeStatusType,
    ChangeTypeType,
    ConnectionStateType,
    ConnectionStatusType,
    ConnectionTypeType,
    ConnectPeerAssociationStateType,
    ConnectPeerErrorCodeType,
    ConnectPeerStateType,
    CoreNetworkPolicyAliasType,
    CoreNetworkStateType,
    CustomerGatewayAssociationStateType,
    DeviceStateType,
    GlobalNetworkStateType,
    LinkAssociationStateType,
    LinkStateType,
    PeeringErrorCodeType,
    PeeringStateType,
    RouteAnalysisCompletionReasonCodeType,
    RouteAnalysisCompletionResultCodeType,
    RouteAnalysisStatusType,
    RouteStateType,
    RouteTableTypeType,
    RouteTypeType,
    SegmentActionServiceInsertionType,
    SendViaModeType,
    SiteStateType,
    TransitGatewayConnectPeerAssociationStateType,
    TransitGatewayRegistrationStateType,
    TunnelProtocolType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AWSLocationTypeDef",
    "AcceptAttachmentRequestRequestTypeDef",
    "AcceptAttachmentResponseTypeDef",
    "AccountStatusTypeDef",
    "AssociateConnectPeerRequestRequestTypeDef",
    "AssociateConnectPeerResponseTypeDef",
    "AssociateCustomerGatewayRequestRequestTypeDef",
    "AssociateCustomerGatewayResponseTypeDef",
    "AssociateLinkRequestRequestTypeDef",
    "AssociateLinkResponseTypeDef",
    "AssociateTransitGatewayConnectPeerRequestRequestTypeDef",
    "AssociateTransitGatewayConnectPeerResponseTypeDef",
    "AttachmentErrorTypeDef",
    "AttachmentTypeDef",
    "BandwidthTypeDef",
    "BgpOptionsTypeDef",
    "ConnectAttachmentOptionsTypeDef",
    "ConnectAttachmentTypeDef",
    "ConnectPeerAssociationTypeDef",
    "ConnectPeerBgpConfigurationTypeDef",
    "ConnectPeerConfigurationTypeDef",
    "ConnectPeerErrorTypeDef",
    "ConnectPeerSummaryTypeDef",
    "ConnectPeerTypeDef",
    "ConnectionHealthTypeDef",
    "ConnectionTypeDef",
    "CoreNetworkChangeEventTypeDef",
    "CoreNetworkChangeEventValuesTypeDef",
    "CoreNetworkChangeTypeDef",
    "CoreNetworkChangeValuesTypeDef",
    "CoreNetworkEdgeTypeDef",
    "CoreNetworkNetworkFunctionGroupIdentifierTypeDef",
    "CoreNetworkNetworkFunctionGroupTypeDef",
    "CoreNetworkPolicyErrorTypeDef",
    "CoreNetworkPolicyTypeDef",
    "CoreNetworkPolicyVersionTypeDef",
    "CoreNetworkSegmentEdgeIdentifierTypeDef",
    "CoreNetworkSegmentTypeDef",
    "CoreNetworkSummaryTypeDef",
    "CoreNetworkTypeDef",
    "CreateConnectAttachmentRequestRequestTypeDef",
    "CreateConnectAttachmentResponseTypeDef",
    "CreateConnectPeerRequestRequestTypeDef",
    "CreateConnectPeerResponseTypeDef",
    "CreateConnectionRequestRequestTypeDef",
    "CreateConnectionResponseTypeDef",
    "CreateCoreNetworkRequestRequestTypeDef",
    "CreateCoreNetworkResponseTypeDef",
    "CreateDeviceRequestRequestTypeDef",
    "CreateDeviceResponseTypeDef",
    "CreateDirectConnectGatewayAttachmentRequestRequestTypeDef",
    "CreateDirectConnectGatewayAttachmentResponseTypeDef",
    "CreateGlobalNetworkRequestRequestTypeDef",
    "CreateGlobalNetworkResponseTypeDef",
    "CreateLinkRequestRequestTypeDef",
    "CreateLinkResponseTypeDef",
    "CreateSiteRequestRequestTypeDef",
    "CreateSiteResponseTypeDef",
    "CreateSiteToSiteVpnAttachmentRequestRequestTypeDef",
    "CreateSiteToSiteVpnAttachmentResponseTypeDef",
    "CreateTransitGatewayPeeringRequestRequestTypeDef",
    "CreateTransitGatewayPeeringResponseTypeDef",
    "CreateTransitGatewayRouteTableAttachmentRequestRequestTypeDef",
    "CreateTransitGatewayRouteTableAttachmentResponseTypeDef",
    "CreateVpcAttachmentRequestRequestTypeDef",
    "CreateVpcAttachmentResponseTypeDef",
    "CustomerGatewayAssociationTypeDef",
    "DeleteAttachmentRequestRequestTypeDef",
    "DeleteAttachmentResponseTypeDef",
    "DeleteConnectPeerRequestRequestTypeDef",
    "DeleteConnectPeerResponseTypeDef",
    "DeleteConnectionRequestRequestTypeDef",
    "DeleteConnectionResponseTypeDef",
    "DeleteCoreNetworkPolicyVersionRequestRequestTypeDef",
    "DeleteCoreNetworkPolicyVersionResponseTypeDef",
    "DeleteCoreNetworkRequestRequestTypeDef",
    "DeleteCoreNetworkResponseTypeDef",
    "DeleteDeviceRequestRequestTypeDef",
    "DeleteDeviceResponseTypeDef",
    "DeleteGlobalNetworkRequestRequestTypeDef",
    "DeleteGlobalNetworkResponseTypeDef",
    "DeleteLinkRequestRequestTypeDef",
    "DeleteLinkResponseTypeDef",
    "DeletePeeringRequestRequestTypeDef",
    "DeletePeeringResponseTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteSiteRequestRequestTypeDef",
    "DeleteSiteResponseTypeDef",
    "DeregisterTransitGatewayRequestRequestTypeDef",
    "DeregisterTransitGatewayResponseTypeDef",
    "DescribeGlobalNetworksRequestPaginateTypeDef",
    "DescribeGlobalNetworksRequestRequestTypeDef",
    "DescribeGlobalNetworksResponseTypeDef",
    "DeviceTypeDef",
    "DirectConnectGatewayAttachmentTypeDef",
    "DisassociateConnectPeerRequestRequestTypeDef",
    "DisassociateConnectPeerResponseTypeDef",
    "DisassociateCustomerGatewayRequestRequestTypeDef",
    "DisassociateCustomerGatewayResponseTypeDef",
    "DisassociateLinkRequestRequestTypeDef",
    "DisassociateLinkResponseTypeDef",
    "DisassociateTransitGatewayConnectPeerRequestRequestTypeDef",
    "DisassociateTransitGatewayConnectPeerResponseTypeDef",
    "EdgeOverrideTypeDef",
    "ExecuteCoreNetworkChangeSetRequestRequestTypeDef",
    "GetConnectAttachmentRequestRequestTypeDef",
    "GetConnectAttachmentResponseTypeDef",
    "GetConnectPeerAssociationsRequestPaginateTypeDef",
    "GetConnectPeerAssociationsRequestRequestTypeDef",
    "GetConnectPeerAssociationsResponseTypeDef",
    "GetConnectPeerRequestRequestTypeDef",
    "GetConnectPeerResponseTypeDef",
    "GetConnectionsRequestPaginateTypeDef",
    "GetConnectionsRequestRequestTypeDef",
    "GetConnectionsResponseTypeDef",
    "GetCoreNetworkChangeEventsRequestPaginateTypeDef",
    "GetCoreNetworkChangeEventsRequestRequestTypeDef",
    "GetCoreNetworkChangeEventsResponseTypeDef",
    "GetCoreNetworkChangeSetRequestPaginateTypeDef",
    "GetCoreNetworkChangeSetRequestRequestTypeDef",
    "GetCoreNetworkChangeSetResponseTypeDef",
    "GetCoreNetworkPolicyRequestRequestTypeDef",
    "GetCoreNetworkPolicyResponseTypeDef",
    "GetCoreNetworkRequestRequestTypeDef",
    "GetCoreNetworkResponseTypeDef",
    "GetCustomerGatewayAssociationsRequestPaginateTypeDef",
    "GetCustomerGatewayAssociationsRequestRequestTypeDef",
    "GetCustomerGatewayAssociationsResponseTypeDef",
    "GetDevicesRequestPaginateTypeDef",
    "GetDevicesRequestRequestTypeDef",
    "GetDevicesResponseTypeDef",
    "GetDirectConnectGatewayAttachmentRequestRequestTypeDef",
    "GetDirectConnectGatewayAttachmentResponseTypeDef",
    "GetLinkAssociationsRequestPaginateTypeDef",
    "GetLinkAssociationsRequestRequestTypeDef",
    "GetLinkAssociationsResponseTypeDef",
    "GetLinksRequestPaginateTypeDef",
    "GetLinksRequestRequestTypeDef",
    "GetLinksResponseTypeDef",
    "GetNetworkResourceCountsRequestPaginateTypeDef",
    "GetNetworkResourceCountsRequestRequestTypeDef",
    "GetNetworkResourceCountsResponseTypeDef",
    "GetNetworkResourceRelationshipsRequestPaginateTypeDef",
    "GetNetworkResourceRelationshipsRequestRequestTypeDef",
    "GetNetworkResourceRelationshipsResponseTypeDef",
    "GetNetworkResourcesRequestPaginateTypeDef",
    "GetNetworkResourcesRequestRequestTypeDef",
    "GetNetworkResourcesResponseTypeDef",
    "GetNetworkRoutesRequestRequestTypeDef",
    "GetNetworkRoutesResponseTypeDef",
    "GetNetworkTelemetryRequestPaginateTypeDef",
    "GetNetworkTelemetryRequestRequestTypeDef",
    "GetNetworkTelemetryResponseTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetRouteAnalysisRequestRequestTypeDef",
    "GetRouteAnalysisResponseTypeDef",
    "GetSiteToSiteVpnAttachmentRequestRequestTypeDef",
    "GetSiteToSiteVpnAttachmentResponseTypeDef",
    "GetSitesRequestPaginateTypeDef",
    "GetSitesRequestRequestTypeDef",
    "GetSitesResponseTypeDef",
    "GetTransitGatewayConnectPeerAssociationsRequestPaginateTypeDef",
    "GetTransitGatewayConnectPeerAssociationsRequestRequestTypeDef",
    "GetTransitGatewayConnectPeerAssociationsResponseTypeDef",
    "GetTransitGatewayPeeringRequestRequestTypeDef",
    "GetTransitGatewayPeeringResponseTypeDef",
    "GetTransitGatewayRegistrationsRequestPaginateTypeDef",
    "GetTransitGatewayRegistrationsRequestRequestTypeDef",
    "GetTransitGatewayRegistrationsResponseTypeDef",
    "GetTransitGatewayRouteTableAttachmentRequestRequestTypeDef",
    "GetTransitGatewayRouteTableAttachmentResponseTypeDef",
    "GetVpcAttachmentRequestRequestTypeDef",
    "GetVpcAttachmentResponseTypeDef",
    "GlobalNetworkTypeDef",
    "LinkAssociationTypeDef",
    "LinkTypeDef",
    "ListAttachmentsRequestPaginateTypeDef",
    "ListAttachmentsRequestRequestTypeDef",
    "ListAttachmentsResponseTypeDef",
    "ListConnectPeersRequestPaginateTypeDef",
    "ListConnectPeersRequestRequestTypeDef",
    "ListConnectPeersResponseTypeDef",
    "ListCoreNetworkPolicyVersionsRequestPaginateTypeDef",
    "ListCoreNetworkPolicyVersionsRequestRequestTypeDef",
    "ListCoreNetworkPolicyVersionsResponseTypeDef",
    "ListCoreNetworksRequestPaginateTypeDef",
    "ListCoreNetworksRequestRequestTypeDef",
    "ListCoreNetworksResponseTypeDef",
    "ListOrganizationServiceAccessStatusRequestRequestTypeDef",
    "ListOrganizationServiceAccessStatusResponseTypeDef",
    "ListPeeringsRequestPaginateTypeDef",
    "ListPeeringsRequestRequestTypeDef",
    "ListPeeringsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LocationTypeDef",
    "NetworkFunctionGroupTypeDef",
    "NetworkResourceCountTypeDef",
    "NetworkResourceSummaryTypeDef",
    "NetworkResourceTypeDef",
    "NetworkRouteDestinationTypeDef",
    "NetworkRouteTypeDef",
    "NetworkTelemetryTypeDef",
    "OrganizationStatusTypeDef",
    "PaginatorConfigTypeDef",
    "PathComponentTypeDef",
    "PeeringErrorTypeDef",
    "PeeringTypeDef",
    "PermissionsErrorContextTypeDef",
    "ProposedNetworkFunctionGroupChangeTypeDef",
    "ProposedSegmentChangeTypeDef",
    "PutCoreNetworkPolicyRequestRequestTypeDef",
    "PutCoreNetworkPolicyResponseTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "RegisterTransitGatewayRequestRequestTypeDef",
    "RegisterTransitGatewayResponseTypeDef",
    "RejectAttachmentRequestRequestTypeDef",
    "RejectAttachmentResponseTypeDef",
    "RelationshipTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreCoreNetworkPolicyVersionRequestRequestTypeDef",
    "RestoreCoreNetworkPolicyVersionResponseTypeDef",
    "RouteAnalysisCompletionTypeDef",
    "RouteAnalysisEndpointOptionsSpecificationTypeDef",
    "RouteAnalysisEndpointOptionsTypeDef",
    "RouteAnalysisPathTypeDef",
    "RouteAnalysisTypeDef",
    "RouteTableIdentifierTypeDef",
    "ServiceInsertionActionTypeDef",
    "ServiceInsertionSegmentsTypeDef",
    "SiteToSiteVpnAttachmentTypeDef",
    "SiteTypeDef",
    "StartOrganizationServiceAccessUpdateRequestRequestTypeDef",
    "StartOrganizationServiceAccessUpdateResponseTypeDef",
    "StartRouteAnalysisRequestRequestTypeDef",
    "StartRouteAnalysisResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TransitGatewayConnectPeerAssociationTypeDef",
    "TransitGatewayPeeringTypeDef",
    "TransitGatewayRegistrationStateReasonTypeDef",
    "TransitGatewayRegistrationTypeDef",
    "TransitGatewayRouteTableAttachmentTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConnectionRequestRequestTypeDef",
    "UpdateConnectionResponseTypeDef",
    "UpdateCoreNetworkRequestRequestTypeDef",
    "UpdateCoreNetworkResponseTypeDef",
    "UpdateDeviceRequestRequestTypeDef",
    "UpdateDeviceResponseTypeDef",
    "UpdateDirectConnectGatewayAttachmentRequestRequestTypeDef",
    "UpdateDirectConnectGatewayAttachmentResponseTypeDef",
    "UpdateGlobalNetworkRequestRequestTypeDef",
    "UpdateGlobalNetworkResponseTypeDef",
    "UpdateLinkRequestRequestTypeDef",
    "UpdateLinkResponseTypeDef",
    "UpdateNetworkResourceMetadataRequestRequestTypeDef",
    "UpdateNetworkResourceMetadataResponseTypeDef",
    "UpdateSiteRequestRequestTypeDef",
    "UpdateSiteResponseTypeDef",
    "UpdateVpcAttachmentRequestRequestTypeDef",
    "UpdateVpcAttachmentResponseTypeDef",
    "ViaTypeDef",
    "VpcAttachmentTypeDef",
    "VpcOptionsTypeDef",
    "WhenSentToTypeDef",
)


class AWSLocationTypeDef(TypedDict):
    Zone: NotRequired[str]
    SubnetArn: NotRequired[str]


class AcceptAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AccountStatusTypeDef(TypedDict):
    AccountId: NotRequired[str]
    SLRDeploymentStatus: NotRequired[str]


class AssociateConnectPeerRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    ConnectPeerId: str
    DeviceId: str
    LinkId: NotRequired[str]


class ConnectPeerAssociationTypeDef(TypedDict):
    ConnectPeerId: NotRequired[str]
    GlobalNetworkId: NotRequired[str]
    DeviceId: NotRequired[str]
    LinkId: NotRequired[str]
    State: NotRequired[ConnectPeerAssociationStateType]


class AssociateCustomerGatewayRequestRequestTypeDef(TypedDict):
    CustomerGatewayArn: str
    GlobalNetworkId: str
    DeviceId: str
    LinkId: NotRequired[str]


class CustomerGatewayAssociationTypeDef(TypedDict):
    CustomerGatewayArn: NotRequired[str]
    GlobalNetworkId: NotRequired[str]
    DeviceId: NotRequired[str]
    LinkId: NotRequired[str]
    State: NotRequired[CustomerGatewayAssociationStateType]


class AssociateLinkRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    DeviceId: str
    LinkId: str


class LinkAssociationTypeDef(TypedDict):
    GlobalNetworkId: NotRequired[str]
    DeviceId: NotRequired[str]
    LinkId: NotRequired[str]
    LinkAssociationState: NotRequired[LinkAssociationStateType]


class AssociateTransitGatewayConnectPeerRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    TransitGatewayConnectPeerArn: str
    DeviceId: str
    LinkId: NotRequired[str]


class TransitGatewayConnectPeerAssociationTypeDef(TypedDict):
    TransitGatewayConnectPeerArn: NotRequired[str]
    GlobalNetworkId: NotRequired[str]
    DeviceId: NotRequired[str]
    LinkId: NotRequired[str]
    State: NotRequired[TransitGatewayConnectPeerAssociationStateType]


class AttachmentErrorTypeDef(TypedDict):
    Code: NotRequired[AttachmentErrorCodeType]
    Message: NotRequired[str]
    ResourceArn: NotRequired[str]
    RequestId: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class BandwidthTypeDef(TypedDict):
    UploadSpeed: NotRequired[int]
    DownloadSpeed: NotRequired[int]


class BgpOptionsTypeDef(TypedDict):
    PeerAsn: NotRequired[int]


ConnectAttachmentOptionsTypeDef = TypedDict(
    "ConnectAttachmentOptionsTypeDef",
    {
        "Protocol": NotRequired[TunnelProtocolType],
    },
)


class ConnectPeerBgpConfigurationTypeDef(TypedDict):
    CoreNetworkAsn: NotRequired[int]
    PeerAsn: NotRequired[int]
    CoreNetworkAddress: NotRequired[str]
    PeerAddress: NotRequired[str]


class ConnectPeerErrorTypeDef(TypedDict):
    Code: NotRequired[ConnectPeerErrorCodeType]
    Message: NotRequired[str]
    ResourceArn: NotRequired[str]
    RequestId: NotRequired[str]


ConnectionHealthTypeDef = TypedDict(
    "ConnectionHealthTypeDef",
    {
        "Type": NotRequired[ConnectionTypeType],
        "Status": NotRequired[ConnectionStatusType],
        "Timestamp": NotRequired[datetime],
    },
)


class CoreNetworkChangeEventValuesTypeDef(TypedDict):
    EdgeLocation: NotRequired[str]
    SegmentName: NotRequired[str]
    NetworkFunctionGroupName: NotRequired[str]
    AttachmentId: NotRequired[str]
    Cidr: NotRequired[str]


class CoreNetworkEdgeTypeDef(TypedDict):
    EdgeLocation: NotRequired[str]
    Asn: NotRequired[int]
    InsideCidrBlocks: NotRequired[list[str]]


class CoreNetworkNetworkFunctionGroupIdentifierTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    NetworkFunctionGroupName: NotRequired[str]
    EdgeLocation: NotRequired[str]


class ServiceInsertionSegmentsTypeDef(TypedDict):
    SendVia: NotRequired[list[str]]
    SendTo: NotRequired[list[str]]


class CoreNetworkPolicyErrorTypeDef(TypedDict):
    ErrorCode: str
    Message: str
    Path: NotRequired[str]


class CoreNetworkPolicyVersionTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    PolicyVersionId: NotRequired[int]
    Alias: NotRequired[CoreNetworkPolicyAliasType]
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    ChangeSetState: NotRequired[ChangeSetStateType]


class CoreNetworkSegmentEdgeIdentifierTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    SegmentName: NotRequired[str]
    EdgeLocation: NotRequired[str]


class CoreNetworkSegmentTypeDef(TypedDict):
    Name: NotRequired[str]
    EdgeLocations: NotRequired[list[str]]
    SharedSegments: NotRequired[list[str]]


class LocationTypeDef(TypedDict):
    Address: NotRequired[str]
    Latitude: NotRequired[str]
    Longitude: NotRequired[str]


class VpcOptionsTypeDef(TypedDict):
    Ipv6Support: NotRequired[bool]
    ApplianceModeSupport: NotRequired[bool]


class DeleteAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str


class DeleteConnectPeerRequestRequestTypeDef(TypedDict):
    ConnectPeerId: str


class DeleteConnectionRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    ConnectionId: str


class DeleteCoreNetworkPolicyVersionRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyVersionId: int


class DeleteCoreNetworkRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str


class DeleteDeviceRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    DeviceId: str


class DeleteGlobalNetworkRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str


class DeleteLinkRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    LinkId: str


class DeletePeeringRequestRequestTypeDef(TypedDict):
    PeeringId: str


class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class DeleteSiteRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    SiteId: str


class DeregisterTransitGatewayRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    TransitGatewayArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeGlobalNetworksRequestRequestTypeDef(TypedDict):
    GlobalNetworkIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DisassociateConnectPeerRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    ConnectPeerId: str


class DisassociateCustomerGatewayRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    CustomerGatewayArn: str


class DisassociateLinkRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    DeviceId: str
    LinkId: str


class DisassociateTransitGatewayConnectPeerRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    TransitGatewayConnectPeerArn: str


class EdgeOverrideTypeDef(TypedDict):
    EdgeSets: NotRequired[list[list[str]]]
    UseEdge: NotRequired[str]


class ExecuteCoreNetworkChangeSetRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyVersionId: int


class GetConnectAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str


class GetConnectPeerAssociationsRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    ConnectPeerIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetConnectPeerRequestRequestTypeDef(TypedDict):
    ConnectPeerId: str


class GetConnectionsRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    ConnectionIds: NotRequired[Sequence[str]]
    DeviceId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetCoreNetworkChangeEventsRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyVersionId: int
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetCoreNetworkChangeSetRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyVersionId: int
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetCoreNetworkPolicyRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyVersionId: NotRequired[int]
    Alias: NotRequired[CoreNetworkPolicyAliasType]


class GetCoreNetworkRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str


class GetCustomerGatewayAssociationsRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    CustomerGatewayArns: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetDevicesRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    DeviceIds: NotRequired[Sequence[str]]
    SiteId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetDirectConnectGatewayAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str


class GetLinkAssociationsRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    DeviceId: NotRequired[str]
    LinkId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


GetLinksRequestRequestTypeDef = TypedDict(
    "GetLinksRequestRequestTypeDef",
    {
        "GlobalNetworkId": str,
        "LinkIds": NotRequired[Sequence[str]],
        "SiteId": NotRequired[str],
        "Type": NotRequired[str],
        "Provider": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)


class GetNetworkResourceCountsRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    ResourceType: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class NetworkResourceCountTypeDef(TypedDict):
    ResourceType: NotRequired[str]
    Count: NotRequired[int]


class GetNetworkResourceRelationshipsRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    CoreNetworkId: NotRequired[str]
    RegisteredGatewayArn: NotRequired[str]
    AwsRegion: NotRequired[str]
    AccountId: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class RelationshipTypeDef(TypedDict):
    From: NotRequired[str]
    To: NotRequired[str]


class GetNetworkResourcesRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    CoreNetworkId: NotRequired[str]
    RegisteredGatewayArn: NotRequired[str]
    AwsRegion: NotRequired[str]
    AccountId: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetNetworkTelemetryRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    CoreNetworkId: NotRequired[str]
    RegisteredGatewayArn: NotRequired[str]
    AwsRegion: NotRequired[str]
    AccountId: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class GetRouteAnalysisRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    RouteAnalysisId: str


class GetSiteToSiteVpnAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str


class GetSitesRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    SiteIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetTransitGatewayConnectPeerAssociationsRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    TransitGatewayConnectPeerArns: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetTransitGatewayPeeringRequestRequestTypeDef(TypedDict):
    PeeringId: str


class GetTransitGatewayRegistrationsRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    TransitGatewayArns: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetTransitGatewayRouteTableAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str


class GetVpcAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str


class ListAttachmentsRequestRequestTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    AttachmentType: NotRequired[AttachmentTypeType]
    EdgeLocation: NotRequired[str]
    State: NotRequired[AttachmentStateType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListConnectPeersRequestRequestTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    ConnectAttachmentId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListCoreNetworkPolicyVersionsRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListCoreNetworksRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListOrganizationServiceAccessStatusRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListPeeringsRequestRequestTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    PeeringType: NotRequired[Literal["TRANSIT_GATEWAY"]]
    EdgeLocation: NotRequired[str]
    State: NotRequired[PeeringStateType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class NetworkFunctionGroupTypeDef(TypedDict):
    Name: NotRequired[str]


class NetworkResourceSummaryTypeDef(TypedDict):
    RegisteredGatewayArn: NotRequired[str]
    ResourceArn: NotRequired[str]
    ResourceType: NotRequired[str]
    Definition: NotRequired[str]
    NameTag: NotRequired[str]
    IsMiddlebox: NotRequired[bool]


class NetworkRouteDestinationTypeDef(TypedDict):
    CoreNetworkAttachmentId: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]
    SegmentName: NotRequired[str]
    NetworkFunctionGroupName: NotRequired[str]
    EdgeLocation: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceId: NotRequired[str]


class PermissionsErrorContextTypeDef(TypedDict):
    MissingPermission: NotRequired[str]


class PutCoreNetworkPolicyRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyDocument: str
    Description: NotRequired[str]
    LatestVersionId: NotRequired[int]
    ClientToken: NotRequired[str]


class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    PolicyDocument: str
    ResourceArn: str


class RegisterTransitGatewayRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    TransitGatewayArn: str


class RejectAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str


class RestoreCoreNetworkPolicyVersionRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyVersionId: int


class RouteAnalysisCompletionTypeDef(TypedDict):
    ResultCode: NotRequired[RouteAnalysisCompletionResultCodeType]
    ReasonCode: NotRequired[RouteAnalysisCompletionReasonCodeType]
    ReasonContext: NotRequired[dict[str, str]]


class RouteAnalysisEndpointOptionsSpecificationTypeDef(TypedDict):
    TransitGatewayAttachmentArn: NotRequired[str]
    IpAddress: NotRequired[str]


class RouteAnalysisEndpointOptionsTypeDef(TypedDict):
    TransitGatewayAttachmentArn: NotRequired[str]
    TransitGatewayArn: NotRequired[str]
    IpAddress: NotRequired[str]


class WhenSentToTypeDef(TypedDict):
    WhenSentToSegmentsList: NotRequired[list[str]]


class StartOrganizationServiceAccessUpdateRequestRequestTypeDef(TypedDict):
    Action: str


class TransitGatewayRegistrationStateReasonTypeDef(TypedDict):
    Code: NotRequired[TransitGatewayRegistrationStateType]
    Message: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateConnectionRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    ConnectionId: str
    LinkId: NotRequired[str]
    ConnectedLinkId: NotRequired[str]
    Description: NotRequired[str]


class UpdateCoreNetworkRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    Description: NotRequired[str]


class UpdateDirectConnectGatewayAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str
    EdgeLocations: NotRequired[Sequence[str]]


class UpdateGlobalNetworkRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    Description: NotRequired[str]


class UpdateNetworkResourceMetadataRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    ResourceArn: str
    Metadata: Mapping[str, str]


class GetResourcePolicyResponseTypeDef(TypedDict):
    PolicyDocument: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNetworkResourceMetadataResponseTypeDef(TypedDict):
    ResourceArn: str
    Metadata: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class OrganizationStatusTypeDef(TypedDict):
    OrganizationId: NotRequired[str]
    OrganizationAwsServiceAccessStatus: NotRequired[str]
    SLRDeploymentStatus: NotRequired[str]
    AccountStatusList: NotRequired[list[AccountStatusTypeDef]]


class AssociateConnectPeerResponseTypeDef(TypedDict):
    ConnectPeerAssociation: ConnectPeerAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateConnectPeerResponseTypeDef(TypedDict):
    ConnectPeerAssociation: ConnectPeerAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetConnectPeerAssociationsResponseTypeDef(TypedDict):
    ConnectPeerAssociations: list[ConnectPeerAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateCustomerGatewayResponseTypeDef(TypedDict):
    CustomerGatewayAssociation: CustomerGatewayAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateCustomerGatewayResponseTypeDef(TypedDict):
    CustomerGatewayAssociation: CustomerGatewayAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetCustomerGatewayAssociationsResponseTypeDef(TypedDict):
    CustomerGatewayAssociations: list[CustomerGatewayAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateLinkResponseTypeDef(TypedDict):
    LinkAssociation: LinkAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateLinkResponseTypeDef(TypedDict):
    LinkAssociation: LinkAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetLinkAssociationsResponseTypeDef(TypedDict):
    LinkAssociations: list[LinkAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateTransitGatewayConnectPeerResponseTypeDef(TypedDict):
    TransitGatewayConnectPeerAssociation: TransitGatewayConnectPeerAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateTransitGatewayConnectPeerResponseTypeDef(TypedDict):
    TransitGatewayConnectPeerAssociation: TransitGatewayConnectPeerAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTransitGatewayConnectPeerAssociationsResponseTypeDef(TypedDict):
    TransitGatewayConnectPeerAssociations: list[TransitGatewayConnectPeerAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ConnectPeerSummaryTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    ConnectAttachmentId: NotRequired[str]
    ConnectPeerId: NotRequired[str]
    EdgeLocation: NotRequired[str]
    ConnectPeerState: NotRequired[ConnectPeerStateType]
    CreatedAt: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]
    SubnetArn: NotRequired[str]


class ConnectionTypeDef(TypedDict):
    ConnectionId: NotRequired[str]
    ConnectionArn: NotRequired[str]
    GlobalNetworkId: NotRequired[str]
    DeviceId: NotRequired[str]
    ConnectedDeviceId: NotRequired[str]
    LinkId: NotRequired[str]
    ConnectedLinkId: NotRequired[str]
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    State: NotRequired[ConnectionStateType]
    Tags: NotRequired[list[TagTypeDef]]


class CoreNetworkSummaryTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    GlobalNetworkId: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    State: NotRequired[CoreNetworkStateType]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class CreateConnectionRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    DeviceId: str
    ConnectedDeviceId: str
    LinkId: NotRequired[str]
    ConnectedLinkId: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateCoreNetworkRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    PolicyDocument: NotRequired[str]
    ClientToken: NotRequired[str]


class CreateDirectConnectGatewayAttachmentRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    DirectConnectGatewayArn: str
    EdgeLocations: Sequence[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]


class CreateGlobalNetworkRequestRequestTypeDef(TypedDict):
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateSiteToSiteVpnAttachmentRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    VpnConnectionArn: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]


class CreateTransitGatewayPeeringRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    TransitGatewayArn: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]


class CreateTransitGatewayRouteTableAttachmentRequestRequestTypeDef(TypedDict):
    PeeringId: str
    TransitGatewayRouteTableArn: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]


class GlobalNetworkTypeDef(TypedDict):
    GlobalNetworkId: NotRequired[str]
    GlobalNetworkArn: NotRequired[str]
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    State: NotRequired[GlobalNetworkStateType]
    Tags: NotRequired[list[TagTypeDef]]


class ListTagsForResourceResponseTypeDef(TypedDict):
    TagList: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class NetworkResourceTypeDef(TypedDict):
    RegisteredGatewayArn: NotRequired[str]
    CoreNetworkId: NotRequired[str]
    AwsRegion: NotRequired[str]
    AccountId: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceArn: NotRequired[str]
    Definition: NotRequired[str]
    DefinitionTimestamp: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]
    Metadata: NotRequired[dict[str, str]]


class ProposedNetworkFunctionGroupChangeTypeDef(TypedDict):
    Tags: NotRequired[list[TagTypeDef]]
    AttachmentPolicyRuleNumber: NotRequired[int]
    NetworkFunctionGroupName: NotRequired[str]


class ProposedSegmentChangeTypeDef(TypedDict):
    Tags: NotRequired[list[TagTypeDef]]
    AttachmentPolicyRuleNumber: NotRequired[int]
    SegmentName: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


CreateLinkRequestRequestTypeDef = TypedDict(
    "CreateLinkRequestRequestTypeDef",
    {
        "GlobalNetworkId": str,
        "Bandwidth": BandwidthTypeDef,
        "SiteId": str,
        "Description": NotRequired[str],
        "Type": NotRequired[str],
        "Provider": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
LinkTypeDef = TypedDict(
    "LinkTypeDef",
    {
        "LinkId": NotRequired[str],
        "LinkArn": NotRequired[str],
        "GlobalNetworkId": NotRequired[str],
        "SiteId": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[str],
        "Bandwidth": NotRequired[BandwidthTypeDef],
        "Provider": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "State": NotRequired[LinkStateType],
        "Tags": NotRequired[list[TagTypeDef]],
    },
)
UpdateLinkRequestRequestTypeDef = TypedDict(
    "UpdateLinkRequestRequestTypeDef",
    {
        "GlobalNetworkId": str,
        "LinkId": str,
        "Description": NotRequired[str],
        "Type": NotRequired[str],
        "Bandwidth": NotRequired[BandwidthTypeDef],
        "Provider": NotRequired[str],
    },
)


class CreateConnectPeerRequestRequestTypeDef(TypedDict):
    ConnectAttachmentId: str
    PeerAddress: str
    CoreNetworkAddress: NotRequired[str]
    BgpOptions: NotRequired[BgpOptionsTypeDef]
    InsideCidrBlocks: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]
    SubnetArn: NotRequired[str]


class CreateConnectAttachmentRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    EdgeLocation: str
    TransportAttachmentId: str
    Options: ConnectAttachmentOptionsTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]


ConnectPeerConfigurationTypeDef = TypedDict(
    "ConnectPeerConfigurationTypeDef",
    {
        "CoreNetworkAddress": NotRequired[str],
        "PeerAddress": NotRequired[str],
        "InsideCidrBlocks": NotRequired[list[str]],
        "Protocol": NotRequired[TunnelProtocolType],
        "BgpConfigurations": NotRequired[list[ConnectPeerBgpConfigurationTypeDef]],
    },
)


class NetworkTelemetryTypeDef(TypedDict):
    RegisteredGatewayArn: NotRequired[str]
    CoreNetworkId: NotRequired[str]
    AwsRegion: NotRequired[str]
    AccountId: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceArn: NotRequired[str]
    Address: NotRequired[str]
    Health: NotRequired[ConnectionHealthTypeDef]


CoreNetworkChangeEventTypeDef = TypedDict(
    "CoreNetworkChangeEventTypeDef",
    {
        "Type": NotRequired[ChangeTypeType],
        "Action": NotRequired[ChangeActionType],
        "IdentifierPath": NotRequired[str],
        "EventTime": NotRequired[datetime],
        "Status": NotRequired[ChangeStatusType],
        "Values": NotRequired[CoreNetworkChangeEventValuesTypeDef],
    },
)


class CoreNetworkNetworkFunctionGroupTypeDef(TypedDict):
    Name: NotRequired[str]
    EdgeLocations: NotRequired[list[str]]
    Segments: NotRequired[ServiceInsertionSegmentsTypeDef]


class CoreNetworkPolicyTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    PolicyVersionId: NotRequired[int]
    Alias: NotRequired[CoreNetworkPolicyAliasType]
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    ChangeSetState: NotRequired[ChangeSetStateType]
    PolicyErrors: NotRequired[list[CoreNetworkPolicyErrorTypeDef]]
    PolicyDocument: NotRequired[str]


class ListCoreNetworkPolicyVersionsResponseTypeDef(TypedDict):
    CoreNetworkPolicyVersions: list[CoreNetworkPolicyVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RouteTableIdentifierTypeDef(TypedDict):
    TransitGatewayRouteTableArn: NotRequired[str]
    CoreNetworkSegmentEdge: NotRequired[CoreNetworkSegmentEdgeIdentifierTypeDef]
    CoreNetworkNetworkFunctionGroup: NotRequired[CoreNetworkNetworkFunctionGroupIdentifierTypeDef]


CreateDeviceRequestRequestTypeDef = TypedDict(
    "CreateDeviceRequestRequestTypeDef",
    {
        "GlobalNetworkId": str,
        "AWSLocation": NotRequired[AWSLocationTypeDef],
        "Description": NotRequired[str],
        "Type": NotRequired[str],
        "Vendor": NotRequired[str],
        "Model": NotRequired[str],
        "SerialNumber": NotRequired[str],
        "Location": NotRequired[LocationTypeDef],
        "SiteId": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class CreateSiteRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    Description: NotRequired[str]
    Location: NotRequired[LocationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


DeviceTypeDef = TypedDict(
    "DeviceTypeDef",
    {
        "DeviceId": NotRequired[str],
        "DeviceArn": NotRequired[str],
        "GlobalNetworkId": NotRequired[str],
        "AWSLocation": NotRequired[AWSLocationTypeDef],
        "Description": NotRequired[str],
        "Type": NotRequired[str],
        "Vendor": NotRequired[str],
        "Model": NotRequired[str],
        "SerialNumber": NotRequired[str],
        "Location": NotRequired[LocationTypeDef],
        "SiteId": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "State": NotRequired[DeviceStateType],
        "Tags": NotRequired[list[TagTypeDef]],
    },
)


class SiteTypeDef(TypedDict):
    SiteId: NotRequired[str]
    SiteArn: NotRequired[str]
    GlobalNetworkId: NotRequired[str]
    Description: NotRequired[str]
    Location: NotRequired[LocationTypeDef]
    CreatedAt: NotRequired[datetime]
    State: NotRequired[SiteStateType]
    Tags: NotRequired[list[TagTypeDef]]


UpdateDeviceRequestRequestTypeDef = TypedDict(
    "UpdateDeviceRequestRequestTypeDef",
    {
        "GlobalNetworkId": str,
        "DeviceId": str,
        "AWSLocation": NotRequired[AWSLocationTypeDef],
        "Description": NotRequired[str],
        "Type": NotRequired[str],
        "Vendor": NotRequired[str],
        "Model": NotRequired[str],
        "SerialNumber": NotRequired[str],
        "Location": NotRequired[LocationTypeDef],
        "SiteId": NotRequired[str],
    },
)


class UpdateSiteRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    SiteId: str
    Description: NotRequired[str]
    Location: NotRequired[LocationTypeDef]


class CreateVpcAttachmentRequestRequestTypeDef(TypedDict):
    CoreNetworkId: str
    VpcArn: str
    SubnetArns: Sequence[str]
    Options: NotRequired[VpcOptionsTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]


class UpdateVpcAttachmentRequestRequestTypeDef(TypedDict):
    AttachmentId: str
    AddSubnetArns: NotRequired[Sequence[str]]
    RemoveSubnetArns: NotRequired[Sequence[str]]
    Options: NotRequired[VpcOptionsTypeDef]


class DescribeGlobalNetworksRequestPaginateTypeDef(TypedDict):
    GlobalNetworkIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetConnectPeerAssociationsRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    ConnectPeerIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetConnectionsRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    ConnectionIds: NotRequired[Sequence[str]]
    DeviceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCoreNetworkChangeEventsRequestPaginateTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyVersionId: int
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCoreNetworkChangeSetRequestPaginateTypeDef(TypedDict):
    CoreNetworkId: str
    PolicyVersionId: int
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCustomerGatewayAssociationsRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    CustomerGatewayArns: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetDevicesRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    DeviceIds: NotRequired[Sequence[str]]
    SiteId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetLinkAssociationsRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    DeviceId: NotRequired[str]
    LinkId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


GetLinksRequestPaginateTypeDef = TypedDict(
    "GetLinksRequestPaginateTypeDef",
    {
        "GlobalNetworkId": str,
        "LinkIds": NotRequired[Sequence[str]],
        "SiteId": NotRequired[str],
        "Type": NotRequired[str],
        "Provider": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class GetNetworkResourceCountsRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    ResourceType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetNetworkResourceRelationshipsRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    CoreNetworkId: NotRequired[str]
    RegisteredGatewayArn: NotRequired[str]
    AwsRegion: NotRequired[str]
    AccountId: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetNetworkResourcesRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    CoreNetworkId: NotRequired[str]
    RegisteredGatewayArn: NotRequired[str]
    AwsRegion: NotRequired[str]
    AccountId: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetNetworkTelemetryRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    CoreNetworkId: NotRequired[str]
    RegisteredGatewayArn: NotRequired[str]
    AwsRegion: NotRequired[str]
    AccountId: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetSitesRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    SiteIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTransitGatewayConnectPeerAssociationsRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    TransitGatewayConnectPeerArns: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTransitGatewayRegistrationsRequestPaginateTypeDef(TypedDict):
    GlobalNetworkId: str
    TransitGatewayArns: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAttachmentsRequestPaginateTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    AttachmentType: NotRequired[AttachmentTypeType]
    EdgeLocation: NotRequired[str]
    State: NotRequired[AttachmentStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListConnectPeersRequestPaginateTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    ConnectAttachmentId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCoreNetworkPolicyVersionsRequestPaginateTypeDef(TypedDict):
    CoreNetworkId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCoreNetworksRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPeeringsRequestPaginateTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    PeeringType: NotRequired[Literal["TRANSIT_GATEWAY"]]
    EdgeLocation: NotRequired[str]
    State: NotRequired[PeeringStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetNetworkResourceCountsResponseTypeDef(TypedDict):
    NetworkResourceCounts: list[NetworkResourceCountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetNetworkResourceRelationshipsResponseTypeDef(TypedDict):
    Relationships: list[RelationshipTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ViaTypeDef(TypedDict):
    NetworkFunctionGroups: NotRequired[list[NetworkFunctionGroupTypeDef]]
    WithEdgeOverrides: NotRequired[list[EdgeOverrideTypeDef]]


PathComponentTypeDef = TypedDict(
    "PathComponentTypeDef",
    {
        "Sequence": NotRequired[int],
        "Resource": NotRequired[NetworkResourceSummaryTypeDef],
        "DestinationCidrBlock": NotRequired[str],
    },
)
NetworkRouteTypeDef = TypedDict(
    "NetworkRouteTypeDef",
    {
        "DestinationCidrBlock": NotRequired[str],
        "Destinations": NotRequired[list[NetworkRouteDestinationTypeDef]],
        "PrefixListId": NotRequired[str],
        "State": NotRequired[RouteStateType],
        "Type": NotRequired[RouteTypeType],
    },
)


class PeeringErrorTypeDef(TypedDict):
    Code: NotRequired[PeeringErrorCodeType]
    Message: NotRequired[str]
    ResourceArn: NotRequired[str]
    RequestId: NotRequired[str]
    MissingPermissionsContext: NotRequired[PermissionsErrorContextTypeDef]


class StartRouteAnalysisRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    Source: RouteAnalysisEndpointOptionsSpecificationTypeDef
    Destination: RouteAnalysisEndpointOptionsSpecificationTypeDef
    IncludeReturnPath: NotRequired[bool]
    UseMiddleboxes: NotRequired[bool]


class TransitGatewayRegistrationTypeDef(TypedDict):
    GlobalNetworkId: NotRequired[str]
    TransitGatewayArn: NotRequired[str]
    State: NotRequired[TransitGatewayRegistrationStateReasonTypeDef]


class ListOrganizationServiceAccessStatusResponseTypeDef(TypedDict):
    OrganizationStatus: OrganizationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartOrganizationServiceAccessUpdateResponseTypeDef(TypedDict):
    OrganizationStatus: OrganizationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListConnectPeersResponseTypeDef(TypedDict):
    ConnectPeers: list[ConnectPeerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateConnectionResponseTypeDef(TypedDict):
    Connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteConnectionResponseTypeDef(TypedDict):
    Connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetConnectionsResponseTypeDef(TypedDict):
    Connections: list[ConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateConnectionResponseTypeDef(TypedDict):
    Connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListCoreNetworksResponseTypeDef(TypedDict):
    CoreNetworks: list[CoreNetworkSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateGlobalNetworkResponseTypeDef(TypedDict):
    GlobalNetwork: GlobalNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGlobalNetworkResponseTypeDef(TypedDict):
    GlobalNetwork: GlobalNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGlobalNetworksResponseTypeDef(TypedDict):
    GlobalNetworks: list[GlobalNetworkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateGlobalNetworkResponseTypeDef(TypedDict):
    GlobalNetwork: GlobalNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNetworkResourcesResponseTypeDef(TypedDict):
    NetworkResources: list[NetworkResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AttachmentTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    AttachmentId: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    AttachmentType: NotRequired[AttachmentTypeType]
    State: NotRequired[AttachmentStateType]
    EdgeLocation: NotRequired[str]
    EdgeLocations: NotRequired[list[str]]
    ResourceArn: NotRequired[str]
    AttachmentPolicyRuleNumber: NotRequired[int]
    SegmentName: NotRequired[str]
    NetworkFunctionGroupName: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    ProposedSegmentChange: NotRequired[ProposedSegmentChangeTypeDef]
    ProposedNetworkFunctionGroupChange: NotRequired[ProposedNetworkFunctionGroupChangeTypeDef]
    CreatedAt: NotRequired[datetime]
    UpdatedAt: NotRequired[datetime]
    LastModificationErrors: NotRequired[list[AttachmentErrorTypeDef]]


class CreateLinkResponseTypeDef(TypedDict):
    Link: LinkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLinkResponseTypeDef(TypedDict):
    Link: LinkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetLinksResponseTypeDef(TypedDict):
    Links: list[LinkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateLinkResponseTypeDef(TypedDict):
    Link: LinkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ConnectPeerTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    ConnectAttachmentId: NotRequired[str]
    ConnectPeerId: NotRequired[str]
    EdgeLocation: NotRequired[str]
    State: NotRequired[ConnectPeerStateType]
    CreatedAt: NotRequired[datetime]
    Configuration: NotRequired[ConnectPeerConfigurationTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    SubnetArn: NotRequired[str]
    LastModificationErrors: NotRequired[list[ConnectPeerErrorTypeDef]]


class GetNetworkTelemetryResponseTypeDef(TypedDict):
    NetworkTelemetry: list[NetworkTelemetryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetCoreNetworkChangeEventsResponseTypeDef(TypedDict):
    CoreNetworkChangeEvents: list[CoreNetworkChangeEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CoreNetworkTypeDef(TypedDict):
    GlobalNetworkId: NotRequired[str]
    CoreNetworkId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    Description: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    State: NotRequired[CoreNetworkStateType]
    Segments: NotRequired[list[CoreNetworkSegmentTypeDef]]
    NetworkFunctionGroups: NotRequired[list[CoreNetworkNetworkFunctionGroupTypeDef]]
    Edges: NotRequired[list[CoreNetworkEdgeTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]


class DeleteCoreNetworkPolicyVersionResponseTypeDef(TypedDict):
    CoreNetworkPolicy: CoreNetworkPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetCoreNetworkPolicyResponseTypeDef(TypedDict):
    CoreNetworkPolicy: CoreNetworkPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutCoreNetworkPolicyResponseTypeDef(TypedDict):
    CoreNetworkPolicy: CoreNetworkPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreCoreNetworkPolicyVersionResponseTypeDef(TypedDict):
    CoreNetworkPolicy: CoreNetworkPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNetworkRoutesRequestRequestTypeDef(TypedDict):
    GlobalNetworkId: str
    RouteTableIdentifier: RouteTableIdentifierTypeDef
    ExactCidrMatches: NotRequired[Sequence[str]]
    LongestPrefixMatches: NotRequired[Sequence[str]]
    SubnetOfMatches: NotRequired[Sequence[str]]
    SupernetOfMatches: NotRequired[Sequence[str]]
    PrefixListIds: NotRequired[Sequence[str]]
    States: NotRequired[Sequence[RouteStateType]]
    Types: NotRequired[Sequence[RouteTypeType]]
    DestinationFilters: NotRequired[Mapping[str, Sequence[str]]]


class CreateDeviceResponseTypeDef(TypedDict):
    Device: DeviceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDeviceResponseTypeDef(TypedDict):
    Device: DeviceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDevicesResponseTypeDef(TypedDict):
    Devices: list[DeviceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateDeviceResponseTypeDef(TypedDict):
    Device: DeviceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSiteResponseTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSiteResponseTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSitesResponseTypeDef(TypedDict):
    Sites: list[SiteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateSiteResponseTypeDef(TypedDict):
    Site: SiteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ServiceInsertionActionTypeDef(TypedDict):
    Action: NotRequired[SegmentActionServiceInsertionType]
    Mode: NotRequired[SendViaModeType]
    WhenSentTo: NotRequired[WhenSentToTypeDef]
    Via: NotRequired[ViaTypeDef]


class RouteAnalysisPathTypeDef(TypedDict):
    CompletionStatus: NotRequired[RouteAnalysisCompletionTypeDef]
    Path: NotRequired[list[PathComponentTypeDef]]


class GetNetworkRoutesResponseTypeDef(TypedDict):
    RouteTableArn: str
    CoreNetworkSegmentEdge: CoreNetworkSegmentEdgeIdentifierTypeDef
    RouteTableType: RouteTableTypeType
    RouteTableTimestamp: datetime
    NetworkRoutes: list[NetworkRouteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PeeringTypeDef(TypedDict):
    CoreNetworkId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    PeeringId: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    PeeringType: NotRequired[Literal["TRANSIT_GATEWAY"]]
    State: NotRequired[PeeringStateType]
    EdgeLocation: NotRequired[str]
    ResourceArn: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    CreatedAt: NotRequired[datetime]
    LastModificationErrors: NotRequired[list[PeeringErrorTypeDef]]


class DeregisterTransitGatewayResponseTypeDef(TypedDict):
    TransitGatewayRegistration: TransitGatewayRegistrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTransitGatewayRegistrationsResponseTypeDef(TypedDict):
    TransitGatewayRegistrations: list[TransitGatewayRegistrationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RegisterTransitGatewayResponseTypeDef(TypedDict):
    TransitGatewayRegistration: TransitGatewayRegistrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptAttachmentResponseTypeDef(TypedDict):
    Attachment: AttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ConnectAttachmentTypeDef(TypedDict):
    Attachment: NotRequired[AttachmentTypeDef]
    TransportAttachmentId: NotRequired[str]
    Options: NotRequired[ConnectAttachmentOptionsTypeDef]


class DeleteAttachmentResponseTypeDef(TypedDict):
    Attachment: AttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DirectConnectGatewayAttachmentTypeDef(TypedDict):
    Attachment: NotRequired[AttachmentTypeDef]
    DirectConnectGatewayArn: NotRequired[str]


class ListAttachmentsResponseTypeDef(TypedDict):
    Attachments: list[AttachmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RejectAttachmentResponseTypeDef(TypedDict):
    Attachment: AttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SiteToSiteVpnAttachmentTypeDef(TypedDict):
    Attachment: NotRequired[AttachmentTypeDef]
    VpnConnectionArn: NotRequired[str]


class TransitGatewayRouteTableAttachmentTypeDef(TypedDict):
    Attachment: NotRequired[AttachmentTypeDef]
    PeeringId: NotRequired[str]
    TransitGatewayRouteTableArn: NotRequired[str]


class VpcAttachmentTypeDef(TypedDict):
    Attachment: NotRequired[AttachmentTypeDef]
    SubnetArns: NotRequired[list[str]]
    Options: NotRequired[VpcOptionsTypeDef]


class CreateConnectPeerResponseTypeDef(TypedDict):
    ConnectPeer: ConnectPeerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteConnectPeerResponseTypeDef(TypedDict):
    ConnectPeer: ConnectPeerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetConnectPeerResponseTypeDef(TypedDict):
    ConnectPeer: ConnectPeerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCoreNetworkResponseTypeDef(TypedDict):
    CoreNetwork: CoreNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCoreNetworkResponseTypeDef(TypedDict):
    CoreNetwork: CoreNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetCoreNetworkResponseTypeDef(TypedDict):
    CoreNetwork: CoreNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCoreNetworkResponseTypeDef(TypedDict):
    CoreNetwork: CoreNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CoreNetworkChangeValuesTypeDef(TypedDict):
    SegmentName: NotRequired[str]
    NetworkFunctionGroupName: NotRequired[str]
    EdgeLocations: NotRequired[list[str]]
    Asn: NotRequired[int]
    Cidr: NotRequired[str]
    DestinationIdentifier: NotRequired[str]
    InsideCidrBlocks: NotRequired[list[str]]
    SharedSegments: NotRequired[list[str]]
    ServiceInsertionActions: NotRequired[list[ServiceInsertionActionTypeDef]]


class RouteAnalysisTypeDef(TypedDict):
    GlobalNetworkId: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    RouteAnalysisId: NotRequired[str]
    StartTimestamp: NotRequired[datetime]
    Status: NotRequired[RouteAnalysisStatusType]
    Source: NotRequired[RouteAnalysisEndpointOptionsTypeDef]
    Destination: NotRequired[RouteAnalysisEndpointOptionsTypeDef]
    IncludeReturnPath: NotRequired[bool]
    UseMiddleboxes: NotRequired[bool]
    ForwardPath: NotRequired[RouteAnalysisPathTypeDef]
    ReturnPath: NotRequired[RouteAnalysisPathTypeDef]


class DeletePeeringResponseTypeDef(TypedDict):
    Peering: PeeringTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListPeeringsResponseTypeDef(TypedDict):
    Peerings: list[PeeringTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TransitGatewayPeeringTypeDef(TypedDict):
    Peering: NotRequired[PeeringTypeDef]
    TransitGatewayArn: NotRequired[str]
    TransitGatewayPeeringAttachmentId: NotRequired[str]


class CreateConnectAttachmentResponseTypeDef(TypedDict):
    ConnectAttachment: ConnectAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetConnectAttachmentResponseTypeDef(TypedDict):
    ConnectAttachment: ConnectAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDirectConnectGatewayAttachmentResponseTypeDef(TypedDict):
    DirectConnectGatewayAttachment: DirectConnectGatewayAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDirectConnectGatewayAttachmentResponseTypeDef(TypedDict):
    DirectConnectGatewayAttachment: DirectConnectGatewayAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDirectConnectGatewayAttachmentResponseTypeDef(TypedDict):
    DirectConnectGatewayAttachment: DirectConnectGatewayAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSiteToSiteVpnAttachmentResponseTypeDef(TypedDict):
    SiteToSiteVpnAttachment: SiteToSiteVpnAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSiteToSiteVpnAttachmentResponseTypeDef(TypedDict):
    SiteToSiteVpnAttachment: SiteToSiteVpnAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTransitGatewayRouteTableAttachmentResponseTypeDef(TypedDict):
    TransitGatewayRouteTableAttachment: TransitGatewayRouteTableAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTransitGatewayRouteTableAttachmentResponseTypeDef(TypedDict):
    TransitGatewayRouteTableAttachment: TransitGatewayRouteTableAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVpcAttachmentResponseTypeDef(TypedDict):
    VpcAttachment: VpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetVpcAttachmentResponseTypeDef(TypedDict):
    VpcAttachment: VpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVpcAttachmentResponseTypeDef(TypedDict):
    VpcAttachment: VpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CoreNetworkChangeTypeDef = TypedDict(
    "CoreNetworkChangeTypeDef",
    {
        "Type": NotRequired[ChangeTypeType],
        "Action": NotRequired[ChangeActionType],
        "Identifier": NotRequired[str],
        "PreviousValues": NotRequired[CoreNetworkChangeValuesTypeDef],
        "NewValues": NotRequired[CoreNetworkChangeValuesTypeDef],
        "IdentifierPath": NotRequired[str],
    },
)


class GetRouteAnalysisResponseTypeDef(TypedDict):
    RouteAnalysis: RouteAnalysisTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartRouteAnalysisResponseTypeDef(TypedDict):
    RouteAnalysis: RouteAnalysisTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTransitGatewayPeeringResponseTypeDef(TypedDict):
    TransitGatewayPeering: TransitGatewayPeeringTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTransitGatewayPeeringResponseTypeDef(TypedDict):
    TransitGatewayPeering: TransitGatewayPeeringTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetCoreNetworkChangeSetResponseTypeDef(TypedDict):
    CoreNetworkChanges: list[CoreNetworkChangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
