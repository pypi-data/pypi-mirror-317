"""
Type annotations for importexport service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_importexport.client import ImportExportClient

    session = Session()
    client: ImportExportClient = session.client("importexport")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListJobsPaginator
from .type_defs import (
    CancelJobInputRequestTypeDef,
    CancelJobOutputTypeDef,
    CreateJobInputRequestTypeDef,
    CreateJobOutputTypeDef,
    GetShippingLabelInputRequestTypeDef,
    GetShippingLabelOutputTypeDef,
    GetStatusInputRequestTypeDef,
    GetStatusOutputTypeDef,
    ListJobsInputRequestTypeDef,
    ListJobsOutputTypeDef,
    UpdateJobInputRequestTypeDef,
    UpdateJobOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ImportExportClient",)

class Exceptions(BaseClientExceptions):
    BucketPermissionException: type[BotocoreClientError]
    CanceledJobIdException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    CreateJobQuotaExceededException: type[BotocoreClientError]
    ExpiredJobIdException: type[BotocoreClientError]
    InvalidAccessKeyIdException: type[BotocoreClientError]
    InvalidAddressException: type[BotocoreClientError]
    InvalidCustomsException: type[BotocoreClientError]
    InvalidFileSystemException: type[BotocoreClientError]
    InvalidJobIdException: type[BotocoreClientError]
    InvalidManifestFieldException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    InvalidVersionException: type[BotocoreClientError]
    MalformedManifestException: type[BotocoreClientError]
    MissingCustomsException: type[BotocoreClientError]
    MissingManifestFieldException: type[BotocoreClientError]
    MissingParameterException: type[BotocoreClientError]
    MultipleRegionsException: type[BotocoreClientError]
    NoSuchBucketException: type[BotocoreClientError]
    UnableToCancelJobIdException: type[BotocoreClientError]
    UnableToUpdateJobIdException: type[BotocoreClientError]

class ImportExportClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ImportExportClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#generate_presigned_url)
        """

    def cancel_job(self, **kwargs: Unpack[CancelJobInputRequestTypeDef]) -> CancelJobOutputTypeDef:
        """
        This operation cancels a specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/cancel_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#cancel_job)
        """

    def create_job(self, **kwargs: Unpack[CreateJobInputRequestTypeDef]) -> CreateJobOutputTypeDef:
        """
        This operation initiates the process of scheduling an upload or download of
        your data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/create_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#create_job)
        """

    def get_shipping_label(
        self, **kwargs: Unpack[GetShippingLabelInputRequestTypeDef]
    ) -> GetShippingLabelOutputTypeDef:
        """
        This operation generates a pre-paid UPS shipping label that you will use to
        ship your device to AWS for processing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/get_shipping_label.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#get_shipping_label)
        """

    def get_status(self, **kwargs: Unpack[GetStatusInputRequestTypeDef]) -> GetStatusOutputTypeDef:
        """
        This operation returns information about a job, including where the job is in
        the processing pipeline, the status of the results, and the signature value
        associated with the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/get_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#get_status)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsInputRequestTypeDef]) -> ListJobsOutputTypeDef:
        """
        This operation returns the jobs associated with the requester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/list_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#list_jobs)
        """

    def update_job(self, **kwargs: Unpack[UpdateJobInputRequestTypeDef]) -> UpdateJobOutputTypeDef:
        """
        You use this operation to change the parameters specified in the original
        manifest file by supplying a new manifest file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/update_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#update_job)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs"]
    ) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_importexport/client/#get_paginator)
        """
