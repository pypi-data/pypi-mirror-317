"""
Type annotations for dax service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dax/type_defs/)

Usage::

    ```python
    from types_boto3_dax.type_defs import EndpointTypeDef

    data: EndpointTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence, Union

from .literals import (
    ChangeTypeType,
    ClusterEndpointEncryptionTypeType,
    IsModifiableType,
    ParameterTypeType,
    SourceTypeType,
    SSEStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ClusterTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateParameterGroupRequestRequestTypeDef",
    "CreateParameterGroupResponseTypeDef",
    "CreateSubnetGroupRequestRequestTypeDef",
    "CreateSubnetGroupResponseTypeDef",
    "DecreaseReplicationFactorRequestRequestTypeDef",
    "DecreaseReplicationFactorResponseTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteParameterGroupRequestRequestTypeDef",
    "DeleteParameterGroupResponseTypeDef",
    "DeleteSubnetGroupRequestRequestTypeDef",
    "DeleteSubnetGroupResponseTypeDef",
    "DescribeClustersRequestPaginateTypeDef",
    "DescribeClustersRequestRequestTypeDef",
    "DescribeClustersResponseTypeDef",
    "DescribeDefaultParametersRequestPaginateTypeDef",
    "DescribeDefaultParametersRequestRequestTypeDef",
    "DescribeDefaultParametersResponseTypeDef",
    "DescribeEventsRequestPaginateTypeDef",
    "DescribeEventsRequestRequestTypeDef",
    "DescribeEventsResponseTypeDef",
    "DescribeParameterGroupsRequestPaginateTypeDef",
    "DescribeParameterGroupsRequestRequestTypeDef",
    "DescribeParameterGroupsResponseTypeDef",
    "DescribeParametersRequestPaginateTypeDef",
    "DescribeParametersRequestRequestTypeDef",
    "DescribeParametersResponseTypeDef",
    "DescribeSubnetGroupsRequestPaginateTypeDef",
    "DescribeSubnetGroupsRequestRequestTypeDef",
    "DescribeSubnetGroupsResponseTypeDef",
    "EndpointTypeDef",
    "EventTypeDef",
    "IncreaseReplicationFactorRequestRequestTypeDef",
    "IncreaseReplicationFactorResponseTypeDef",
    "ListTagsRequestPaginateTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ListTagsResponseTypeDef",
    "NodeTypeDef",
    "NodeTypeSpecificValueTypeDef",
    "NotificationConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterGroupStatusTypeDef",
    "ParameterGroupTypeDef",
    "ParameterNameValueTypeDef",
    "ParameterTypeDef",
    "RebootNodeRequestRequestTypeDef",
    "RebootNodeResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SSEDescriptionTypeDef",
    "SSESpecificationTypeDef",
    "SecurityGroupMembershipTypeDef",
    "SubnetGroupTypeDef",
    "SubnetTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagResourceResponseTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UntagResourceResponseTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateParameterGroupRequestRequestTypeDef",
    "UpdateParameterGroupResponseTypeDef",
    "UpdateSubnetGroupRequestRequestTypeDef",
    "UpdateSubnetGroupResponseTypeDef",
)


class EndpointTypeDef(TypedDict):
    Address: NotRequired[str]
    Port: NotRequired[int]
    URL: NotRequired[str]


class NotificationConfigurationTypeDef(TypedDict):
    TopicArn: NotRequired[str]
    TopicStatus: NotRequired[str]


class ParameterGroupStatusTypeDef(TypedDict):
    ParameterGroupName: NotRequired[str]
    ParameterApplyStatus: NotRequired[str]
    NodeIdsToReboot: NotRequired[list[str]]


class SSEDescriptionTypeDef(TypedDict):
    Status: NotRequired[SSEStatusType]


class SecurityGroupMembershipTypeDef(TypedDict):
    SecurityGroupIdentifier: NotRequired[str]
    Status: NotRequired[str]


class SSESpecificationTypeDef(TypedDict):
    Enabled: bool


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CreateParameterGroupRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str
    Description: NotRequired[str]


class ParameterGroupTypeDef(TypedDict):
    ParameterGroupName: NotRequired[str]
    Description: NotRequired[str]


class CreateSubnetGroupRequestRequestTypeDef(TypedDict):
    SubnetGroupName: str
    SubnetIds: Sequence[str]
    Description: NotRequired[str]


class DecreaseReplicationFactorRequestRequestTypeDef(TypedDict):
    ClusterName: str
    NewReplicationFactor: int
    AvailabilityZones: NotRequired[Sequence[str]]
    NodeIdsToRemove: NotRequired[Sequence[str]]


class DeleteClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str


class DeleteParameterGroupRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str


class DeleteSubnetGroupRequestRequestTypeDef(TypedDict):
    SubnetGroupName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeClustersRequestRequestTypeDef(TypedDict):
    ClusterNames: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeDefaultParametersRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class EventTypeDef(TypedDict):
    SourceName: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    Message: NotRequired[str]
    Date: NotRequired[datetime]


class DescribeParameterGroupsRequestRequestTypeDef(TypedDict):
    ParameterGroupNames: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeParametersRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str
    Source: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeSubnetGroupsRequestRequestTypeDef(TypedDict):
    SubnetGroupNames: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class IncreaseReplicationFactorRequestRequestTypeDef(TypedDict):
    ClusterName: str
    NewReplicationFactor: int
    AvailabilityZones: NotRequired[Sequence[str]]


class ListTagsRequestRequestTypeDef(TypedDict):
    ResourceName: str
    NextToken: NotRequired[str]


class NodeTypeSpecificValueTypeDef(TypedDict):
    NodeType: NotRequired[str]
    Value: NotRequired[str]


class ParameterNameValueTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    ParameterValue: NotRequired[str]


class RebootNodeRequestRequestTypeDef(TypedDict):
    ClusterName: str
    NodeId: str


class SubnetTypeDef(TypedDict):
    SubnetIdentifier: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceName: str
    TagKeys: Sequence[str]


class UpdateClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str
    Description: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    NotificationTopicArn: NotRequired[str]
    NotificationTopicStatus: NotRequired[str]
    ParameterGroupName: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]


class UpdateSubnetGroupRequestRequestTypeDef(TypedDict):
    SubnetGroupName: str
    Description: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]


class NodeTypeDef(TypedDict):
    NodeId: NotRequired[str]
    Endpoint: NotRequired[EndpointTypeDef]
    NodeCreateTime: NotRequired[datetime]
    AvailabilityZone: NotRequired[str]
    NodeStatus: NotRequired[str]
    ParameterGroupStatus: NotRequired[str]


class CreateClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str
    NodeType: str
    ReplicationFactor: int
    IamRoleArn: str
    Description: NotRequired[str]
    AvailabilityZones: NotRequired[Sequence[str]]
    SubnetGroupName: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    PreferredMaintenanceWindow: NotRequired[str]
    NotificationTopicArn: NotRequired[str]
    ParameterGroupName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SSESpecification: NotRequired[SSESpecificationTypeDef]
    ClusterEndpointEncryptionType: NotRequired[ClusterEndpointEncryptionTypeType]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceName: str
    Tags: Sequence[TagTypeDef]


class DeleteParameterGroupResponseTypeDef(TypedDict):
    DeletionMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSubnetGroupResponseTypeDef(TypedDict):
    DeletionMessage: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TagResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UntagResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateParameterGroupResponseTypeDef(TypedDict):
    ParameterGroup: ParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeParameterGroupsResponseTypeDef(TypedDict):
    ParameterGroups: list[ParameterGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateParameterGroupResponseTypeDef(TypedDict):
    ParameterGroup: ParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClustersRequestPaginateTypeDef(TypedDict):
    ClusterNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDefaultParametersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeParameterGroupsRequestPaginateTypeDef(TypedDict):
    ParameterGroupNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeParametersRequestPaginateTypeDef(TypedDict):
    ParameterGroupName: str
    Source: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSubnetGroupsRequestPaginateTypeDef(TypedDict):
    SubnetGroupNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsRequestPaginateTypeDef(TypedDict):
    ResourceName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEventsRequestPaginateTypeDef(TypedDict):
    SourceName: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEventsRequestRequestTypeDef(TypedDict):
    SourceName: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeEventsResponseTypeDef(TypedDict):
    Events: list[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ParameterTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    ParameterType: NotRequired[ParameterTypeType]
    ParameterValue: NotRequired[str]
    NodeTypeSpecificValues: NotRequired[list[NodeTypeSpecificValueTypeDef]]
    Description: NotRequired[str]
    Source: NotRequired[str]
    DataType: NotRequired[str]
    AllowedValues: NotRequired[str]
    IsModifiable: NotRequired[IsModifiableType]
    ChangeType: NotRequired[ChangeTypeType]


class UpdateParameterGroupRequestRequestTypeDef(TypedDict):
    ParameterGroupName: str
    ParameterNameValues: Sequence[ParameterNameValueTypeDef]


class SubnetGroupTypeDef(TypedDict):
    SubnetGroupName: NotRequired[str]
    Description: NotRequired[str]
    VpcId: NotRequired[str]
    Subnets: NotRequired[list[SubnetTypeDef]]


class ClusterTypeDef(TypedDict):
    ClusterName: NotRequired[str]
    Description: NotRequired[str]
    ClusterArn: NotRequired[str]
    TotalNodes: NotRequired[int]
    ActiveNodes: NotRequired[int]
    NodeType: NotRequired[str]
    Status: NotRequired[str]
    ClusterDiscoveryEndpoint: NotRequired[EndpointTypeDef]
    NodeIdsToRemove: NotRequired[list[str]]
    Nodes: NotRequired[list[NodeTypeDef]]
    PreferredMaintenanceWindow: NotRequired[str]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    SubnetGroup: NotRequired[str]
    SecurityGroups: NotRequired[list[SecurityGroupMembershipTypeDef]]
    IamRoleArn: NotRequired[str]
    ParameterGroup: NotRequired[ParameterGroupStatusTypeDef]
    SSEDescription: NotRequired[SSEDescriptionTypeDef]
    ClusterEndpointEncryptionType: NotRequired[ClusterEndpointEncryptionTypeType]


class DescribeDefaultParametersResponseTypeDef(TypedDict):
    Parameters: list[ParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeParametersResponseTypeDef(TypedDict):
    Parameters: list[ParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateSubnetGroupResponseTypeDef(TypedDict):
    SubnetGroup: SubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSubnetGroupsResponseTypeDef(TypedDict):
    SubnetGroups: list[SubnetGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateSubnetGroupResponseTypeDef(TypedDict):
    SubnetGroup: SubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DecreaseReplicationFactorResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClustersResponseTypeDef(TypedDict):
    Clusters: list[ClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class IncreaseReplicationFactorResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RebootNodeResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
