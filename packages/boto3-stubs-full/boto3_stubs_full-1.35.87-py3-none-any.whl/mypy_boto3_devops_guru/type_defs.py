"""
Type annotations for devops-guru service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_guru/type_defs/)

Usage::

    ```python
    from mypy_boto3_devops_guru.type_defs import AccountInsightHealthTypeDef

    data: AccountInsightHealthTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence, Union

from .literals import (
    AnomalySeverityType,
    AnomalyStatusType,
    AnomalyTypeType,
    CloudWatchMetricDataStatusCodeType,
    CloudWatchMetricsStatType,
    CostEstimationServiceResourceStateType,
    CostEstimationStatusType,
    EventClassType,
    EventDataSourceType,
    EventSourceOptInStatusType,
    InsightFeedbackOptionType,
    InsightSeverityType,
    InsightStatusType,
    InsightTypeType,
    LocaleType,
    LogAnomalyTypeType,
    NotificationMessageTypeType,
    OptInStatusType,
    OrganizationResourceCollectionTypeType,
    ResourceCollectionTypeType,
    ResourcePermissionType,
    ResourceTypeFilterType,
    ServerSideEncryptionTypeType,
    ServiceNameType,
    UpdateResourceCollectionActionType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccountHealthTypeDef",
    "AccountInsightHealthTypeDef",
    "AddNotificationChannelRequestRequestTypeDef",
    "AddNotificationChannelResponseTypeDef",
    "AmazonCodeGuruProfilerIntegrationTypeDef",
    "AnomalousLogGroupTypeDef",
    "AnomalyReportedTimeRangeTypeDef",
    "AnomalyResourceTypeDef",
    "AnomalySourceDetailsTypeDef",
    "AnomalySourceMetadataTypeDef",
    "AnomalyTimeRangeTypeDef",
    "CloudFormationCollectionFilterTypeDef",
    "CloudFormationCollectionOutputTypeDef",
    "CloudFormationCollectionTypeDef",
    "CloudFormationCostEstimationResourceCollectionFilterOutputTypeDef",
    "CloudFormationCostEstimationResourceCollectionFilterTypeDef",
    "CloudFormationCostEstimationResourceCollectionFilterUnionTypeDef",
    "CloudFormationHealthTypeDef",
    "CloudWatchMetricsDataSummaryTypeDef",
    "CloudWatchMetricsDetailTypeDef",
    "CloudWatchMetricsDimensionTypeDef",
    "CostEstimationResourceCollectionFilterOutputTypeDef",
    "CostEstimationResourceCollectionFilterTypeDef",
    "CostEstimationTimeRangeTypeDef",
    "DeleteInsightRequestRequestTypeDef",
    "DescribeAccountHealthResponseTypeDef",
    "DescribeAccountOverviewRequestRequestTypeDef",
    "DescribeAccountOverviewResponseTypeDef",
    "DescribeAnomalyRequestRequestTypeDef",
    "DescribeAnomalyResponseTypeDef",
    "DescribeEventSourcesConfigResponseTypeDef",
    "DescribeFeedbackRequestRequestTypeDef",
    "DescribeFeedbackResponseTypeDef",
    "DescribeInsightRequestRequestTypeDef",
    "DescribeInsightResponseTypeDef",
    "DescribeOrganizationHealthRequestRequestTypeDef",
    "DescribeOrganizationHealthResponseTypeDef",
    "DescribeOrganizationOverviewRequestRequestTypeDef",
    "DescribeOrganizationOverviewResponseTypeDef",
    "DescribeOrganizationResourceCollectionHealthRequestPaginateTypeDef",
    "DescribeOrganizationResourceCollectionHealthRequestRequestTypeDef",
    "DescribeOrganizationResourceCollectionHealthResponseTypeDef",
    "DescribeResourceCollectionHealthRequestPaginateTypeDef",
    "DescribeResourceCollectionHealthRequestRequestTypeDef",
    "DescribeResourceCollectionHealthResponseTypeDef",
    "DescribeServiceIntegrationResponseTypeDef",
    "EndTimeRangeTypeDef",
    "EventResourceTypeDef",
    "EventSourcesConfigTypeDef",
    "EventTimeRangeTypeDef",
    "EventTypeDef",
    "GetCostEstimationRequestPaginateTypeDef",
    "GetCostEstimationRequestRequestTypeDef",
    "GetCostEstimationResponseTypeDef",
    "GetResourceCollectionRequestPaginateTypeDef",
    "GetResourceCollectionRequestRequestTypeDef",
    "GetResourceCollectionResponseTypeDef",
    "InsightFeedbackTypeDef",
    "InsightHealthTypeDef",
    "InsightTimeRangeTypeDef",
    "KMSServerSideEncryptionIntegrationConfigTypeDef",
    "KMSServerSideEncryptionIntegrationTypeDef",
    "ListAnomaliesForInsightFiltersTypeDef",
    "ListAnomaliesForInsightRequestPaginateTypeDef",
    "ListAnomaliesForInsightRequestRequestTypeDef",
    "ListAnomaliesForInsightResponseTypeDef",
    "ListAnomalousLogGroupsRequestPaginateTypeDef",
    "ListAnomalousLogGroupsRequestRequestTypeDef",
    "ListAnomalousLogGroupsResponseTypeDef",
    "ListEventsFiltersTypeDef",
    "ListEventsRequestPaginateTypeDef",
    "ListEventsRequestRequestTypeDef",
    "ListEventsResponseTypeDef",
    "ListInsightsAnyStatusFilterTypeDef",
    "ListInsightsClosedStatusFilterTypeDef",
    "ListInsightsOngoingStatusFilterTypeDef",
    "ListInsightsRequestPaginateTypeDef",
    "ListInsightsRequestRequestTypeDef",
    "ListInsightsResponseTypeDef",
    "ListInsightsStatusFilterTypeDef",
    "ListMonitoredResourcesFiltersTypeDef",
    "ListMonitoredResourcesRequestPaginateTypeDef",
    "ListMonitoredResourcesRequestRequestTypeDef",
    "ListMonitoredResourcesResponseTypeDef",
    "ListNotificationChannelsRequestPaginateTypeDef",
    "ListNotificationChannelsRequestRequestTypeDef",
    "ListNotificationChannelsResponseTypeDef",
    "ListOrganizationInsightsRequestPaginateTypeDef",
    "ListOrganizationInsightsRequestRequestTypeDef",
    "ListOrganizationInsightsResponseTypeDef",
    "ListRecommendationsRequestPaginateTypeDef",
    "ListRecommendationsRequestRequestTypeDef",
    "ListRecommendationsResponseTypeDef",
    "LogAnomalyClassTypeDef",
    "LogAnomalyShowcaseTypeDef",
    "LogsAnomalyDetectionIntegrationConfigTypeDef",
    "LogsAnomalyDetectionIntegrationTypeDef",
    "MonitoredResourceIdentifierTypeDef",
    "NotificationChannelConfigOutputTypeDef",
    "NotificationChannelConfigTypeDef",
    "NotificationChannelTypeDef",
    "NotificationFilterConfigOutputTypeDef",
    "NotificationFilterConfigTypeDef",
    "NotificationFilterConfigUnionTypeDef",
    "OpsCenterIntegrationConfigTypeDef",
    "OpsCenterIntegrationTypeDef",
    "PaginatorConfigTypeDef",
    "PerformanceInsightsMetricDimensionGroupTypeDef",
    "PerformanceInsightsMetricQueryTypeDef",
    "PerformanceInsightsMetricsDetailTypeDef",
    "PerformanceInsightsReferenceComparisonValuesTypeDef",
    "PerformanceInsightsReferenceDataTypeDef",
    "PerformanceInsightsReferenceMetricTypeDef",
    "PerformanceInsightsReferenceScalarTypeDef",
    "PerformanceInsightsStatTypeDef",
    "PredictionTimeRangeTypeDef",
    "ProactiveAnomalySummaryTypeDef",
    "ProactiveAnomalyTypeDef",
    "ProactiveInsightSummaryTypeDef",
    "ProactiveInsightTypeDef",
    "ProactiveOrganizationInsightSummaryTypeDef",
    "PutFeedbackRequestRequestTypeDef",
    "ReactiveAnomalySummaryTypeDef",
    "ReactiveAnomalyTypeDef",
    "ReactiveInsightSummaryTypeDef",
    "ReactiveInsightTypeDef",
    "ReactiveOrganizationInsightSummaryTypeDef",
    "RecommendationRelatedAnomalyResourceTypeDef",
    "RecommendationRelatedAnomalySourceDetailTypeDef",
    "RecommendationRelatedAnomalyTypeDef",
    "RecommendationRelatedCloudWatchMetricsSourceDetailTypeDef",
    "RecommendationRelatedEventResourceTypeDef",
    "RecommendationRelatedEventTypeDef",
    "RecommendationTypeDef",
    "RemoveNotificationChannelRequestRequestTypeDef",
    "ResourceCollectionFilterTypeDef",
    "ResourceCollectionOutputTypeDef",
    "ResourceCollectionTypeDef",
    "ResponseMetadataTypeDef",
    "SearchInsightsFiltersTypeDef",
    "SearchInsightsRequestPaginateTypeDef",
    "SearchInsightsRequestRequestTypeDef",
    "SearchInsightsResponseTypeDef",
    "SearchOrganizationInsightsFiltersTypeDef",
    "SearchOrganizationInsightsRequestPaginateTypeDef",
    "SearchOrganizationInsightsRequestRequestTypeDef",
    "SearchOrganizationInsightsResponseTypeDef",
    "ServiceCollectionOutputTypeDef",
    "ServiceCollectionTypeDef",
    "ServiceHealthTypeDef",
    "ServiceInsightHealthTypeDef",
    "ServiceIntegrationConfigTypeDef",
    "ServiceResourceCostTypeDef",
    "SnsChannelConfigTypeDef",
    "StartCostEstimationRequestRequestTypeDef",
    "StartTimeRangeTypeDef",
    "TagCollectionFilterTypeDef",
    "TagCollectionOutputTypeDef",
    "TagCollectionTypeDef",
    "TagCostEstimationResourceCollectionFilterOutputTypeDef",
    "TagCostEstimationResourceCollectionFilterTypeDef",
    "TagCostEstimationResourceCollectionFilterUnionTypeDef",
    "TagHealthTypeDef",
    "TimestampMetricValuePairTypeDef",
    "TimestampTypeDef",
    "UpdateCloudFormationCollectionFilterTypeDef",
    "UpdateEventSourcesConfigRequestRequestTypeDef",
    "UpdateResourceCollectionFilterTypeDef",
    "UpdateResourceCollectionRequestRequestTypeDef",
    "UpdateServiceIntegrationConfigTypeDef",
    "UpdateServiceIntegrationRequestRequestTypeDef",
    "UpdateTagCollectionFilterTypeDef",
)


class AccountInsightHealthTypeDef(TypedDict):
    OpenProactiveInsights: NotRequired[int]
    OpenReactiveInsights: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AmazonCodeGuruProfilerIntegrationTypeDef(TypedDict):
    Status: NotRequired[EventSourceOptInStatusType]


class AnomalyReportedTimeRangeTypeDef(TypedDict):
    OpenTime: datetime
    CloseTime: NotRequired[datetime]


AnomalyResourceTypeDef = TypedDict(
    "AnomalyResourceTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[str],
    },
)


class AnomalySourceMetadataTypeDef(TypedDict):
    Source: NotRequired[str]
    SourceResourceName: NotRequired[str]
    SourceResourceType: NotRequired[str]


class AnomalyTimeRangeTypeDef(TypedDict):
    StartTime: datetime
    EndTime: NotRequired[datetime]


class CloudFormationCollectionFilterTypeDef(TypedDict):
    StackNames: NotRequired[list[str]]


class CloudFormationCollectionOutputTypeDef(TypedDict):
    StackNames: NotRequired[list[str]]


class CloudFormationCollectionTypeDef(TypedDict):
    StackNames: NotRequired[Sequence[str]]


class CloudFormationCostEstimationResourceCollectionFilterOutputTypeDef(TypedDict):
    StackNames: NotRequired[list[str]]


class CloudFormationCostEstimationResourceCollectionFilterTypeDef(TypedDict):
    StackNames: NotRequired[Sequence[str]]


class InsightHealthTypeDef(TypedDict):
    OpenProactiveInsights: NotRequired[int]
    OpenReactiveInsights: NotRequired[int]
    MeanTimeToRecoverInMilliseconds: NotRequired[int]


class TimestampMetricValuePairTypeDef(TypedDict):
    Timestamp: NotRequired[datetime]
    MetricValue: NotRequired[float]


class CloudWatchMetricsDimensionTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class TagCostEstimationResourceCollectionFilterOutputTypeDef(TypedDict):
    AppBoundaryKey: str
    TagValues: list[str]


class CostEstimationTimeRangeTypeDef(TypedDict):
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class DeleteInsightRequestRequestTypeDef(TypedDict):
    Id: str


TimestampTypeDef = Union[datetime, str]


class DescribeAnomalyRequestRequestTypeDef(TypedDict):
    Id: str
    AccountId: NotRequired[str]


class DescribeFeedbackRequestRequestTypeDef(TypedDict):
    InsightId: NotRequired[str]


class InsightFeedbackTypeDef(TypedDict):
    Id: NotRequired[str]
    Feedback: NotRequired[InsightFeedbackOptionType]


class DescribeInsightRequestRequestTypeDef(TypedDict):
    Id: str
    AccountId: NotRequired[str]


class DescribeOrganizationHealthRequestRequestTypeDef(TypedDict):
    AccountIds: NotRequired[Sequence[str]]
    OrganizationalUnitIds: NotRequired[Sequence[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeOrganizationResourceCollectionHealthRequestRequestTypeDef(TypedDict):
    OrganizationResourceCollectionType: OrganizationResourceCollectionTypeType
    AccountIds: NotRequired[Sequence[str]]
    OrganizationalUnitIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeResourceCollectionHealthRequestRequestTypeDef(TypedDict):
    ResourceCollectionType: ResourceCollectionTypeType
    NextToken: NotRequired[str]


EventResourceTypeDef = TypedDict(
    "EventResourceTypeDef",
    {
        "Type": NotRequired[str],
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
    },
)


class GetCostEstimationRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]


ServiceResourceCostTypeDef = TypedDict(
    "ServiceResourceCostTypeDef",
    {
        "Type": NotRequired[str],
        "State": NotRequired[CostEstimationServiceResourceStateType],
        "Count": NotRequired[int],
        "UnitCost": NotRequired[float],
        "Cost": NotRequired[float],
    },
)


class GetResourceCollectionRequestRequestTypeDef(TypedDict):
    ResourceCollectionType: ResourceCollectionTypeType
    NextToken: NotRequired[str]


class InsightTimeRangeTypeDef(TypedDict):
    StartTime: datetime
    EndTime: NotRequired[datetime]


KMSServerSideEncryptionIntegrationConfigTypeDef = TypedDict(
    "KMSServerSideEncryptionIntegrationConfigTypeDef",
    {
        "KMSKeyId": NotRequired[str],
        "OptInStatus": NotRequired[OptInStatusType],
        "Type": NotRequired[ServerSideEncryptionTypeType],
    },
)
KMSServerSideEncryptionIntegrationTypeDef = TypedDict(
    "KMSServerSideEncryptionIntegrationTypeDef",
    {
        "KMSKeyId": NotRequired[str],
        "OptInStatus": NotRequired[OptInStatusType],
        "Type": NotRequired[ServerSideEncryptionTypeType],
    },
)


class ServiceCollectionTypeDef(TypedDict):
    ServiceNames: NotRequired[Sequence[ServiceNameType]]


class ListAnomalousLogGroupsRequestRequestTypeDef(TypedDict):
    InsightId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


ListInsightsOngoingStatusFilterTypeDef = TypedDict(
    "ListInsightsOngoingStatusFilterTypeDef",
    {
        "Type": InsightTypeType,
    },
)


class ListMonitoredResourcesFiltersTypeDef(TypedDict):
    ResourcePermission: ResourcePermissionType
    ResourceTypeFilters: Sequence[ResourceTypeFilterType]


class ListNotificationChannelsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]


class ListRecommendationsRequestRequestTypeDef(TypedDict):
    InsightId: str
    NextToken: NotRequired[str]
    Locale: NotRequired[LocaleType]
    AccountId: NotRequired[str]


class LogAnomalyClassTypeDef(TypedDict):
    LogStreamName: NotRequired[str]
    LogAnomalyType: NotRequired[LogAnomalyTypeType]
    LogAnomalyToken: NotRequired[str]
    LogEventId: NotRequired[str]
    Explanation: NotRequired[str]
    NumberOfLogLinesOccurrences: NotRequired[int]
    LogEventTimestamp: NotRequired[datetime]


class LogsAnomalyDetectionIntegrationConfigTypeDef(TypedDict):
    OptInStatus: NotRequired[OptInStatusType]


class LogsAnomalyDetectionIntegrationTypeDef(TypedDict):
    OptInStatus: NotRequired[OptInStatusType]


class NotificationFilterConfigOutputTypeDef(TypedDict):
    Severities: NotRequired[list[InsightSeverityType]]
    MessageTypes: NotRequired[list[NotificationMessageTypeType]]


class SnsChannelConfigTypeDef(TypedDict):
    TopicArn: NotRequired[str]


class NotificationFilterConfigTypeDef(TypedDict):
    Severities: NotRequired[Sequence[InsightSeverityType]]
    MessageTypes: NotRequired[Sequence[NotificationMessageTypeType]]


class OpsCenterIntegrationConfigTypeDef(TypedDict):
    OptInStatus: NotRequired[OptInStatusType]


class OpsCenterIntegrationTypeDef(TypedDict):
    OptInStatus: NotRequired[OptInStatusType]


class PerformanceInsightsMetricDimensionGroupTypeDef(TypedDict):
    Group: NotRequired[str]
    Dimensions: NotRequired[list[str]]
    Limit: NotRequired[int]


PerformanceInsightsStatTypeDef = TypedDict(
    "PerformanceInsightsStatTypeDef",
    {
        "Type": NotRequired[str],
        "Value": NotRequired[float],
    },
)


class PerformanceInsightsReferenceScalarTypeDef(TypedDict):
    Value: NotRequired[float]


class PredictionTimeRangeTypeDef(TypedDict):
    StartTime: datetime
    EndTime: NotRequired[datetime]


class ServiceCollectionOutputTypeDef(TypedDict):
    ServiceNames: NotRequired[list[ServiceNameType]]


RecommendationRelatedAnomalyResourceTypeDef = TypedDict(
    "RecommendationRelatedAnomalyResourceTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[str],
    },
)


class RecommendationRelatedCloudWatchMetricsSourceDetailTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]


RecommendationRelatedEventResourceTypeDef = TypedDict(
    "RecommendationRelatedEventResourceTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[str],
    },
)


class RemoveNotificationChannelRequestRequestTypeDef(TypedDict):
    Id: str


class TagCollectionFilterTypeDef(TypedDict):
    AppBoundaryKey: str
    TagValues: list[str]


class TagCollectionOutputTypeDef(TypedDict):
    AppBoundaryKey: str
    TagValues: list[str]


class TagCollectionTypeDef(TypedDict):
    AppBoundaryKey: str
    TagValues: Sequence[str]


class ServiceInsightHealthTypeDef(TypedDict):
    OpenProactiveInsights: NotRequired[int]
    OpenReactiveInsights: NotRequired[int]


class TagCostEstimationResourceCollectionFilterTypeDef(TypedDict):
    AppBoundaryKey: str
    TagValues: Sequence[str]


class UpdateCloudFormationCollectionFilterTypeDef(TypedDict):
    StackNames: NotRequired[Sequence[str]]


class UpdateTagCollectionFilterTypeDef(TypedDict):
    AppBoundaryKey: str
    TagValues: Sequence[str]


class AccountHealthTypeDef(TypedDict):
    AccountId: NotRequired[str]
    Insight: NotRequired[AccountInsightHealthTypeDef]


class AddNotificationChannelResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountHealthResponseTypeDef(TypedDict):
    OpenReactiveInsights: int
    OpenProactiveInsights: int
    MetricsAnalyzed: int
    ResourceHours: int
    AnalyzedResourceCount: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountOverviewResponseTypeDef(TypedDict):
    ReactiveInsights: int
    ProactiveInsights: int
    MeanTimeToRecoverInMilliseconds: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeOrganizationHealthResponseTypeDef(TypedDict):
    OpenReactiveInsights: int
    OpenProactiveInsights: int
    MetricsAnalyzed: int
    ResourceHours: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeOrganizationOverviewResponseTypeDef(TypedDict):
    ReactiveInsights: int
    ProactiveInsights: int
    ResponseMetadata: ResponseMetadataTypeDef


class EventSourcesConfigTypeDef(TypedDict):
    AmazonCodeGuruProfiler: NotRequired[AmazonCodeGuruProfilerIntegrationTypeDef]


CloudFormationCostEstimationResourceCollectionFilterUnionTypeDef = Union[
    CloudFormationCostEstimationResourceCollectionFilterTypeDef,
    CloudFormationCostEstimationResourceCollectionFilterOutputTypeDef,
]


class CloudFormationHealthTypeDef(TypedDict):
    StackName: NotRequired[str]
    Insight: NotRequired[InsightHealthTypeDef]
    AnalyzedResourceCount: NotRequired[int]


class TagHealthTypeDef(TypedDict):
    AppBoundaryKey: NotRequired[str]
    TagValue: NotRequired[str]
    Insight: NotRequired[InsightHealthTypeDef]
    AnalyzedResourceCount: NotRequired[int]


class CloudWatchMetricsDataSummaryTypeDef(TypedDict):
    TimestampMetricValuePairList: NotRequired[list[TimestampMetricValuePairTypeDef]]
    StatusCode: NotRequired[CloudWatchMetricDataStatusCodeType]


class CostEstimationResourceCollectionFilterOutputTypeDef(TypedDict):
    CloudFormation: NotRequired[CloudFormationCostEstimationResourceCollectionFilterOutputTypeDef]
    Tags: NotRequired[list[TagCostEstimationResourceCollectionFilterOutputTypeDef]]


class DescribeAccountOverviewRequestRequestTypeDef(TypedDict):
    FromTime: TimestampTypeDef
    ToTime: NotRequired[TimestampTypeDef]


class DescribeOrganizationOverviewRequestRequestTypeDef(TypedDict):
    FromTime: TimestampTypeDef
    ToTime: NotRequired[TimestampTypeDef]
    AccountIds: NotRequired[Sequence[str]]
    OrganizationalUnitIds: NotRequired[Sequence[str]]


class EndTimeRangeTypeDef(TypedDict):
    FromTime: NotRequired[TimestampTypeDef]
    ToTime: NotRequired[TimestampTypeDef]


class EventTimeRangeTypeDef(TypedDict):
    FromTime: TimestampTypeDef
    ToTime: TimestampTypeDef


class StartTimeRangeTypeDef(TypedDict):
    FromTime: NotRequired[TimestampTypeDef]
    ToTime: NotRequired[TimestampTypeDef]


class DescribeFeedbackResponseTypeDef(TypedDict):
    InsightFeedback: InsightFeedbackTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutFeedbackRequestRequestTypeDef(TypedDict):
    InsightFeedback: NotRequired[InsightFeedbackTypeDef]


class DescribeOrganizationResourceCollectionHealthRequestPaginateTypeDef(TypedDict):
    OrganizationResourceCollectionType: OrganizationResourceCollectionTypeType
    AccountIds: NotRequired[Sequence[str]]
    OrganizationalUnitIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeResourceCollectionHealthRequestPaginateTypeDef(TypedDict):
    ResourceCollectionType: ResourceCollectionTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCostEstimationRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetResourceCollectionRequestPaginateTypeDef(TypedDict):
    ResourceCollectionType: ResourceCollectionTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAnomalousLogGroupsRequestPaginateTypeDef(TypedDict):
    InsightId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNotificationChannelsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRecommendationsRequestPaginateTypeDef(TypedDict):
    InsightId: str
    Locale: NotRequired[LocaleType]
    AccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAnomaliesForInsightFiltersTypeDef(TypedDict):
    ServiceCollection: NotRequired[ServiceCollectionTypeDef]


class ListMonitoredResourcesRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[ListMonitoredResourcesFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoredResourcesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[ListMonitoredResourcesFiltersTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class LogAnomalyShowcaseTypeDef(TypedDict):
    LogAnomalyClasses: NotRequired[list[LogAnomalyClassTypeDef]]


class NotificationChannelConfigOutputTypeDef(TypedDict):
    Sns: SnsChannelConfigTypeDef
    Filters: NotRequired[NotificationFilterConfigOutputTypeDef]


NotificationFilterConfigUnionTypeDef = Union[
    NotificationFilterConfigTypeDef, NotificationFilterConfigOutputTypeDef
]


class UpdateServiceIntegrationConfigTypeDef(TypedDict):
    OpsCenter: NotRequired[OpsCenterIntegrationConfigTypeDef]
    LogsAnomalyDetection: NotRequired[LogsAnomalyDetectionIntegrationConfigTypeDef]
    KMSServerSideEncryption: NotRequired[KMSServerSideEncryptionIntegrationConfigTypeDef]


class ServiceIntegrationConfigTypeDef(TypedDict):
    OpsCenter: NotRequired[OpsCenterIntegrationTypeDef]
    LogsAnomalyDetection: NotRequired[LogsAnomalyDetectionIntegrationTypeDef]
    KMSServerSideEncryption: NotRequired[KMSServerSideEncryptionIntegrationTypeDef]


class PerformanceInsightsMetricQueryTypeDef(TypedDict):
    Metric: NotRequired[str]
    GroupBy: NotRequired[PerformanceInsightsMetricDimensionGroupTypeDef]
    Filter: NotRequired[dict[str, str]]


class RecommendationRelatedAnomalySourceDetailTypeDef(TypedDict):
    CloudWatchMetrics: NotRequired[list[RecommendationRelatedCloudWatchMetricsSourceDetailTypeDef]]


class RecommendationRelatedEventTypeDef(TypedDict):
    Name: NotRequired[str]
    Resources: NotRequired[list[RecommendationRelatedEventResourceTypeDef]]


class ResourceCollectionFilterTypeDef(TypedDict):
    CloudFormation: NotRequired[CloudFormationCollectionFilterTypeDef]
    Tags: NotRequired[list[TagCollectionFilterTypeDef]]


class ResourceCollectionOutputTypeDef(TypedDict):
    CloudFormation: NotRequired[CloudFormationCollectionOutputTypeDef]
    Tags: NotRequired[list[TagCollectionOutputTypeDef]]


class ResourceCollectionTypeDef(TypedDict):
    CloudFormation: NotRequired[CloudFormationCollectionTypeDef]
    Tags: NotRequired[Sequence[TagCollectionTypeDef]]


ServiceHealthTypeDef = TypedDict(
    "ServiceHealthTypeDef",
    {
        "ServiceName": NotRequired[ServiceNameType],
        "Insight": NotRequired[ServiceInsightHealthTypeDef],
        "AnalyzedResourceCount": NotRequired[int],
    },
)
TagCostEstimationResourceCollectionFilterUnionTypeDef = Union[
    TagCostEstimationResourceCollectionFilterTypeDef,
    TagCostEstimationResourceCollectionFilterOutputTypeDef,
]


class UpdateResourceCollectionFilterTypeDef(TypedDict):
    CloudFormation: NotRequired[UpdateCloudFormationCollectionFilterTypeDef]
    Tags: NotRequired[Sequence[UpdateTagCollectionFilterTypeDef]]


class DescribeEventSourcesConfigResponseTypeDef(TypedDict):
    EventSources: EventSourcesConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEventSourcesConfigRequestRequestTypeDef(TypedDict):
    EventSources: NotRequired[EventSourcesConfigTypeDef]


class CloudWatchMetricsDetailTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]
    Dimensions: NotRequired[list[CloudWatchMetricsDimensionTypeDef]]
    Stat: NotRequired[CloudWatchMetricsStatType]
    Unit: NotRequired[str]
    Period: NotRequired[int]
    MetricDataSummary: NotRequired[CloudWatchMetricsDataSummaryTypeDef]


class GetCostEstimationResponseTypeDef(TypedDict):
    ResourceCollection: CostEstimationResourceCollectionFilterOutputTypeDef
    Status: CostEstimationStatusType
    Costs: list[ServiceResourceCostTypeDef]
    TimeRange: CostEstimationTimeRangeTypeDef
    TotalCost: float
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


ListInsightsClosedStatusFilterTypeDef = TypedDict(
    "ListInsightsClosedStatusFilterTypeDef",
    {
        "Type": InsightTypeType,
        "EndTimeRange": EndTimeRangeTypeDef,
    },
)
ListInsightsAnyStatusFilterTypeDef = TypedDict(
    "ListInsightsAnyStatusFilterTypeDef",
    {
        "Type": InsightTypeType,
        "StartTimeRange": StartTimeRangeTypeDef,
    },
)


class ListAnomaliesForInsightRequestPaginateTypeDef(TypedDict):
    InsightId: str
    StartTimeRange: NotRequired[StartTimeRangeTypeDef]
    AccountId: NotRequired[str]
    Filters: NotRequired[ListAnomaliesForInsightFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAnomaliesForInsightRequestRequestTypeDef(TypedDict):
    InsightId: str
    StartTimeRange: NotRequired[StartTimeRangeTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccountId: NotRequired[str]
    Filters: NotRequired[ListAnomaliesForInsightFiltersTypeDef]


class AnomalousLogGroupTypeDef(TypedDict):
    LogGroupName: NotRequired[str]
    ImpactStartTime: NotRequired[datetime]
    ImpactEndTime: NotRequired[datetime]
    NumberOfLogLinesScanned: NotRequired[int]
    LogAnomalyShowcases: NotRequired[list[LogAnomalyShowcaseTypeDef]]


class NotificationChannelTypeDef(TypedDict):
    Id: NotRequired[str]
    Config: NotRequired[NotificationChannelConfigOutputTypeDef]


class NotificationChannelConfigTypeDef(TypedDict):
    Sns: SnsChannelConfigTypeDef
    Filters: NotRequired[NotificationFilterConfigUnionTypeDef]


class UpdateServiceIntegrationRequestRequestTypeDef(TypedDict):
    ServiceIntegration: UpdateServiceIntegrationConfigTypeDef


class DescribeServiceIntegrationResponseTypeDef(TypedDict):
    ServiceIntegration: ServiceIntegrationConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PerformanceInsightsReferenceMetricTypeDef(TypedDict):
    MetricQuery: NotRequired[PerformanceInsightsMetricQueryTypeDef]


class RecommendationRelatedAnomalyTypeDef(TypedDict):
    Resources: NotRequired[list[RecommendationRelatedAnomalyResourceTypeDef]]
    SourceDetails: NotRequired[list[RecommendationRelatedAnomalySourceDetailTypeDef]]
    AnomalyId: NotRequired[str]


class GetResourceCollectionResponseTypeDef(TypedDict):
    ResourceCollection: ResourceCollectionFilterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EventTypeDef(TypedDict):
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    Id: NotRequired[str]
    Time: NotRequired[datetime]
    EventSource: NotRequired[str]
    Name: NotRequired[str]
    DataSource: NotRequired[EventDataSourceType]
    EventClass: NotRequired[EventClassType]
    Resources: NotRequired[list[EventResourceTypeDef]]


MonitoredResourceIdentifierTypeDef = TypedDict(
    "MonitoredResourceIdentifierTypeDef",
    {
        "MonitoredResourceName": NotRequired[str],
        "Type": NotRequired[str],
        "ResourcePermission": NotRequired[ResourcePermissionType],
        "LastUpdated": NotRequired[datetime],
        "ResourceCollection": NotRequired[ResourceCollectionOutputTypeDef],
    },
)


class ProactiveInsightSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Severity: NotRequired[InsightSeverityType]
    Status: NotRequired[InsightStatusType]
    InsightTimeRange: NotRequired[InsightTimeRangeTypeDef]
    PredictionTimeRange: NotRequired[PredictionTimeRangeTypeDef]
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    ServiceCollection: NotRequired[ServiceCollectionOutputTypeDef]
    AssociatedResourceArns: NotRequired[list[str]]


class ProactiveInsightTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Severity: NotRequired[InsightSeverityType]
    Status: NotRequired[InsightStatusType]
    InsightTimeRange: NotRequired[InsightTimeRangeTypeDef]
    PredictionTimeRange: NotRequired[PredictionTimeRangeTypeDef]
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    SsmOpsItemId: NotRequired[str]
    Description: NotRequired[str]


class ProactiveOrganizationInsightSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    AccountId: NotRequired[str]
    OrganizationalUnitId: NotRequired[str]
    Name: NotRequired[str]
    Severity: NotRequired[InsightSeverityType]
    Status: NotRequired[InsightStatusType]
    InsightTimeRange: NotRequired[InsightTimeRangeTypeDef]
    PredictionTimeRange: NotRequired[PredictionTimeRangeTypeDef]
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    ServiceCollection: NotRequired[ServiceCollectionOutputTypeDef]


class ReactiveInsightSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Severity: NotRequired[InsightSeverityType]
    Status: NotRequired[InsightStatusType]
    InsightTimeRange: NotRequired[InsightTimeRangeTypeDef]
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    ServiceCollection: NotRequired[ServiceCollectionOutputTypeDef]
    AssociatedResourceArns: NotRequired[list[str]]


class ReactiveInsightTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Severity: NotRequired[InsightSeverityType]
    Status: NotRequired[InsightStatusType]
    InsightTimeRange: NotRequired[InsightTimeRangeTypeDef]
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    SsmOpsItemId: NotRequired[str]
    Description: NotRequired[str]


class ReactiveOrganizationInsightSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    AccountId: NotRequired[str]
    OrganizationalUnitId: NotRequired[str]
    Name: NotRequired[str]
    Severity: NotRequired[InsightSeverityType]
    Status: NotRequired[InsightStatusType]
    InsightTimeRange: NotRequired[InsightTimeRangeTypeDef]
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    ServiceCollection: NotRequired[ServiceCollectionOutputTypeDef]


class ListEventsFiltersTypeDef(TypedDict):
    InsightId: NotRequired[str]
    EventTimeRange: NotRequired[EventTimeRangeTypeDef]
    EventClass: NotRequired[EventClassType]
    EventSource: NotRequired[str]
    DataSource: NotRequired[EventDataSourceType]
    ResourceCollection: NotRequired[ResourceCollectionTypeDef]


class SearchInsightsFiltersTypeDef(TypedDict):
    Severities: NotRequired[Sequence[InsightSeverityType]]
    Statuses: NotRequired[Sequence[InsightStatusType]]
    ResourceCollection: NotRequired[ResourceCollectionTypeDef]
    ServiceCollection: NotRequired[ServiceCollectionTypeDef]


class SearchOrganizationInsightsFiltersTypeDef(TypedDict):
    Severities: NotRequired[Sequence[InsightSeverityType]]
    Statuses: NotRequired[Sequence[InsightStatusType]]
    ResourceCollection: NotRequired[ResourceCollectionTypeDef]
    ServiceCollection: NotRequired[ServiceCollectionTypeDef]


class DescribeOrganizationResourceCollectionHealthResponseTypeDef(TypedDict):
    CloudFormation: list[CloudFormationHealthTypeDef]
    Service: list[ServiceHealthTypeDef]
    Account: list[AccountHealthTypeDef]
    Tags: list[TagHealthTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeResourceCollectionHealthResponseTypeDef(TypedDict):
    CloudFormation: list[CloudFormationHealthTypeDef]
    Service: list[ServiceHealthTypeDef]
    Tags: list[TagHealthTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CostEstimationResourceCollectionFilterTypeDef(TypedDict):
    CloudFormation: NotRequired[CloudFormationCostEstimationResourceCollectionFilterUnionTypeDef]
    Tags: NotRequired[Sequence[TagCostEstimationResourceCollectionFilterUnionTypeDef]]


class UpdateResourceCollectionRequestRequestTypeDef(TypedDict):
    Action: UpdateResourceCollectionActionType
    ResourceCollection: UpdateResourceCollectionFilterTypeDef


ListInsightsStatusFilterTypeDef = TypedDict(
    "ListInsightsStatusFilterTypeDef",
    {
        "Ongoing": NotRequired[ListInsightsOngoingStatusFilterTypeDef],
        "Closed": NotRequired[ListInsightsClosedStatusFilterTypeDef],
        "Any": NotRequired[ListInsightsAnyStatusFilterTypeDef],
    },
)


class ListAnomalousLogGroupsResponseTypeDef(TypedDict):
    InsightId: str
    AnomalousLogGroups: list[AnomalousLogGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNotificationChannelsResponseTypeDef(TypedDict):
    Channels: list[NotificationChannelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AddNotificationChannelRequestRequestTypeDef(TypedDict):
    Config: NotificationChannelConfigTypeDef


class PerformanceInsightsReferenceComparisonValuesTypeDef(TypedDict):
    ReferenceScalar: NotRequired[PerformanceInsightsReferenceScalarTypeDef]
    ReferenceMetric: NotRequired[PerformanceInsightsReferenceMetricTypeDef]


class RecommendationTypeDef(TypedDict):
    Description: NotRequired[str]
    Link: NotRequired[str]
    Name: NotRequired[str]
    Reason: NotRequired[str]
    RelatedEvents: NotRequired[list[RecommendationRelatedEventTypeDef]]
    RelatedAnomalies: NotRequired[list[RecommendationRelatedAnomalyTypeDef]]
    Category: NotRequired[str]


class ListEventsResponseTypeDef(TypedDict):
    Events: list[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMonitoredResourcesResponseTypeDef(TypedDict):
    MonitoredResourceIdentifiers: list[MonitoredResourceIdentifierTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListInsightsResponseTypeDef(TypedDict):
    ProactiveInsights: list[ProactiveInsightSummaryTypeDef]
    ReactiveInsights: list[ReactiveInsightSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchInsightsResponseTypeDef(TypedDict):
    ProactiveInsights: list[ProactiveInsightSummaryTypeDef]
    ReactiveInsights: list[ReactiveInsightSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchOrganizationInsightsResponseTypeDef(TypedDict):
    ProactiveInsights: list[ProactiveInsightSummaryTypeDef]
    ReactiveInsights: list[ReactiveInsightSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInsightResponseTypeDef(TypedDict):
    ProactiveInsight: ProactiveInsightTypeDef
    ReactiveInsight: ReactiveInsightTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListOrganizationInsightsResponseTypeDef(TypedDict):
    ProactiveInsights: list[ProactiveOrganizationInsightSummaryTypeDef]
    ReactiveInsights: list[ReactiveOrganizationInsightSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListEventsRequestPaginateTypeDef(TypedDict):
    Filters: ListEventsFiltersTypeDef
    AccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEventsRequestRequestTypeDef(TypedDict):
    Filters: ListEventsFiltersTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    AccountId: NotRequired[str]


SearchInsightsRequestPaginateTypeDef = TypedDict(
    "SearchInsightsRequestPaginateTypeDef",
    {
        "StartTimeRange": StartTimeRangeTypeDef,
        "Type": InsightTypeType,
        "Filters": NotRequired[SearchInsightsFiltersTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchInsightsRequestRequestTypeDef = TypedDict(
    "SearchInsightsRequestRequestTypeDef",
    {
        "StartTimeRange": StartTimeRangeTypeDef,
        "Type": InsightTypeType,
        "Filters": NotRequired[SearchInsightsFiltersTypeDef],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
SearchOrganizationInsightsRequestPaginateTypeDef = TypedDict(
    "SearchOrganizationInsightsRequestPaginateTypeDef",
    {
        "AccountIds": Sequence[str],
        "StartTimeRange": StartTimeRangeTypeDef,
        "Type": InsightTypeType,
        "Filters": NotRequired[SearchOrganizationInsightsFiltersTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchOrganizationInsightsRequestRequestTypeDef = TypedDict(
    "SearchOrganizationInsightsRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
        "StartTimeRange": StartTimeRangeTypeDef,
        "Type": InsightTypeType,
        "Filters": NotRequired[SearchOrganizationInsightsFiltersTypeDef],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)


class StartCostEstimationRequestRequestTypeDef(TypedDict):
    ResourceCollection: CostEstimationResourceCollectionFilterTypeDef
    ClientToken: NotRequired[str]


class ListInsightsRequestPaginateTypeDef(TypedDict):
    StatusFilter: ListInsightsStatusFilterTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInsightsRequestRequestTypeDef(TypedDict):
    StatusFilter: ListInsightsStatusFilterTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListOrganizationInsightsRequestPaginateTypeDef(TypedDict):
    StatusFilter: ListInsightsStatusFilterTypeDef
    AccountIds: NotRequired[Sequence[str]]
    OrganizationalUnitIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOrganizationInsightsRequestRequestTypeDef(TypedDict):
    StatusFilter: ListInsightsStatusFilterTypeDef
    MaxResults: NotRequired[int]
    AccountIds: NotRequired[Sequence[str]]
    OrganizationalUnitIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]


class PerformanceInsightsReferenceDataTypeDef(TypedDict):
    Name: NotRequired[str]
    ComparisonValues: NotRequired[PerformanceInsightsReferenceComparisonValuesTypeDef]


class ListRecommendationsResponseTypeDef(TypedDict):
    Recommendations: list[RecommendationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PerformanceInsightsMetricsDetailTypeDef(TypedDict):
    MetricDisplayName: NotRequired[str]
    Unit: NotRequired[str]
    MetricQuery: NotRequired[PerformanceInsightsMetricQueryTypeDef]
    ReferenceData: NotRequired[list[PerformanceInsightsReferenceDataTypeDef]]
    StatsAtAnomaly: NotRequired[list[PerformanceInsightsStatTypeDef]]
    StatsAtBaseline: NotRequired[list[PerformanceInsightsStatTypeDef]]


class AnomalySourceDetailsTypeDef(TypedDict):
    CloudWatchMetrics: NotRequired[list[CloudWatchMetricsDetailTypeDef]]
    PerformanceInsightsMetrics: NotRequired[list[PerformanceInsightsMetricsDetailTypeDef]]


class ProactiveAnomalySummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Severity: NotRequired[AnomalySeverityType]
    Status: NotRequired[AnomalyStatusType]
    UpdateTime: NotRequired[datetime]
    AnomalyTimeRange: NotRequired[AnomalyTimeRangeTypeDef]
    AnomalyReportedTimeRange: NotRequired[AnomalyReportedTimeRangeTypeDef]
    PredictionTimeRange: NotRequired[PredictionTimeRangeTypeDef]
    SourceDetails: NotRequired[AnomalySourceDetailsTypeDef]
    AssociatedInsightId: NotRequired[str]
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    Limit: NotRequired[float]
    SourceMetadata: NotRequired[AnomalySourceMetadataTypeDef]
    AnomalyResources: NotRequired[list[AnomalyResourceTypeDef]]
    Description: NotRequired[str]


class ProactiveAnomalyTypeDef(TypedDict):
    Id: NotRequired[str]
    Severity: NotRequired[AnomalySeverityType]
    Status: NotRequired[AnomalyStatusType]
    UpdateTime: NotRequired[datetime]
    AnomalyTimeRange: NotRequired[AnomalyTimeRangeTypeDef]
    AnomalyReportedTimeRange: NotRequired[AnomalyReportedTimeRangeTypeDef]
    PredictionTimeRange: NotRequired[PredictionTimeRangeTypeDef]
    SourceDetails: NotRequired[AnomalySourceDetailsTypeDef]
    AssociatedInsightId: NotRequired[str]
    ResourceCollection: NotRequired[ResourceCollectionOutputTypeDef]
    Limit: NotRequired[float]
    SourceMetadata: NotRequired[AnomalySourceMetadataTypeDef]
    AnomalyResources: NotRequired[list[AnomalyResourceTypeDef]]
    Description: NotRequired[str]


ReactiveAnomalySummaryTypeDef = TypedDict(
    "ReactiveAnomalySummaryTypeDef",
    {
        "Id": NotRequired[str],
        "Severity": NotRequired[AnomalySeverityType],
        "Status": NotRequired[AnomalyStatusType],
        "AnomalyTimeRange": NotRequired[AnomalyTimeRangeTypeDef],
        "AnomalyReportedTimeRange": NotRequired[AnomalyReportedTimeRangeTypeDef],
        "SourceDetails": NotRequired[AnomalySourceDetailsTypeDef],
        "AssociatedInsightId": NotRequired[str],
        "ResourceCollection": NotRequired[ResourceCollectionOutputTypeDef],
        "Type": NotRequired[AnomalyTypeType],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "CausalAnomalyId": NotRequired[str],
        "AnomalyResources": NotRequired[list[AnomalyResourceTypeDef]],
    },
)
ReactiveAnomalyTypeDef = TypedDict(
    "ReactiveAnomalyTypeDef",
    {
        "Id": NotRequired[str],
        "Severity": NotRequired[AnomalySeverityType],
        "Status": NotRequired[AnomalyStatusType],
        "AnomalyTimeRange": NotRequired[AnomalyTimeRangeTypeDef],
        "AnomalyReportedTimeRange": NotRequired[AnomalyReportedTimeRangeTypeDef],
        "SourceDetails": NotRequired[AnomalySourceDetailsTypeDef],
        "AssociatedInsightId": NotRequired[str],
        "ResourceCollection": NotRequired[ResourceCollectionOutputTypeDef],
        "Type": NotRequired[AnomalyTypeType],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "CausalAnomalyId": NotRequired[str],
        "AnomalyResources": NotRequired[list[AnomalyResourceTypeDef]],
    },
)


class ListAnomaliesForInsightResponseTypeDef(TypedDict):
    ProactiveAnomalies: list[ProactiveAnomalySummaryTypeDef]
    ReactiveAnomalies: list[ReactiveAnomalySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeAnomalyResponseTypeDef(TypedDict):
    ProactiveAnomaly: ProactiveAnomalyTypeDef
    ReactiveAnomaly: ReactiveAnomalyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
