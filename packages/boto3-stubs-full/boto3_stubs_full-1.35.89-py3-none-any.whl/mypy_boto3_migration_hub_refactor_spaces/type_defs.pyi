"""
Type annotations for migration-hub-refactor-spaces service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_migration_hub_refactor_spaces/type_defs/)

Usage::

    ```python
    from mypy_boto3_migration_hub_refactor_spaces.type_defs import ApiGatewayProxyConfigTypeDef

    data: ApiGatewayProxyConfigTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence

from .literals import (
    ApiGatewayEndpointTypeType,
    ApplicationStateType,
    EnvironmentStateType,
    ErrorCodeType,
    ErrorResourceTypeType,
    HttpMethodType,
    NetworkFabricTypeType,
    RouteActivationStateType,
    RouteStateType,
    RouteTypeType,
    ServiceEndpointTypeType,
    ServiceStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ApiGatewayProxyConfigTypeDef",
    "ApiGatewayProxyInputTypeDef",
    "ApiGatewayProxySummaryTypeDef",
    "ApplicationSummaryTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "CreateRouteRequestRequestTypeDef",
    "CreateRouteResponseTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "CreateServiceResponseTypeDef",
    "DefaultRouteInputTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteApplicationResponseTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeleteEnvironmentResponseTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteRouteRequestRequestTypeDef",
    "DeleteRouteResponseTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "DeleteServiceResponseTypeDef",
    "EnvironmentSummaryTypeDef",
    "EnvironmentVpcTypeDef",
    "ErrorResponseTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetEnvironmentResponseTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetRouteRequestRequestTypeDef",
    "GetRouteResponseTypeDef",
    "GetServiceRequestRequestTypeDef",
    "GetServiceResponseTypeDef",
    "LambdaEndpointConfigTypeDef",
    "LambdaEndpointInputTypeDef",
    "LambdaEndpointSummaryTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListEnvironmentVpcsRequestPaginateTypeDef",
    "ListEnvironmentVpcsRequestRequestTypeDef",
    "ListEnvironmentVpcsResponseTypeDef",
    "ListEnvironmentsRequestPaginateTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "ListRoutesRequestPaginateTypeDef",
    "ListRoutesRequestRequestTypeDef",
    "ListRoutesResponseTypeDef",
    "ListServicesRequestPaginateTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RouteSummaryTypeDef",
    "ServiceSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateRouteRequestRequestTypeDef",
    "UpdateRouteResponseTypeDef",
    "UriPathRouteInputOutputTypeDef",
    "UriPathRouteInputTypeDef",
    "UrlEndpointConfigTypeDef",
    "UrlEndpointInputTypeDef",
    "UrlEndpointSummaryTypeDef",
)

class ApiGatewayProxyConfigTypeDef(TypedDict):
    ApiGatewayId: NotRequired[str]
    EndpointType: NotRequired[ApiGatewayEndpointTypeType]
    NlbArn: NotRequired[str]
    NlbName: NotRequired[str]
    ProxyUrl: NotRequired[str]
    StageName: NotRequired[str]
    VpcLinkId: NotRequired[str]

class ApiGatewayProxyInputTypeDef(TypedDict):
    EndpointType: NotRequired[ApiGatewayEndpointTypeType]
    StageName: NotRequired[str]

class ApiGatewayProxySummaryTypeDef(TypedDict):
    ApiGatewayId: NotRequired[str]
    EndpointType: NotRequired[ApiGatewayEndpointTypeType]
    NlbArn: NotRequired[str]
    NlbName: NotRequired[str]
    ProxyUrl: NotRequired[str]
    StageName: NotRequired[str]
    VpcLinkId: NotRequired[str]

class ErrorResponseTypeDef(TypedDict):
    AccountId: NotRequired[str]
    AdditionalDetails: NotRequired[dict[str, str]]
    Code: NotRequired[ErrorCodeType]
    Message: NotRequired[str]
    ResourceIdentifier: NotRequired[str]
    ResourceType: NotRequired[ErrorResourceTypeType]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateEnvironmentRequestRequestTypeDef(TypedDict):
    Name: str
    NetworkFabricType: NetworkFabricTypeType
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class DefaultRouteInputTypeDef(TypedDict):
    ActivationState: NotRequired[RouteActivationStateType]

class UriPathRouteInputTypeDef(TypedDict):
    ActivationState: RouteActivationStateType
    SourcePath: str
    AppendSourcePath: NotRequired[bool]
    IncludeChildPaths: NotRequired[bool]
    Methods: NotRequired[Sequence[HttpMethodType]]

class UriPathRouteInputOutputTypeDef(TypedDict):
    ActivationState: RouteActivationStateType
    SourcePath: str
    AppendSourcePath: NotRequired[bool]
    IncludeChildPaths: NotRequired[bool]
    Methods: NotRequired[list[HttpMethodType]]

class LambdaEndpointInputTypeDef(TypedDict):
    Arn: str

class UrlEndpointInputTypeDef(TypedDict):
    Url: str
    HealthUrl: NotRequired[str]

class DeleteApplicationRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str

class DeleteEnvironmentRequestRequestTypeDef(TypedDict):
    EnvironmentIdentifier: str

class DeleteResourcePolicyRequestRequestTypeDef(TypedDict):
    Identifier: str

class DeleteRouteRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    RouteIdentifier: str

class DeleteServiceRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    ServiceIdentifier: str

class EnvironmentVpcTypeDef(TypedDict):
    AccountId: NotRequired[str]
    CidrBlocks: NotRequired[list[str]]
    CreatedTime: NotRequired[datetime]
    EnvironmentId: NotRequired[str]
    LastUpdatedTime: NotRequired[datetime]
    VpcId: NotRequired[str]
    VpcName: NotRequired[str]

class GetApplicationRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str

class GetEnvironmentRequestRequestTypeDef(TypedDict):
    EnvironmentIdentifier: str

class GetResourcePolicyRequestRequestTypeDef(TypedDict):
    Identifier: str

class GetRouteRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    RouteIdentifier: str

class GetServiceRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    ServiceIdentifier: str

class LambdaEndpointConfigTypeDef(TypedDict):
    Arn: NotRequired[str]

class UrlEndpointConfigTypeDef(TypedDict):
    HealthUrl: NotRequired[str]
    Url: NotRequired[str]

class LambdaEndpointSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListApplicationsRequestRequestTypeDef(TypedDict):
    EnvironmentIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListEnvironmentVpcsRequestRequestTypeDef(TypedDict):
    EnvironmentIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListEnvironmentsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRoutesRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListServicesRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class PutResourcePolicyRequestRequestTypeDef(TypedDict):
    Policy: str
    ResourceArn: str

class UrlEndpointSummaryTypeDef(TypedDict):
    HealthUrl: NotRequired[str]
    Url: NotRequired[str]

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateRouteRequestRequestTypeDef(TypedDict):
    ActivationState: RouteActivationStateType
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    RouteIdentifier: str

class CreateApplicationRequestRequestTypeDef(TypedDict):
    EnvironmentIdentifier: str
    Name: str
    ProxyType: Literal["API_GATEWAY"]
    VpcId: str
    ApiGatewayProxy: NotRequired[ApiGatewayProxyInputTypeDef]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class ApplicationSummaryTypeDef(TypedDict):
    ApiGatewayProxy: NotRequired[ApiGatewayProxySummaryTypeDef]
    ApplicationId: NotRequired[str]
    Arn: NotRequired[str]
    CreatedByAccountId: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    EnvironmentId: NotRequired[str]
    Error: NotRequired[ErrorResponseTypeDef]
    LastUpdatedTime: NotRequired[datetime]
    Name: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    ProxyType: NotRequired[Literal["API_GATEWAY"]]
    State: NotRequired[ApplicationStateType]
    Tags: NotRequired[dict[str, str]]
    VpcId: NotRequired[str]

class EnvironmentSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    Description: NotRequired[str]
    EnvironmentId: NotRequired[str]
    Error: NotRequired[ErrorResponseTypeDef]
    LastUpdatedTime: NotRequired[datetime]
    Name: NotRequired[str]
    NetworkFabricType: NotRequired[NetworkFabricTypeType]
    OwnerAccountId: NotRequired[str]
    State: NotRequired[EnvironmentStateType]
    Tags: NotRequired[dict[str, str]]
    TransitGatewayId: NotRequired[str]

class RouteSummaryTypeDef(TypedDict):
    AppendSourcePath: NotRequired[bool]
    ApplicationId: NotRequired[str]
    Arn: NotRequired[str]
    CreatedByAccountId: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    EnvironmentId: NotRequired[str]
    Error: NotRequired[ErrorResponseTypeDef]
    IncludeChildPaths: NotRequired[bool]
    LastUpdatedTime: NotRequired[datetime]
    Methods: NotRequired[list[HttpMethodType]]
    OwnerAccountId: NotRequired[str]
    PathResourceToId: NotRequired[dict[str, str]]
    RouteId: NotRequired[str]
    RouteType: NotRequired[RouteTypeType]
    ServiceId: NotRequired[str]
    SourcePath: NotRequired[str]
    State: NotRequired[RouteStateType]
    Tags: NotRequired[dict[str, str]]

class CreateApplicationResponseTypeDef(TypedDict):
    ApiGatewayProxy: ApiGatewayProxyInputTypeDef
    ApplicationId: str
    Arn: str
    CreatedByAccountId: str
    CreatedTime: datetime
    EnvironmentId: str
    LastUpdatedTime: datetime
    Name: str
    OwnerAccountId: str
    ProxyType: Literal["API_GATEWAY"]
    State: ApplicationStateType
    Tags: dict[str, str]
    VpcId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEnvironmentResponseTypeDef(TypedDict):
    Arn: str
    CreatedTime: datetime
    Description: str
    EnvironmentId: str
    LastUpdatedTime: datetime
    Name: str
    NetworkFabricType: NetworkFabricTypeType
    OwnerAccountId: str
    State: EnvironmentStateType
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteApplicationResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    EnvironmentId: str
    LastUpdatedTime: datetime
    Name: str
    State: ApplicationStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteEnvironmentResponseTypeDef(TypedDict):
    Arn: str
    EnvironmentId: str
    LastUpdatedTime: datetime
    Name: str
    State: EnvironmentStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRouteResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    LastUpdatedTime: datetime
    RouteId: str
    ServiceId: str
    State: RouteStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteServiceResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    EnvironmentId: str
    LastUpdatedTime: datetime
    Name: str
    ServiceId: str
    State: ServiceStateType
    ResponseMetadata: ResponseMetadataTypeDef

class GetApplicationResponseTypeDef(TypedDict):
    ApiGatewayProxy: ApiGatewayProxyConfigTypeDef
    ApplicationId: str
    Arn: str
    CreatedByAccountId: str
    CreatedTime: datetime
    EnvironmentId: str
    Error: ErrorResponseTypeDef
    LastUpdatedTime: datetime
    Name: str
    OwnerAccountId: str
    ProxyType: Literal["API_GATEWAY"]
    State: ApplicationStateType
    Tags: dict[str, str]
    VpcId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentResponseTypeDef(TypedDict):
    Arn: str
    CreatedTime: datetime
    Description: str
    EnvironmentId: str
    Error: ErrorResponseTypeDef
    LastUpdatedTime: datetime
    Name: str
    NetworkFabricType: NetworkFabricTypeType
    OwnerAccountId: str
    State: EnvironmentStateType
    Tags: dict[str, str]
    TransitGatewayId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyResponseTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRouteResponseTypeDef(TypedDict):
    AppendSourcePath: bool
    ApplicationId: str
    Arn: str
    CreatedByAccountId: str
    CreatedTime: datetime
    EnvironmentId: str
    Error: ErrorResponseTypeDef
    IncludeChildPaths: bool
    LastUpdatedTime: datetime
    Methods: list[HttpMethodType]
    OwnerAccountId: str
    PathResourceToId: dict[str, str]
    RouteId: str
    RouteType: RouteTypeType
    ServiceId: str
    SourcePath: str
    State: RouteStateType
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRouteResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    LastUpdatedTime: datetime
    RouteId: str
    ServiceId: str
    State: RouteStateType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRouteRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    RouteType: RouteTypeType
    ServiceIdentifier: str
    ClientToken: NotRequired[str]
    DefaultRoute: NotRequired[DefaultRouteInputTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    UriPathRoute: NotRequired[UriPathRouteInputTypeDef]

class CreateRouteResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    CreatedByAccountId: str
    CreatedTime: datetime
    LastUpdatedTime: datetime
    OwnerAccountId: str
    RouteId: str
    RouteType: RouteTypeType
    ServiceId: str
    State: RouteStateType
    Tags: dict[str, str]
    UriPathRoute: UriPathRouteInputOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServiceRequestRequestTypeDef(TypedDict):
    ApplicationIdentifier: str
    EndpointType: ServiceEndpointTypeType
    EnvironmentIdentifier: str
    Name: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    LambdaEndpoint: NotRequired[LambdaEndpointInputTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    UrlEndpoint: NotRequired[UrlEndpointInputTypeDef]
    VpcId: NotRequired[str]

class CreateServiceResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    CreatedByAccountId: str
    CreatedTime: datetime
    Description: str
    EndpointType: ServiceEndpointTypeType
    EnvironmentId: str
    LambdaEndpoint: LambdaEndpointInputTypeDef
    LastUpdatedTime: datetime
    Name: str
    OwnerAccountId: str
    ServiceId: str
    State: ServiceStateType
    Tags: dict[str, str]
    UrlEndpoint: UrlEndpointInputTypeDef
    VpcId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListEnvironmentVpcsResponseTypeDef(TypedDict):
    EnvironmentVpcList: list[EnvironmentVpcTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetServiceResponseTypeDef(TypedDict):
    ApplicationId: str
    Arn: str
    CreatedByAccountId: str
    CreatedTime: datetime
    Description: str
    EndpointType: ServiceEndpointTypeType
    EnvironmentId: str
    Error: ErrorResponseTypeDef
    LambdaEndpoint: LambdaEndpointConfigTypeDef
    LastUpdatedTime: datetime
    Name: str
    OwnerAccountId: str
    ServiceId: str
    State: ServiceStateType
    Tags: dict[str, str]
    UrlEndpoint: UrlEndpointConfigTypeDef
    VpcId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListApplicationsRequestPaginateTypeDef(TypedDict):
    EnvironmentIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentVpcsRequestPaginateTypeDef(TypedDict):
    EnvironmentIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRoutesRequestPaginateTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicesRequestPaginateTypeDef(TypedDict):
    ApplicationIdentifier: str
    EnvironmentIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ServiceSummaryTypeDef(TypedDict):
    ApplicationId: NotRequired[str]
    Arn: NotRequired[str]
    CreatedByAccountId: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    Description: NotRequired[str]
    EndpointType: NotRequired[ServiceEndpointTypeType]
    EnvironmentId: NotRequired[str]
    Error: NotRequired[ErrorResponseTypeDef]
    LambdaEndpoint: NotRequired[LambdaEndpointSummaryTypeDef]
    LastUpdatedTime: NotRequired[datetime]
    Name: NotRequired[str]
    OwnerAccountId: NotRequired[str]
    ServiceId: NotRequired[str]
    State: NotRequired[ServiceStateType]
    Tags: NotRequired[dict[str, str]]
    UrlEndpoint: NotRequired[UrlEndpointSummaryTypeDef]
    VpcId: NotRequired[str]

class ListApplicationsResponseTypeDef(TypedDict):
    ApplicationSummaryList: list[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListEnvironmentsResponseTypeDef(TypedDict):
    EnvironmentSummaryList: list[EnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRoutesResponseTypeDef(TypedDict):
    RouteSummaryList: list[RouteSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListServicesResponseTypeDef(TypedDict):
    ServiceSummaryList: list[ServiceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
