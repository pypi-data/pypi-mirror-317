"""
Type annotations for cloudtrail service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cloudtrail.client import CloudTrailClient

    session = Session()
    client: CloudTrailClient = session.client("cloudtrail")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListImportFailuresPaginator,
    ListImportsPaginator,
    ListPublicKeysPaginator,
    ListTagsPaginator,
    ListTrailsPaginator,
    LookupEventsPaginator,
)
from .type_defs import (
    AddTagsRequestRequestTypeDef,
    CancelQueryRequestRequestTypeDef,
    CancelQueryResponseTypeDef,
    CreateChannelRequestRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateDashboardRequestRequestTypeDef,
    CreateDashboardResponseTypeDef,
    CreateEventDataStoreRequestRequestTypeDef,
    CreateEventDataStoreResponseTypeDef,
    CreateTrailRequestRequestTypeDef,
    CreateTrailResponseTypeDef,
    DeleteChannelRequestRequestTypeDef,
    DeleteDashboardRequestRequestTypeDef,
    DeleteEventDataStoreRequestRequestTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteTrailRequestRequestTypeDef,
    DeregisterOrganizationDelegatedAdminRequestRequestTypeDef,
    DescribeQueryRequestRequestTypeDef,
    DescribeQueryResponseTypeDef,
    DescribeTrailsRequestRequestTypeDef,
    DescribeTrailsResponseTypeDef,
    DisableFederationRequestRequestTypeDef,
    DisableFederationResponseTypeDef,
    EnableFederationRequestRequestTypeDef,
    EnableFederationResponseTypeDef,
    GenerateQueryRequestRequestTypeDef,
    GenerateQueryResponseTypeDef,
    GetChannelRequestRequestTypeDef,
    GetChannelResponseTypeDef,
    GetDashboardRequestRequestTypeDef,
    GetDashboardResponseTypeDef,
    GetEventDataStoreRequestRequestTypeDef,
    GetEventDataStoreResponseTypeDef,
    GetEventSelectorsRequestRequestTypeDef,
    GetEventSelectorsResponseTypeDef,
    GetImportRequestRequestTypeDef,
    GetImportResponseTypeDef,
    GetInsightSelectorsRequestRequestTypeDef,
    GetInsightSelectorsResponseTypeDef,
    GetQueryResultsRequestRequestTypeDef,
    GetQueryResultsResponseTypeDef,
    GetResourcePolicyRequestRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetTrailRequestRequestTypeDef,
    GetTrailResponseTypeDef,
    GetTrailStatusRequestRequestTypeDef,
    GetTrailStatusResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListDashboardsRequestRequestTypeDef,
    ListDashboardsResponseTypeDef,
    ListEventDataStoresRequestRequestTypeDef,
    ListEventDataStoresResponseTypeDef,
    ListImportFailuresRequestRequestTypeDef,
    ListImportFailuresResponseTypeDef,
    ListImportsRequestRequestTypeDef,
    ListImportsResponseTypeDef,
    ListInsightsMetricDataRequestRequestTypeDef,
    ListInsightsMetricDataResponseTypeDef,
    ListPublicKeysRequestRequestTypeDef,
    ListPublicKeysResponseTypeDef,
    ListQueriesRequestRequestTypeDef,
    ListQueriesResponseTypeDef,
    ListTagsRequestRequestTypeDef,
    ListTagsResponseTypeDef,
    ListTrailsRequestRequestTypeDef,
    ListTrailsResponseTypeDef,
    LookupEventsRequestRequestTypeDef,
    LookupEventsResponseTypeDef,
    PutEventSelectorsRequestRequestTypeDef,
    PutEventSelectorsResponseTypeDef,
    PutInsightSelectorsRequestRequestTypeDef,
    PutInsightSelectorsResponseTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    RegisterOrganizationDelegatedAdminRequestRequestTypeDef,
    RemoveTagsRequestRequestTypeDef,
    RestoreEventDataStoreRequestRequestTypeDef,
    RestoreEventDataStoreResponseTypeDef,
    StartDashboardRefreshRequestRequestTypeDef,
    StartDashboardRefreshResponseTypeDef,
    StartEventDataStoreIngestionRequestRequestTypeDef,
    StartImportRequestRequestTypeDef,
    StartImportResponseTypeDef,
    StartLoggingRequestRequestTypeDef,
    StartQueryRequestRequestTypeDef,
    StartQueryResponseTypeDef,
    StopEventDataStoreIngestionRequestRequestTypeDef,
    StopImportRequestRequestTypeDef,
    StopImportResponseTypeDef,
    StopLoggingRequestRequestTypeDef,
    UpdateChannelRequestRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateDashboardRequestRequestTypeDef,
    UpdateDashboardResponseTypeDef,
    UpdateEventDataStoreRequestRequestTypeDef,
    UpdateEventDataStoreResponseTypeDef,
    UpdateTrailRequestRequestTypeDef,
    UpdateTrailResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CloudTrailClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    AccountHasOngoingImportException: type[BotocoreClientError]
    AccountNotFoundException: type[BotocoreClientError]
    AccountNotRegisteredException: type[BotocoreClientError]
    AccountRegisteredException: type[BotocoreClientError]
    CannotDelegateManagementAccountException: type[BotocoreClientError]
    ChannelARNInvalidException: type[BotocoreClientError]
    ChannelAlreadyExistsException: type[BotocoreClientError]
    ChannelExistsForEDSException: type[BotocoreClientError]
    ChannelMaxLimitExceededException: type[BotocoreClientError]
    ChannelNotFoundException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    CloudTrailARNInvalidException: type[BotocoreClientError]
    CloudTrailAccessNotEnabledException: type[BotocoreClientError]
    CloudTrailInvalidClientTokenIdException: type[BotocoreClientError]
    CloudWatchLogsDeliveryUnavailableException: type[BotocoreClientError]
    ConcurrentModificationException: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    DelegatedAdminAccountLimitExceededException: type[BotocoreClientError]
    EventDataStoreARNInvalidException: type[BotocoreClientError]
    EventDataStoreAlreadyExistsException: type[BotocoreClientError]
    EventDataStoreFederationEnabledException: type[BotocoreClientError]
    EventDataStoreHasOngoingImportException: type[BotocoreClientError]
    EventDataStoreMaxLimitExceededException: type[BotocoreClientError]
    EventDataStoreNotFoundException: type[BotocoreClientError]
    EventDataStoreTerminationProtectedException: type[BotocoreClientError]
    GenerateResponseException: type[BotocoreClientError]
    ImportNotFoundException: type[BotocoreClientError]
    InactiveEventDataStoreException: type[BotocoreClientError]
    InactiveQueryException: type[BotocoreClientError]
    InsightNotEnabledException: type[BotocoreClientError]
    InsufficientDependencyServiceAccessPermissionException: type[BotocoreClientError]
    InsufficientEncryptionPolicyException: type[BotocoreClientError]
    InsufficientS3BucketPolicyException: type[BotocoreClientError]
    InsufficientSnsTopicPolicyException: type[BotocoreClientError]
    InvalidCloudWatchLogsLogGroupArnException: type[BotocoreClientError]
    InvalidCloudWatchLogsRoleArnException: type[BotocoreClientError]
    InvalidDateRangeException: type[BotocoreClientError]
    InvalidEventCategoryException: type[BotocoreClientError]
    InvalidEventDataStoreCategoryException: type[BotocoreClientError]
    InvalidEventDataStoreStatusException: type[BotocoreClientError]
    InvalidEventSelectorsException: type[BotocoreClientError]
    InvalidHomeRegionException: type[BotocoreClientError]
    InvalidImportSourceException: type[BotocoreClientError]
    InvalidInsightSelectorsException: type[BotocoreClientError]
    InvalidKmsKeyIdException: type[BotocoreClientError]
    InvalidLookupAttributesException: type[BotocoreClientError]
    InvalidMaxResultsException: type[BotocoreClientError]
    InvalidNextTokenException: type[BotocoreClientError]
    InvalidParameterCombinationException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    InvalidQueryStatementException: type[BotocoreClientError]
    InvalidQueryStatusException: type[BotocoreClientError]
    InvalidS3BucketNameException: type[BotocoreClientError]
    InvalidS3PrefixException: type[BotocoreClientError]
    InvalidSnsTopicNameException: type[BotocoreClientError]
    InvalidSourceException: type[BotocoreClientError]
    InvalidTagParameterException: type[BotocoreClientError]
    InvalidTimeRangeException: type[BotocoreClientError]
    InvalidTokenException: type[BotocoreClientError]
    InvalidTrailNameException: type[BotocoreClientError]
    KmsException: type[BotocoreClientError]
    KmsKeyDisabledException: type[BotocoreClientError]
    KmsKeyNotFoundException: type[BotocoreClientError]
    MaxConcurrentQueriesException: type[BotocoreClientError]
    MaximumNumberOfTrailsExceededException: type[BotocoreClientError]
    NoManagementAccountSLRExistsException: type[BotocoreClientError]
    NotOrganizationManagementAccountException: type[BotocoreClientError]
    NotOrganizationMasterAccountException: type[BotocoreClientError]
    OperationNotPermittedException: type[BotocoreClientError]
    OrganizationNotInAllFeaturesModeException: type[BotocoreClientError]
    OrganizationsNotInUseException: type[BotocoreClientError]
    QueryIdNotFoundException: type[BotocoreClientError]
    ResourceARNNotValidException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ResourcePolicyNotFoundException: type[BotocoreClientError]
    ResourcePolicyNotValidException: type[BotocoreClientError]
    ResourceTypeNotSupportedException: type[BotocoreClientError]
    S3BucketDoesNotExistException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    TagsLimitExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TrailAlreadyExistsException: type[BotocoreClientError]
    TrailNotFoundException: type[BotocoreClientError]
    TrailNotProvidedException: type[BotocoreClientError]
    UnsupportedOperationException: type[BotocoreClientError]

class CloudTrailClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudTrailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#generate_presigned_url)
        """

    def add_tags(self, **kwargs: Unpack[AddTagsRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Adds one or more tags to a trail, event data store, dashboard, or channel, up
        to a limit of 50.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/add_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#add_tags)
        """

    def cancel_query(
        self, **kwargs: Unpack[CancelQueryRequestRequestTypeDef]
    ) -> CancelQueryResponseTypeDef:
        """
        Cancels a query if the query is not in a terminated state, such as
        <code>CANCELLED</code>, <code>FAILED</code>, <code>TIMED_OUT</code>, or
        <code>FINISHED</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/cancel_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#cancel_query)
        """

    def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel for CloudTrail to ingest events from a partner or external
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/create_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#create_channel)
        """

    def create_dashboard(
        self, **kwargs: Unpack[CreateDashboardRequestRequestTypeDef]
    ) -> CreateDashboardResponseTypeDef:
        """
        Creates a custom dashboard or the Highlights dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/create_dashboard.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#create_dashboard)
        """

    def create_event_data_store(
        self, **kwargs: Unpack[CreateEventDataStoreRequestRequestTypeDef]
    ) -> CreateEventDataStoreResponseTypeDef:
        """
        Creates a new event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/create_event_data_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#create_event_data_store)
        """

    def create_trail(
        self, **kwargs: Unpack[CreateTrailRequestRequestTypeDef]
    ) -> CreateTrailResponseTypeDef:
        """
        Creates a trail that specifies the settings for delivery of log data to an
        Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/create_trail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#create_trail)
        """

    def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#delete_channel)
        """

    def delete_dashboard(
        self, **kwargs: Unpack[DeleteDashboardRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the specified dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_dashboard.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#delete_dashboard)
        """

    def delete_event_data_store(
        self, **kwargs: Unpack[DeleteEventDataStoreRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disables the event data store specified by <code>EventDataStore</code>, which
        accepts an event data store ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_event_data_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#delete_event_data_store)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the resource-based policy attached to the CloudTrail event data store,
        dashboard, or channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#delete_resource_policy)
        """

    def delete_trail(self, **kwargs: Unpack[DeleteTrailRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes a trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/delete_trail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#delete_trail)
        """

    def deregister_organization_delegated_admin(
        self, **kwargs: Unpack[DeregisterOrganizationDelegatedAdminRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes CloudTrail delegated administrator permissions from a member account in
        an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/deregister_organization_delegated_admin.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#deregister_organization_delegated_admin)
        """

    def describe_query(
        self, **kwargs: Unpack[DescribeQueryRequestRequestTypeDef]
    ) -> DescribeQueryResponseTypeDef:
        """
        Returns metadata about a query, including query run time in milliseconds,
        number of events scanned and matched, and query status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/describe_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#describe_query)
        """

    def describe_trails(
        self, **kwargs: Unpack[DescribeTrailsRequestRequestTypeDef]
    ) -> DescribeTrailsResponseTypeDef:
        """
        Retrieves settings for one or more trails associated with the current Region
        for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/describe_trails.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#describe_trails)
        """

    def disable_federation(
        self, **kwargs: Unpack[DisableFederationRequestRequestTypeDef]
    ) -> DisableFederationResponseTypeDef:
        """
        Disables Lake query federation on the specified event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/disable_federation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#disable_federation)
        """

    def enable_federation(
        self, **kwargs: Unpack[EnableFederationRequestRequestTypeDef]
    ) -> EnableFederationResponseTypeDef:
        """
        Enables Lake query federation on the specified event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/enable_federation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#enable_federation)
        """

    def generate_query(
        self, **kwargs: Unpack[GenerateQueryRequestRequestTypeDef]
    ) -> GenerateQueryResponseTypeDef:
        """
        Generates a query from a natural language prompt.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/generate_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#generate_query)
        """

    def get_channel(
        self, **kwargs: Unpack[GetChannelRequestRequestTypeDef]
    ) -> GetChannelResponseTypeDef:
        """
        Returns information about a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_channel)
        """

    def get_dashboard(
        self, **kwargs: Unpack[GetDashboardRequestRequestTypeDef]
    ) -> GetDashboardResponseTypeDef:
        """
        Returns the specified dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_dashboard.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_dashboard)
        """

    def get_event_data_store(
        self, **kwargs: Unpack[GetEventDataStoreRequestRequestTypeDef]
    ) -> GetEventDataStoreResponseTypeDef:
        """
        Returns information about an event data store specified as either an ARN or the
        ID portion of the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_event_data_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_event_data_store)
        """

    def get_event_selectors(
        self, **kwargs: Unpack[GetEventSelectorsRequestRequestTypeDef]
    ) -> GetEventSelectorsResponseTypeDef:
        """
        Describes the settings for the event selectors that you configured for your
        trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_event_selectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_event_selectors)
        """

    def get_import(
        self, **kwargs: Unpack[GetImportRequestRequestTypeDef]
    ) -> GetImportResponseTypeDef:
        """
        Returns information about a specific import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_import.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_import)
        """

    def get_insight_selectors(
        self, **kwargs: Unpack[GetInsightSelectorsRequestRequestTypeDef]
    ) -> GetInsightSelectorsResponseTypeDef:
        """
        Describes the settings for the Insights event selectors that you configured for
        your trail or event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_insight_selectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_insight_selectors)
        """

    def get_query_results(
        self, **kwargs: Unpack[GetQueryResultsRequestRequestTypeDef]
    ) -> GetQueryResultsResponseTypeDef:
        """
        Gets event data results of a query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_query_results.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_query_results)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves the JSON text of the resource-based policy document attached to the
        CloudTrail event data store, dashboard, or channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_resource_policy)
        """

    def get_trail(self, **kwargs: Unpack[GetTrailRequestRequestTypeDef]) -> GetTrailResponseTypeDef:
        """
        Returns settings information for a specified trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_trail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_trail)
        """

    def get_trail_status(
        self, **kwargs: Unpack[GetTrailStatusRequestRequestTypeDef]
    ) -> GetTrailStatusResponseTypeDef:
        """
        Returns a JSON-formatted list of information about the specified trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_trail_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_trail_status)
        """

    def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Lists the channels in the current account, and their source names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_channels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_channels)
        """

    def list_dashboards(
        self, **kwargs: Unpack[ListDashboardsRequestRequestTypeDef]
    ) -> ListDashboardsResponseTypeDef:
        """
        Returns information about all dashboards in the account, in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_dashboards.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_dashboards)
        """

    def list_event_data_stores(
        self, **kwargs: Unpack[ListEventDataStoresRequestRequestTypeDef]
    ) -> ListEventDataStoresResponseTypeDef:
        """
        Returns information about all event data stores in the account, in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_event_data_stores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_event_data_stores)
        """

    def list_import_failures(
        self, **kwargs: Unpack[ListImportFailuresRequestRequestTypeDef]
    ) -> ListImportFailuresResponseTypeDef:
        """
        Returns a list of failures for the specified import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_import_failures.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_import_failures)
        """

    def list_imports(
        self, **kwargs: Unpack[ListImportsRequestRequestTypeDef]
    ) -> ListImportsResponseTypeDef:
        """
        Returns information on all imports, or a select set of imports by
        <code>ImportStatus</code> or <code>Destination</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_imports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_imports)
        """

    def list_insights_metric_data(
        self, **kwargs: Unpack[ListInsightsMetricDataRequestRequestTypeDef]
    ) -> ListInsightsMetricDataResponseTypeDef:
        """
        Returns Insights metrics data for trails that have enabled Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_insights_metric_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_insights_metric_data)
        """

    def list_public_keys(
        self, **kwargs: Unpack[ListPublicKeysRequestRequestTypeDef]
    ) -> ListPublicKeysResponseTypeDef:
        """
        Returns all public keys whose private keys were used to sign the digest files
        within the specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_public_keys.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_public_keys)
        """

    def list_queries(
        self, **kwargs: Unpack[ListQueriesRequestRequestTypeDef]
    ) -> ListQueriesResponseTypeDef:
        """
        Returns a list of queries and query statuses for the past seven days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_queries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_queries)
        """

    def list_tags(self, **kwargs: Unpack[ListTagsRequestRequestTypeDef]) -> ListTagsResponseTypeDef:
        """
        Lists the tags for the specified trails, event data stores, dashboards, or
        channels in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_tags)
        """

    def list_trails(
        self, **kwargs: Unpack[ListTrailsRequestRequestTypeDef]
    ) -> ListTrailsResponseTypeDef:
        """
        Lists trails that are in the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/list_trails.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#list_trails)
        """

    def lookup_events(
        self, **kwargs: Unpack[LookupEventsRequestRequestTypeDef]
    ) -> LookupEventsResponseTypeDef:
        """
        Looks up <a
        href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-management-events">management
        events</a> or <a
        href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-insights-events">C...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/lookup_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#lookup_events)
        """

    def put_event_selectors(
        self, **kwargs: Unpack[PutEventSelectorsRequestRequestTypeDef]
    ) -> PutEventSelectorsResponseTypeDef:
        """
        Configures event selectors (also referred to as <i>basic event selectors</i>)
        or advanced event selectors for your trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/put_event_selectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#put_event_selectors)
        """

    def put_insight_selectors(
        self, **kwargs: Unpack[PutInsightSelectorsRequestRequestTypeDef]
    ) -> PutInsightSelectorsResponseTypeDef:
        """
        Lets you enable Insights event logging by specifying the Insights selectors
        that you want to enable on an existing trail or event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/put_insight_selectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#put_insight_selectors)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Attaches a resource-based permission policy to a CloudTrail event data store,
        dashboard, or channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#put_resource_policy)
        """

    def register_organization_delegated_admin(
        self, **kwargs: Unpack[RegisterOrganizationDelegatedAdminRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Registers an organization's member account as the CloudTrail <a
        href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-delegated-administrator.html">delegated
        administrator</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/register_organization_delegated_admin.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#register_organization_delegated_admin)
        """

    def remove_tags(self, **kwargs: Unpack[RemoveTagsRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Removes the specified tags from a trail, event data store, dashboard, or
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/remove_tags.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#remove_tags)
        """

    def restore_event_data_store(
        self, **kwargs: Unpack[RestoreEventDataStoreRequestRequestTypeDef]
    ) -> RestoreEventDataStoreResponseTypeDef:
        """
        Restores a deleted event data store specified by <code>EventDataStore</code>,
        which accepts an event data store ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/restore_event_data_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#restore_event_data_store)
        """

    def start_dashboard_refresh(
        self, **kwargs: Unpack[StartDashboardRefreshRequestRequestTypeDef]
    ) -> StartDashboardRefreshResponseTypeDef:
        """
        Starts a refresh of the specified dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_dashboard_refresh.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#start_dashboard_refresh)
        """

    def start_event_data_store_ingestion(
        self, **kwargs: Unpack[StartEventDataStoreIngestionRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Starts the ingestion of live events on an event data store specified as either
        an ARN or the ID portion of the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_event_data_store_ingestion.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#start_event_data_store_ingestion)
        """

    def start_import(
        self, **kwargs: Unpack[StartImportRequestRequestTypeDef]
    ) -> StartImportResponseTypeDef:
        """
        Starts an import of logged trail events from a source S3 bucket to a
        destination event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_import.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#start_import)
        """

    def start_logging(self, **kwargs: Unpack[StartLoggingRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Starts the recording of Amazon Web Services API calls and log file delivery for
        a trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_logging.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#start_logging)
        """

    def start_query(
        self, **kwargs: Unpack[StartQueryRequestRequestTypeDef]
    ) -> StartQueryResponseTypeDef:
        """
        Starts a CloudTrail Lake query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/start_query.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#start_query)
        """

    def stop_event_data_store_ingestion(
        self, **kwargs: Unpack[StopEventDataStoreIngestionRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Stops the ingestion of live events on an event data store specified as either
        an ARN or the ID portion of the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/stop_event_data_store_ingestion.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#stop_event_data_store_ingestion)
        """

    def stop_import(
        self, **kwargs: Unpack[StopImportRequestRequestTypeDef]
    ) -> StopImportResponseTypeDef:
        """
        Stops a specified import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/stop_import.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#stop_import)
        """

    def stop_logging(self, **kwargs: Unpack[StopLoggingRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Suspends the recording of Amazon Web Services API calls and log file delivery
        for the specified trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/stop_logging.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#stop_logging)
        """

    def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates a channel specified by a required channel ARN or UUID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/update_channel.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#update_channel)
        """

    def update_dashboard(
        self, **kwargs: Unpack[UpdateDashboardRequestRequestTypeDef]
    ) -> UpdateDashboardResponseTypeDef:
        """
        Updates the specified dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/update_dashboard.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#update_dashboard)
        """

    def update_event_data_store(
        self, **kwargs: Unpack[UpdateEventDataStoreRequestRequestTypeDef]
    ) -> UpdateEventDataStoreResponseTypeDef:
        """
        Updates an event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/update_event_data_store.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#update_event_data_store)
        """

    def update_trail(
        self, **kwargs: Unpack[UpdateTrailRequestRequestTypeDef]
    ) -> UpdateTrailResponseTypeDef:
        """
        Updates trail settings that control what events you are logging, and how to
        handle log files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/update_trail.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#update_trail)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_import_failures"]
    ) -> ListImportFailuresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_imports"]
    ) -> ListImportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_public_keys"]
    ) -> ListPublicKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags"]
    ) -> ListTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_trails"]
    ) -> ListTrailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["lookup_events"]
    ) -> LookupEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cloudtrail/client/#get_paginator)
        """
