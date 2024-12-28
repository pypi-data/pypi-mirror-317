"""
Type annotations for appintegrations service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appintegrations/type_defs/)

Usage::

    ```python
    from mypy_boto3_appintegrations.type_defs import ApplicationAssociationSummaryTypeDef

    data: ApplicationAssociationSummaryTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import ExecutionModeType, ExecutionStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "ApplicationAssociationSummaryTypeDef",
    "ApplicationSourceConfigOutputTypeDef",
    "ApplicationSourceConfigTypeDef",
    "ApplicationSummaryTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateDataIntegrationAssociationRequestRequestTypeDef",
    "CreateDataIntegrationAssociationResponseTypeDef",
    "CreateDataIntegrationRequestRequestTypeDef",
    "CreateDataIntegrationResponseTypeDef",
    "CreateEventIntegrationRequestRequestTypeDef",
    "CreateEventIntegrationResponseTypeDef",
    "DataIntegrationAssociationSummaryTypeDef",
    "DataIntegrationSummaryTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteDataIntegrationRequestRequestTypeDef",
    "DeleteEventIntegrationRequestRequestTypeDef",
    "EventFilterTypeDef",
    "EventIntegrationAssociationTypeDef",
    "EventIntegrationTypeDef",
    "ExecutionConfigurationTypeDef",
    "ExternalUrlConfigOutputTypeDef",
    "ExternalUrlConfigTypeDef",
    "ExternalUrlConfigUnionTypeDef",
    "FileConfigurationOutputTypeDef",
    "FileConfigurationTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "GetDataIntegrationRequestRequestTypeDef",
    "GetDataIntegrationResponseTypeDef",
    "GetEventIntegrationRequestRequestTypeDef",
    "GetEventIntegrationResponseTypeDef",
    "LastExecutionStatusTypeDef",
    "ListApplicationAssociationsRequestPaginateTypeDef",
    "ListApplicationAssociationsRequestRequestTypeDef",
    "ListApplicationAssociationsResponseTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListDataIntegrationAssociationsRequestPaginateTypeDef",
    "ListDataIntegrationAssociationsRequestRequestTypeDef",
    "ListDataIntegrationAssociationsResponseTypeDef",
    "ListDataIntegrationsRequestPaginateTypeDef",
    "ListDataIntegrationsRequestRequestTypeDef",
    "ListDataIntegrationsResponseTypeDef",
    "ListEventIntegrationAssociationsRequestPaginateTypeDef",
    "ListEventIntegrationAssociationsRequestRequestTypeDef",
    "ListEventIntegrationAssociationsResponseTypeDef",
    "ListEventIntegrationsRequestPaginateTypeDef",
    "ListEventIntegrationsRequestRequestTypeDef",
    "ListEventIntegrationsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OnDemandConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PublicationTypeDef",
    "ResponseMetadataTypeDef",
    "ScheduleConfigurationTypeDef",
    "SubscriptionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateDataIntegrationAssociationRequestRequestTypeDef",
    "UpdateDataIntegrationRequestRequestTypeDef",
    "UpdateEventIntegrationRequestRequestTypeDef",
)

class ApplicationAssociationSummaryTypeDef(TypedDict):
    ApplicationAssociationArn: NotRequired[str]
    ApplicationArn: NotRequired[str]
    ClientId: NotRequired[str]

class ExternalUrlConfigOutputTypeDef(TypedDict):
    AccessUrl: str
    ApprovedOrigins: NotRequired[list[str]]

class ApplicationSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    Namespace: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class PublicationTypeDef(TypedDict):
    Event: str
    Schema: str
    Description: NotRequired[str]

class SubscriptionTypeDef(TypedDict):
    Event: str
    Description: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class FileConfigurationTypeDef(TypedDict):
    Folders: Sequence[str]
    Filters: NotRequired[Mapping[str, Sequence[str]]]

class ScheduleConfigurationTypeDef(TypedDict):
    ScheduleExpression: str
    FirstExecutionFrom: NotRequired[str]
    Object: NotRequired[str]

class FileConfigurationOutputTypeDef(TypedDict):
    Folders: list[str]
    Filters: NotRequired[dict[str, list[str]]]

class EventFilterTypeDef(TypedDict):
    Source: str

class LastExecutionStatusTypeDef(TypedDict):
    ExecutionStatus: NotRequired[ExecutionStatusType]
    StatusMessage: NotRequired[str]

class DataIntegrationSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    SourceURI: NotRequired[str]

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    Arn: str

class DeleteDataIntegrationRequestRequestTypeDef(TypedDict):
    DataIntegrationIdentifier: str

class DeleteEventIntegrationRequestRequestTypeDef(TypedDict):
    Name: str

class EventIntegrationAssociationTypeDef(TypedDict):
    EventIntegrationAssociationArn: NotRequired[str]
    EventIntegrationAssociationId: NotRequired[str]
    EventIntegrationName: NotRequired[str]
    ClientId: NotRequired[str]
    EventBridgeRuleName: NotRequired[str]
    ClientAssociationMetadata: NotRequired[dict[str, str]]

class OnDemandConfigurationTypeDef(TypedDict):
    StartTime: str
    EndTime: NotRequired[str]

class ExternalUrlConfigTypeDef(TypedDict):
    AccessUrl: str
    ApprovedOrigins: NotRequired[Sequence[str]]

class GetApplicationRequestRequestTypeDef(TypedDict):
    Arn: str

class GetDataIntegrationRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetEventIntegrationRequestRequestTypeDef(TypedDict):
    Name: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListApplicationAssociationsRequestRequestTypeDef(TypedDict):
    ApplicationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListApplicationsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListDataIntegrationAssociationsRequestRequestTypeDef(TypedDict):
    DataIntegrationIdentifier: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListDataIntegrationsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEventIntegrationAssociationsRequestRequestTypeDef(TypedDict):
    EventIntegrationName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListEventIntegrationsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateDataIntegrationRequestRequestTypeDef(TypedDict):
    Identifier: str
    Name: NotRequired[str]
    Description: NotRequired[str]

class UpdateEventIntegrationRequestRequestTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]

class ApplicationSourceConfigOutputTypeDef(TypedDict):
    ExternalUrlConfig: NotRequired[ExternalUrlConfigOutputTypeDef]

class CreateApplicationResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataIntegrationAssociationResponseTypeDef(TypedDict):
    DataIntegrationAssociationId: str
    DataIntegrationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEventIntegrationResponseTypeDef(TypedDict):
    EventIntegrationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationAssociationsResponseTypeDef(TypedDict):
    ApplicationAssociations: list[ApplicationAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListApplicationsResponseTypeDef(TypedDict):
    Applications: list[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataIntegrationRequestRequestTypeDef(TypedDict):
    Name: str
    KmsKey: str
    Description: NotRequired[str]
    SourceURI: NotRequired[str]
    ScheduleConfig: NotRequired[ScheduleConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]
    FileConfiguration: NotRequired[FileConfigurationTypeDef]
    ObjectConfiguration: NotRequired[Mapping[str, Mapping[str, Sequence[str]]]]

class CreateDataIntegrationResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Name: str
    Description: str
    KmsKey: str
    SourceURI: str
    ScheduleConfiguration: ScheduleConfigurationTypeDef
    Tags: dict[str, str]
    ClientToken: str
    FileConfiguration: FileConfigurationOutputTypeDef
    ObjectConfiguration: dict[str, dict[str, list[str]]]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataIntegrationResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Name: str
    Description: str
    KmsKey: str
    SourceURI: str
    ScheduleConfiguration: ScheduleConfigurationTypeDef
    Tags: dict[str, str]
    FileConfiguration: FileConfigurationOutputTypeDef
    ObjectConfiguration: dict[str, dict[str, list[str]]]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEventIntegrationRequestRequestTypeDef(TypedDict):
    Name: str
    EventFilter: EventFilterTypeDef
    EventBridgeBus: str
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class EventIntegrationTypeDef(TypedDict):
    EventIntegrationArn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    EventFilter: NotRequired[EventFilterTypeDef]
    EventBridgeBus: NotRequired[str]
    Tags: NotRequired[dict[str, str]]

class GetEventIntegrationResponseTypeDef(TypedDict):
    Name: str
    Description: str
    EventIntegrationArn: str
    EventBridgeBus: str
    EventFilter: EventFilterTypeDef
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataIntegrationsResponseTypeDef(TypedDict):
    DataIntegrations: list[DataIntegrationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEventIntegrationAssociationsResponseTypeDef(TypedDict):
    EventIntegrationAssociations: list[EventIntegrationAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ExecutionConfigurationTypeDef(TypedDict):
    ExecutionMode: ExecutionModeType
    OnDemandConfiguration: NotRequired[OnDemandConfigurationTypeDef]
    ScheduleConfiguration: NotRequired[ScheduleConfigurationTypeDef]

ExternalUrlConfigUnionTypeDef = Union[ExternalUrlConfigTypeDef, ExternalUrlConfigOutputTypeDef]

class ListApplicationAssociationsRequestPaginateTypeDef(TypedDict):
    ApplicationId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataIntegrationAssociationsRequestPaginateTypeDef(TypedDict):
    DataIntegrationIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataIntegrationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEventIntegrationAssociationsRequestPaginateTypeDef(TypedDict):
    EventIntegrationName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEventIntegrationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetApplicationResponseTypeDef(TypedDict):
    Arn: str
    Id: str
    Name: str
    Namespace: str
    Description: str
    ApplicationSourceConfig: ApplicationSourceConfigOutputTypeDef
    Subscriptions: list[SubscriptionTypeDef]
    Publications: list[PublicationTypeDef]
    CreatedTime: datetime
    LastModifiedTime: datetime
    Tags: dict[str, str]
    Permissions: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListEventIntegrationsResponseTypeDef(TypedDict):
    EventIntegrations: list[EventIntegrationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateDataIntegrationAssociationRequestRequestTypeDef(TypedDict):
    DataIntegrationIdentifier: str
    ClientId: NotRequired[str]
    ObjectConfiguration: NotRequired[Mapping[str, Mapping[str, Sequence[str]]]]
    DestinationURI: NotRequired[str]
    ClientAssociationMetadata: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]
    ExecutionConfiguration: NotRequired[ExecutionConfigurationTypeDef]

class DataIntegrationAssociationSummaryTypeDef(TypedDict):
    DataIntegrationAssociationArn: NotRequired[str]
    DataIntegrationArn: NotRequired[str]
    ClientId: NotRequired[str]
    DestinationURI: NotRequired[str]
    LastExecutionStatus: NotRequired[LastExecutionStatusTypeDef]
    ExecutionConfiguration: NotRequired[ExecutionConfigurationTypeDef]

class UpdateDataIntegrationAssociationRequestRequestTypeDef(TypedDict):
    DataIntegrationIdentifier: str
    DataIntegrationAssociationIdentifier: str
    ExecutionConfiguration: ExecutionConfigurationTypeDef

class ApplicationSourceConfigTypeDef(TypedDict):
    ExternalUrlConfig: NotRequired[ExternalUrlConfigUnionTypeDef]

class ListDataIntegrationAssociationsResponseTypeDef(TypedDict):
    DataIntegrationAssociations: list[DataIntegrationAssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateApplicationRequestRequestTypeDef(TypedDict):
    Name: str
    Namespace: str
    ApplicationSourceConfig: ApplicationSourceConfigTypeDef
    Description: NotRequired[str]
    Subscriptions: NotRequired[Sequence[SubscriptionTypeDef]]
    Publications: NotRequired[Sequence[PublicationTypeDef]]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    Permissions: NotRequired[Sequence[str]]

class UpdateApplicationRequestRequestTypeDef(TypedDict):
    Arn: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    ApplicationSourceConfig: NotRequired[ApplicationSourceConfigTypeDef]
    Subscriptions: NotRequired[Sequence[SubscriptionTypeDef]]
    Publications: NotRequired[Sequence[PublicationTypeDef]]
    Permissions: NotRequired[Sequence[str]]
