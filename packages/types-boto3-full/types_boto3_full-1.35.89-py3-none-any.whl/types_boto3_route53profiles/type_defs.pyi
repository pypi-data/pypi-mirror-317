"""
Type annotations for route53profiles service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/type_defs/)

Usage::

    ```python
    from types_boto3_route53profiles.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence

from .literals import ProfileStatusType, ShareStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AssociateProfileRequestRequestTypeDef",
    "AssociateProfileResponseTypeDef",
    "AssociateResourceToProfileRequestRequestTypeDef",
    "AssociateResourceToProfileResponseTypeDef",
    "CreateProfileRequestRequestTypeDef",
    "CreateProfileResponseTypeDef",
    "DeleteProfileRequestRequestTypeDef",
    "DeleteProfileResponseTypeDef",
    "DisassociateProfileRequestRequestTypeDef",
    "DisassociateProfileResponseTypeDef",
    "DisassociateResourceFromProfileRequestRequestTypeDef",
    "DisassociateResourceFromProfileResponseTypeDef",
    "GetProfileAssociationRequestRequestTypeDef",
    "GetProfileAssociationResponseTypeDef",
    "GetProfileRequestRequestTypeDef",
    "GetProfileResourceAssociationRequestRequestTypeDef",
    "GetProfileResourceAssociationResponseTypeDef",
    "GetProfileResponseTypeDef",
    "ListProfileAssociationsRequestPaginateTypeDef",
    "ListProfileAssociationsRequestRequestTypeDef",
    "ListProfileAssociationsResponseTypeDef",
    "ListProfileResourceAssociationsRequestPaginateTypeDef",
    "ListProfileResourceAssociationsRequestRequestTypeDef",
    "ListProfileResourceAssociationsResponseTypeDef",
    "ListProfilesRequestPaginateTypeDef",
    "ListProfilesRequestRequestTypeDef",
    "ListProfilesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ProfileAssociationTypeDef",
    "ProfileResourceAssociationTypeDef",
    "ProfileSummaryTypeDef",
    "ProfileTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateProfileResourceAssociationRequestRequestTypeDef",
    "UpdateProfileResourceAssociationResponseTypeDef",
)

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ProfileAssociationTypeDef(TypedDict):
    CreationTime: NotRequired[datetime]
    Id: NotRequired[str]
    ModificationTime: NotRequired[datetime]
    Name: NotRequired[str]
    OwnerId: NotRequired[str]
    ProfileId: NotRequired[str]
    ResourceId: NotRequired[str]
    Status: NotRequired[ProfileStatusType]
    StatusMessage: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociateResourceToProfileRequestRequestTypeDef(TypedDict):
    Name: str
    ProfileId: str
    ResourceArn: str
    ResourceProperties: NotRequired[str]

class ProfileResourceAssociationTypeDef(TypedDict):
    CreationTime: NotRequired[datetime]
    Id: NotRequired[str]
    ModificationTime: NotRequired[datetime]
    Name: NotRequired[str]
    OwnerId: NotRequired[str]
    ProfileId: NotRequired[str]
    ResourceArn: NotRequired[str]
    ResourceProperties: NotRequired[str]
    ResourceType: NotRequired[str]
    Status: NotRequired[ProfileStatusType]
    StatusMessage: NotRequired[str]

class ProfileTypeDef(TypedDict):
    Arn: NotRequired[str]
    ClientToken: NotRequired[str]
    CreationTime: NotRequired[datetime]
    Id: NotRequired[str]
    ModificationTime: NotRequired[datetime]
    Name: NotRequired[str]
    OwnerId: NotRequired[str]
    ShareStatus: NotRequired[ShareStatusType]
    Status: NotRequired[ProfileStatusType]
    StatusMessage: NotRequired[str]

class DeleteProfileRequestRequestTypeDef(TypedDict):
    ProfileId: str

class DisassociateProfileRequestRequestTypeDef(TypedDict):
    ProfileId: str
    ResourceId: str

class DisassociateResourceFromProfileRequestRequestTypeDef(TypedDict):
    ProfileId: str
    ResourceArn: str

class GetProfileAssociationRequestRequestTypeDef(TypedDict):
    ProfileAssociationId: str

class GetProfileRequestRequestTypeDef(TypedDict):
    ProfileId: str

class GetProfileResourceAssociationRequestRequestTypeDef(TypedDict):
    ProfileResourceAssociationId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListProfileAssociationsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ProfileId: NotRequired[str]
    ResourceId: NotRequired[str]

class ListProfileResourceAssociationsRequestRequestTypeDef(TypedDict):
    ProfileId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ResourceType: NotRequired[str]

class ListProfilesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ProfileSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    ShareStatus: NotRequired[ShareStatusType]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateProfileResourceAssociationRequestRequestTypeDef(TypedDict):
    ProfileResourceAssociationId: str
    Name: NotRequired[str]
    ResourceProperties: NotRequired[str]

class AssociateProfileRequestRequestTypeDef(TypedDict):
    Name: str
    ProfileId: str
    ResourceId: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateProfileRequestRequestTypeDef(TypedDict):
    ClientToken: str
    Name: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class AssociateProfileResponseTypeDef(TypedDict):
    ProfileAssociation: ProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateProfileResponseTypeDef(TypedDict):
    ProfileAssociation: ProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetProfileAssociationResponseTypeDef(TypedDict):
    ProfileAssociation: ProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListProfileAssociationsResponseTypeDef(TypedDict):
    ProfileAssociations: list[ProfileAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class AssociateResourceToProfileResponseTypeDef(TypedDict):
    ProfileResourceAssociation: ProfileResourceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DisassociateResourceFromProfileResponseTypeDef(TypedDict):
    ProfileResourceAssociation: ProfileResourceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetProfileResourceAssociationResponseTypeDef(TypedDict):
    ProfileResourceAssociation: ProfileResourceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListProfileResourceAssociationsResponseTypeDef(TypedDict):
    ProfileResourceAssociations: list[ProfileResourceAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateProfileResourceAssociationResponseTypeDef(TypedDict):
    ProfileResourceAssociation: ProfileResourceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProfileResponseTypeDef(TypedDict):
    Profile: ProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteProfileResponseTypeDef(TypedDict):
    Profile: ProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetProfileResponseTypeDef(TypedDict):
    Profile: ProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListProfileAssociationsRequestPaginateTypeDef(TypedDict):
    ProfileId: NotRequired[str]
    ResourceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProfileResourceAssociationsRequestPaginateTypeDef(TypedDict):
    ProfileId: str
    ResourceType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProfilesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProfilesResponseTypeDef(TypedDict):
    ProfileSummaries: list[ProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
