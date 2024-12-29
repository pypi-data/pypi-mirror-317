"""
Type annotations for application-insights service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_application_insights.client import ApplicationInsightsClient

    session = Session()
    client: ApplicationInsightsClient = session.client("application-insights")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    AddWorkloadRequestRequestTypeDef,
    AddWorkloadResponseTypeDef,
    CreateApplicationRequestRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateComponentRequestRequestTypeDef,
    CreateLogPatternRequestRequestTypeDef,
    CreateLogPatternResponseTypeDef,
    DeleteApplicationRequestRequestTypeDef,
    DeleteComponentRequestRequestTypeDef,
    DeleteLogPatternRequestRequestTypeDef,
    DescribeApplicationRequestRequestTypeDef,
    DescribeApplicationResponseTypeDef,
    DescribeComponentConfigurationRecommendationRequestRequestTypeDef,
    DescribeComponentConfigurationRecommendationResponseTypeDef,
    DescribeComponentConfigurationRequestRequestTypeDef,
    DescribeComponentConfigurationResponseTypeDef,
    DescribeComponentRequestRequestTypeDef,
    DescribeComponentResponseTypeDef,
    DescribeLogPatternRequestRequestTypeDef,
    DescribeLogPatternResponseTypeDef,
    DescribeObservationRequestRequestTypeDef,
    DescribeObservationResponseTypeDef,
    DescribeProblemObservationsRequestRequestTypeDef,
    DescribeProblemObservationsResponseTypeDef,
    DescribeProblemRequestRequestTypeDef,
    DescribeProblemResponseTypeDef,
    DescribeWorkloadRequestRequestTypeDef,
    DescribeWorkloadResponseTypeDef,
    ListApplicationsRequestRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListComponentsRequestRequestTypeDef,
    ListComponentsResponseTypeDef,
    ListConfigurationHistoryRequestRequestTypeDef,
    ListConfigurationHistoryResponseTypeDef,
    ListLogPatternSetsRequestRequestTypeDef,
    ListLogPatternSetsResponseTypeDef,
    ListLogPatternsRequestRequestTypeDef,
    ListLogPatternsResponseTypeDef,
    ListProblemsRequestRequestTypeDef,
    ListProblemsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkloadsRequestRequestTypeDef,
    ListWorkloadsResponseTypeDef,
    RemoveWorkloadRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateApplicationRequestRequestTypeDef,
    UpdateApplicationResponseTypeDef,
    UpdateComponentConfigurationRequestRequestTypeDef,
    UpdateComponentRequestRequestTypeDef,
    UpdateLogPatternRequestRequestTypeDef,
    UpdateLogPatternResponseTypeDef,
    UpdateProblemRequestRequestTypeDef,
    UpdateWorkloadRequestRequestTypeDef,
    UpdateWorkloadResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ApplicationInsightsClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    BadRequestException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceInUseException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    TagsAlreadyExistException: type[BotocoreClientError]
    TooManyTagsException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class ApplicationInsightsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApplicationInsightsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#generate_presigned_url)
        """

    def add_workload(
        self, **kwargs: Unpack[AddWorkloadRequestRequestTypeDef]
    ) -> AddWorkloadResponseTypeDef:
        """
        Adds a workload to a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/add_workload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#add_workload)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Adds an application that is created from a resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/create_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#create_application)
        """

    def create_component(
        self, **kwargs: Unpack[CreateComponentRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates a custom component by grouping similar standalone instances to monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/create_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#create_component)
        """

    def create_log_pattern(
        self, **kwargs: Unpack[CreateLogPatternRequestRequestTypeDef]
    ) -> CreateLogPatternResponseTypeDef:
        """
        Adds an log pattern to a <code>LogPatternSet</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/create_log_pattern.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#create_log_pattern)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes the specified application from monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/delete_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#delete_application)
        """

    def delete_component(
        self, **kwargs: Unpack[DeleteComponentRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Ungroups a custom component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/delete_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#delete_component)
        """

    def delete_log_pattern(
        self, **kwargs: Unpack[DeleteLogPatternRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes the specified log pattern from a <code>LogPatternSet</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/delete_log_pattern.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#delete_log_pattern)
        """

    def describe_application(
        self, **kwargs: Unpack[DescribeApplicationRequestRequestTypeDef]
    ) -> DescribeApplicationResponseTypeDef:
        """
        Describes the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_application)
        """

    def describe_component(
        self, **kwargs: Unpack[DescribeComponentRequestRequestTypeDef]
    ) -> DescribeComponentResponseTypeDef:
        """
        Describes a component and lists the resources that are grouped together in a
        component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_component)
        """

    def describe_component_configuration(
        self, **kwargs: Unpack[DescribeComponentConfigurationRequestRequestTypeDef]
    ) -> DescribeComponentConfigurationResponseTypeDef:
        """
        Describes the monitoring configuration of the component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_component_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_component_configuration)
        """

    def describe_component_configuration_recommendation(
        self, **kwargs: Unpack[DescribeComponentConfigurationRecommendationRequestRequestTypeDef]
    ) -> DescribeComponentConfigurationRecommendationResponseTypeDef:
        """
        Describes the recommended monitoring configuration of the component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_component_configuration_recommendation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_component_configuration_recommendation)
        """

    def describe_log_pattern(
        self, **kwargs: Unpack[DescribeLogPatternRequestRequestTypeDef]
    ) -> DescribeLogPatternResponseTypeDef:
        """
        Describe a specific log pattern from a <code>LogPatternSet</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_log_pattern.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_log_pattern)
        """

    def describe_observation(
        self, **kwargs: Unpack[DescribeObservationRequestRequestTypeDef]
    ) -> DescribeObservationResponseTypeDef:
        """
        Describes an anomaly or error with the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_observation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_observation)
        """

    def describe_problem(
        self, **kwargs: Unpack[DescribeProblemRequestRequestTypeDef]
    ) -> DescribeProblemResponseTypeDef:
        """
        Describes an application problem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_problem.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_problem)
        """

    def describe_problem_observations(
        self, **kwargs: Unpack[DescribeProblemObservationsRequestRequestTypeDef]
    ) -> DescribeProblemObservationsResponseTypeDef:
        """
        Describes the anomalies or errors associated with the problem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_problem_observations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_problem_observations)
        """

    def describe_workload(
        self, **kwargs: Unpack[DescribeWorkloadRequestRequestTypeDef]
    ) -> DescribeWorkloadResponseTypeDef:
        """
        Describes a workload and its configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/describe_workload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#describe_workload)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists the IDs of the applications that you are monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/list_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#list_applications)
        """

    def list_components(
        self, **kwargs: Unpack[ListComponentsRequestRequestTypeDef]
    ) -> ListComponentsResponseTypeDef:
        """
        Lists the auto-grouped, standalone, and custom components of the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/list_components.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#list_components)
        """

    def list_configuration_history(
        self, **kwargs: Unpack[ListConfigurationHistoryRequestRequestTypeDef]
    ) -> ListConfigurationHistoryResponseTypeDef:
        """
        Lists the INFO, WARN, and ERROR events for periodic configuration updates
        performed by Application Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/list_configuration_history.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#list_configuration_history)
        """

    def list_log_pattern_sets(
        self, **kwargs: Unpack[ListLogPatternSetsRequestRequestTypeDef]
    ) -> ListLogPatternSetsResponseTypeDef:
        """
        Lists the log pattern sets in the specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/list_log_pattern_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#list_log_pattern_sets)
        """

    def list_log_patterns(
        self, **kwargs: Unpack[ListLogPatternsRequestRequestTypeDef]
    ) -> ListLogPatternsResponseTypeDef:
        """
        Lists the log patterns in the specific log <code>LogPatternSet</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/list_log_patterns.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#list_log_patterns)
        """

    def list_problems(
        self, **kwargs: Unpack[ListProblemsRequestRequestTypeDef]
    ) -> ListProblemsResponseTypeDef:
        """
        Lists the problems with your application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/list_problems.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#list_problems)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieve a list of the tags (keys and values) that are associated with a
        specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#list_tags_for_resource)
        """

    def list_workloads(
        self, **kwargs: Unpack[ListWorkloadsRequestRequestTypeDef]
    ) -> ListWorkloadsResponseTypeDef:
        """
        Lists the workloads that are configured on a given component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/list_workloads.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#list_workloads)
        """

    def remove_workload(
        self, **kwargs: Unpack[RemoveWorkloadRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Remove workload from a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/remove_workload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#remove_workload)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Add one or more tags (keys and values) to a specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#untag_resource)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestRequestTypeDef]
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/update_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#update_application)
        """

    def update_component(
        self, **kwargs: Unpack[UpdateComponentRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the custom component name and/or the list of resources that make up the
        component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/update_component.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#update_component)
        """

    def update_component_configuration(
        self, **kwargs: Unpack[UpdateComponentConfigurationRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the monitoring configurations for the component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/update_component_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#update_component_configuration)
        """

    def update_log_pattern(
        self, **kwargs: Unpack[UpdateLogPatternRequestRequestTypeDef]
    ) -> UpdateLogPatternResponseTypeDef:
        """
        Adds a log pattern to a <code>LogPatternSet</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/update_log_pattern.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#update_log_pattern)
        """

    def update_problem(
        self, **kwargs: Unpack[UpdateProblemRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the visibility of the problem or specifies the problem as
        <code>RESOLVED</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/update_problem.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#update_problem)
        """

    def update_workload(
        self, **kwargs: Unpack[UpdateWorkloadRequestRequestTypeDef]
    ) -> UpdateWorkloadResponseTypeDef:
        """
        Adds a workload to a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights/client/update_workload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_application_insights/client/#update_workload)
        """
