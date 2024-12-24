"""
Type annotations for snow-device-management service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_snow_device_management.client import SnowDeviceManagementClient

    session = Session()
    client: SnowDeviceManagementClient = session.client("snow-device-management")
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
    ListDeviceResourcesPaginator,
    ListDevicesPaginator,
    ListExecutionsPaginator,
    ListTasksPaginator,
)
from .type_defs import (
    CancelTaskInputRequestTypeDef,
    CancelTaskOutputTypeDef,
    CreateTaskInputRequestTypeDef,
    CreateTaskOutputTypeDef,
    DescribeDeviceEc2InputRequestTypeDef,
    DescribeDeviceEc2OutputTypeDef,
    DescribeDeviceInputRequestTypeDef,
    DescribeDeviceOutputTypeDef,
    DescribeExecutionInputRequestTypeDef,
    DescribeExecutionOutputTypeDef,
    DescribeTaskInputRequestTypeDef,
    DescribeTaskOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ListDeviceResourcesInputRequestTypeDef,
    ListDeviceResourcesOutputTypeDef,
    ListDevicesInputRequestTypeDef,
    ListDevicesOutputTypeDef,
    ListExecutionsInputRequestTypeDef,
    ListExecutionsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTasksInputRequestTypeDef,
    ListTasksOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SnowDeviceManagementClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class SnowDeviceManagementClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SnowDeviceManagementClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#generate_presigned_url)
        """

    def cancel_task(
        self, **kwargs: Unpack[CancelTaskInputRequestTypeDef]
    ) -> CancelTaskOutputTypeDef:
        """
        Sends a cancel request for a specified task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/cancel_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#cancel_task)
        """

    def create_task(
        self, **kwargs: Unpack[CreateTaskInputRequestTypeDef]
    ) -> CreateTaskOutputTypeDef:
        """
        Instructs one or more devices to start a task, such as unlocking or rebooting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/create_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#create_task)
        """

    def describe_device(
        self, **kwargs: Unpack[DescribeDeviceInputRequestTypeDef]
    ) -> DescribeDeviceOutputTypeDef:
        """
        Checks device-specific information, such as the device type, software version,
        IP addresses, and lock status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/describe_device.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#describe_device)
        """

    def describe_device_ec2_instances(
        self, **kwargs: Unpack[DescribeDeviceEc2InputRequestTypeDef]
    ) -> DescribeDeviceEc2OutputTypeDef:
        """
        Checks the current state of the Amazon EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/describe_device_ec2_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#describe_device_ec2_instances)
        """

    def describe_execution(
        self, **kwargs: Unpack[DescribeExecutionInputRequestTypeDef]
    ) -> DescribeExecutionOutputTypeDef:
        """
        Checks the status of a remote task running on one or more target devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/describe_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#describe_execution)
        """

    def describe_task(
        self, **kwargs: Unpack[DescribeTaskInputRequestTypeDef]
    ) -> DescribeTaskOutputTypeDef:
        """
        Checks the metadata for a given task on a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/describe_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#describe_task)
        """

    def list_device_resources(
        self, **kwargs: Unpack[ListDeviceResourcesInputRequestTypeDef]
    ) -> ListDeviceResourcesOutputTypeDef:
        """
        Returns a list of the Amazon Web Services resources available for a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/list_device_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#list_device_resources)
        """

    def list_devices(
        self, **kwargs: Unpack[ListDevicesInputRequestTypeDef]
    ) -> ListDevicesOutputTypeDef:
        """
        Returns a list of all devices on your Amazon Web Services account that have
        Amazon Web Services Snow Device Management enabled in the Amazon Web Services
        Region where the command is run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/list_devices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#list_devices)
        """

    def list_executions(
        self, **kwargs: Unpack[ListExecutionsInputRequestTypeDef]
    ) -> ListExecutionsOutputTypeDef:
        """
        Returns the status of tasks for one or more target devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/list_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#list_executions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns a list of tags for a managed device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#list_tags_for_resource)
        """

    def list_tasks(self, **kwargs: Unpack[ListTasksInputRequestTypeDef]) -> ListTasksOutputTypeDef:
        """
        Returns a list of tasks that can be filtered by state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/list_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#list_tasks)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or replaces tags on a device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a tag from a device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_device_resources"]
    ) -> ListDeviceResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_devices"]
    ) -> ListDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_executions"]
    ) -> ListExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tasks"]
    ) -> ListTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/client/#get_paginator)
        """
