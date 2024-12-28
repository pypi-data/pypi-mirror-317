"""
Type annotations for snowball service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_snowball.client import SnowballClient

    session = Session()
    client: SnowballClient = session.client("snowball")
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
    DescribeAddressesPaginator,
    ListClusterJobsPaginator,
    ListClustersPaginator,
    ListCompatibleImagesPaginator,
    ListJobsPaginator,
    ListLongTermPricingPaginator,
)
from .type_defs import (
    CancelClusterRequestRequestTypeDef,
    CancelJobRequestRequestTypeDef,
    CreateAddressRequestRequestTypeDef,
    CreateAddressResultTypeDef,
    CreateClusterRequestRequestTypeDef,
    CreateClusterResultTypeDef,
    CreateJobRequestRequestTypeDef,
    CreateJobResultTypeDef,
    CreateLongTermPricingRequestRequestTypeDef,
    CreateLongTermPricingResultTypeDef,
    CreateReturnShippingLabelRequestRequestTypeDef,
    CreateReturnShippingLabelResultTypeDef,
    DescribeAddressesRequestRequestTypeDef,
    DescribeAddressesResultTypeDef,
    DescribeAddressRequestRequestTypeDef,
    DescribeAddressResultTypeDef,
    DescribeClusterRequestRequestTypeDef,
    DescribeClusterResultTypeDef,
    DescribeJobRequestRequestTypeDef,
    DescribeJobResultTypeDef,
    DescribeReturnShippingLabelRequestRequestTypeDef,
    DescribeReturnShippingLabelResultTypeDef,
    GetJobManifestRequestRequestTypeDef,
    GetJobManifestResultTypeDef,
    GetJobUnlockCodeRequestRequestTypeDef,
    GetJobUnlockCodeResultTypeDef,
    GetSnowballUsageResultTypeDef,
    GetSoftwareUpdatesRequestRequestTypeDef,
    GetSoftwareUpdatesResultTypeDef,
    ListClusterJobsRequestRequestTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersRequestRequestTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesRequestRequestTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResultTypeDef,
    ListLongTermPricingRequestRequestTypeDef,
    ListLongTermPricingResultTypeDef,
    ListPickupLocationsRequestRequestTypeDef,
    ListPickupLocationsResultTypeDef,
    ListServiceVersionsRequestRequestTypeDef,
    ListServiceVersionsResultTypeDef,
    UpdateClusterRequestRequestTypeDef,
    UpdateJobRequestRequestTypeDef,
    UpdateJobShipmentStateRequestRequestTypeDef,
    UpdateLongTermPricingRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SnowballClient",)

class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ClusterLimitExceededException: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    Ec2RequestFailedException: type[BotocoreClientError]
    InvalidAddressException: type[BotocoreClientError]
    InvalidInputCombinationException: type[BotocoreClientError]
    InvalidJobStateException: type[BotocoreClientError]
    InvalidNextTokenException: type[BotocoreClientError]
    InvalidResourceException: type[BotocoreClientError]
    KMSRequestFailedException: type[BotocoreClientError]
    ReturnShippingLabelAlreadyExistsException: type[BotocoreClientError]
    UnsupportedAddressException: type[BotocoreClientError]

class SnowballClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SnowballClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#generate_presigned_url)
        """

    def cancel_cluster(
        self, **kwargs: Unpack[CancelClusterRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Cancels a cluster job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/cancel_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#cancel_cluster)
        """

    def cancel_job(self, **kwargs: Unpack[CancelJobRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Cancels the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/cancel_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#cancel_job)
        """

    def create_address(
        self, **kwargs: Unpack[CreateAddressRequestRequestTypeDef]
    ) -> CreateAddressResultTypeDef:
        """
        Creates an address for a Snow device to be shipped to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_address.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#create_address)
        """

    def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResultTypeDef:
        """
        Creates an empty cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#create_cluster)
        """

    def create_job(
        self, **kwargs: Unpack[CreateJobRequestRequestTypeDef]
    ) -> CreateJobResultTypeDef:
        """
        Creates a job to import or export data between Amazon S3 and your on-premises
        data center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#create_job)
        """

    def create_long_term_pricing(
        self, **kwargs: Unpack[CreateLongTermPricingRequestRequestTypeDef]
    ) -> CreateLongTermPricingResultTypeDef:
        """
        Creates a job with the long-term usage option for a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_long_term_pricing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#create_long_term_pricing)
        """

    def create_return_shipping_label(
        self, **kwargs: Unpack[CreateReturnShippingLabelRequestRequestTypeDef]
    ) -> CreateReturnShippingLabelResultTypeDef:
        """
        Creates a shipping label that will be used to return the Snow device to Amazon
        Web Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/create_return_shipping_label.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#create_return_shipping_label)
        """

    def describe_address(
        self, **kwargs: Unpack[DescribeAddressRequestRequestTypeDef]
    ) -> DescribeAddressResultTypeDef:
        """
        Takes an <code>AddressId</code> and returns specific details about that address
        in the form of an <code>Address</code> object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_address.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#describe_address)
        """

    def describe_addresses(
        self, **kwargs: Unpack[DescribeAddressesRequestRequestTypeDef]
    ) -> DescribeAddressesResultTypeDef:
        """
        Returns a specified number of <code>ADDRESS</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_addresses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#describe_addresses)
        """

    def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterRequestRequestTypeDef]
    ) -> DescribeClusterResultTypeDef:
        """
        Returns information about a specific cluster including shipping information,
        cluster status, and other important metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#describe_cluster)
        """

    def describe_job(
        self, **kwargs: Unpack[DescribeJobRequestRequestTypeDef]
    ) -> DescribeJobResultTypeDef:
        """
        Returns information about a specific job including shipping information, job
        status, and other important metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#describe_job)
        """

    def describe_return_shipping_label(
        self, **kwargs: Unpack[DescribeReturnShippingLabelRequestRequestTypeDef]
    ) -> DescribeReturnShippingLabelResultTypeDef:
        """
        Information on the shipping label of a Snow device that is being returned to
        Amazon Web Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/describe_return_shipping_label.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#describe_return_shipping_label)
        """

    def get_job_manifest(
        self, **kwargs: Unpack[GetJobManifestRequestRequestTypeDef]
    ) -> GetJobManifestResultTypeDef:
        """
        Returns a link to an Amazon S3 presigned URL for the manifest file associated
        with the specified <code>JobId</code> value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_job_manifest.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_job_manifest)
        """

    def get_job_unlock_code(
        self, **kwargs: Unpack[GetJobUnlockCodeRequestRequestTypeDef]
    ) -> GetJobUnlockCodeResultTypeDef:
        """
        Returns the <code>UnlockCode</code> code value for the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_job_unlock_code.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_job_unlock_code)
        """

    def get_snowball_usage(self) -> GetSnowballUsageResultTypeDef:
        """
        Returns information about the Snow Family service limit for your account, and
        also the number of Snow devices your account has in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_snowball_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_snowball_usage)
        """

    def get_software_updates(
        self, **kwargs: Unpack[GetSoftwareUpdatesRequestRequestTypeDef]
    ) -> GetSoftwareUpdatesResultTypeDef:
        """
        Returns an Amazon S3 presigned URL for an update file associated with a
        specified <code>JobId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_software_updates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_software_updates)
        """

    def list_cluster_jobs(
        self, **kwargs: Unpack[ListClusterJobsRequestRequestTypeDef]
    ) -> ListClusterJobsResultTypeDef:
        """
        Returns an array of <code>JobListEntry</code> objects of the specified length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_cluster_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#list_cluster_jobs)
        """

    def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestRequestTypeDef]
    ) -> ListClustersResultTypeDef:
        """
        Returns an array of <code>ClusterListEntry</code> objects of the specified
        length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_clusters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#list_clusters)
        """

    def list_compatible_images(
        self, **kwargs: Unpack[ListCompatibleImagesRequestRequestTypeDef]
    ) -> ListCompatibleImagesResultTypeDef:
        """
        This action returns a list of the different Amazon EC2-compatible Amazon
        Machine Images (AMIs) that are owned by your Amazon Web Services accountthat
        would be supported for use on a Snow device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_compatible_images.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#list_compatible_images)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]) -> ListJobsResultTypeDef:
        """
        Returns an array of <code>JobListEntry</code> objects of the specified length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#list_jobs)
        """

    def list_long_term_pricing(
        self, **kwargs: Unpack[ListLongTermPricingRequestRequestTypeDef]
    ) -> ListLongTermPricingResultTypeDef:
        """
        Lists all long-term pricing types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_long_term_pricing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#list_long_term_pricing)
        """

    def list_pickup_locations(
        self, **kwargs: Unpack[ListPickupLocationsRequestRequestTypeDef]
    ) -> ListPickupLocationsResultTypeDef:
        """
        A list of locations from which the customer can choose to pickup a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_pickup_locations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#list_pickup_locations)
        """

    def list_service_versions(
        self, **kwargs: Unpack[ListServiceVersionsRequestRequestTypeDef]
    ) -> ListServiceVersionsResultTypeDef:
        """
        Lists all supported versions for Snow on-device services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/list_service_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#list_service_versions)
        """

    def update_cluster(
        self, **kwargs: Unpack[UpdateClusterRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        While a cluster's <code>ClusterState</code> value is in the
        <code>AwaitingQuorum</code> state, you can update some of the information
        associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/update_cluster.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#update_cluster)
        """

    def update_job(self, **kwargs: Unpack[UpdateJobRequestRequestTypeDef]) -> dict[str, Any]:
        """
        While a job's <code>JobState</code> value is <code>New</code>, you can update
        some of the information associated with a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/update_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#update_job)
        """

    def update_job_shipment_state(
        self, **kwargs: Unpack[UpdateJobShipmentStateRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the state when a shipment state changes to a different state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/update_job_shipment_state.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#update_job_shipment_state)
        """

    def update_long_term_pricing(
        self, **kwargs: Unpack[UpdateLongTermPricingRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the long-term pricing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/update_long_term_pricing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#update_long_term_pricing)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_addresses"]
    ) -> DescribeAddressesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cluster_jobs"]
    ) -> ListClusterJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_clusters"]
    ) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_compatible_images"]
    ) -> ListCompatibleImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs"]
    ) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_long_term_pricing"]
    ) -> ListLongTermPricingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/client/#get_paginator)
        """
