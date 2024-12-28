"""
Type annotations for sms service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sms.client import SMSClient

    session = Session()
    client: SMSClient = session.client("sms")
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
    GetConnectorsPaginator,
    GetReplicationJobsPaginator,
    GetReplicationRunsPaginator,
    GetServersPaginator,
    ListAppsPaginator,
)
from .type_defs import (
    CreateAppRequestRequestTypeDef,
    CreateAppResponseTypeDef,
    CreateReplicationJobRequestRequestTypeDef,
    CreateReplicationJobResponseTypeDef,
    DeleteAppLaunchConfigurationRequestRequestTypeDef,
    DeleteAppReplicationConfigurationRequestRequestTypeDef,
    DeleteAppRequestRequestTypeDef,
    DeleteAppValidationConfigurationRequestRequestTypeDef,
    DeleteReplicationJobRequestRequestTypeDef,
    DisassociateConnectorRequestRequestTypeDef,
    GenerateChangeSetRequestRequestTypeDef,
    GenerateChangeSetResponseTypeDef,
    GenerateTemplateRequestRequestTypeDef,
    GenerateTemplateResponseTypeDef,
    GetAppLaunchConfigurationRequestRequestTypeDef,
    GetAppLaunchConfigurationResponseTypeDef,
    GetAppReplicationConfigurationRequestRequestTypeDef,
    GetAppReplicationConfigurationResponseTypeDef,
    GetAppRequestRequestTypeDef,
    GetAppResponseTypeDef,
    GetAppValidationConfigurationRequestRequestTypeDef,
    GetAppValidationConfigurationResponseTypeDef,
    GetAppValidationOutputRequestRequestTypeDef,
    GetAppValidationOutputResponseTypeDef,
    GetConnectorsRequestRequestTypeDef,
    GetConnectorsResponseTypeDef,
    GetReplicationJobsRequestRequestTypeDef,
    GetReplicationJobsResponseTypeDef,
    GetReplicationRunsRequestRequestTypeDef,
    GetReplicationRunsResponseTypeDef,
    GetServersRequestRequestTypeDef,
    GetServersResponseTypeDef,
    ImportAppCatalogRequestRequestTypeDef,
    LaunchAppRequestRequestTypeDef,
    ListAppsRequestRequestTypeDef,
    ListAppsResponseTypeDef,
    NotifyAppValidationOutputRequestRequestTypeDef,
    PutAppLaunchConfigurationRequestRequestTypeDef,
    PutAppReplicationConfigurationRequestRequestTypeDef,
    PutAppValidationConfigurationRequestRequestTypeDef,
    StartAppReplicationRequestRequestTypeDef,
    StartOnDemandAppReplicationRequestRequestTypeDef,
    StartOnDemandReplicationRunRequestRequestTypeDef,
    StartOnDemandReplicationRunResponseTypeDef,
    StopAppReplicationRequestRequestTypeDef,
    TerminateAppRequestRequestTypeDef,
    UpdateAppRequestRequestTypeDef,
    UpdateAppResponseTypeDef,
    UpdateReplicationJobRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SMSClient",)

class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    DryRunOperationException: type[BotocoreClientError]
    InternalError: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    MissingRequiredParameterException: type[BotocoreClientError]
    NoConnectorsAvailableException: type[BotocoreClientError]
    OperationNotPermittedException: type[BotocoreClientError]
    ReplicationJobAlreadyExistsException: type[BotocoreClientError]
    ReplicationJobNotFoundException: type[BotocoreClientError]
    ReplicationRunLimitExceededException: type[BotocoreClientError]
    ServerCannotBeReplicatedException: type[BotocoreClientError]
    TemporarilyUnavailableException: type[BotocoreClientError]
    UnauthorizedOperationException: type[BotocoreClientError]

class SMSClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms.html#SMS.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SMSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms.html#SMS.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#generate_presigned_url)
        """

    def create_app(
        self, **kwargs: Unpack[CreateAppRequestRequestTypeDef]
    ) -> CreateAppResponseTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/create_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#create_app)
        """

    def create_replication_job(
        self, **kwargs: Unpack[CreateReplicationJobRequestRequestTypeDef]
    ) -> CreateReplicationJobResponseTypeDef:
        """
        Creates a replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/create_replication_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#create_replication_job)
        """

    def delete_app(self, **kwargs: Unpack[DeleteAppRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#delete_app)
        """

    def delete_app_launch_configuration(
        self, **kwargs: Unpack[DeleteAppLaunchConfigurationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the launch configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_app_launch_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#delete_app_launch_configuration)
        """

    def delete_app_replication_configuration(
        self, **kwargs: Unpack[DeleteAppReplicationConfigurationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the replication configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_app_replication_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#delete_app_replication_configuration)
        """

    def delete_app_validation_configuration(
        self, **kwargs: Unpack[DeleteAppValidationConfigurationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the validation configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_app_validation_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#delete_app_validation_configuration)
        """

    def delete_replication_job(
        self, **kwargs: Unpack[DeleteReplicationJobRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the specified replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_replication_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#delete_replication_job)
        """

    def delete_server_catalog(self) -> dict[str, Any]:
        """
        Deletes all servers from your server catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/delete_server_catalog.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#delete_server_catalog)
        """

    def disassociate_connector(
        self, **kwargs: Unpack[DisassociateConnectorRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates the specified connector from Server Migration Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/disassociate_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#disassociate_connector)
        """

    def generate_change_set(
        self, **kwargs: Unpack[GenerateChangeSetRequestRequestTypeDef]
    ) -> GenerateChangeSetResponseTypeDef:
        """
        Generates a target change set for a currently launched stack and writes it to
        an Amazon S3 object in the customer's Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/generate_change_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#generate_change_set)
        """

    def generate_template(
        self, **kwargs: Unpack[GenerateTemplateRequestRequestTypeDef]
    ) -> GenerateTemplateResponseTypeDef:
        """
        Generates an CloudFormation template based on the current launch configuration
        and writes it to an Amazon S3 object in the customer's Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/generate_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#generate_template)
        """

    def get_app(self, **kwargs: Unpack[GetAppRequestRequestTypeDef]) -> GetAppResponseTypeDef:
        """
        Retrieve information about the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_app)
        """

    def get_app_launch_configuration(
        self, **kwargs: Unpack[GetAppLaunchConfigurationRequestRequestTypeDef]
    ) -> GetAppLaunchConfigurationResponseTypeDef:
        """
        Retrieves the application launch configuration associated with the specified
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app_launch_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_app_launch_configuration)
        """

    def get_app_replication_configuration(
        self, **kwargs: Unpack[GetAppReplicationConfigurationRequestRequestTypeDef]
    ) -> GetAppReplicationConfigurationResponseTypeDef:
        """
        Retrieves the application replication configuration associated with the
        specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app_replication_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_app_replication_configuration)
        """

    def get_app_validation_configuration(
        self, **kwargs: Unpack[GetAppValidationConfigurationRequestRequestTypeDef]
    ) -> GetAppValidationConfigurationResponseTypeDef:
        """
        Retrieves information about a configuration for validating an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app_validation_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_app_validation_configuration)
        """

    def get_app_validation_output(
        self, **kwargs: Unpack[GetAppValidationOutputRequestRequestTypeDef]
    ) -> GetAppValidationOutputResponseTypeDef:
        """
        Retrieves output from validating an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_app_validation_output.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_app_validation_output)
        """

    def get_connectors(
        self, **kwargs: Unpack[GetConnectorsRequestRequestTypeDef]
    ) -> GetConnectorsResponseTypeDef:
        """
        Describes the connectors registered with the Server Migration Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_connectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_connectors)
        """

    def get_replication_jobs(
        self, **kwargs: Unpack[GetReplicationJobsRequestRequestTypeDef]
    ) -> GetReplicationJobsResponseTypeDef:
        """
        Describes the specified replication job or all of your replication jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_replication_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_replication_jobs)
        """

    def get_replication_runs(
        self, **kwargs: Unpack[GetReplicationRunsRequestRequestTypeDef]
    ) -> GetReplicationRunsResponseTypeDef:
        """
        Describes the replication runs for the specified replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_replication_runs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_replication_runs)
        """

    def get_servers(
        self, **kwargs: Unpack[GetServersRequestRequestTypeDef]
    ) -> GetServersResponseTypeDef:
        """
        Describes the servers in your server catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_servers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_servers)
        """

    def import_app_catalog(
        self, **kwargs: Unpack[ImportAppCatalogRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Allows application import from Migration Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/import_app_catalog.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#import_app_catalog)
        """

    def import_server_catalog(self) -> dict[str, Any]:
        """
        Gathers a complete list of on-premises servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/import_server_catalog.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#import_server_catalog)
        """

    def launch_app(self, **kwargs: Unpack[LaunchAppRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Launches the specified application as a stack in CloudFormation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/launch_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#launch_app)
        """

    def list_apps(self, **kwargs: Unpack[ListAppsRequestRequestTypeDef]) -> ListAppsResponseTypeDef:
        """
        Retrieves summaries for all applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/list_apps.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#list_apps)
        """

    def notify_app_validation_output(
        self, **kwargs: Unpack[NotifyAppValidationOutputRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Provides information to Server Migration Service about whether application
        validation is successful.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/notify_app_validation_output.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#notify_app_validation_output)
        """

    def put_app_launch_configuration(
        self, **kwargs: Unpack[PutAppLaunchConfigurationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates or updates the launch configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/put_app_launch_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#put_app_launch_configuration)
        """

    def put_app_replication_configuration(
        self, **kwargs: Unpack[PutAppReplicationConfigurationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates or updates the replication configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/put_app_replication_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#put_app_replication_configuration)
        """

    def put_app_validation_configuration(
        self, **kwargs: Unpack[PutAppValidationConfigurationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates or updates a validation configuration for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/put_app_validation_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#put_app_validation_configuration)
        """

    def start_app_replication(
        self, **kwargs: Unpack[StartAppReplicationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Starts replicating the specified application by creating replication jobs for
        each server in the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/start_app_replication.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#start_app_replication)
        """

    def start_on_demand_app_replication(
        self, **kwargs: Unpack[StartOnDemandAppReplicationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Starts an on-demand replication run for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/start_on_demand_app_replication.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#start_on_demand_app_replication)
        """

    def start_on_demand_replication_run(
        self, **kwargs: Unpack[StartOnDemandReplicationRunRequestRequestTypeDef]
    ) -> StartOnDemandReplicationRunResponseTypeDef:
        """
        Starts an on-demand replication run for the specified replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/start_on_demand_replication_run.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#start_on_demand_replication_run)
        """

    def stop_app_replication(
        self, **kwargs: Unpack[StopAppReplicationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Stops replicating the specified application by deleting the replication job for
        each server in the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/stop_app_replication.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#stop_app_replication)
        """

    def terminate_app(self, **kwargs: Unpack[TerminateAppRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Terminates the stack for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/terminate_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#terminate_app)
        """

    def update_app(
        self, **kwargs: Unpack[UpdateAppRequestRequestTypeDef]
    ) -> UpdateAppResponseTypeDef:
        """
        Updates the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/update_app.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#update_app)
        """

    def update_replication_job(
        self, **kwargs: Unpack[UpdateReplicationJobRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the specified settings for the specified replication job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/update_replication_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#update_replication_job)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_connectors"]
    ) -> GetConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_replication_jobs"]
    ) -> GetReplicationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_replication_runs"]
    ) -> GetReplicationRunsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_servers"]
    ) -> GetServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_apps"]
    ) -> ListAppsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sms/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sms/client/#get_paginator)
        """
