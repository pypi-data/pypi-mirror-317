"""
Type annotations for clouddirectory service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_clouddirectory/type_defs/)

Usage::

    ```python
    from types_boto3_clouddirectory.type_defs import ObjectReferenceTypeDef

    data: ObjectReferenceTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import IO, Any, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    BatchReadExceptionTypeType,
    ConsistencyLevelType,
    DirectoryStateType,
    FacetAttributeTypeType,
    FacetStyleType,
    ObjectTypeType,
    RangeModeType,
    RequiredAttributeBehaviorType,
    RuleTypeType,
    UpdateActionTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AddFacetToObjectRequestRequestTypeDef",
    "ApplySchemaRequestRequestTypeDef",
    "ApplySchemaResponseTypeDef",
    "AttachObjectRequestRequestTypeDef",
    "AttachObjectResponseTypeDef",
    "AttachPolicyRequestRequestTypeDef",
    "AttachToIndexRequestRequestTypeDef",
    "AttachToIndexResponseTypeDef",
    "AttachTypedLinkRequestRequestTypeDef",
    "AttachTypedLinkResponseTypeDef",
    "AttributeKeyAndValueOutputTypeDef",
    "AttributeKeyAndValueTypeDef",
    "AttributeKeyAndValueUnionTypeDef",
    "AttributeKeyTypeDef",
    "AttributeNameAndValueOutputTypeDef",
    "AttributeNameAndValueTypeDef",
    "AttributeNameAndValueUnionTypeDef",
    "BatchAddFacetToObjectTypeDef",
    "BatchAttachObjectResponseTypeDef",
    "BatchAttachObjectTypeDef",
    "BatchAttachPolicyTypeDef",
    "BatchAttachToIndexResponseTypeDef",
    "BatchAttachToIndexTypeDef",
    "BatchAttachTypedLinkResponseTypeDef",
    "BatchAttachTypedLinkTypeDef",
    "BatchCreateIndexResponseTypeDef",
    "BatchCreateIndexTypeDef",
    "BatchCreateObjectResponseTypeDef",
    "BatchCreateObjectTypeDef",
    "BatchDeleteObjectTypeDef",
    "BatchDetachFromIndexResponseTypeDef",
    "BatchDetachFromIndexTypeDef",
    "BatchDetachObjectResponseTypeDef",
    "BatchDetachObjectTypeDef",
    "BatchDetachPolicyTypeDef",
    "BatchDetachTypedLinkTypeDef",
    "BatchGetLinkAttributesResponseTypeDef",
    "BatchGetLinkAttributesTypeDef",
    "BatchGetObjectAttributesResponseTypeDef",
    "BatchGetObjectAttributesTypeDef",
    "BatchGetObjectInformationResponseTypeDef",
    "BatchGetObjectInformationTypeDef",
    "BatchListAttachedIndicesResponseTypeDef",
    "BatchListAttachedIndicesTypeDef",
    "BatchListIncomingTypedLinksResponseTypeDef",
    "BatchListIncomingTypedLinksTypeDef",
    "BatchListIndexResponseTypeDef",
    "BatchListIndexTypeDef",
    "BatchListObjectAttributesResponseTypeDef",
    "BatchListObjectAttributesTypeDef",
    "BatchListObjectChildrenResponseTypeDef",
    "BatchListObjectChildrenTypeDef",
    "BatchListObjectParentPathsResponseTypeDef",
    "BatchListObjectParentPathsTypeDef",
    "BatchListObjectParentsResponseTypeDef",
    "BatchListObjectParentsTypeDef",
    "BatchListObjectPoliciesResponseTypeDef",
    "BatchListObjectPoliciesTypeDef",
    "BatchListOutgoingTypedLinksResponseTypeDef",
    "BatchListOutgoingTypedLinksTypeDef",
    "BatchListPolicyAttachmentsResponseTypeDef",
    "BatchListPolicyAttachmentsTypeDef",
    "BatchLookupPolicyResponseTypeDef",
    "BatchLookupPolicyTypeDef",
    "BatchReadExceptionTypeDef",
    "BatchReadOperationResponseTypeDef",
    "BatchReadOperationTypeDef",
    "BatchReadRequestRequestTypeDef",
    "BatchReadResponseTypeDef",
    "BatchReadSuccessfulResponseTypeDef",
    "BatchRemoveFacetFromObjectTypeDef",
    "BatchUpdateLinkAttributesTypeDef",
    "BatchUpdateObjectAttributesResponseTypeDef",
    "BatchUpdateObjectAttributesTypeDef",
    "BatchWriteOperationResponseTypeDef",
    "BatchWriteOperationTypeDef",
    "BatchWriteRequestRequestTypeDef",
    "BatchWriteResponseTypeDef",
    "BlobTypeDef",
    "CreateDirectoryRequestRequestTypeDef",
    "CreateDirectoryResponseTypeDef",
    "CreateFacetRequestRequestTypeDef",
    "CreateIndexRequestRequestTypeDef",
    "CreateIndexResponseTypeDef",
    "CreateObjectRequestRequestTypeDef",
    "CreateObjectResponseTypeDef",
    "CreateSchemaRequestRequestTypeDef",
    "CreateSchemaResponseTypeDef",
    "CreateTypedLinkFacetRequestRequestTypeDef",
    "DeleteDirectoryRequestRequestTypeDef",
    "DeleteDirectoryResponseTypeDef",
    "DeleteFacetRequestRequestTypeDef",
    "DeleteObjectRequestRequestTypeDef",
    "DeleteSchemaRequestRequestTypeDef",
    "DeleteSchemaResponseTypeDef",
    "DeleteTypedLinkFacetRequestRequestTypeDef",
    "DetachFromIndexRequestRequestTypeDef",
    "DetachFromIndexResponseTypeDef",
    "DetachObjectRequestRequestTypeDef",
    "DetachObjectResponseTypeDef",
    "DetachPolicyRequestRequestTypeDef",
    "DetachTypedLinkRequestRequestTypeDef",
    "DirectoryTypeDef",
    "DisableDirectoryRequestRequestTypeDef",
    "DisableDirectoryResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableDirectoryRequestRequestTypeDef",
    "EnableDirectoryResponseTypeDef",
    "FacetAttributeDefinitionOutputTypeDef",
    "FacetAttributeDefinitionTypeDef",
    "FacetAttributeDefinitionUnionTypeDef",
    "FacetAttributeOutputTypeDef",
    "FacetAttributeReferenceTypeDef",
    "FacetAttributeTypeDef",
    "FacetAttributeUnionTypeDef",
    "FacetAttributeUpdateTypeDef",
    "FacetTypeDef",
    "GetAppliedSchemaVersionRequestRequestTypeDef",
    "GetAppliedSchemaVersionResponseTypeDef",
    "GetDirectoryRequestRequestTypeDef",
    "GetDirectoryResponseTypeDef",
    "GetFacetRequestRequestTypeDef",
    "GetFacetResponseTypeDef",
    "GetLinkAttributesRequestRequestTypeDef",
    "GetLinkAttributesResponseTypeDef",
    "GetObjectAttributesRequestRequestTypeDef",
    "GetObjectAttributesResponseTypeDef",
    "GetObjectInformationRequestRequestTypeDef",
    "GetObjectInformationResponseTypeDef",
    "GetSchemaAsJsonRequestRequestTypeDef",
    "GetSchemaAsJsonResponseTypeDef",
    "GetTypedLinkFacetInformationRequestRequestTypeDef",
    "GetTypedLinkFacetInformationResponseTypeDef",
    "IndexAttachmentTypeDef",
    "LinkAttributeActionTypeDef",
    "LinkAttributeUpdateTypeDef",
    "ListAppliedSchemaArnsRequestPaginateTypeDef",
    "ListAppliedSchemaArnsRequestRequestTypeDef",
    "ListAppliedSchemaArnsResponseTypeDef",
    "ListAttachedIndicesRequestPaginateTypeDef",
    "ListAttachedIndicesRequestRequestTypeDef",
    "ListAttachedIndicesResponseTypeDef",
    "ListDevelopmentSchemaArnsRequestPaginateTypeDef",
    "ListDevelopmentSchemaArnsRequestRequestTypeDef",
    "ListDevelopmentSchemaArnsResponseTypeDef",
    "ListDirectoriesRequestPaginateTypeDef",
    "ListDirectoriesRequestRequestTypeDef",
    "ListDirectoriesResponseTypeDef",
    "ListFacetAttributesRequestPaginateTypeDef",
    "ListFacetAttributesRequestRequestTypeDef",
    "ListFacetAttributesResponseTypeDef",
    "ListFacetNamesRequestPaginateTypeDef",
    "ListFacetNamesRequestRequestTypeDef",
    "ListFacetNamesResponseTypeDef",
    "ListIncomingTypedLinksRequestPaginateTypeDef",
    "ListIncomingTypedLinksRequestRequestTypeDef",
    "ListIncomingTypedLinksResponseTypeDef",
    "ListIndexRequestPaginateTypeDef",
    "ListIndexRequestRequestTypeDef",
    "ListIndexResponseTypeDef",
    "ListManagedSchemaArnsRequestPaginateTypeDef",
    "ListManagedSchemaArnsRequestRequestTypeDef",
    "ListManagedSchemaArnsResponseTypeDef",
    "ListObjectAttributesRequestPaginateTypeDef",
    "ListObjectAttributesRequestRequestTypeDef",
    "ListObjectAttributesResponseTypeDef",
    "ListObjectChildrenRequestRequestTypeDef",
    "ListObjectChildrenResponseTypeDef",
    "ListObjectParentPathsRequestPaginateTypeDef",
    "ListObjectParentPathsRequestRequestTypeDef",
    "ListObjectParentPathsResponseTypeDef",
    "ListObjectParentsRequestRequestTypeDef",
    "ListObjectParentsResponseTypeDef",
    "ListObjectPoliciesRequestPaginateTypeDef",
    "ListObjectPoliciesRequestRequestTypeDef",
    "ListObjectPoliciesResponseTypeDef",
    "ListOutgoingTypedLinksRequestPaginateTypeDef",
    "ListOutgoingTypedLinksRequestRequestTypeDef",
    "ListOutgoingTypedLinksResponseTypeDef",
    "ListPolicyAttachmentsRequestPaginateTypeDef",
    "ListPolicyAttachmentsRequestRequestTypeDef",
    "ListPolicyAttachmentsResponseTypeDef",
    "ListPublishedSchemaArnsRequestPaginateTypeDef",
    "ListPublishedSchemaArnsRequestRequestTypeDef",
    "ListPublishedSchemaArnsResponseTypeDef",
    "ListTagsForResourceRequestPaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTypedLinkFacetAttributesRequestPaginateTypeDef",
    "ListTypedLinkFacetAttributesRequestRequestTypeDef",
    "ListTypedLinkFacetAttributesResponseTypeDef",
    "ListTypedLinkFacetNamesRequestPaginateTypeDef",
    "ListTypedLinkFacetNamesRequestRequestTypeDef",
    "ListTypedLinkFacetNamesResponseTypeDef",
    "LookupPolicyRequestPaginateTypeDef",
    "LookupPolicyRequestRequestTypeDef",
    "LookupPolicyResponseTypeDef",
    "ObjectAttributeActionTypeDef",
    "ObjectAttributeRangeTypeDef",
    "ObjectAttributeUpdateTypeDef",
    "ObjectIdentifierAndLinkNameTupleTypeDef",
    "ObjectReferenceTypeDef",
    "PaginatorConfigTypeDef",
    "PathToObjectIdentifiersTypeDef",
    "PolicyAttachmentTypeDef",
    "PolicyToPathTypeDef",
    "PublishSchemaRequestRequestTypeDef",
    "PublishSchemaResponseTypeDef",
    "PutSchemaFromJsonRequestRequestTypeDef",
    "PutSchemaFromJsonResponseTypeDef",
    "RemoveFacetFromObjectRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "SchemaFacetTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimestampTypeDef",
    "TypedAttributeValueOutputTypeDef",
    "TypedAttributeValueRangeTypeDef",
    "TypedAttributeValueTypeDef",
    "TypedAttributeValueUnionTypeDef",
    "TypedLinkAttributeDefinitionOutputTypeDef",
    "TypedLinkAttributeDefinitionTypeDef",
    "TypedLinkAttributeDefinitionUnionTypeDef",
    "TypedLinkAttributeRangeTypeDef",
    "TypedLinkFacetAttributeUpdateTypeDef",
    "TypedLinkFacetTypeDef",
    "TypedLinkSchemaAndFacetNameTypeDef",
    "TypedLinkSpecifierOutputTypeDef",
    "TypedLinkSpecifierTypeDef",
    "TypedLinkSpecifierUnionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFacetRequestRequestTypeDef",
    "UpdateLinkAttributesRequestRequestTypeDef",
    "UpdateObjectAttributesRequestRequestTypeDef",
    "UpdateObjectAttributesResponseTypeDef",
    "UpdateSchemaRequestRequestTypeDef",
    "UpdateSchemaResponseTypeDef",
    "UpdateTypedLinkFacetRequestRequestTypeDef",
    "UpgradeAppliedSchemaRequestRequestTypeDef",
    "UpgradeAppliedSchemaResponseTypeDef",
    "UpgradePublishedSchemaRequestRequestTypeDef",
    "UpgradePublishedSchemaResponseTypeDef",
)


class ObjectReferenceTypeDef(TypedDict):
    Selector: NotRequired[str]


class SchemaFacetTypeDef(TypedDict):
    SchemaArn: NotRequired[str]
    FacetName: NotRequired[str]


class ApplySchemaRequestRequestTypeDef(TypedDict):
    PublishedSchemaArn: str
    DirectoryArn: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TypedLinkSchemaAndFacetNameTypeDef(TypedDict):
    SchemaArn: str
    TypedLinkName: str


class AttributeKeyTypeDef(TypedDict):
    SchemaArn: str
    FacetName: str
    Name: str


class TypedAttributeValueOutputTypeDef(TypedDict):
    StringValue: NotRequired[str]
    BinaryValue: NotRequired[bytes]
    BooleanValue: NotRequired[bool]
    NumberValue: NotRequired[str]
    DatetimeValue: NotRequired[datetime]


class BatchAttachObjectResponseTypeDef(TypedDict):
    attachedObjectIdentifier: NotRequired[str]


class BatchAttachToIndexResponseTypeDef(TypedDict):
    AttachedObjectIdentifier: NotRequired[str]


class BatchCreateIndexResponseTypeDef(TypedDict):
    ObjectIdentifier: NotRequired[str]


class BatchCreateObjectResponseTypeDef(TypedDict):
    ObjectIdentifier: NotRequired[str]


class BatchDetachFromIndexResponseTypeDef(TypedDict):
    DetachedObjectIdentifier: NotRequired[str]


class BatchDetachObjectResponseTypeDef(TypedDict):
    detachedObjectIdentifier: NotRequired[str]


class BatchListObjectChildrenResponseTypeDef(TypedDict):
    Children: NotRequired[dict[str, str]]
    NextToken: NotRequired[str]


class PathToObjectIdentifiersTypeDef(TypedDict):
    Path: NotRequired[str]
    ObjectIdentifiers: NotRequired[list[str]]


class ObjectIdentifierAndLinkNameTupleTypeDef(TypedDict):
    ObjectIdentifier: NotRequired[str]
    LinkName: NotRequired[str]


class BatchListObjectPoliciesResponseTypeDef(TypedDict):
    AttachedPolicyIds: NotRequired[list[str]]
    NextToken: NotRequired[str]


class BatchListPolicyAttachmentsResponseTypeDef(TypedDict):
    ObjectIdentifiers: NotRequired[list[str]]
    NextToken: NotRequired[str]


BatchReadExceptionTypeDef = TypedDict(
    "BatchReadExceptionTypeDef",
    {
        "Type": NotRequired[BatchReadExceptionTypeType],
        "Message": NotRequired[str],
    },
)


class BatchUpdateObjectAttributesResponseTypeDef(TypedDict):
    ObjectIdentifier: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CreateDirectoryRequestRequestTypeDef(TypedDict):
    Name: str
    SchemaArn: str


class CreateSchemaRequestRequestTypeDef(TypedDict):
    Name: str


class DeleteDirectoryRequestRequestTypeDef(TypedDict):
    DirectoryArn: str


class DeleteFacetRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str


class DeleteSchemaRequestRequestTypeDef(TypedDict):
    SchemaArn: str


class DeleteTypedLinkFacetRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str


class DirectoryTypeDef(TypedDict):
    Name: NotRequired[str]
    DirectoryArn: NotRequired[str]
    State: NotRequired[DirectoryStateType]
    CreationDateTime: NotRequired[datetime]


class DisableDirectoryRequestRequestTypeDef(TypedDict):
    DirectoryArn: str


class EnableDirectoryRequestRequestTypeDef(TypedDict):
    DirectoryArn: str


RuleOutputTypeDef = TypedDict(
    "RuleOutputTypeDef",
    {
        "Type": NotRequired[RuleTypeType],
        "Parameters": NotRequired[dict[str, str]],
    },
)


class FacetAttributeReferenceTypeDef(TypedDict):
    TargetFacetName: str
    TargetAttributeName: str


class FacetTypeDef(TypedDict):
    Name: NotRequired[str]
    ObjectType: NotRequired[ObjectTypeType]
    FacetStyle: NotRequired[FacetStyleType]


class GetAppliedSchemaVersionRequestRequestTypeDef(TypedDict):
    SchemaArn: str


class GetDirectoryRequestRequestTypeDef(TypedDict):
    DirectoryArn: str


class GetFacetRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str


class GetSchemaAsJsonRequestRequestTypeDef(TypedDict):
    SchemaArn: str


class GetTypedLinkFacetInformationRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAppliedSchemaArnsRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    SchemaArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDevelopmentSchemaArnsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDirectoriesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    state: NotRequired[DirectoryStateType]


class ListFacetAttributesRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFacetNamesRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListManagedSchemaArnsRequestRequestTypeDef(TypedDict):
    SchemaArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPublishedSchemaArnsRequestRequestTypeDef(TypedDict):
    SchemaArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class ListTypedLinkFacetAttributesRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTypedLinkFacetNamesRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PolicyAttachmentTypeDef(TypedDict):
    PolicyId: NotRequired[str]
    ObjectIdentifier: NotRequired[str]
    PolicyType: NotRequired[str]


class PublishSchemaRequestRequestTypeDef(TypedDict):
    DevelopmentSchemaArn: str
    Version: str
    MinorVersion: NotRequired[str]
    Name: NotRequired[str]


class PutSchemaFromJsonRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Document: str


RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "Type": NotRequired[RuleTypeType],
        "Parameters": NotRequired[Mapping[str, str]],
    },
)
TimestampTypeDef = Union[datetime, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateSchemaRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str


class UpgradeAppliedSchemaRequestRequestTypeDef(TypedDict):
    PublishedSchemaArn: str
    DirectoryArn: str
    DryRun: NotRequired[bool]


class UpgradePublishedSchemaRequestRequestTypeDef(TypedDict):
    DevelopmentSchemaArn: str
    PublishedSchemaArn: str
    MinorVersion: str
    DryRun: NotRequired[bool]


class AttachObjectRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ParentReference: ObjectReferenceTypeDef
    ChildReference: ObjectReferenceTypeDef
    LinkName: str


class AttachPolicyRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    PolicyReference: ObjectReferenceTypeDef
    ObjectReference: ObjectReferenceTypeDef


class AttachToIndexRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    IndexReference: ObjectReferenceTypeDef
    TargetReference: ObjectReferenceTypeDef


class BatchAttachObjectTypeDef(TypedDict):
    ParentReference: ObjectReferenceTypeDef
    ChildReference: ObjectReferenceTypeDef
    LinkName: str


class BatchAttachPolicyTypeDef(TypedDict):
    PolicyReference: ObjectReferenceTypeDef
    ObjectReference: ObjectReferenceTypeDef


class BatchAttachToIndexTypeDef(TypedDict):
    IndexReference: ObjectReferenceTypeDef
    TargetReference: ObjectReferenceTypeDef


class BatchDeleteObjectTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef


class BatchDetachFromIndexTypeDef(TypedDict):
    IndexReference: ObjectReferenceTypeDef
    TargetReference: ObjectReferenceTypeDef


class BatchDetachObjectTypeDef(TypedDict):
    ParentReference: ObjectReferenceTypeDef
    LinkName: str
    BatchReferenceName: NotRequired[str]


class BatchDetachPolicyTypeDef(TypedDict):
    PolicyReference: ObjectReferenceTypeDef
    ObjectReference: ObjectReferenceTypeDef


class BatchGetObjectInformationTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef


class BatchListAttachedIndicesTypeDef(TypedDict):
    TargetReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class BatchListObjectChildrenTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class BatchListObjectParentPathsTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class BatchListObjectParentsTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class BatchListObjectPoliciesTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class BatchListPolicyAttachmentsTypeDef(TypedDict):
    PolicyReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class BatchLookupPolicyTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DeleteObjectRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef


class DetachFromIndexRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    IndexReference: ObjectReferenceTypeDef
    TargetReference: ObjectReferenceTypeDef


class DetachObjectRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ParentReference: ObjectReferenceTypeDef
    LinkName: str


class DetachPolicyRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    PolicyReference: ObjectReferenceTypeDef
    ObjectReference: ObjectReferenceTypeDef


class GetObjectInformationRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class ListAttachedIndicesRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    TargetReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class ListObjectChildrenRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class ListObjectParentPathsRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListObjectParentsRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    IncludeAllLinksToEachParent: NotRequired[bool]


class ListObjectPoliciesRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class ListPolicyAttachmentsRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    PolicyReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class LookupPolicyRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class BatchGetObjectAttributesTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    SchemaFacet: SchemaFacetTypeDef
    AttributeNames: Sequence[str]


class BatchGetObjectInformationResponseTypeDef(TypedDict):
    SchemaFacets: NotRequired[list[SchemaFacetTypeDef]]
    ObjectIdentifier: NotRequired[str]


class BatchListObjectAttributesTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    FacetFilter: NotRequired[SchemaFacetTypeDef]


class BatchRemoveFacetFromObjectTypeDef(TypedDict):
    SchemaFacet: SchemaFacetTypeDef
    ObjectReference: ObjectReferenceTypeDef


class GetObjectAttributesRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    SchemaFacet: SchemaFacetTypeDef
    AttributeNames: Sequence[str]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class ListObjectAttributesRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    FacetFilter: NotRequired[SchemaFacetTypeDef]


class RemoveFacetFromObjectRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    SchemaFacet: SchemaFacetTypeDef
    ObjectReference: ObjectReferenceTypeDef


class ApplySchemaResponseTypeDef(TypedDict):
    AppliedSchemaArn: str
    DirectoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AttachObjectResponseTypeDef(TypedDict):
    AttachedObjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class AttachToIndexResponseTypeDef(TypedDict):
    AttachedObjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDirectoryResponseTypeDef(TypedDict):
    DirectoryArn: str
    Name: str
    ObjectIdentifier: str
    AppliedSchemaArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIndexResponseTypeDef(TypedDict):
    ObjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateObjectResponseTypeDef(TypedDict):
    ObjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSchemaResponseTypeDef(TypedDict):
    SchemaArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDirectoryResponseTypeDef(TypedDict):
    DirectoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSchemaResponseTypeDef(TypedDict):
    SchemaArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DetachFromIndexResponseTypeDef(TypedDict):
    DetachedObjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class DetachObjectResponseTypeDef(TypedDict):
    DetachedObjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisableDirectoryResponseTypeDef(TypedDict):
    DirectoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class EnableDirectoryResponseTypeDef(TypedDict):
    DirectoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetAppliedSchemaVersionResponseTypeDef(TypedDict):
    AppliedSchemaArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetObjectInformationResponseTypeDef(TypedDict):
    SchemaFacets: list[SchemaFacetTypeDef]
    ObjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSchemaAsJsonResponseTypeDef(TypedDict):
    Name: str
    Document: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTypedLinkFacetInformationResponseTypeDef(TypedDict):
    IdentityAttributeOrder: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAppliedSchemaArnsResponseTypeDef(TypedDict):
    SchemaArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDevelopmentSchemaArnsResponseTypeDef(TypedDict):
    SchemaArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFacetNamesResponseTypeDef(TypedDict):
    FacetNames: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListManagedSchemaArnsResponseTypeDef(TypedDict):
    SchemaArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListObjectChildrenResponseTypeDef(TypedDict):
    Children: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListObjectPoliciesResponseTypeDef(TypedDict):
    AttachedPolicyIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPolicyAttachmentsResponseTypeDef(TypedDict):
    ObjectIdentifiers: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPublishedSchemaArnsResponseTypeDef(TypedDict):
    SchemaArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTypedLinkFacetNamesResponseTypeDef(TypedDict):
    FacetNames: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PublishSchemaResponseTypeDef(TypedDict):
    PublishedSchemaArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutSchemaFromJsonResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateObjectAttributesResponseTypeDef(TypedDict):
    ObjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSchemaResponseTypeDef(TypedDict):
    SchemaArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpgradeAppliedSchemaResponseTypeDef(TypedDict):
    UpgradedSchemaArn: str
    DirectoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpgradePublishedSchemaResponseTypeDef(TypedDict):
    UpgradedSchemaArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class BatchCreateIndexTypeDef(TypedDict):
    OrderedIndexedAttributeList: Sequence[AttributeKeyTypeDef]
    IsUnique: bool
    ParentReference: NotRequired[ObjectReferenceTypeDef]
    LinkName: NotRequired[str]
    BatchReferenceName: NotRequired[str]


class CreateIndexRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    OrderedIndexedAttributeList: Sequence[AttributeKeyTypeDef]
    IsUnique: bool
    ParentReference: NotRequired[ObjectReferenceTypeDef]
    LinkName: NotRequired[str]


class AttributeKeyAndValueOutputTypeDef(TypedDict):
    Key: AttributeKeyTypeDef
    Value: TypedAttributeValueOutputTypeDef


class AttributeNameAndValueOutputTypeDef(TypedDict):
    AttributeName: str
    Value: TypedAttributeValueOutputTypeDef


class BatchListObjectParentPathsResponseTypeDef(TypedDict):
    PathToObjectIdentifiersList: NotRequired[list[PathToObjectIdentifiersTypeDef]]
    NextToken: NotRequired[str]


class ListObjectParentPathsResponseTypeDef(TypedDict):
    PathToObjectIdentifiersList: list[PathToObjectIdentifiersTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BatchListObjectParentsResponseTypeDef(TypedDict):
    ParentLinks: NotRequired[list[ObjectIdentifierAndLinkNameTupleTypeDef]]
    NextToken: NotRequired[str]


class ListObjectParentsResponseTypeDef(TypedDict):
    Parents: dict[str, str]
    ParentLinks: list[ObjectIdentifierAndLinkNameTupleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetDirectoryResponseTypeDef(TypedDict):
    Directory: DirectoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDirectoriesResponseTypeDef(TypedDict):
    Directories: list[DirectoryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


FacetAttributeDefinitionOutputTypeDef = TypedDict(
    "FacetAttributeDefinitionOutputTypeDef",
    {
        "Type": FacetAttributeTypeType,
        "DefaultValue": NotRequired[TypedAttributeValueOutputTypeDef],
        "IsImmutable": NotRequired[bool],
        "Rules": NotRequired[dict[str, RuleOutputTypeDef]],
    },
)
TypedLinkAttributeDefinitionOutputTypeDef = TypedDict(
    "TypedLinkAttributeDefinitionOutputTypeDef",
    {
        "Name": str,
        "Type": FacetAttributeTypeType,
        "RequiredBehavior": RequiredAttributeBehaviorType,
        "DefaultValue": NotRequired[TypedAttributeValueOutputTypeDef],
        "IsImmutable": NotRequired[bool],
        "Rules": NotRequired[dict[str, RuleOutputTypeDef]],
    },
)


class GetFacetResponseTypeDef(TypedDict):
    Facet: FacetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAppliedSchemaArnsRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    SchemaArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAttachedIndicesRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    TargetReference: ObjectReferenceTypeDef
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDevelopmentSchemaArnsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDirectoriesRequestPaginateTypeDef(TypedDict):
    state: NotRequired[DirectoryStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFacetAttributesRequestPaginateTypeDef(TypedDict):
    SchemaArn: str
    Name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFacetNamesRequestPaginateTypeDef(TypedDict):
    SchemaArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedSchemaArnsRequestPaginateTypeDef(TypedDict):
    SchemaArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListObjectAttributesRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    FacetFilter: NotRequired[SchemaFacetTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListObjectParentPathsRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListObjectPoliciesRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPolicyAttachmentsRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    PolicyReference: ObjectReferenceTypeDef
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPublishedSchemaArnsRequestPaginateTypeDef(TypedDict):
    SchemaArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceRequestPaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTypedLinkFacetAttributesRequestPaginateTypeDef(TypedDict):
    SchemaArn: str
    Name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTypedLinkFacetNamesRequestPaginateTypeDef(TypedDict):
    SchemaArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class LookupPolicyRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class PolicyToPathTypeDef(TypedDict):
    Path: NotRequired[str]
    Policies: NotRequired[list[PolicyAttachmentTypeDef]]


RuleUnionTypeDef = Union[RuleTypeDef, RuleOutputTypeDef]


class TypedAttributeValueTypeDef(TypedDict):
    StringValue: NotRequired[str]
    BinaryValue: NotRequired[BlobTypeDef]
    BooleanValue: NotRequired[bool]
    NumberValue: NotRequired[str]
    DatetimeValue: NotRequired[TimestampTypeDef]


class BatchGetLinkAttributesResponseTypeDef(TypedDict):
    Attributes: NotRequired[list[AttributeKeyAndValueOutputTypeDef]]


class BatchGetObjectAttributesResponseTypeDef(TypedDict):
    Attributes: NotRequired[list[AttributeKeyAndValueOutputTypeDef]]


class BatchListObjectAttributesResponseTypeDef(TypedDict):
    Attributes: NotRequired[list[AttributeKeyAndValueOutputTypeDef]]
    NextToken: NotRequired[str]


class GetLinkAttributesResponseTypeDef(TypedDict):
    Attributes: list[AttributeKeyAndValueOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetObjectAttributesResponseTypeDef(TypedDict):
    Attributes: list[AttributeKeyAndValueOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class IndexAttachmentTypeDef(TypedDict):
    IndexedAttributes: NotRequired[list[AttributeKeyAndValueOutputTypeDef]]
    ObjectIdentifier: NotRequired[str]


class ListObjectAttributesResponseTypeDef(TypedDict):
    Attributes: list[AttributeKeyAndValueOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TypedLinkSpecifierOutputTypeDef(TypedDict):
    TypedLinkFacet: TypedLinkSchemaAndFacetNameTypeDef
    SourceObjectReference: ObjectReferenceTypeDef
    TargetObjectReference: ObjectReferenceTypeDef
    IdentityAttributeValues: list[AttributeNameAndValueOutputTypeDef]


class FacetAttributeOutputTypeDef(TypedDict):
    Name: str
    AttributeDefinition: NotRequired[FacetAttributeDefinitionOutputTypeDef]
    AttributeReference: NotRequired[FacetAttributeReferenceTypeDef]
    RequiredBehavior: NotRequired[RequiredAttributeBehaviorType]


class ListTypedLinkFacetAttributesResponseTypeDef(TypedDict):
    Attributes: list[TypedLinkAttributeDefinitionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BatchLookupPolicyResponseTypeDef(TypedDict):
    PolicyToPathList: NotRequired[list[PolicyToPathTypeDef]]
    NextToken: NotRequired[str]


class LookupPolicyResponseTypeDef(TypedDict):
    PolicyToPathList: list[PolicyToPathTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


TypedAttributeValueUnionTypeDef = Union[
    TypedAttributeValueTypeDef, TypedAttributeValueOutputTypeDef
]


class BatchListAttachedIndicesResponseTypeDef(TypedDict):
    IndexAttachments: NotRequired[list[IndexAttachmentTypeDef]]
    NextToken: NotRequired[str]


class BatchListIndexResponseTypeDef(TypedDict):
    IndexAttachments: NotRequired[list[IndexAttachmentTypeDef]]
    NextToken: NotRequired[str]


class ListAttachedIndicesResponseTypeDef(TypedDict):
    IndexAttachments: list[IndexAttachmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIndexResponseTypeDef(TypedDict):
    IndexAttachments: list[IndexAttachmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AttachTypedLinkResponseTypeDef(TypedDict):
    TypedLinkSpecifier: TypedLinkSpecifierOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchAttachTypedLinkResponseTypeDef(TypedDict):
    TypedLinkSpecifier: NotRequired[TypedLinkSpecifierOutputTypeDef]


class BatchListIncomingTypedLinksResponseTypeDef(TypedDict):
    LinkSpecifiers: NotRequired[list[TypedLinkSpecifierOutputTypeDef]]
    NextToken: NotRequired[str]


class BatchListOutgoingTypedLinksResponseTypeDef(TypedDict):
    TypedLinkSpecifiers: NotRequired[list[TypedLinkSpecifierOutputTypeDef]]
    NextToken: NotRequired[str]


class ListIncomingTypedLinksResponseTypeDef(TypedDict):
    LinkSpecifiers: list[TypedLinkSpecifierOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListOutgoingTypedLinksResponseTypeDef(TypedDict):
    TypedLinkSpecifiers: list[TypedLinkSpecifierOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFacetAttributesResponseTypeDef(TypedDict):
    Attributes: list[FacetAttributeOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AttributeKeyAndValueTypeDef(TypedDict):
    Key: AttributeKeyTypeDef
    Value: TypedAttributeValueUnionTypeDef


class AttributeNameAndValueTypeDef(TypedDict):
    AttributeName: str
    Value: TypedAttributeValueUnionTypeDef


FacetAttributeDefinitionTypeDef = TypedDict(
    "FacetAttributeDefinitionTypeDef",
    {
        "Type": FacetAttributeTypeType,
        "DefaultValue": NotRequired[TypedAttributeValueUnionTypeDef],
        "IsImmutable": NotRequired[bool],
        "Rules": NotRequired[Mapping[str, RuleUnionTypeDef]],
    },
)


class LinkAttributeActionTypeDef(TypedDict):
    AttributeActionType: NotRequired[UpdateActionTypeType]
    AttributeUpdateValue: NotRequired[TypedAttributeValueUnionTypeDef]


class ObjectAttributeActionTypeDef(TypedDict):
    ObjectAttributeActionType: NotRequired[UpdateActionTypeType]
    ObjectAttributeUpdateValue: NotRequired[TypedAttributeValueUnionTypeDef]


class TypedAttributeValueRangeTypeDef(TypedDict):
    StartMode: RangeModeType
    EndMode: RangeModeType
    StartValue: NotRequired[TypedAttributeValueUnionTypeDef]
    EndValue: NotRequired[TypedAttributeValueUnionTypeDef]


TypedLinkAttributeDefinitionTypeDef = TypedDict(
    "TypedLinkAttributeDefinitionTypeDef",
    {
        "Name": str,
        "Type": FacetAttributeTypeType,
        "RequiredBehavior": RequiredAttributeBehaviorType,
        "DefaultValue": NotRequired[TypedAttributeValueUnionTypeDef],
        "IsImmutable": NotRequired[bool],
        "Rules": NotRequired[Mapping[str, RuleUnionTypeDef]],
    },
)


class BatchWriteOperationResponseTypeDef(TypedDict):
    CreateObject: NotRequired[BatchCreateObjectResponseTypeDef]
    AttachObject: NotRequired[BatchAttachObjectResponseTypeDef]
    DetachObject: NotRequired[BatchDetachObjectResponseTypeDef]
    UpdateObjectAttributes: NotRequired[BatchUpdateObjectAttributesResponseTypeDef]
    DeleteObject: NotRequired[dict[str, Any]]
    AddFacetToObject: NotRequired[dict[str, Any]]
    RemoveFacetFromObject: NotRequired[dict[str, Any]]
    AttachPolicy: NotRequired[dict[str, Any]]
    DetachPolicy: NotRequired[dict[str, Any]]
    CreateIndex: NotRequired[BatchCreateIndexResponseTypeDef]
    AttachToIndex: NotRequired[BatchAttachToIndexResponseTypeDef]
    DetachFromIndex: NotRequired[BatchDetachFromIndexResponseTypeDef]
    AttachTypedLink: NotRequired[BatchAttachTypedLinkResponseTypeDef]
    DetachTypedLink: NotRequired[dict[str, Any]]
    UpdateLinkAttributes: NotRequired[dict[str, Any]]


class BatchReadSuccessfulResponseTypeDef(TypedDict):
    ListObjectAttributes: NotRequired[BatchListObjectAttributesResponseTypeDef]
    ListObjectChildren: NotRequired[BatchListObjectChildrenResponseTypeDef]
    GetObjectInformation: NotRequired[BatchGetObjectInformationResponseTypeDef]
    GetObjectAttributes: NotRequired[BatchGetObjectAttributesResponseTypeDef]
    ListAttachedIndices: NotRequired[BatchListAttachedIndicesResponseTypeDef]
    ListObjectParentPaths: NotRequired[BatchListObjectParentPathsResponseTypeDef]
    ListObjectPolicies: NotRequired[BatchListObjectPoliciesResponseTypeDef]
    ListPolicyAttachments: NotRequired[BatchListPolicyAttachmentsResponseTypeDef]
    LookupPolicy: NotRequired[BatchLookupPolicyResponseTypeDef]
    ListIndex: NotRequired[BatchListIndexResponseTypeDef]
    ListOutgoingTypedLinks: NotRequired[BatchListOutgoingTypedLinksResponseTypeDef]
    ListIncomingTypedLinks: NotRequired[BatchListIncomingTypedLinksResponseTypeDef]
    GetLinkAttributes: NotRequired[BatchGetLinkAttributesResponseTypeDef]
    ListObjectParents: NotRequired[BatchListObjectParentsResponseTypeDef]


AttributeKeyAndValueUnionTypeDef = Union[
    AttributeKeyAndValueTypeDef, AttributeKeyAndValueOutputTypeDef
]


class BatchCreateObjectTypeDef(TypedDict):
    SchemaFacet: Sequence[SchemaFacetTypeDef]
    ObjectAttributeList: Sequence[AttributeKeyAndValueTypeDef]
    ParentReference: NotRequired[ObjectReferenceTypeDef]
    LinkName: NotRequired[str]
    BatchReferenceName: NotRequired[str]


class CreateObjectRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    SchemaFacets: Sequence[SchemaFacetTypeDef]
    ObjectAttributeList: NotRequired[Sequence[AttributeKeyAndValueTypeDef]]
    ParentReference: NotRequired[ObjectReferenceTypeDef]
    LinkName: NotRequired[str]


AttributeNameAndValueUnionTypeDef = Union[
    AttributeNameAndValueTypeDef, AttributeNameAndValueOutputTypeDef
]


class BatchAttachTypedLinkTypeDef(TypedDict):
    SourceObjectReference: ObjectReferenceTypeDef
    TargetObjectReference: ObjectReferenceTypeDef
    TypedLinkFacet: TypedLinkSchemaAndFacetNameTypeDef
    Attributes: Sequence[AttributeNameAndValueTypeDef]


FacetAttributeDefinitionUnionTypeDef = Union[
    FacetAttributeDefinitionTypeDef, FacetAttributeDefinitionOutputTypeDef
]


class LinkAttributeUpdateTypeDef(TypedDict):
    AttributeKey: NotRequired[AttributeKeyTypeDef]
    AttributeAction: NotRequired[LinkAttributeActionTypeDef]


class ObjectAttributeUpdateTypeDef(TypedDict):
    ObjectAttributeKey: NotRequired[AttributeKeyTypeDef]
    ObjectAttributeAction: NotRequired[ObjectAttributeActionTypeDef]


class ObjectAttributeRangeTypeDef(TypedDict):
    AttributeKey: NotRequired[AttributeKeyTypeDef]
    Range: NotRequired[TypedAttributeValueRangeTypeDef]


class TypedLinkAttributeRangeTypeDef(TypedDict):
    Range: TypedAttributeValueRangeTypeDef
    AttributeName: NotRequired[str]


TypedLinkAttributeDefinitionUnionTypeDef = Union[
    TypedLinkAttributeDefinitionTypeDef, TypedLinkAttributeDefinitionOutputTypeDef
]


class BatchWriteResponseTypeDef(TypedDict):
    Responses: list[BatchWriteOperationResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchReadOperationResponseTypeDef(TypedDict):
    SuccessfulResponse: NotRequired[BatchReadSuccessfulResponseTypeDef]
    ExceptionResponse: NotRequired[BatchReadExceptionTypeDef]


class AddFacetToObjectRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    SchemaFacet: SchemaFacetTypeDef
    ObjectReference: ObjectReferenceTypeDef
    ObjectAttributeList: NotRequired[Sequence[AttributeKeyAndValueUnionTypeDef]]


class BatchAddFacetToObjectTypeDef(TypedDict):
    SchemaFacet: SchemaFacetTypeDef
    ObjectAttributeList: Sequence[AttributeKeyAndValueUnionTypeDef]
    ObjectReference: ObjectReferenceTypeDef


class AttachTypedLinkRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    SourceObjectReference: ObjectReferenceTypeDef
    TargetObjectReference: ObjectReferenceTypeDef
    TypedLinkFacet: TypedLinkSchemaAndFacetNameTypeDef
    Attributes: Sequence[AttributeNameAndValueUnionTypeDef]


class TypedLinkSpecifierTypeDef(TypedDict):
    TypedLinkFacet: TypedLinkSchemaAndFacetNameTypeDef
    SourceObjectReference: ObjectReferenceTypeDef
    TargetObjectReference: ObjectReferenceTypeDef
    IdentityAttributeValues: Sequence[AttributeNameAndValueUnionTypeDef]


class FacetAttributeTypeDef(TypedDict):
    Name: str
    AttributeDefinition: NotRequired[FacetAttributeDefinitionUnionTypeDef]
    AttributeReference: NotRequired[FacetAttributeReferenceTypeDef]
    RequiredBehavior: NotRequired[RequiredAttributeBehaviorType]


class BatchUpdateObjectAttributesTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    AttributeUpdates: Sequence[ObjectAttributeUpdateTypeDef]


class UpdateObjectAttributesRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    AttributeUpdates: Sequence[ObjectAttributeUpdateTypeDef]


class BatchListIndexTypeDef(TypedDict):
    IndexReference: ObjectReferenceTypeDef
    RangesOnIndexedValues: NotRequired[Sequence[ObjectAttributeRangeTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListIndexRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    IndexReference: ObjectReferenceTypeDef
    RangesOnIndexedValues: NotRequired[Sequence[ObjectAttributeRangeTypeDef]]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIndexRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    IndexReference: ObjectReferenceTypeDef
    RangesOnIndexedValues: NotRequired[Sequence[ObjectAttributeRangeTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class BatchListIncomingTypedLinksTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    FilterAttributeRanges: NotRequired[Sequence[TypedLinkAttributeRangeTypeDef]]
    FilterTypedLink: NotRequired[TypedLinkSchemaAndFacetNameTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class BatchListOutgoingTypedLinksTypeDef(TypedDict):
    ObjectReference: ObjectReferenceTypeDef
    FilterAttributeRanges: NotRequired[Sequence[TypedLinkAttributeRangeTypeDef]]
    FilterTypedLink: NotRequired[TypedLinkSchemaAndFacetNameTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIncomingTypedLinksRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    FilterAttributeRanges: NotRequired[Sequence[TypedLinkAttributeRangeTypeDef]]
    FilterTypedLink: NotRequired[TypedLinkSchemaAndFacetNameTypeDef]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIncomingTypedLinksRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    FilterAttributeRanges: NotRequired[Sequence[TypedLinkAttributeRangeTypeDef]]
    FilterTypedLink: NotRequired[TypedLinkSchemaAndFacetNameTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class ListOutgoingTypedLinksRequestPaginateTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    FilterAttributeRanges: NotRequired[Sequence[TypedLinkAttributeRangeTypeDef]]
    FilterTypedLink: NotRequired[TypedLinkSchemaAndFacetNameTypeDef]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOutgoingTypedLinksRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    ObjectReference: ObjectReferenceTypeDef
    FilterAttributeRanges: NotRequired[Sequence[TypedLinkAttributeRangeTypeDef]]
    FilterTypedLink: NotRequired[TypedLinkSchemaAndFacetNameTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class TypedLinkFacetAttributeUpdateTypeDef(TypedDict):
    Attribute: TypedLinkAttributeDefinitionUnionTypeDef
    Action: UpdateActionTypeType


class TypedLinkFacetTypeDef(TypedDict):
    Name: str
    Attributes: Sequence[TypedLinkAttributeDefinitionUnionTypeDef]
    IdentityAttributeOrder: Sequence[str]


class BatchReadResponseTypeDef(TypedDict):
    Responses: list[BatchReadOperationResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DetachTypedLinkRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    TypedLinkSpecifier: TypedLinkSpecifierTypeDef


class GetLinkAttributesRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    TypedLinkSpecifier: TypedLinkSpecifierTypeDef
    AttributeNames: Sequence[str]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


TypedLinkSpecifierUnionTypeDef = Union[TypedLinkSpecifierTypeDef, TypedLinkSpecifierOutputTypeDef]


class UpdateLinkAttributesRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    TypedLinkSpecifier: TypedLinkSpecifierTypeDef
    AttributeUpdates: Sequence[LinkAttributeUpdateTypeDef]


FacetAttributeUnionTypeDef = Union[FacetAttributeTypeDef, FacetAttributeOutputTypeDef]


class UpdateTypedLinkFacetRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str
    AttributeUpdates: Sequence[TypedLinkFacetAttributeUpdateTypeDef]
    IdentityAttributeOrder: Sequence[str]


class CreateTypedLinkFacetRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Facet: TypedLinkFacetTypeDef


class BatchDetachTypedLinkTypeDef(TypedDict):
    TypedLinkSpecifier: TypedLinkSpecifierUnionTypeDef


class BatchGetLinkAttributesTypeDef(TypedDict):
    TypedLinkSpecifier: TypedLinkSpecifierUnionTypeDef
    AttributeNames: Sequence[str]


class BatchUpdateLinkAttributesTypeDef(TypedDict):
    TypedLinkSpecifier: TypedLinkSpecifierUnionTypeDef
    AttributeUpdates: Sequence[LinkAttributeUpdateTypeDef]


class CreateFacetRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str
    Attributes: NotRequired[Sequence[FacetAttributeUnionTypeDef]]
    ObjectType: NotRequired[ObjectTypeType]
    FacetStyle: NotRequired[FacetStyleType]


class FacetAttributeUpdateTypeDef(TypedDict):
    Attribute: NotRequired[FacetAttributeUnionTypeDef]
    Action: NotRequired[UpdateActionTypeType]


class BatchReadOperationTypeDef(TypedDict):
    ListObjectAttributes: NotRequired[BatchListObjectAttributesTypeDef]
    ListObjectChildren: NotRequired[BatchListObjectChildrenTypeDef]
    ListAttachedIndices: NotRequired[BatchListAttachedIndicesTypeDef]
    ListObjectParentPaths: NotRequired[BatchListObjectParentPathsTypeDef]
    GetObjectInformation: NotRequired[BatchGetObjectInformationTypeDef]
    GetObjectAttributes: NotRequired[BatchGetObjectAttributesTypeDef]
    ListObjectParents: NotRequired[BatchListObjectParentsTypeDef]
    ListObjectPolicies: NotRequired[BatchListObjectPoliciesTypeDef]
    ListPolicyAttachments: NotRequired[BatchListPolicyAttachmentsTypeDef]
    LookupPolicy: NotRequired[BatchLookupPolicyTypeDef]
    ListIndex: NotRequired[BatchListIndexTypeDef]
    ListOutgoingTypedLinks: NotRequired[BatchListOutgoingTypedLinksTypeDef]
    ListIncomingTypedLinks: NotRequired[BatchListIncomingTypedLinksTypeDef]
    GetLinkAttributes: NotRequired[BatchGetLinkAttributesTypeDef]


class BatchWriteOperationTypeDef(TypedDict):
    CreateObject: NotRequired[BatchCreateObjectTypeDef]
    AttachObject: NotRequired[BatchAttachObjectTypeDef]
    DetachObject: NotRequired[BatchDetachObjectTypeDef]
    UpdateObjectAttributes: NotRequired[BatchUpdateObjectAttributesTypeDef]
    DeleteObject: NotRequired[BatchDeleteObjectTypeDef]
    AddFacetToObject: NotRequired[BatchAddFacetToObjectTypeDef]
    RemoveFacetFromObject: NotRequired[BatchRemoveFacetFromObjectTypeDef]
    AttachPolicy: NotRequired[BatchAttachPolicyTypeDef]
    DetachPolicy: NotRequired[BatchDetachPolicyTypeDef]
    CreateIndex: NotRequired[BatchCreateIndexTypeDef]
    AttachToIndex: NotRequired[BatchAttachToIndexTypeDef]
    DetachFromIndex: NotRequired[BatchDetachFromIndexTypeDef]
    AttachTypedLink: NotRequired[BatchAttachTypedLinkTypeDef]
    DetachTypedLink: NotRequired[BatchDetachTypedLinkTypeDef]
    UpdateLinkAttributes: NotRequired[BatchUpdateLinkAttributesTypeDef]


class UpdateFacetRequestRequestTypeDef(TypedDict):
    SchemaArn: str
    Name: str
    AttributeUpdates: NotRequired[Sequence[FacetAttributeUpdateTypeDef]]
    ObjectType: NotRequired[ObjectTypeType]


class BatchReadRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    Operations: Sequence[BatchReadOperationTypeDef]
    ConsistencyLevel: NotRequired[ConsistencyLevelType]


class BatchWriteRequestRequestTypeDef(TypedDict):
    DirectoryArn: str
    Operations: Sequence[BatchWriteOperationTypeDef]
