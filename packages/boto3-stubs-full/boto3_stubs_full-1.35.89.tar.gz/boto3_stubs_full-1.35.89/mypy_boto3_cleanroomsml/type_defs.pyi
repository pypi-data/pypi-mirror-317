"""
Type annotations for cleanroomsml service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cleanroomsml/type_defs/)

Usage::

    ```python
    from mypy_boto3_cleanroomsml.type_defs import S3ConfigMapTypeDef

    data: S3ConfigMapTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    AudienceExportJobStatusType,
    AudienceGenerationJobStatusType,
    AudienceModelStatusType,
    AudienceSizeTypeType,
    ColumnTypeType,
    InferenceInstanceTypeType,
    InstanceTypeType,
    LogsStatusType,
    MetricsStatusType,
    MLInputChannelStatusType,
    NoiseLevelTypeType,
    PolicyExistenceConditionType,
    SharedAudienceMetricsType,
    TagOnCreatePolicyType,
    TrainedModelExportFileTypeType,
    TrainedModelExportJobStatusType,
    TrainedModelInferenceJobStatusType,
    TrainedModelStatusType,
    WorkerComputeTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AudienceDestinationTypeDef",
    "AudienceExportJobSummaryTypeDef",
    "AudienceGenerationJobDataSourceOutputTypeDef",
    "AudienceGenerationJobDataSourceTypeDef",
    "AudienceGenerationJobSummaryTypeDef",
    "AudienceModelSummaryTypeDef",
    "AudienceQualityMetricsTypeDef",
    "AudienceSizeConfigOutputTypeDef",
    "AudienceSizeConfigTypeDef",
    "AudienceSizeTypeDef",
    "CancelTrainedModelInferenceJobRequestRequestTypeDef",
    "CancelTrainedModelRequestRequestTypeDef",
    "CollaborationConfiguredModelAlgorithmAssociationSummaryTypeDef",
    "CollaborationMLInputChannelSummaryTypeDef",
    "CollaborationTrainedModelExportJobSummaryTypeDef",
    "CollaborationTrainedModelInferenceJobSummaryTypeDef",
    "CollaborationTrainedModelSummaryTypeDef",
    "ColumnSchemaOutputTypeDef",
    "ColumnSchemaTypeDef",
    "ColumnSchemaUnionTypeDef",
    "ComputeConfigurationTypeDef",
    "ConfiguredAudienceModelOutputConfigTypeDef",
    "ConfiguredAudienceModelSummaryTypeDef",
    "ConfiguredModelAlgorithmAssociationSummaryTypeDef",
    "ConfiguredModelAlgorithmSummaryTypeDef",
    "ContainerConfigOutputTypeDef",
    "ContainerConfigTypeDef",
    "CreateAudienceModelRequestRequestTypeDef",
    "CreateAudienceModelResponseTypeDef",
    "CreateConfiguredAudienceModelRequestRequestTypeDef",
    "CreateConfiguredAudienceModelResponseTypeDef",
    "CreateConfiguredModelAlgorithmAssociationRequestRequestTypeDef",
    "CreateConfiguredModelAlgorithmAssociationResponseTypeDef",
    "CreateConfiguredModelAlgorithmRequestRequestTypeDef",
    "CreateConfiguredModelAlgorithmResponseTypeDef",
    "CreateMLInputChannelRequestRequestTypeDef",
    "CreateMLInputChannelResponseTypeDef",
    "CreateTrainedModelRequestRequestTypeDef",
    "CreateTrainedModelResponseTypeDef",
    "CreateTrainingDatasetRequestRequestTypeDef",
    "CreateTrainingDatasetResponseTypeDef",
    "DataSourceTypeDef",
    "DatasetInputConfigOutputTypeDef",
    "DatasetInputConfigTypeDef",
    "DatasetInputConfigUnionTypeDef",
    "DatasetOutputTypeDef",
    "DatasetTypeDef",
    "DatasetUnionTypeDef",
    "DeleteAudienceGenerationJobRequestRequestTypeDef",
    "DeleteAudienceModelRequestRequestTypeDef",
    "DeleteConfiguredAudienceModelPolicyRequestRequestTypeDef",
    "DeleteConfiguredAudienceModelRequestRequestTypeDef",
    "DeleteConfiguredModelAlgorithmAssociationRequestRequestTypeDef",
    "DeleteConfiguredModelAlgorithmRequestRequestTypeDef",
    "DeleteMLConfigurationRequestRequestTypeDef",
    "DeleteMLInputChannelDataRequestRequestTypeDef",
    "DeleteTrainedModelOutputRequestRequestTypeDef",
    "DeleteTrainingDatasetRequestRequestTypeDef",
    "DestinationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAudienceGenerationJobRequestRequestTypeDef",
    "GetAudienceGenerationJobResponseTypeDef",
    "GetAudienceModelRequestRequestTypeDef",
    "GetAudienceModelResponseTypeDef",
    "GetCollaborationConfiguredModelAlgorithmAssociationRequestRequestTypeDef",
    "GetCollaborationConfiguredModelAlgorithmAssociationResponseTypeDef",
    "GetCollaborationMLInputChannelRequestRequestTypeDef",
    "GetCollaborationMLInputChannelResponseTypeDef",
    "GetCollaborationTrainedModelRequestRequestTypeDef",
    "GetCollaborationTrainedModelResponseTypeDef",
    "GetConfiguredAudienceModelPolicyRequestRequestTypeDef",
    "GetConfiguredAudienceModelPolicyResponseTypeDef",
    "GetConfiguredAudienceModelRequestRequestTypeDef",
    "GetConfiguredAudienceModelResponseTypeDef",
    "GetConfiguredModelAlgorithmAssociationRequestRequestTypeDef",
    "GetConfiguredModelAlgorithmAssociationResponseTypeDef",
    "GetConfiguredModelAlgorithmRequestRequestTypeDef",
    "GetConfiguredModelAlgorithmResponseTypeDef",
    "GetMLConfigurationRequestRequestTypeDef",
    "GetMLConfigurationResponseTypeDef",
    "GetMLInputChannelRequestRequestTypeDef",
    "GetMLInputChannelResponseTypeDef",
    "GetTrainedModelInferenceJobRequestRequestTypeDef",
    "GetTrainedModelInferenceJobResponseTypeDef",
    "GetTrainedModelRequestRequestTypeDef",
    "GetTrainedModelResponseTypeDef",
    "GetTrainingDatasetRequestRequestTypeDef",
    "GetTrainingDatasetResponseTypeDef",
    "GlueDataSourceTypeDef",
    "InferenceContainerConfigTypeDef",
    "InferenceContainerExecutionParametersTypeDef",
    "InferenceOutputConfigurationOutputTypeDef",
    "InferenceOutputConfigurationTypeDef",
    "InferenceReceiverMemberTypeDef",
    "InferenceResourceConfigTypeDef",
    "InputChannelDataSourceOutputTypeDef",
    "InputChannelDataSourceTypeDef",
    "InputChannelDataSourceUnionTypeDef",
    "InputChannelOutputTypeDef",
    "InputChannelTypeDef",
    "ListAudienceExportJobsRequestPaginateTypeDef",
    "ListAudienceExportJobsRequestRequestTypeDef",
    "ListAudienceExportJobsResponseTypeDef",
    "ListAudienceGenerationJobsRequestPaginateTypeDef",
    "ListAudienceGenerationJobsRequestRequestTypeDef",
    "ListAudienceGenerationJobsResponseTypeDef",
    "ListAudienceModelsRequestPaginateTypeDef",
    "ListAudienceModelsRequestRequestTypeDef",
    "ListAudienceModelsResponseTypeDef",
    "ListCollaborationConfiguredModelAlgorithmAssociationsRequestPaginateTypeDef",
    "ListCollaborationConfiguredModelAlgorithmAssociationsRequestRequestTypeDef",
    "ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef",
    "ListCollaborationMLInputChannelsRequestPaginateTypeDef",
    "ListCollaborationMLInputChannelsRequestRequestTypeDef",
    "ListCollaborationMLInputChannelsResponseTypeDef",
    "ListCollaborationTrainedModelExportJobsRequestPaginateTypeDef",
    "ListCollaborationTrainedModelExportJobsRequestRequestTypeDef",
    "ListCollaborationTrainedModelExportJobsResponseTypeDef",
    "ListCollaborationTrainedModelInferenceJobsRequestPaginateTypeDef",
    "ListCollaborationTrainedModelInferenceJobsRequestRequestTypeDef",
    "ListCollaborationTrainedModelInferenceJobsResponseTypeDef",
    "ListCollaborationTrainedModelsRequestPaginateTypeDef",
    "ListCollaborationTrainedModelsRequestRequestTypeDef",
    "ListCollaborationTrainedModelsResponseTypeDef",
    "ListConfiguredAudienceModelsRequestPaginateTypeDef",
    "ListConfiguredAudienceModelsRequestRequestTypeDef",
    "ListConfiguredAudienceModelsResponseTypeDef",
    "ListConfiguredModelAlgorithmAssociationsRequestPaginateTypeDef",
    "ListConfiguredModelAlgorithmAssociationsRequestRequestTypeDef",
    "ListConfiguredModelAlgorithmAssociationsResponseTypeDef",
    "ListConfiguredModelAlgorithmsRequestPaginateTypeDef",
    "ListConfiguredModelAlgorithmsRequestRequestTypeDef",
    "ListConfiguredModelAlgorithmsResponseTypeDef",
    "ListMLInputChannelsRequestPaginateTypeDef",
    "ListMLInputChannelsRequestRequestTypeDef",
    "ListMLInputChannelsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrainedModelInferenceJobsRequestPaginateTypeDef",
    "ListTrainedModelInferenceJobsRequestRequestTypeDef",
    "ListTrainedModelInferenceJobsResponseTypeDef",
    "ListTrainedModelsRequestPaginateTypeDef",
    "ListTrainedModelsRequestRequestTypeDef",
    "ListTrainedModelsResponseTypeDef",
    "ListTrainingDatasetsRequestPaginateTypeDef",
    "ListTrainingDatasetsRequestRequestTypeDef",
    "ListTrainingDatasetsResponseTypeDef",
    "LogsConfigurationPolicyOutputTypeDef",
    "LogsConfigurationPolicyTypeDef",
    "LogsConfigurationPolicyUnionTypeDef",
    "MLInputChannelSummaryTypeDef",
    "MLOutputConfigurationTypeDef",
    "MetricDefinitionTypeDef",
    "MetricsConfigurationPolicyTypeDef",
    "ModelInferenceDataSourceTypeDef",
    "ModelTrainingDataChannelTypeDef",
    "PaginatorConfigTypeDef",
    "PrivacyConfigurationOutputTypeDef",
    "PrivacyConfigurationPoliciesOutputTypeDef",
    "PrivacyConfigurationPoliciesTypeDef",
    "PrivacyConfigurationPoliciesUnionTypeDef",
    "PrivacyConfigurationTypeDef",
    "ProtectedQueryInputParametersOutputTypeDef",
    "ProtectedQueryInputParametersTypeDef",
    "ProtectedQueryInputParametersUnionTypeDef",
    "ProtectedQuerySQLParametersOutputTypeDef",
    "ProtectedQuerySQLParametersTypeDef",
    "ProtectedQuerySQLParametersUnionTypeDef",
    "PutConfiguredAudienceModelPolicyRequestRequestTypeDef",
    "PutConfiguredAudienceModelPolicyResponseTypeDef",
    "PutMLConfigurationRequestRequestTypeDef",
    "RelevanceMetricTypeDef",
    "ResourceConfigTypeDef",
    "ResponseMetadataTypeDef",
    "S3ConfigMapTypeDef",
    "StartAudienceExportJobRequestRequestTypeDef",
    "StartAudienceGenerationJobRequestRequestTypeDef",
    "StartAudienceGenerationJobResponseTypeDef",
    "StartTrainedModelExportJobRequestRequestTypeDef",
    "StartTrainedModelInferenceJobRequestRequestTypeDef",
    "StartTrainedModelInferenceJobResponseTypeDef",
    "StatusDetailsTypeDef",
    "StoppingConditionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "TrainedModelExportOutputConfigurationOutputTypeDef",
    "TrainedModelExportOutputConfigurationTypeDef",
    "TrainedModelExportReceiverMemberTypeDef",
    "TrainedModelExportsConfigurationPolicyOutputTypeDef",
    "TrainedModelExportsConfigurationPolicyTypeDef",
    "TrainedModelExportsConfigurationPolicyUnionTypeDef",
    "TrainedModelExportsMaxSizeTypeDef",
    "TrainedModelInferenceJobSummaryTypeDef",
    "TrainedModelInferenceJobsConfigurationPolicyOutputTypeDef",
    "TrainedModelInferenceJobsConfigurationPolicyTypeDef",
    "TrainedModelInferenceJobsConfigurationPolicyUnionTypeDef",
    "TrainedModelInferenceMaxOutputSizeTypeDef",
    "TrainedModelSummaryTypeDef",
    "TrainedModelsConfigurationPolicyOutputTypeDef",
    "TrainedModelsConfigurationPolicyTypeDef",
    "TrainedModelsConfigurationPolicyUnionTypeDef",
    "TrainingDatasetSummaryTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConfiguredAudienceModelRequestRequestTypeDef",
    "UpdateConfiguredAudienceModelResponseTypeDef",
    "WorkerComputeConfigurationTypeDef",
)

class S3ConfigMapTypeDef(TypedDict):
    s3Uri: str

AudienceSizeTypeDef = TypedDict(
    "AudienceSizeTypeDef",
    {
        "type": AudienceSizeTypeType,
        "value": int,
    },
)

class StatusDetailsTypeDef(TypedDict):
    statusCode: NotRequired[str]
    message: NotRequired[str]

class ProtectedQuerySQLParametersOutputTypeDef(TypedDict):
    queryString: NotRequired[str]
    analysisTemplateArn: NotRequired[str]
    parameters: NotRequired[dict[str, str]]

class AudienceGenerationJobSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    audienceGenerationJobArn: str
    name: str
    status: AudienceGenerationJobStatusType
    configuredAudienceModelArn: str
    description: NotRequired[str]
    collaborationId: NotRequired[str]
    startedBy: NotRequired[str]

class AudienceModelSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    audienceModelArn: str
    name: str
    trainingDatasetArn: str
    status: AudienceModelStatusType
    description: NotRequired[str]

class AudienceSizeConfigOutputTypeDef(TypedDict):
    audienceSizeType: AudienceSizeTypeType
    audienceSizeBins: list[int]

class AudienceSizeConfigTypeDef(TypedDict):
    audienceSizeType: AudienceSizeTypeType
    audienceSizeBins: Sequence[int]

class CancelTrainedModelInferenceJobRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    trainedModelInferenceJobArn: str

class CancelTrainedModelRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    trainedModelArn: str

class CollaborationConfiguredModelAlgorithmAssociationSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    configuredModelAlgorithmAssociationArn: str
    name: str
    membershipIdentifier: str
    collaborationIdentifier: str
    configuredModelAlgorithmArn: str
    creatorAccountId: str
    description: NotRequired[str]

class CollaborationMLInputChannelSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    membershipIdentifier: str
    collaborationIdentifier: str
    name: str
    configuredModelAlgorithmAssociations: list[str]
    mlInputChannelArn: str
    status: MLInputChannelStatusType
    creatorAccountId: str
    description: NotRequired[str]

class CollaborationTrainedModelSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainedModelArn: str
    name: str
    membershipIdentifier: str
    collaborationIdentifier: str
    status: TrainedModelStatusType
    configuredModelAlgorithmAssociationArn: str
    creatorAccountId: str
    description: NotRequired[str]

class ColumnSchemaOutputTypeDef(TypedDict):
    columnName: str
    columnTypes: list[ColumnTypeType]

class ColumnSchemaTypeDef(TypedDict):
    columnName: str
    columnTypes: Sequence[ColumnTypeType]

WorkerComputeConfigurationTypeDef = TypedDict(
    "WorkerComputeConfigurationTypeDef",
    {
        "type": NotRequired[WorkerComputeTypeType],
        "number": NotRequired[int],
    },
)

class ConfiguredModelAlgorithmAssociationSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    configuredModelAlgorithmAssociationArn: str
    configuredModelAlgorithmArn: str
    name: str
    membershipIdentifier: str
    collaborationIdentifier: str
    description: NotRequired[str]

class ConfiguredModelAlgorithmSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    configuredModelAlgorithmArn: str
    name: str
    description: NotRequired[str]

class MetricDefinitionTypeDef(TypedDict):
    name: str
    regex: str

TimestampTypeDef = Union[datetime, str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class InferenceContainerConfigTypeDef(TypedDict):
    imageUri: str

class ModelTrainingDataChannelTypeDef(TypedDict):
    mlInputChannelArn: str
    channelName: str

class ResourceConfigTypeDef(TypedDict):
    instanceType: InstanceTypeType
    volumeSizeInGB: int
    instanceCount: NotRequired[int]

class StoppingConditionTypeDef(TypedDict):
    maxRuntimeInSeconds: NotRequired[int]

class GlueDataSourceTypeDef(TypedDict):
    tableName: str
    databaseName: str
    catalogId: NotRequired[str]

class DeleteAudienceGenerationJobRequestRequestTypeDef(TypedDict):
    audienceGenerationJobArn: str

class DeleteAudienceModelRequestRequestTypeDef(TypedDict):
    audienceModelArn: str

class DeleteConfiguredAudienceModelPolicyRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str

class DeleteConfiguredAudienceModelRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str

class DeleteConfiguredModelAlgorithmAssociationRequestRequestTypeDef(TypedDict):
    configuredModelAlgorithmAssociationArn: str
    membershipIdentifier: str

class DeleteConfiguredModelAlgorithmRequestRequestTypeDef(TypedDict):
    configuredModelAlgorithmArn: str

class DeleteMLConfigurationRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str

class DeleteMLInputChannelDataRequestRequestTypeDef(TypedDict):
    mlInputChannelArn: str
    membershipIdentifier: str

class DeleteTrainedModelOutputRequestRequestTypeDef(TypedDict):
    trainedModelArn: str
    membershipIdentifier: str

class DeleteTrainingDatasetRequestRequestTypeDef(TypedDict):
    trainingDatasetArn: str

class GetAudienceGenerationJobRequestRequestTypeDef(TypedDict):
    audienceGenerationJobArn: str

class GetAudienceModelRequestRequestTypeDef(TypedDict):
    audienceModelArn: str

class GetCollaborationConfiguredModelAlgorithmAssociationRequestRequestTypeDef(TypedDict):
    configuredModelAlgorithmAssociationArn: str
    collaborationIdentifier: str

class GetCollaborationMLInputChannelRequestRequestTypeDef(TypedDict):
    mlInputChannelArn: str
    collaborationIdentifier: str

class GetCollaborationTrainedModelRequestRequestTypeDef(TypedDict):
    trainedModelArn: str
    collaborationIdentifier: str

class GetConfiguredAudienceModelPolicyRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str

class GetConfiguredAudienceModelRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str

class GetConfiguredModelAlgorithmAssociationRequestRequestTypeDef(TypedDict):
    configuredModelAlgorithmAssociationArn: str
    membershipIdentifier: str

class GetConfiguredModelAlgorithmRequestRequestTypeDef(TypedDict):
    configuredModelAlgorithmArn: str

class GetMLConfigurationRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str

class GetMLInputChannelRequestRequestTypeDef(TypedDict):
    mlInputChannelArn: str
    membershipIdentifier: str

class GetTrainedModelInferenceJobRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    trainedModelInferenceJobArn: str

class InferenceContainerExecutionParametersTypeDef(TypedDict):
    maxPayloadInMB: NotRequired[int]

class InferenceResourceConfigTypeDef(TypedDict):
    instanceType: InferenceInstanceTypeType
    instanceCount: NotRequired[int]

class ModelInferenceDataSourceTypeDef(TypedDict):
    mlInputChannelArn: str

class GetTrainedModelRequestRequestTypeDef(TypedDict):
    trainedModelArn: str
    membershipIdentifier: str

class GetTrainingDatasetRequestRequestTypeDef(TypedDict):
    trainingDatasetArn: str

class InferenceReceiverMemberTypeDef(TypedDict):
    accountId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAudienceExportJobsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    audienceGenerationJobArn: NotRequired[str]

class ListAudienceGenerationJobsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    configuredAudienceModelArn: NotRequired[str]
    collaborationId: NotRequired[str]

class ListAudienceModelsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationConfiguredModelAlgorithmAssociationsRequestRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationMLInputChannelsRequestRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationTrainedModelExportJobsRequestRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    trainedModelArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCollaborationTrainedModelInferenceJobsRequestRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    trainedModelArn: NotRequired[str]

class ListCollaborationTrainedModelsRequestRequestTypeDef(TypedDict):
    collaborationIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListConfiguredAudienceModelsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListConfiguredModelAlgorithmAssociationsRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListConfiguredModelAlgorithmsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListMLInputChannelsRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class MLInputChannelSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    membershipIdentifier: str
    collaborationIdentifier: str
    name: str
    configuredModelAlgorithmAssociations: list[str]
    mlInputChannelArn: str
    status: MLInputChannelStatusType
    protectedQueryIdentifier: NotRequired[str]
    description: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class ListTrainedModelInferenceJobsRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    trainedModelArn: NotRequired[str]

class ListTrainedModelsRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class TrainedModelSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainedModelArn: str
    name: str
    membershipIdentifier: str
    collaborationIdentifier: str
    status: TrainedModelStatusType
    configuredModelAlgorithmAssociationArn: str
    description: NotRequired[str]

class ListTrainingDatasetsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class TrainingDatasetSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainingDatasetArn: str
    name: str
    status: Literal["ACTIVE"]
    description: NotRequired[str]

class LogsConfigurationPolicyOutputTypeDef(TypedDict):
    allowedAccountIds: list[str]
    filterPattern: NotRequired[str]

class LogsConfigurationPolicyTypeDef(TypedDict):
    allowedAccountIds: Sequence[str]
    filterPattern: NotRequired[str]

class MetricsConfigurationPolicyTypeDef(TypedDict):
    noiseLevel: NoiseLevelTypeType

class ProtectedQuerySQLParametersTypeDef(TypedDict):
    queryString: NotRequired[str]
    analysisTemplateArn: NotRequired[str]
    parameters: NotRequired[Mapping[str, str]]

class PutConfiguredAudienceModelPolicyRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str
    configuredAudienceModelPolicy: str
    previousPolicyHash: NotRequired[str]
    policyExistenceCondition: NotRequired[PolicyExistenceConditionType]

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TrainedModelExportReceiverMemberTypeDef(TypedDict):
    accountId: str

class TrainedModelExportsMaxSizeTypeDef(TypedDict):
    unit: Literal["GB"]
    value: float

class TrainedModelInferenceMaxOutputSizeTypeDef(TypedDict):
    unit: Literal["GB"]
    value: float

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class AudienceDestinationTypeDef(TypedDict):
    s3Destination: S3ConfigMapTypeDef

class DestinationTypeDef(TypedDict):
    s3Destination: S3ConfigMapTypeDef

class RelevanceMetricTypeDef(TypedDict):
    audienceSize: AudienceSizeTypeDef
    score: NotRequired[float]

class StartAudienceExportJobRequestRequestTypeDef(TypedDict):
    name: str
    audienceGenerationJobArn: str
    audienceSize: AudienceSizeTypeDef
    description: NotRequired[str]

class AudienceExportJobSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    name: str
    audienceGenerationJobArn: str
    audienceSize: AudienceSizeTypeDef
    status: AudienceExportJobStatusType
    description: NotRequired[str]
    statusDetails: NotRequired[StatusDetailsTypeDef]
    outputLocation: NotRequired[str]

ColumnSchemaUnionTypeDef = Union[ColumnSchemaTypeDef, ColumnSchemaOutputTypeDef]

class ComputeConfigurationTypeDef(TypedDict):
    worker: NotRequired[WorkerComputeConfigurationTypeDef]

class ContainerConfigOutputTypeDef(TypedDict):
    imageUri: str
    entrypoint: NotRequired[list[str]]
    arguments: NotRequired[list[str]]
    metricDefinitions: NotRequired[list[MetricDefinitionTypeDef]]

class ContainerConfigTypeDef(TypedDict):
    imageUri: str
    entrypoint: NotRequired[Sequence[str]]
    arguments: NotRequired[Sequence[str]]
    metricDefinitions: NotRequired[Sequence[MetricDefinitionTypeDef]]

class CreateAudienceModelRequestRequestTypeDef(TypedDict):
    name: str
    trainingDatasetArn: str
    trainingDataStartTime: NotRequired[TimestampTypeDef]
    trainingDataEndTime: NotRequired[TimestampTypeDef]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    description: NotRequired[str]

class CreateAudienceModelResponseTypeDef(TypedDict):
    audienceModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConfiguredAudienceModelResponseTypeDef(TypedDict):
    configuredAudienceModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConfiguredModelAlgorithmAssociationResponseTypeDef(TypedDict):
    configuredModelAlgorithmAssociationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConfiguredModelAlgorithmResponseTypeDef(TypedDict):
    configuredModelAlgorithmArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMLInputChannelResponseTypeDef(TypedDict):
    mlInputChannelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrainedModelResponseTypeDef(TypedDict):
    trainedModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrainingDatasetResponseTypeDef(TypedDict):
    trainingDatasetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetAudienceModelResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainingDataStartTime: datetime
    trainingDataEndTime: datetime
    audienceModelArn: str
    name: str
    trainingDatasetArn: str
    status: AudienceModelStatusType
    statusDetails: StatusDetailsTypeDef
    kmsKeyArn: str
    tags: dict[str, str]
    description: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCollaborationMLInputChannelResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    creatorAccountId: str
    membershipIdentifier: str
    collaborationIdentifier: str
    mlInputChannelArn: str
    name: str
    configuredModelAlgorithmAssociations: list[str]
    status: MLInputChannelStatusType
    statusDetails: StatusDetailsTypeDef
    retentionInDays: int
    numberOfRecords: int
    description: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfiguredAudienceModelPolicyResponseTypeDef(TypedDict):
    configuredAudienceModelArn: str
    configuredAudienceModelPolicy: str
    policyHash: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAudienceGenerationJobsResponseTypeDef(TypedDict):
    audienceGenerationJobs: list[AudienceGenerationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAudienceModelsResponseTypeDef(TypedDict):
    audienceModels: list[AudienceModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef(TypedDict):
    collaborationConfiguredModelAlgorithmAssociations: list[
        CollaborationConfiguredModelAlgorithmAssociationSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCollaborationMLInputChannelsResponseTypeDef(TypedDict):
    collaborationMLInputChannelsList: list[CollaborationMLInputChannelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCollaborationTrainedModelsResponseTypeDef(TypedDict):
    collaborationTrainedModels: list[CollaborationTrainedModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListConfiguredModelAlgorithmAssociationsResponseTypeDef(TypedDict):
    configuredModelAlgorithmAssociations: list[ConfiguredModelAlgorithmAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListConfiguredModelAlgorithmsResponseTypeDef(TypedDict):
    configuredModelAlgorithms: list[ConfiguredModelAlgorithmSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutConfiguredAudienceModelPolicyResponseTypeDef(TypedDict):
    configuredAudienceModelPolicy: str
    policyHash: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartAudienceGenerationJobResponseTypeDef(TypedDict):
    audienceGenerationJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartTrainedModelInferenceJobResponseTypeDef(TypedDict):
    trainedModelInferenceJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredAudienceModelResponseTypeDef(TypedDict):
    configuredAudienceModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTrainedModelRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    name: str
    configuredModelAlgorithmAssociationArn: str
    resourceConfig: ResourceConfigTypeDef
    dataChannels: Sequence[ModelTrainingDataChannelTypeDef]
    hyperparameters: NotRequired[Mapping[str, str]]
    environment: NotRequired[Mapping[str, str]]
    stoppingCondition: NotRequired[StoppingConditionTypeDef]
    description: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class GetCollaborationTrainedModelResponseTypeDef(TypedDict):
    membershipIdentifier: str
    collaborationIdentifier: str
    trainedModelArn: str
    name: str
    description: str
    status: TrainedModelStatusType
    statusDetails: StatusDetailsTypeDef
    configuredModelAlgorithmAssociationArn: str
    resourceConfig: ResourceConfigTypeDef
    stoppingCondition: StoppingConditionTypeDef
    metricsStatus: MetricsStatusType
    metricsStatusDetails: str
    logsStatus: LogsStatusType
    logsStatusDetails: str
    trainingContainerImageDigest: str
    createTime: datetime
    updateTime: datetime
    creatorAccountId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetTrainedModelResponseTypeDef(TypedDict):
    membershipIdentifier: str
    collaborationIdentifier: str
    trainedModelArn: str
    name: str
    description: str
    status: TrainedModelStatusType
    statusDetails: StatusDetailsTypeDef
    configuredModelAlgorithmAssociationArn: str
    resourceConfig: ResourceConfigTypeDef
    stoppingCondition: StoppingConditionTypeDef
    metricsStatus: MetricsStatusType
    metricsStatusDetails: str
    logsStatus: LogsStatusType
    logsStatusDetails: str
    trainingContainerImageDigest: str
    createTime: datetime
    updateTime: datetime
    hyperparameters: dict[str, str]
    environment: dict[str, str]
    kmsKeyArn: str
    tags: dict[str, str]
    dataChannels: list[ModelTrainingDataChannelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DataSourceTypeDef(TypedDict):
    glueDataSource: GlueDataSourceTypeDef

class InferenceOutputConfigurationOutputTypeDef(TypedDict):
    members: list[InferenceReceiverMemberTypeDef]
    accept: NotRequired[str]

class InferenceOutputConfigurationTypeDef(TypedDict):
    members: Sequence[InferenceReceiverMemberTypeDef]
    accept: NotRequired[str]

class ListAudienceExportJobsRequestPaginateTypeDef(TypedDict):
    audienceGenerationJobArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAudienceGenerationJobsRequestPaginateTypeDef(TypedDict):
    configuredAudienceModelArn: NotRequired[str]
    collaborationId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAudienceModelsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationConfiguredModelAlgorithmAssociationsRequestPaginateTypeDef(TypedDict):
    collaborationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationMLInputChannelsRequestPaginateTypeDef(TypedDict):
    collaborationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationTrainedModelExportJobsRequestPaginateTypeDef(TypedDict):
    collaborationIdentifier: str
    trainedModelArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationTrainedModelInferenceJobsRequestPaginateTypeDef(TypedDict):
    collaborationIdentifier: str
    trainedModelArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCollaborationTrainedModelsRequestPaginateTypeDef(TypedDict):
    collaborationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfiguredAudienceModelsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfiguredModelAlgorithmAssociationsRequestPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConfiguredModelAlgorithmsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMLInputChannelsRequestPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrainedModelInferenceJobsRequestPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    trainedModelArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrainedModelsRequestPaginateTypeDef(TypedDict):
    membershipIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTrainingDatasetsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMLInputChannelsResponseTypeDef(TypedDict):
    mlInputChannelsList: list[MLInputChannelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTrainedModelsResponseTypeDef(TypedDict):
    trainedModels: list[TrainedModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTrainingDatasetsResponseTypeDef(TypedDict):
    trainingDatasets: list[TrainingDatasetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

LogsConfigurationPolicyUnionTypeDef = Union[
    LogsConfigurationPolicyTypeDef, LogsConfigurationPolicyOutputTypeDef
]

class TrainedModelsConfigurationPolicyOutputTypeDef(TypedDict):
    containerLogs: NotRequired[list[LogsConfigurationPolicyOutputTypeDef]]
    containerMetrics: NotRequired[MetricsConfigurationPolicyTypeDef]

class TrainedModelsConfigurationPolicyTypeDef(TypedDict):
    containerLogs: NotRequired[Sequence[LogsConfigurationPolicyTypeDef]]
    containerMetrics: NotRequired[MetricsConfigurationPolicyTypeDef]

ProtectedQuerySQLParametersUnionTypeDef = Union[
    ProtectedQuerySQLParametersTypeDef, ProtectedQuerySQLParametersOutputTypeDef
]

class TrainedModelExportOutputConfigurationOutputTypeDef(TypedDict):
    members: list[TrainedModelExportReceiverMemberTypeDef]

class TrainedModelExportOutputConfigurationTypeDef(TypedDict):
    members: Sequence[TrainedModelExportReceiverMemberTypeDef]

class TrainedModelExportsConfigurationPolicyOutputTypeDef(TypedDict):
    maxSize: TrainedModelExportsMaxSizeTypeDef
    filesToExport: list[TrainedModelExportFileTypeType]

class TrainedModelExportsConfigurationPolicyTypeDef(TypedDict):
    maxSize: TrainedModelExportsMaxSizeTypeDef
    filesToExport: Sequence[TrainedModelExportFileTypeType]

class TrainedModelInferenceJobsConfigurationPolicyOutputTypeDef(TypedDict):
    containerLogs: NotRequired[list[LogsConfigurationPolicyOutputTypeDef]]
    maxOutputSize: NotRequired[TrainedModelInferenceMaxOutputSizeTypeDef]

class ConfiguredAudienceModelOutputConfigTypeDef(TypedDict):
    destination: AudienceDestinationTypeDef
    roleArn: str

class MLOutputConfigurationTypeDef(TypedDict):
    roleArn: str
    destination: NotRequired[DestinationTypeDef]

class AudienceQualityMetricsTypeDef(TypedDict):
    relevanceMetrics: list[RelevanceMetricTypeDef]
    recallMetric: NotRequired[float]

class ListAudienceExportJobsResponseTypeDef(TypedDict):
    audienceExportJobs: list[AudienceExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AudienceGenerationJobDataSourceOutputTypeDef(TypedDict):
    roleArn: str
    dataSource: NotRequired[S3ConfigMapTypeDef]
    sqlParameters: NotRequired[ProtectedQuerySQLParametersOutputTypeDef]
    sqlComputeConfiguration: NotRequired[ComputeConfigurationTypeDef]

class ProtectedQueryInputParametersOutputTypeDef(TypedDict):
    sqlParameters: ProtectedQuerySQLParametersOutputTypeDef
    computeConfiguration: NotRequired[ComputeConfigurationTypeDef]

class GetConfiguredModelAlgorithmResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    configuredModelAlgorithmArn: str
    name: str
    trainingContainerConfig: ContainerConfigOutputTypeDef
    inferenceContainerConfig: InferenceContainerConfigTypeDef
    roleArn: str
    description: str
    tags: dict[str, str]
    kmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConfiguredModelAlgorithmRequestRequestTypeDef(TypedDict):
    name: str
    roleArn: str
    description: NotRequired[str]
    trainingContainerConfig: NotRequired[ContainerConfigTypeDef]
    inferenceContainerConfig: NotRequired[InferenceContainerConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]
    kmsKeyArn: NotRequired[str]

class DatasetInputConfigOutputTypeDef(TypedDict):
    schema: list[ColumnSchemaOutputTypeDef]
    dataSource: DataSourceTypeDef

class DatasetInputConfigTypeDef(TypedDict):
    schema: Sequence[ColumnSchemaUnionTypeDef]
    dataSource: DataSourceTypeDef

class CollaborationTrainedModelInferenceJobSummaryTypeDef(TypedDict):
    trainedModelInferenceJobArn: str
    membershipIdentifier: str
    trainedModelArn: str
    collaborationIdentifier: str
    status: TrainedModelInferenceJobStatusType
    outputConfiguration: InferenceOutputConfigurationOutputTypeDef
    name: str
    createTime: datetime
    updateTime: datetime
    creatorAccountId: str
    configuredModelAlgorithmAssociationArn: NotRequired[str]
    description: NotRequired[str]
    metricsStatus: NotRequired[MetricsStatusType]
    metricsStatusDetails: NotRequired[str]
    logsStatus: NotRequired[LogsStatusType]
    logsStatusDetails: NotRequired[str]

class GetTrainedModelInferenceJobResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainedModelInferenceJobArn: str
    configuredModelAlgorithmAssociationArn: str
    name: str
    status: TrainedModelInferenceJobStatusType
    trainedModelArn: str
    resourceConfig: InferenceResourceConfigTypeDef
    outputConfiguration: InferenceOutputConfigurationOutputTypeDef
    membershipIdentifier: str
    dataSource: ModelInferenceDataSourceTypeDef
    containerExecutionParameters: InferenceContainerExecutionParametersTypeDef
    statusDetails: StatusDetailsTypeDef
    description: str
    inferenceContainerImageDigest: str
    environment: dict[str, str]
    kmsKeyArn: str
    metricsStatus: MetricsStatusType
    metricsStatusDetails: str
    logsStatus: LogsStatusType
    logsStatusDetails: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class TrainedModelInferenceJobSummaryTypeDef(TypedDict):
    trainedModelInferenceJobArn: str
    membershipIdentifier: str
    trainedModelArn: str
    collaborationIdentifier: str
    status: TrainedModelInferenceJobStatusType
    outputConfiguration: InferenceOutputConfigurationOutputTypeDef
    name: str
    createTime: datetime
    updateTime: datetime
    configuredModelAlgorithmAssociationArn: NotRequired[str]
    description: NotRequired[str]
    metricsStatus: NotRequired[MetricsStatusType]
    metricsStatusDetails: NotRequired[str]
    logsStatus: NotRequired[LogsStatusType]
    logsStatusDetails: NotRequired[str]

class StartTrainedModelInferenceJobRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    name: str
    trainedModelArn: str
    resourceConfig: InferenceResourceConfigTypeDef
    outputConfiguration: InferenceOutputConfigurationTypeDef
    dataSource: ModelInferenceDataSourceTypeDef
    configuredModelAlgorithmAssociationArn: NotRequired[str]
    description: NotRequired[str]
    containerExecutionParameters: NotRequired[InferenceContainerExecutionParametersTypeDef]
    environment: NotRequired[Mapping[str, str]]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class TrainedModelInferenceJobsConfigurationPolicyTypeDef(TypedDict):
    containerLogs: NotRequired[Sequence[LogsConfigurationPolicyUnionTypeDef]]
    maxOutputSize: NotRequired[TrainedModelInferenceMaxOutputSizeTypeDef]

TrainedModelsConfigurationPolicyUnionTypeDef = Union[
    TrainedModelsConfigurationPolicyTypeDef, TrainedModelsConfigurationPolicyOutputTypeDef
]

class AudienceGenerationJobDataSourceTypeDef(TypedDict):
    roleArn: str
    dataSource: NotRequired[S3ConfigMapTypeDef]
    sqlParameters: NotRequired[ProtectedQuerySQLParametersUnionTypeDef]
    sqlComputeConfiguration: NotRequired[ComputeConfigurationTypeDef]

class ProtectedQueryInputParametersTypeDef(TypedDict):
    sqlParameters: ProtectedQuerySQLParametersUnionTypeDef
    computeConfiguration: NotRequired[ComputeConfigurationTypeDef]

class CollaborationTrainedModelExportJobSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    name: str
    outputConfiguration: TrainedModelExportOutputConfigurationOutputTypeDef
    status: TrainedModelExportJobStatusType
    creatorAccountId: str
    trainedModelArn: str
    membershipIdentifier: str
    collaborationIdentifier: str
    statusDetails: NotRequired[StatusDetailsTypeDef]
    description: NotRequired[str]

class StartTrainedModelExportJobRequestRequestTypeDef(TypedDict):
    name: str
    trainedModelArn: str
    membershipIdentifier: str
    outputConfiguration: TrainedModelExportOutputConfigurationTypeDef
    description: NotRequired[str]

TrainedModelExportsConfigurationPolicyUnionTypeDef = Union[
    TrainedModelExportsConfigurationPolicyTypeDef,
    TrainedModelExportsConfigurationPolicyOutputTypeDef,
]

class PrivacyConfigurationPoliciesOutputTypeDef(TypedDict):
    trainedModels: NotRequired[TrainedModelsConfigurationPolicyOutputTypeDef]
    trainedModelExports: NotRequired[TrainedModelExportsConfigurationPolicyOutputTypeDef]
    trainedModelInferenceJobs: NotRequired[
        TrainedModelInferenceJobsConfigurationPolicyOutputTypeDef
    ]

class ConfiguredAudienceModelSummaryTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    name: str
    audienceModelArn: str
    outputConfig: ConfiguredAudienceModelOutputConfigTypeDef
    configuredAudienceModelArn: str
    status: Literal["ACTIVE"]
    description: NotRequired[str]

class CreateConfiguredAudienceModelRequestRequestTypeDef(TypedDict):
    name: str
    audienceModelArn: str
    outputConfig: ConfiguredAudienceModelOutputConfigTypeDef
    sharedAudienceMetrics: Sequence[SharedAudienceMetricsType]
    description: NotRequired[str]
    minMatchingSeedSize: NotRequired[int]
    audienceSizeConfig: NotRequired[AudienceSizeConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]
    childResourceTagOnCreatePolicy: NotRequired[TagOnCreatePolicyType]

class GetConfiguredAudienceModelResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    configuredAudienceModelArn: str
    name: str
    audienceModelArn: str
    outputConfig: ConfiguredAudienceModelOutputConfigTypeDef
    description: str
    status: Literal["ACTIVE"]
    sharedAudienceMetrics: list[SharedAudienceMetricsType]
    minMatchingSeedSize: int
    audienceSizeConfig: AudienceSizeConfigOutputTypeDef
    tags: dict[str, str]
    childResourceTagOnCreatePolicy: TagOnCreatePolicyType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfiguredAudienceModelRequestRequestTypeDef(TypedDict):
    configuredAudienceModelArn: str
    outputConfig: NotRequired[ConfiguredAudienceModelOutputConfigTypeDef]
    audienceModelArn: NotRequired[str]
    sharedAudienceMetrics: NotRequired[Sequence[SharedAudienceMetricsType]]
    minMatchingSeedSize: NotRequired[int]
    audienceSizeConfig: NotRequired[AudienceSizeConfigTypeDef]
    description: NotRequired[str]

class GetMLConfigurationResponseTypeDef(TypedDict):
    membershipIdentifier: str
    defaultOutputLocation: MLOutputConfigurationTypeDef
    createTime: datetime
    updateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PutMLConfigurationRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    defaultOutputLocation: MLOutputConfigurationTypeDef

class GetAudienceGenerationJobResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    audienceGenerationJobArn: str
    name: str
    description: str
    status: AudienceGenerationJobStatusType
    statusDetails: StatusDetailsTypeDef
    configuredAudienceModelArn: str
    seedAudience: AudienceGenerationJobDataSourceOutputTypeDef
    includeSeedInOutput: bool
    collaborationId: str
    metrics: AudienceQualityMetricsTypeDef
    startedBy: str
    tags: dict[str, str]
    protectedQueryIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef

class InputChannelDataSourceOutputTypeDef(TypedDict):
    protectedQueryInputParameters: NotRequired[ProtectedQueryInputParametersOutputTypeDef]

DatasetOutputTypeDef = TypedDict(
    "DatasetOutputTypeDef",
    {
        "type": Literal["INTERACTIONS"],
        "inputConfig": DatasetInputConfigOutputTypeDef,
    },
)
DatasetInputConfigUnionTypeDef = Union[DatasetInputConfigTypeDef, DatasetInputConfigOutputTypeDef]

class ListCollaborationTrainedModelInferenceJobsResponseTypeDef(TypedDict):
    collaborationTrainedModelInferenceJobs: list[
        CollaborationTrainedModelInferenceJobSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTrainedModelInferenceJobsResponseTypeDef(TypedDict):
    trainedModelInferenceJobs: list[TrainedModelInferenceJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

TrainedModelInferenceJobsConfigurationPolicyUnionTypeDef = Union[
    TrainedModelInferenceJobsConfigurationPolicyTypeDef,
    TrainedModelInferenceJobsConfigurationPolicyOutputTypeDef,
]

class StartAudienceGenerationJobRequestRequestTypeDef(TypedDict):
    name: str
    configuredAudienceModelArn: str
    seedAudience: AudienceGenerationJobDataSourceTypeDef
    includeSeedInOutput: NotRequired[bool]
    collaborationId: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

ProtectedQueryInputParametersUnionTypeDef = Union[
    ProtectedQueryInputParametersTypeDef, ProtectedQueryInputParametersOutputTypeDef
]

class ListCollaborationTrainedModelExportJobsResponseTypeDef(TypedDict):
    collaborationTrainedModelExportJobs: list[CollaborationTrainedModelExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PrivacyConfigurationOutputTypeDef(TypedDict):
    policies: PrivacyConfigurationPoliciesOutputTypeDef

class ListConfiguredAudienceModelsResponseTypeDef(TypedDict):
    configuredAudienceModels: list[ConfiguredAudienceModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class InputChannelOutputTypeDef(TypedDict):
    dataSource: InputChannelDataSourceOutputTypeDef
    roleArn: str

class GetTrainingDatasetResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    trainingDatasetArn: str
    name: str
    trainingData: list[DatasetOutputTypeDef]
    status: Literal["ACTIVE"]
    roleArn: str
    tags: dict[str, str]
    description: str
    ResponseMetadata: ResponseMetadataTypeDef

DatasetTypeDef = TypedDict(
    "DatasetTypeDef",
    {
        "type": Literal["INTERACTIONS"],
        "inputConfig": DatasetInputConfigUnionTypeDef,
    },
)

class PrivacyConfigurationPoliciesTypeDef(TypedDict):
    trainedModels: NotRequired[TrainedModelsConfigurationPolicyUnionTypeDef]
    trainedModelExports: NotRequired[TrainedModelExportsConfigurationPolicyUnionTypeDef]
    trainedModelInferenceJobs: NotRequired[TrainedModelInferenceJobsConfigurationPolicyUnionTypeDef]

class InputChannelDataSourceTypeDef(TypedDict):
    protectedQueryInputParameters: NotRequired[ProtectedQueryInputParametersUnionTypeDef]

class GetCollaborationConfiguredModelAlgorithmAssociationResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    configuredModelAlgorithmAssociationArn: str
    membershipIdentifier: str
    collaborationIdentifier: str
    configuredModelAlgorithmArn: str
    name: str
    description: str
    creatorAccountId: str
    privacyConfiguration: PrivacyConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfiguredModelAlgorithmAssociationResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    configuredModelAlgorithmAssociationArn: str
    membershipIdentifier: str
    collaborationIdentifier: str
    configuredModelAlgorithmArn: str
    name: str
    privacyConfiguration: PrivacyConfigurationOutputTypeDef
    description: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetMLInputChannelResponseTypeDef(TypedDict):
    createTime: datetime
    updateTime: datetime
    membershipIdentifier: str
    collaborationIdentifier: str
    inputChannel: InputChannelOutputTypeDef
    protectedQueryIdentifier: str
    mlInputChannelArn: str
    name: str
    configuredModelAlgorithmAssociations: list[str]
    status: MLInputChannelStatusType
    statusDetails: StatusDetailsTypeDef
    retentionInDays: int
    numberOfRecords: int
    numberOfFiles: float
    sizeInGb: float
    description: str
    kmsKeyArn: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

DatasetUnionTypeDef = Union[DatasetTypeDef, DatasetOutputTypeDef]
PrivacyConfigurationPoliciesUnionTypeDef = Union[
    PrivacyConfigurationPoliciesTypeDef, PrivacyConfigurationPoliciesOutputTypeDef
]
InputChannelDataSourceUnionTypeDef = Union[
    InputChannelDataSourceTypeDef, InputChannelDataSourceOutputTypeDef
]

class CreateTrainingDatasetRequestRequestTypeDef(TypedDict):
    name: str
    roleArn: str
    trainingData: Sequence[DatasetUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]
    description: NotRequired[str]

class PrivacyConfigurationTypeDef(TypedDict):
    policies: PrivacyConfigurationPoliciesUnionTypeDef

class InputChannelTypeDef(TypedDict):
    dataSource: InputChannelDataSourceUnionTypeDef
    roleArn: str

class CreateConfiguredModelAlgorithmAssociationRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    configuredModelAlgorithmArn: str
    name: str
    description: NotRequired[str]
    privacyConfiguration: NotRequired[PrivacyConfigurationTypeDef]
    tags: NotRequired[Mapping[str, str]]

class CreateMLInputChannelRequestRequestTypeDef(TypedDict):
    membershipIdentifier: str
    configuredModelAlgorithmAssociations: Sequence[str]
    inputChannel: InputChannelTypeDef
    name: str
    retentionInDays: int
    description: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
