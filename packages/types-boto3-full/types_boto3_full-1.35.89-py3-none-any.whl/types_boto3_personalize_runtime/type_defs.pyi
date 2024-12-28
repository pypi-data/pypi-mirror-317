"""
Type annotations for personalize-runtime service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_personalize_runtime/type_defs/)

Usage::

    ```python
    from types_boto3_personalize_runtime.type_defs import GetActionRecommendationsRequestRequestTypeDef

    data: GetActionRecommendationsRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Mapping, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetActionRecommendationsRequestRequestTypeDef",
    "GetActionRecommendationsResponseTypeDef",
    "GetPersonalizedRankingRequestRequestTypeDef",
    "GetPersonalizedRankingResponseTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetRecommendationsResponseTypeDef",
    "PredictedActionTypeDef",
    "PredictedItemTypeDef",
    "PromotionTypeDef",
    "ResponseMetadataTypeDef",
)

class GetActionRecommendationsRequestRequestTypeDef(TypedDict):
    campaignArn: NotRequired[str]
    userId: NotRequired[str]
    numResults: NotRequired[int]
    filterArn: NotRequired[str]
    filterValues: NotRequired[Mapping[str, str]]

class PredictedActionTypeDef(TypedDict):
    actionId: NotRequired[str]
    score: NotRequired[float]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetPersonalizedRankingRequestRequestTypeDef(TypedDict):
    campaignArn: str
    inputList: Sequence[str]
    userId: str
    context: NotRequired[Mapping[str, str]]
    filterArn: NotRequired[str]
    filterValues: NotRequired[Mapping[str, str]]
    metadataColumns: NotRequired[Mapping[str, Sequence[str]]]

class PredictedItemTypeDef(TypedDict):
    itemId: NotRequired[str]
    score: NotRequired[float]
    promotionName: NotRequired[str]
    metadata: NotRequired[dict[str, str]]
    reason: NotRequired[list[str]]

class PromotionTypeDef(TypedDict):
    name: NotRequired[str]
    percentPromotedItems: NotRequired[int]
    filterArn: NotRequired[str]
    filterValues: NotRequired[Mapping[str, str]]

class GetActionRecommendationsResponseTypeDef(TypedDict):
    actionList: list[PredictedActionTypeDef]
    recommendationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetPersonalizedRankingResponseTypeDef(TypedDict):
    personalizedRanking: list[PredictedItemTypeDef]
    recommendationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRecommendationsResponseTypeDef(TypedDict):
    itemList: list[PredictedItemTypeDef]
    recommendationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRecommendationsRequestRequestTypeDef(TypedDict):
    campaignArn: NotRequired[str]
    itemId: NotRequired[str]
    userId: NotRequired[str]
    numResults: NotRequired[int]
    context: NotRequired[Mapping[str, str]]
    filterArn: NotRequired[str]
    filterValues: NotRequired[Mapping[str, str]]
    recommenderArn: NotRequired[str]
    promotions: NotRequired[Sequence[PromotionTypeDef]]
    metadataColumns: NotRequired[Mapping[str, Sequence[str]]]
