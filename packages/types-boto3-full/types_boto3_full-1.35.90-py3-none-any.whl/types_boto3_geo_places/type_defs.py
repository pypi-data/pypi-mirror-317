"""
Type annotations for geo-places service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_geo_places/type_defs/)

Usage::

    ```python
    from types_boto3_geo_places.type_defs import AccessPointTypeDef

    data: AccessPointTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Sequence

from .literals import (
    AutocompleteFilterPlaceTypeType,
    GeocodeAdditionalFeatureType,
    GeocodeFilterPlaceTypeType,
    GeocodeIntendedUseType,
    GetPlaceAdditionalFeatureType,
    GetPlaceIntendedUseType,
    PlaceTypeType,
    PostalCodeModeType,
    PostalCodeTypeType,
    QueryTypeType,
    RecordTypeCodeType,
    ReverseGeocodeAdditionalFeatureType,
    ReverseGeocodeFilterPlaceTypeType,
    ReverseGeocodeIntendedUseType,
    SearchNearbyAdditionalFeatureType,
    SearchNearbyIntendedUseType,
    SearchTextAdditionalFeatureType,
    SearchTextIntendedUseType,
    SuggestAdditionalFeatureType,
    SuggestResultItemTypeType,
    TypePlacementType,
    ZipClassificationCodeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessPointTypeDef",
    "AccessRestrictionTypeDef",
    "AddressComponentMatchScoresTypeDef",
    "AddressComponentPhonemesTypeDef",
    "AddressTypeDef",
    "AutocompleteAddressHighlightsTypeDef",
    "AutocompleteFilterTypeDef",
    "AutocompleteHighlightsTypeDef",
    "AutocompleteRequestRequestTypeDef",
    "AutocompleteResponseTypeDef",
    "AutocompleteResultItemTypeDef",
    "BusinessChainTypeDef",
    "CategoryTypeDef",
    "ComponentMatchScoresTypeDef",
    "ContactDetailsTypeDef",
    "ContactsTypeDef",
    "CountryHighlightsTypeDef",
    "CountryTypeDef",
    "FilterCircleTypeDef",
    "FoodTypeTypeDef",
    "GeocodeFilterTypeDef",
    "GeocodeQueryComponentsTypeDef",
    "GeocodeRequestRequestTypeDef",
    "GeocodeResponseTypeDef",
    "GeocodeResultItemTypeDef",
    "GetPlaceRequestRequestTypeDef",
    "GetPlaceResponseTypeDef",
    "HighlightTypeDef",
    "MatchScoreDetailsTypeDef",
    "OpeningHoursComponentsTypeDef",
    "OpeningHoursTypeDef",
    "PhonemeDetailsTypeDef",
    "PhonemeTranscriptionTypeDef",
    "PostalCodeDetailsTypeDef",
    "QueryRefinementTypeDef",
    "RegionHighlightsTypeDef",
    "RegionTypeDef",
    "ResponseMetadataTypeDef",
    "ReverseGeocodeFilterTypeDef",
    "ReverseGeocodeRequestRequestTypeDef",
    "ReverseGeocodeResponseTypeDef",
    "ReverseGeocodeResultItemTypeDef",
    "SearchNearbyFilterTypeDef",
    "SearchNearbyRequestRequestTypeDef",
    "SearchNearbyResponseTypeDef",
    "SearchNearbyResultItemTypeDef",
    "SearchTextFilterTypeDef",
    "SearchTextRequestRequestTypeDef",
    "SearchTextResponseTypeDef",
    "SearchTextResultItemTypeDef",
    "StreetComponentsTypeDef",
    "SubRegionHighlightsTypeDef",
    "SubRegionTypeDef",
    "SuggestAddressHighlightsTypeDef",
    "SuggestFilterTypeDef",
    "SuggestHighlightsTypeDef",
    "SuggestPlaceResultTypeDef",
    "SuggestQueryResultTypeDef",
    "SuggestRequestRequestTypeDef",
    "SuggestResponseTypeDef",
    "SuggestResultItemTypeDef",
    "TimeZoneTypeDef",
    "UspsZipPlus4TypeDef",
    "UspsZipTypeDef",
)


class AccessPointTypeDef(TypedDict):
    Position: NotRequired[list[float]]


class CategoryTypeDef(TypedDict):
    Id: str
    Name: str
    LocalizedName: NotRequired[str]
    Primary: NotRequired[bool]


class AddressComponentMatchScoresTypeDef(TypedDict):
    Country: NotRequired[float]
    Region: NotRequired[float]
    SubRegion: NotRequired[float]
    Locality: NotRequired[float]
    District: NotRequired[float]
    SubDistrict: NotRequired[float]
    PostalCode: NotRequired[float]
    Block: NotRequired[float]
    SubBlock: NotRequired[float]
    Intersection: NotRequired[list[float]]
    AddressNumber: NotRequired[float]
    Building: NotRequired[float]


class PhonemeTranscriptionTypeDef(TypedDict):
    Value: NotRequired[str]
    Language: NotRequired[str]
    Preferred: NotRequired[bool]


class CountryTypeDef(TypedDict):
    Code2: NotRequired[str]
    Code3: NotRequired[str]
    Name: NotRequired[str]


class RegionTypeDef(TypedDict):
    Code: NotRequired[str]
    Name: NotRequired[str]


StreetComponentsTypeDef = TypedDict(
    "StreetComponentsTypeDef",
    {
        "BaseName": NotRequired[str],
        "Type": NotRequired[str],
        "TypePlacement": NotRequired[TypePlacementType],
        "TypeSeparator": NotRequired[str],
        "Prefix": NotRequired[str],
        "Suffix": NotRequired[str],
        "Direction": NotRequired[str],
        "Language": NotRequired[str],
    },
)


class SubRegionTypeDef(TypedDict):
    Code: NotRequired[str]
    Name: NotRequired[str]


class HighlightTypeDef(TypedDict):
    StartIndex: NotRequired[int]
    EndIndex: NotRequired[int]
    Value: NotRequired[str]


class FilterCircleTypeDef(TypedDict):
    Center: Sequence[float]
    Radius: int


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BusinessChainTypeDef(TypedDict):
    Name: NotRequired[str]
    Id: NotRequired[str]


class FoodTypeTypeDef(TypedDict):
    LocalizedName: str
    Id: NotRequired[str]
    Primary: NotRequired[bool]


class GeocodeFilterTypeDef(TypedDict):
    IncludeCountries: NotRequired[Sequence[str]]
    IncludePlaceTypes: NotRequired[Sequence[GeocodeFilterPlaceTypeType]]


class GeocodeQueryComponentsTypeDef(TypedDict):
    Country: NotRequired[str]
    Region: NotRequired[str]
    SubRegion: NotRequired[str]
    Locality: NotRequired[str]
    District: NotRequired[str]
    Street: NotRequired[str]
    AddressNumber: NotRequired[str]
    PostalCode: NotRequired[str]


class TimeZoneTypeDef(TypedDict):
    Name: str
    Offset: NotRequired[str]
    OffsetSeconds: NotRequired[int]


class GetPlaceRequestRequestTypeDef(TypedDict):
    PlaceId: str
    AdditionalFeatures: NotRequired[Sequence[GetPlaceAdditionalFeatureType]]
    Language: NotRequired[str]
    PoliticalView: NotRequired[str]
    IntendedUse: NotRequired[GetPlaceIntendedUseType]
    Key: NotRequired[str]


class OpeningHoursComponentsTypeDef(TypedDict):
    OpenTime: NotRequired[str]
    OpenDuration: NotRequired[str]
    Recurrence: NotRequired[str]


class UspsZipPlus4TypeDef(TypedDict):
    RecordTypeCode: NotRequired[RecordTypeCodeType]


class UspsZipTypeDef(TypedDict):
    ZipClassificationCode: NotRequired[ZipClassificationCodeType]


class QueryRefinementTypeDef(TypedDict):
    RefinedTerm: str
    OriginalTerm: str
    StartIndex: int
    EndIndex: int


class ReverseGeocodeFilterTypeDef(TypedDict):
    IncludePlaceTypes: NotRequired[Sequence[ReverseGeocodeFilterPlaceTypeType]]


class SearchNearbyFilterTypeDef(TypedDict):
    BoundingBox: NotRequired[Sequence[float]]
    IncludeCountries: NotRequired[Sequence[str]]
    IncludeCategories: NotRequired[Sequence[str]]
    ExcludeCategories: NotRequired[Sequence[str]]
    IncludeBusinessChains: NotRequired[Sequence[str]]
    ExcludeBusinessChains: NotRequired[Sequence[str]]
    IncludeFoodTypes: NotRequired[Sequence[str]]
    ExcludeFoodTypes: NotRequired[Sequence[str]]


class SuggestQueryResultTypeDef(TypedDict):
    QueryId: NotRequired[str]
    QueryType: NotRequired[QueryTypeType]


class AccessRestrictionTypeDef(TypedDict):
    Restricted: NotRequired[bool]
    Categories: NotRequired[list[CategoryTypeDef]]


class ContactDetailsTypeDef(TypedDict):
    Label: NotRequired[str]
    Value: NotRequired[str]
    Categories: NotRequired[list[CategoryTypeDef]]


class ComponentMatchScoresTypeDef(TypedDict):
    Title: NotRequired[float]
    Address: NotRequired[AddressComponentMatchScoresTypeDef]


class AddressComponentPhonemesTypeDef(TypedDict):
    Country: NotRequired[list[PhonemeTranscriptionTypeDef]]
    Region: NotRequired[list[PhonemeTranscriptionTypeDef]]
    SubRegion: NotRequired[list[PhonemeTranscriptionTypeDef]]
    Locality: NotRequired[list[PhonemeTranscriptionTypeDef]]
    District: NotRequired[list[PhonemeTranscriptionTypeDef]]
    SubDistrict: NotRequired[list[PhonemeTranscriptionTypeDef]]
    Block: NotRequired[list[PhonemeTranscriptionTypeDef]]
    SubBlock: NotRequired[list[PhonemeTranscriptionTypeDef]]
    Street: NotRequired[list[PhonemeTranscriptionTypeDef]]


class AddressTypeDef(TypedDict):
    Label: NotRequired[str]
    Country: NotRequired[CountryTypeDef]
    Region: NotRequired[RegionTypeDef]
    SubRegion: NotRequired[SubRegionTypeDef]
    Locality: NotRequired[str]
    District: NotRequired[str]
    SubDistrict: NotRequired[str]
    PostalCode: NotRequired[str]
    Block: NotRequired[str]
    SubBlock: NotRequired[str]
    Intersection: NotRequired[list[str]]
    Street: NotRequired[str]
    StreetComponents: NotRequired[list[StreetComponentsTypeDef]]
    AddressNumber: NotRequired[str]
    Building: NotRequired[str]


class CountryHighlightsTypeDef(TypedDict):
    Code: NotRequired[list[HighlightTypeDef]]
    Name: NotRequired[list[HighlightTypeDef]]


class RegionHighlightsTypeDef(TypedDict):
    Code: NotRequired[list[HighlightTypeDef]]
    Name: NotRequired[list[HighlightTypeDef]]


class SubRegionHighlightsTypeDef(TypedDict):
    Code: NotRequired[list[HighlightTypeDef]]
    Name: NotRequired[list[HighlightTypeDef]]


class SuggestAddressHighlightsTypeDef(TypedDict):
    Label: NotRequired[list[HighlightTypeDef]]


class AutocompleteFilterTypeDef(TypedDict):
    BoundingBox: NotRequired[Sequence[float]]
    Circle: NotRequired[FilterCircleTypeDef]
    IncludeCountries: NotRequired[Sequence[str]]
    IncludePlaceTypes: NotRequired[Sequence[AutocompleteFilterPlaceTypeType]]


class SearchTextFilterTypeDef(TypedDict):
    BoundingBox: NotRequired[Sequence[float]]
    Circle: NotRequired[FilterCircleTypeDef]
    IncludeCountries: NotRequired[Sequence[str]]


class SuggestFilterTypeDef(TypedDict):
    BoundingBox: NotRequired[Sequence[float]]
    Circle: NotRequired[FilterCircleTypeDef]
    IncludeCountries: NotRequired[Sequence[str]]


class GeocodeRequestRequestTypeDef(TypedDict):
    QueryText: NotRequired[str]
    QueryComponents: NotRequired[GeocodeQueryComponentsTypeDef]
    MaxResults: NotRequired[int]
    BiasPosition: NotRequired[Sequence[float]]
    Filter: NotRequired[GeocodeFilterTypeDef]
    AdditionalFeatures: NotRequired[Sequence[GeocodeAdditionalFeatureType]]
    Language: NotRequired[str]
    PoliticalView: NotRequired[str]
    IntendedUse: NotRequired[GeocodeIntendedUseType]
    Key: NotRequired[str]


class OpeningHoursTypeDef(TypedDict):
    Display: NotRequired[list[str]]
    OpenNow: NotRequired[bool]
    Components: NotRequired[list[OpeningHoursComponentsTypeDef]]
    Categories: NotRequired[list[CategoryTypeDef]]


class PostalCodeDetailsTypeDef(TypedDict):
    PostalCode: NotRequired[str]
    PostalAuthority: NotRequired[Literal["Usps"]]
    PostalCodeType: NotRequired[PostalCodeTypeType]
    UspsZip: NotRequired[UspsZipTypeDef]
    UspsZipPlus4: NotRequired[UspsZipPlus4TypeDef]


class ReverseGeocodeRequestRequestTypeDef(TypedDict):
    QueryPosition: Sequence[float]
    QueryRadius: NotRequired[int]
    MaxResults: NotRequired[int]
    Filter: NotRequired[ReverseGeocodeFilterTypeDef]
    AdditionalFeatures: NotRequired[Sequence[ReverseGeocodeAdditionalFeatureType]]
    Language: NotRequired[str]
    PoliticalView: NotRequired[str]
    IntendedUse: NotRequired[ReverseGeocodeIntendedUseType]
    Key: NotRequired[str]


class SearchNearbyRequestRequestTypeDef(TypedDict):
    QueryPosition: Sequence[float]
    QueryRadius: NotRequired[int]
    MaxResults: NotRequired[int]
    Filter: NotRequired[SearchNearbyFilterTypeDef]
    AdditionalFeatures: NotRequired[Sequence[SearchNearbyAdditionalFeatureType]]
    Language: NotRequired[str]
    PoliticalView: NotRequired[str]
    IntendedUse: NotRequired[SearchNearbyIntendedUseType]
    NextToken: NotRequired[str]
    Key: NotRequired[str]


class ContactsTypeDef(TypedDict):
    Phones: NotRequired[list[ContactDetailsTypeDef]]
    Faxes: NotRequired[list[ContactDetailsTypeDef]]
    Websites: NotRequired[list[ContactDetailsTypeDef]]
    Emails: NotRequired[list[ContactDetailsTypeDef]]


class MatchScoreDetailsTypeDef(TypedDict):
    Overall: NotRequired[float]
    Components: NotRequired[ComponentMatchScoresTypeDef]


class PhonemeDetailsTypeDef(TypedDict):
    Title: NotRequired[list[PhonemeTranscriptionTypeDef]]
    Address: NotRequired[AddressComponentPhonemesTypeDef]


class AutocompleteAddressHighlightsTypeDef(TypedDict):
    Label: NotRequired[list[HighlightTypeDef]]
    Country: NotRequired[CountryHighlightsTypeDef]
    Region: NotRequired[RegionHighlightsTypeDef]
    SubRegion: NotRequired[SubRegionHighlightsTypeDef]
    Locality: NotRequired[list[HighlightTypeDef]]
    District: NotRequired[list[HighlightTypeDef]]
    SubDistrict: NotRequired[list[HighlightTypeDef]]
    Street: NotRequired[list[HighlightTypeDef]]
    Block: NotRequired[list[HighlightTypeDef]]
    SubBlock: NotRequired[list[HighlightTypeDef]]
    Intersection: NotRequired[list[list[HighlightTypeDef]]]
    PostalCode: NotRequired[list[HighlightTypeDef]]
    AddressNumber: NotRequired[list[HighlightTypeDef]]
    Building: NotRequired[list[HighlightTypeDef]]


class SuggestHighlightsTypeDef(TypedDict):
    Title: NotRequired[list[HighlightTypeDef]]
    Address: NotRequired[SuggestAddressHighlightsTypeDef]


class AutocompleteRequestRequestTypeDef(TypedDict):
    QueryText: str
    MaxResults: NotRequired[int]
    BiasPosition: NotRequired[Sequence[float]]
    Filter: NotRequired[AutocompleteFilterTypeDef]
    PostalCodeMode: NotRequired[PostalCodeModeType]
    AdditionalFeatures: NotRequired[Sequence[Literal["Core"]]]
    Language: NotRequired[str]
    PoliticalView: NotRequired[str]
    IntendedUse: NotRequired[Literal["SingleUse"]]
    Key: NotRequired[str]


class SearchTextRequestRequestTypeDef(TypedDict):
    QueryText: NotRequired[str]
    QueryId: NotRequired[str]
    MaxResults: NotRequired[int]
    BiasPosition: NotRequired[Sequence[float]]
    Filter: NotRequired[SearchTextFilterTypeDef]
    AdditionalFeatures: NotRequired[Sequence[SearchTextAdditionalFeatureType]]
    Language: NotRequired[str]
    PoliticalView: NotRequired[str]
    IntendedUse: NotRequired[SearchTextIntendedUseType]
    NextToken: NotRequired[str]
    Key: NotRequired[str]


class SuggestRequestRequestTypeDef(TypedDict):
    QueryText: str
    MaxResults: NotRequired[int]
    MaxQueryRefinements: NotRequired[int]
    BiasPosition: NotRequired[Sequence[float]]
    Filter: NotRequired[SuggestFilterTypeDef]
    AdditionalFeatures: NotRequired[Sequence[SuggestAdditionalFeatureType]]
    Language: NotRequired[str]
    PoliticalView: NotRequired[str]
    IntendedUse: NotRequired[Literal["SingleUse"]]
    Key: NotRequired[str]


class ReverseGeocodeResultItemTypeDef(TypedDict):
    PlaceId: str
    PlaceType: PlaceTypeType
    Title: str
    Address: NotRequired[AddressTypeDef]
    AddressNumberCorrected: NotRequired[bool]
    PostalCodeDetails: NotRequired[list[PostalCodeDetailsTypeDef]]
    Position: NotRequired[list[float]]
    Distance: NotRequired[int]
    MapView: NotRequired[list[float]]
    Categories: NotRequired[list[CategoryTypeDef]]
    FoodTypes: NotRequired[list[FoodTypeTypeDef]]
    AccessPoints: NotRequired[list[AccessPointTypeDef]]
    TimeZone: NotRequired[TimeZoneTypeDef]
    PoliticalView: NotRequired[str]


class GeocodeResultItemTypeDef(TypedDict):
    PlaceId: str
    PlaceType: PlaceTypeType
    Title: str
    Address: NotRequired[AddressTypeDef]
    AddressNumberCorrected: NotRequired[bool]
    PostalCodeDetails: NotRequired[list[PostalCodeDetailsTypeDef]]
    Position: NotRequired[list[float]]
    Distance: NotRequired[int]
    MapView: NotRequired[list[float]]
    Categories: NotRequired[list[CategoryTypeDef]]
    FoodTypes: NotRequired[list[FoodTypeTypeDef]]
    AccessPoints: NotRequired[list[AccessPointTypeDef]]
    TimeZone: NotRequired[TimeZoneTypeDef]
    PoliticalView: NotRequired[str]
    MatchScores: NotRequired[MatchScoreDetailsTypeDef]


class GetPlaceResponseTypeDef(TypedDict):
    PlaceId: str
    PlaceType: PlaceTypeType
    Title: str
    PricingBucket: str
    Address: AddressTypeDef
    AddressNumberCorrected: bool
    PostalCodeDetails: list[PostalCodeDetailsTypeDef]
    Position: list[float]
    MapView: list[float]
    Categories: list[CategoryTypeDef]
    FoodTypes: list[FoodTypeTypeDef]
    BusinessChains: list[BusinessChainTypeDef]
    Contacts: ContactsTypeDef
    OpeningHours: list[OpeningHoursTypeDef]
    AccessPoints: list[AccessPointTypeDef]
    AccessRestrictions: list[AccessRestrictionTypeDef]
    TimeZone: TimeZoneTypeDef
    PoliticalView: str
    Phonemes: PhonemeDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchNearbyResultItemTypeDef(TypedDict):
    PlaceId: str
    PlaceType: PlaceTypeType
    Title: str
    Address: NotRequired[AddressTypeDef]
    AddressNumberCorrected: NotRequired[bool]
    Position: NotRequired[list[float]]
    Distance: NotRequired[int]
    MapView: NotRequired[list[float]]
    Categories: NotRequired[list[CategoryTypeDef]]
    FoodTypes: NotRequired[list[FoodTypeTypeDef]]
    BusinessChains: NotRequired[list[BusinessChainTypeDef]]
    Contacts: NotRequired[ContactsTypeDef]
    OpeningHours: NotRequired[list[OpeningHoursTypeDef]]
    AccessPoints: NotRequired[list[AccessPointTypeDef]]
    AccessRestrictions: NotRequired[list[AccessRestrictionTypeDef]]
    TimeZone: NotRequired[TimeZoneTypeDef]
    PoliticalView: NotRequired[str]
    Phonemes: NotRequired[PhonemeDetailsTypeDef]


class SearchTextResultItemTypeDef(TypedDict):
    PlaceId: str
    PlaceType: PlaceTypeType
    Title: str
    Address: NotRequired[AddressTypeDef]
    AddressNumberCorrected: NotRequired[bool]
    Position: NotRequired[list[float]]
    Distance: NotRequired[int]
    MapView: NotRequired[list[float]]
    Categories: NotRequired[list[CategoryTypeDef]]
    FoodTypes: NotRequired[list[FoodTypeTypeDef]]
    BusinessChains: NotRequired[list[BusinessChainTypeDef]]
    Contacts: NotRequired[ContactsTypeDef]
    OpeningHours: NotRequired[list[OpeningHoursTypeDef]]
    AccessPoints: NotRequired[list[AccessPointTypeDef]]
    AccessRestrictions: NotRequired[list[AccessRestrictionTypeDef]]
    TimeZone: NotRequired[TimeZoneTypeDef]
    PoliticalView: NotRequired[str]
    Phonemes: NotRequired[PhonemeDetailsTypeDef]


class SuggestPlaceResultTypeDef(TypedDict):
    PlaceId: NotRequired[str]
    PlaceType: NotRequired[PlaceTypeType]
    Address: NotRequired[AddressTypeDef]
    Position: NotRequired[list[float]]
    Distance: NotRequired[int]
    MapView: NotRequired[list[float]]
    Categories: NotRequired[list[CategoryTypeDef]]
    FoodTypes: NotRequired[list[FoodTypeTypeDef]]
    BusinessChains: NotRequired[list[BusinessChainTypeDef]]
    AccessPoints: NotRequired[list[AccessPointTypeDef]]
    AccessRestrictions: NotRequired[list[AccessRestrictionTypeDef]]
    TimeZone: NotRequired[TimeZoneTypeDef]
    PoliticalView: NotRequired[str]
    Phonemes: NotRequired[PhonemeDetailsTypeDef]


class AutocompleteHighlightsTypeDef(TypedDict):
    Title: NotRequired[list[HighlightTypeDef]]
    Address: NotRequired[AutocompleteAddressHighlightsTypeDef]


class ReverseGeocodeResponseTypeDef(TypedDict):
    PricingBucket: str
    ResultItems: list[ReverseGeocodeResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GeocodeResponseTypeDef(TypedDict):
    PricingBucket: str
    ResultItems: list[GeocodeResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SearchNearbyResponseTypeDef(TypedDict):
    PricingBucket: str
    ResultItems: list[SearchNearbyResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchTextResponseTypeDef(TypedDict):
    PricingBucket: str
    ResultItems: list[SearchTextResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SuggestResultItemTypeDef(TypedDict):
    Title: str
    SuggestResultItemType: SuggestResultItemTypeType
    Place: NotRequired[SuggestPlaceResultTypeDef]
    Query: NotRequired[SuggestQueryResultTypeDef]
    Highlights: NotRequired[SuggestHighlightsTypeDef]


class AutocompleteResultItemTypeDef(TypedDict):
    PlaceId: str
    PlaceType: PlaceTypeType
    Title: str
    Address: NotRequired[AddressTypeDef]
    Distance: NotRequired[int]
    Language: NotRequired[str]
    PoliticalView: NotRequired[str]
    Highlights: NotRequired[AutocompleteHighlightsTypeDef]


class SuggestResponseTypeDef(TypedDict):
    PricingBucket: str
    ResultItems: list[SuggestResultItemTypeDef]
    QueryRefinements: list[QueryRefinementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AutocompleteResponseTypeDef(TypedDict):
    PricingBucket: str
    ResultItems: list[AutocompleteResultItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
