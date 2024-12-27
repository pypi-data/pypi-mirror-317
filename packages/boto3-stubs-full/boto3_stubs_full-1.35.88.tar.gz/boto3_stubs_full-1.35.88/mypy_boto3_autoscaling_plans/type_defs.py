"""
Type annotations for autoscaling-plans service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_autoscaling_plans/type_defs/)

Usage::

    ```python
    from mypy_boto3_autoscaling_plans.type_defs import TagFilterOutputTypeDef

    data: TagFilterOutputTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence, Union

from .literals import (
    ForecastDataTypeType,
    LoadMetricTypeType,
    MetricStatisticType,
    PredictiveScalingMaxCapacityBehaviorType,
    PredictiveScalingModeType,
    ScalableDimensionType,
    ScalingMetricTypeType,
    ScalingPlanStatusCodeType,
    ScalingPolicyUpdateBehaviorType,
    ScalingStatusCodeType,
    ServiceNamespaceType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ApplicationSourceOutputTypeDef",
    "ApplicationSourceTypeDef",
    "CreateScalingPlanRequestRequestTypeDef",
    "CreateScalingPlanResponseTypeDef",
    "CustomizedLoadMetricSpecificationOutputTypeDef",
    "CustomizedLoadMetricSpecificationTypeDef",
    "CustomizedLoadMetricSpecificationUnionTypeDef",
    "CustomizedScalingMetricSpecificationOutputTypeDef",
    "CustomizedScalingMetricSpecificationTypeDef",
    "CustomizedScalingMetricSpecificationUnionTypeDef",
    "DatapointTypeDef",
    "DeleteScalingPlanRequestRequestTypeDef",
    "DescribeScalingPlanResourcesRequestPaginateTypeDef",
    "DescribeScalingPlanResourcesRequestRequestTypeDef",
    "DescribeScalingPlanResourcesResponseTypeDef",
    "DescribeScalingPlansRequestPaginateTypeDef",
    "DescribeScalingPlansRequestRequestTypeDef",
    "DescribeScalingPlansResponseTypeDef",
    "GetScalingPlanResourceForecastDataRequestRequestTypeDef",
    "GetScalingPlanResourceForecastDataResponseTypeDef",
    "MetricDimensionTypeDef",
    "PaginatorConfigTypeDef",
    "PredefinedLoadMetricSpecificationTypeDef",
    "PredefinedScalingMetricSpecificationTypeDef",
    "ResponseMetadataTypeDef",
    "ScalingInstructionOutputTypeDef",
    "ScalingInstructionTypeDef",
    "ScalingInstructionUnionTypeDef",
    "ScalingPlanResourceTypeDef",
    "ScalingPlanTypeDef",
    "ScalingPolicyTypeDef",
    "TagFilterOutputTypeDef",
    "TagFilterTypeDef",
    "TagFilterUnionTypeDef",
    "TargetTrackingConfigurationOutputTypeDef",
    "TargetTrackingConfigurationTypeDef",
    "TargetTrackingConfigurationUnionTypeDef",
    "TimestampTypeDef",
    "UpdateScalingPlanRequestRequestTypeDef",
)


class TagFilterOutputTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[list[str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class MetricDimensionTypeDef(TypedDict):
    Name: str
    Value: str


class DatapointTypeDef(TypedDict):
    Timestamp: NotRequired[datetime]
    Value: NotRequired[float]


class DeleteScalingPlanRequestRequestTypeDef(TypedDict):
    ScalingPlanName: str
    ScalingPlanVersion: int


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeScalingPlanResourcesRequestRequestTypeDef(TypedDict):
    ScalingPlanName: str
    ScalingPlanVersion: int
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class PredefinedLoadMetricSpecificationTypeDef(TypedDict):
    PredefinedLoadMetricType: LoadMetricTypeType
    ResourceLabel: NotRequired[str]


class PredefinedScalingMetricSpecificationTypeDef(TypedDict):
    PredefinedScalingMetricType: ScalingMetricTypeType
    ResourceLabel: NotRequired[str]


class TagFilterTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class ApplicationSourceOutputTypeDef(TypedDict):
    CloudFormationStackARN: NotRequired[str]
    TagFilters: NotRequired[list[TagFilterOutputTypeDef]]


class CreateScalingPlanResponseTypeDef(TypedDict):
    ScalingPlanVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class CustomizedLoadMetricSpecificationOutputTypeDef(TypedDict):
    MetricName: str
    Namespace: str
    Statistic: MetricStatisticType
    Dimensions: NotRequired[list[MetricDimensionTypeDef]]
    Unit: NotRequired[str]


class CustomizedLoadMetricSpecificationTypeDef(TypedDict):
    MetricName: str
    Namespace: str
    Statistic: MetricStatisticType
    Dimensions: NotRequired[Sequence[MetricDimensionTypeDef]]
    Unit: NotRequired[str]


class CustomizedScalingMetricSpecificationOutputTypeDef(TypedDict):
    MetricName: str
    Namespace: str
    Statistic: MetricStatisticType
    Dimensions: NotRequired[list[MetricDimensionTypeDef]]
    Unit: NotRequired[str]


class CustomizedScalingMetricSpecificationTypeDef(TypedDict):
    MetricName: str
    Namespace: str
    Statistic: MetricStatisticType
    Dimensions: NotRequired[Sequence[MetricDimensionTypeDef]]
    Unit: NotRequired[str]


class GetScalingPlanResourceForecastDataResponseTypeDef(TypedDict):
    Datapoints: list[DatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeScalingPlanResourcesRequestPaginateTypeDef(TypedDict):
    ScalingPlanName: str
    ScalingPlanVersion: int
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetScalingPlanResourceForecastDataRequestRequestTypeDef(TypedDict):
    ScalingPlanName: str
    ScalingPlanVersion: int
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    ForecastDataType: ForecastDataTypeType
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef


TagFilterUnionTypeDef = Union[TagFilterTypeDef, TagFilterOutputTypeDef]
CustomizedLoadMetricSpecificationUnionTypeDef = Union[
    CustomizedLoadMetricSpecificationTypeDef, CustomizedLoadMetricSpecificationOutputTypeDef
]


class TargetTrackingConfigurationOutputTypeDef(TypedDict):
    TargetValue: float
    PredefinedScalingMetricSpecification: NotRequired[PredefinedScalingMetricSpecificationTypeDef]
    CustomizedScalingMetricSpecification: NotRequired[
        CustomizedScalingMetricSpecificationOutputTypeDef
    ]
    DisableScaleIn: NotRequired[bool]
    ScaleOutCooldown: NotRequired[int]
    ScaleInCooldown: NotRequired[int]
    EstimatedInstanceWarmup: NotRequired[int]


CustomizedScalingMetricSpecificationUnionTypeDef = Union[
    CustomizedScalingMetricSpecificationTypeDef, CustomizedScalingMetricSpecificationOutputTypeDef
]


class ApplicationSourceTypeDef(TypedDict):
    CloudFormationStackARN: NotRequired[str]
    TagFilters: NotRequired[Sequence[TagFilterUnionTypeDef]]


class ScalingInstructionOutputTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    MinCapacity: int
    MaxCapacity: int
    TargetTrackingConfigurations: list[TargetTrackingConfigurationOutputTypeDef]
    PredefinedLoadMetricSpecification: NotRequired[PredefinedLoadMetricSpecificationTypeDef]
    CustomizedLoadMetricSpecification: NotRequired[CustomizedLoadMetricSpecificationOutputTypeDef]
    ScheduledActionBufferTime: NotRequired[int]
    PredictiveScalingMaxCapacityBehavior: NotRequired[PredictiveScalingMaxCapacityBehaviorType]
    PredictiveScalingMaxCapacityBuffer: NotRequired[int]
    PredictiveScalingMode: NotRequired[PredictiveScalingModeType]
    ScalingPolicyUpdateBehavior: NotRequired[ScalingPolicyUpdateBehaviorType]
    DisableDynamicScaling: NotRequired[bool]


class ScalingPolicyTypeDef(TypedDict):
    PolicyName: str
    PolicyType: Literal["TargetTrackingScaling"]
    TargetTrackingConfiguration: NotRequired[TargetTrackingConfigurationOutputTypeDef]


class TargetTrackingConfigurationTypeDef(TypedDict):
    TargetValue: float
    PredefinedScalingMetricSpecification: NotRequired[PredefinedScalingMetricSpecificationTypeDef]
    CustomizedScalingMetricSpecification: NotRequired[
        CustomizedScalingMetricSpecificationUnionTypeDef
    ]
    DisableScaleIn: NotRequired[bool]
    ScaleOutCooldown: NotRequired[int]
    ScaleInCooldown: NotRequired[int]
    EstimatedInstanceWarmup: NotRequired[int]


class DescribeScalingPlansRequestPaginateTypeDef(TypedDict):
    ScalingPlanNames: NotRequired[Sequence[str]]
    ScalingPlanVersion: NotRequired[int]
    ApplicationSources: NotRequired[Sequence[ApplicationSourceTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeScalingPlansRequestRequestTypeDef(TypedDict):
    ScalingPlanNames: NotRequired[Sequence[str]]
    ScalingPlanVersion: NotRequired[int]
    ApplicationSources: NotRequired[Sequence[ApplicationSourceTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ScalingPlanTypeDef(TypedDict):
    ScalingPlanName: str
    ScalingPlanVersion: int
    ApplicationSource: ApplicationSourceOutputTypeDef
    ScalingInstructions: list[ScalingInstructionOutputTypeDef]
    StatusCode: ScalingPlanStatusCodeType
    StatusMessage: NotRequired[str]
    StatusStartTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]


class ScalingPlanResourceTypeDef(TypedDict):
    ScalingPlanName: str
    ScalingPlanVersion: int
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    ScalingStatusCode: ScalingStatusCodeType
    ScalingPolicies: NotRequired[list[ScalingPolicyTypeDef]]
    ScalingStatusMessage: NotRequired[str]


TargetTrackingConfigurationUnionTypeDef = Union[
    TargetTrackingConfigurationTypeDef, TargetTrackingConfigurationOutputTypeDef
]


class DescribeScalingPlansResponseTypeDef(TypedDict):
    ScalingPlans: list[ScalingPlanTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeScalingPlanResourcesResponseTypeDef(TypedDict):
    ScalingPlanResources: list[ScalingPlanResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ScalingInstructionTypeDef(TypedDict):
    ServiceNamespace: ServiceNamespaceType
    ResourceId: str
    ScalableDimension: ScalableDimensionType
    MinCapacity: int
    MaxCapacity: int
    TargetTrackingConfigurations: Sequence[TargetTrackingConfigurationUnionTypeDef]
    PredefinedLoadMetricSpecification: NotRequired[PredefinedLoadMetricSpecificationTypeDef]
    CustomizedLoadMetricSpecification: NotRequired[CustomizedLoadMetricSpecificationUnionTypeDef]
    ScheduledActionBufferTime: NotRequired[int]
    PredictiveScalingMaxCapacityBehavior: NotRequired[PredictiveScalingMaxCapacityBehaviorType]
    PredictiveScalingMaxCapacityBuffer: NotRequired[int]
    PredictiveScalingMode: NotRequired[PredictiveScalingModeType]
    ScalingPolicyUpdateBehavior: NotRequired[ScalingPolicyUpdateBehaviorType]
    DisableDynamicScaling: NotRequired[bool]


ScalingInstructionUnionTypeDef = Union[ScalingInstructionTypeDef, ScalingInstructionOutputTypeDef]


class UpdateScalingPlanRequestRequestTypeDef(TypedDict):
    ScalingPlanName: str
    ScalingPlanVersion: int
    ApplicationSource: NotRequired[ApplicationSourceTypeDef]
    ScalingInstructions: NotRequired[Sequence[ScalingInstructionTypeDef]]


class CreateScalingPlanRequestRequestTypeDef(TypedDict):
    ScalingPlanName: str
    ApplicationSource: ApplicationSourceTypeDef
    ScalingInstructions: Sequence[ScalingInstructionUnionTypeDef]
