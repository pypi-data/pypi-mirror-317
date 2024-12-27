"""
Type annotations for application-autoscaling service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_application_autoscaling.client import ApplicationAutoScalingClient

    session = get_session()
    async with session.create_client("application-autoscaling") as client:
        client: ApplicationAutoScalingClient
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, Mapping, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeScalableTargetsPaginator,
    DescribeScalingActivitiesPaginator,
    DescribeScalingPoliciesPaginator,
    DescribeScheduledActionsPaginator,
)
from .type_defs import (
    DeleteScalingPolicyRequestRequestTypeDef,
    DeleteScheduledActionRequestRequestTypeDef,
    DeregisterScalableTargetRequestRequestTypeDef,
    DescribeScalableTargetsRequestRequestTypeDef,
    DescribeScalableTargetsResponseTypeDef,
    DescribeScalingActivitiesRequestRequestTypeDef,
    DescribeScalingActivitiesResponseTypeDef,
    DescribeScalingPoliciesRequestRequestTypeDef,
    DescribeScalingPoliciesResponseTypeDef,
    DescribeScheduledActionsRequestRequestTypeDef,
    DescribeScheduledActionsResponseTypeDef,
    GetPredictiveScalingForecastRequestRequestTypeDef,
    GetPredictiveScalingForecastResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutScalingPolicyRequestRequestTypeDef,
    PutScalingPolicyResponseTypeDef,
    PutScheduledActionRequestRequestTypeDef,
    RegisterScalableTargetRequestRequestTypeDef,
    RegisterScalableTargetResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("ApplicationAutoScalingClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ConcurrentUpdateException: type[BotocoreClientError]
    FailedResourceAccessException: type[BotocoreClientError]
    InternalServiceException: type[BotocoreClientError]
    InvalidNextTokenException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    ObjectNotFoundException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    TooManyTagsException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class ApplicationAutoScalingClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApplicationAutoScalingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#generate_presigned_url)
        """

    async def delete_scaling_policy(
        self, **kwargs: Unpack[DeleteScalingPolicyRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the specified scaling policy for an Application Auto Scaling scalable
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/delete_scaling_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#delete_scaling_policy)
        """

    async def delete_scheduled_action(
        self, **kwargs: Unpack[DeleteScheduledActionRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the specified scheduled action for an Application Auto Scaling scalable
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/delete_scheduled_action.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#delete_scheduled_action)
        """

    async def deregister_scalable_target(
        self, **kwargs: Unpack[DeregisterScalableTargetRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deregisters an Application Auto Scaling scalable target when you have finished
        using it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/deregister_scalable_target.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#deregister_scalable_target)
        """

    async def describe_scalable_targets(
        self, **kwargs: Unpack[DescribeScalableTargetsRequestRequestTypeDef]
    ) -> DescribeScalableTargetsResponseTypeDef:
        """
        Gets information about the scalable targets in the specified namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/describe_scalable_targets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#describe_scalable_targets)
        """

    async def describe_scaling_activities(
        self, **kwargs: Unpack[DescribeScalingActivitiesRequestRequestTypeDef]
    ) -> DescribeScalingActivitiesResponseTypeDef:
        """
        Provides descriptive information about the scaling activities in the specified
        namespace from the previous six weeks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/describe_scaling_activities.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#describe_scaling_activities)
        """

    async def describe_scaling_policies(
        self, **kwargs: Unpack[DescribeScalingPoliciesRequestRequestTypeDef]
    ) -> DescribeScalingPoliciesResponseTypeDef:
        """
        Describes the Application Auto Scaling scaling policies for the specified
        service namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/describe_scaling_policies.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#describe_scaling_policies)
        """

    async def describe_scheduled_actions(
        self, **kwargs: Unpack[DescribeScheduledActionsRequestRequestTypeDef]
    ) -> DescribeScheduledActionsResponseTypeDef:
        """
        Describes the Application Auto Scaling scheduled actions for the specified
        service namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/describe_scheduled_actions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#describe_scheduled_actions)
        """

    async def get_predictive_scaling_forecast(
        self, **kwargs: Unpack[GetPredictiveScalingForecastRequestRequestTypeDef]
    ) -> GetPredictiveScalingForecastResponseTypeDef:
        """
        Retrieves the forecast data for a predictive scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/get_predictive_scaling_forecast.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#get_predictive_scaling_forecast)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns all the tags on the specified Application Auto Scaling scalable target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#list_tags_for_resource)
        """

    async def put_scaling_policy(
        self, **kwargs: Unpack[PutScalingPolicyRequestRequestTypeDef]
    ) -> PutScalingPolicyResponseTypeDef:
        """
        Creates or updates a scaling policy for an Application Auto Scaling scalable
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/put_scaling_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#put_scaling_policy)
        """

    async def put_scheduled_action(
        self, **kwargs: Unpack[PutScheduledActionRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates or updates a scheduled action for an Application Auto Scaling scalable
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/put_scheduled_action.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#put_scheduled_action)
        """

    async def register_scalable_target(
        self, **kwargs: Unpack[RegisterScalableTargetRequestRequestTypeDef]
    ) -> RegisterScalableTargetResponseTypeDef:
        """
        Registers or updates a scalable target, which is the resource that you want to
        scale.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/register_scalable_target.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#register_scalable_target)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Adds or edits tags on an Application Auto Scaling scalable target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes tags from an Application Auto Scaling scalable target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_scalable_targets"]
    ) -> DescribeScalableTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_scaling_activities"]
    ) -> DescribeScalingActivitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_scaling_policies"]
    ) -> DescribeScalingPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_scheduled_actions"]
    ) -> DescribeScheduledActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-autoscaling.html#ApplicationAutoScaling.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_autoscaling/client/)
        """
