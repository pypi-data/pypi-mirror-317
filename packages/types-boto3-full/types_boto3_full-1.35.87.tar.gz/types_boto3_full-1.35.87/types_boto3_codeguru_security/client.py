"""
Type annotations for codeguru-security service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_codeguru_security.client import CodeGuruSecurityClient

    session = Session()
    client: CodeGuruSecurityClient = session.client("codeguru-security")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import GetFindingsPaginator, ListFindingsMetricsPaginator, ListScansPaginator
from .type_defs import (
    BatchGetFindingsRequestRequestTypeDef,
    BatchGetFindingsResponseTypeDef,
    CreateScanRequestRequestTypeDef,
    CreateScanResponseTypeDef,
    CreateUploadUrlRequestRequestTypeDef,
    CreateUploadUrlResponseTypeDef,
    GetAccountConfigurationResponseTypeDef,
    GetFindingsRequestRequestTypeDef,
    GetFindingsResponseTypeDef,
    GetMetricsSummaryRequestRequestTypeDef,
    GetMetricsSummaryResponseTypeDef,
    GetScanRequestRequestTypeDef,
    GetScanResponseTypeDef,
    ListFindingsMetricsRequestRequestTypeDef,
    ListFindingsMetricsResponseTypeDef,
    ListScansRequestRequestTypeDef,
    ListScansResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccountConfigurationRequestRequestTypeDef,
    UpdateAccountConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("CodeGuruSecurityClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class CodeGuruSecurityClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeGuruSecurityClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#generate_presigned_url)
        """

    def batch_get_findings(
        self, **kwargs: Unpack[BatchGetFindingsRequestRequestTypeDef]
    ) -> BatchGetFindingsResponseTypeDef:
        """
        Returns a list of requested findings from standard scans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/batch_get_findings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#batch_get_findings)
        """

    def create_scan(
        self, **kwargs: Unpack[CreateScanRequestRequestTypeDef]
    ) -> CreateScanResponseTypeDef:
        """
        Use to create a scan using code uploaded to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/create_scan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#create_scan)
        """

    def create_upload_url(
        self, **kwargs: Unpack[CreateUploadUrlRequestRequestTypeDef]
    ) -> CreateUploadUrlResponseTypeDef:
        """
        Generates a pre-signed URL, request headers used to upload a code resource, and
        code artifact identifier for the uploaded resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/create_upload_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#create_upload_url)
        """

    def get_account_configuration(self) -> GetAccountConfigurationResponseTypeDef:
        """
        Use to get the encryption configuration for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/get_account_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#get_account_configuration)
        """

    def get_findings(
        self, **kwargs: Unpack[GetFindingsRequestRequestTypeDef]
    ) -> GetFindingsResponseTypeDef:
        """
        Returns a list of all findings generated by a particular scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/get_findings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#get_findings)
        """

    def get_metrics_summary(
        self, **kwargs: Unpack[GetMetricsSummaryRequestRequestTypeDef]
    ) -> GetMetricsSummaryResponseTypeDef:
        """
        Returns a summary of metrics for an account from a specified date, including
        number of open findings, the categories with most findings, the scans with most
        open findings, and scans with most open critical findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/get_metrics_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#get_metrics_summary)
        """

    def get_scan(self, **kwargs: Unpack[GetScanRequestRequestTypeDef]) -> GetScanResponseTypeDef:
        """
        Returns details about a scan, including whether or not a scan has completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/get_scan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#get_scan)
        """

    def list_findings_metrics(
        self, **kwargs: Unpack[ListFindingsMetricsRequestRequestTypeDef]
    ) -> ListFindingsMetricsResponseTypeDef:
        """
        Returns metrics about all findings in an account within a specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/list_findings_metrics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#list_findings_metrics)
        """

    def list_scans(
        self, **kwargs: Unpack[ListScansRequestRequestTypeDef]
    ) -> ListScansResponseTypeDef:
        """
        Returns a list of all scans in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/list_scans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#list_scans)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all tags associated with a scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Use to add one or more tags to an existing scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Use to remove one or more tags from an existing scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#untag_resource)
        """

    def update_account_configuration(
        self, **kwargs: Unpack[UpdateAccountConfigurationRequestRequestTypeDef]
    ) -> UpdateAccountConfigurationResponseTypeDef:
        """
        Use to update the encryption configuration for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/update_account_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#update_account_configuration)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_findings"]
    ) -> GetFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_findings_metrics"]
    ) -> ListFindingsMetricsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_scans"]
    ) -> ListScansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_security/client/#get_paginator)
        """
