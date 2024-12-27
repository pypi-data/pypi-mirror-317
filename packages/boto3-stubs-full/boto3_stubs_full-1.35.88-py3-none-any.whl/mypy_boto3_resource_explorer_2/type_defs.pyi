"""
Type annotations for resource-explorer-2 service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_explorer_2/type_defs/)

Usage::

    ```python
    from mypy_boto3_resource_explorer_2.type_defs import AssociateDefaultViewInputRequestTypeDef

    data: AssociateDefaultViewInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Mapping, Sequence

from .literals import AWSServiceAccessStatusType, IndexStateType, IndexTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AssociateDefaultViewInputRequestTypeDef",
    "AssociateDefaultViewOutputTypeDef",
    "BatchGetViewErrorTypeDef",
    "BatchGetViewInputRequestTypeDef",
    "BatchGetViewOutputTypeDef",
    "CreateIndexInputRequestTypeDef",
    "CreateIndexOutputTypeDef",
    "CreateViewInputRequestTypeDef",
    "CreateViewOutputTypeDef",
    "DeleteIndexInputRequestTypeDef",
    "DeleteIndexOutputTypeDef",
    "DeleteViewInputRequestTypeDef",
    "DeleteViewOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAccountLevelServiceConfigurationOutputTypeDef",
    "GetDefaultViewOutputTypeDef",
    "GetIndexOutputTypeDef",
    "GetManagedViewInputRequestTypeDef",
    "GetManagedViewOutputTypeDef",
    "GetViewInputRequestTypeDef",
    "GetViewOutputTypeDef",
    "IncludedPropertyTypeDef",
    "IndexTypeDef",
    "ListIndexesForMembersInputPaginateTypeDef",
    "ListIndexesForMembersInputRequestTypeDef",
    "ListIndexesForMembersOutputTypeDef",
    "ListIndexesInputPaginateTypeDef",
    "ListIndexesInputRequestTypeDef",
    "ListIndexesOutputTypeDef",
    "ListManagedViewsInputPaginateTypeDef",
    "ListManagedViewsInputRequestTypeDef",
    "ListManagedViewsOutputTypeDef",
    "ListResourcesInputPaginateTypeDef",
    "ListResourcesInputRequestTypeDef",
    "ListResourcesOutputTypeDef",
    "ListSupportedResourceTypesInputPaginateTypeDef",
    "ListSupportedResourceTypesInputRequestTypeDef",
    "ListSupportedResourceTypesOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListViewsInputPaginateTypeDef",
    "ListViewsInputRequestTypeDef",
    "ListViewsOutputTypeDef",
    "ManagedViewTypeDef",
    "MemberIndexTypeDef",
    "OrgConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceCountTypeDef",
    "ResourcePropertyTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "SearchFilterTypeDef",
    "SearchInputPaginateTypeDef",
    "SearchInputRequestTypeDef",
    "SearchOutputTypeDef",
    "SupportedResourceTypeTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateIndexTypeInputRequestTypeDef",
    "UpdateIndexTypeOutputTypeDef",
    "UpdateViewInputRequestTypeDef",
    "UpdateViewOutputTypeDef",
    "ViewTypeDef",
)

class AssociateDefaultViewInputRequestTypeDef(TypedDict):
    ViewArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchGetViewErrorTypeDef(TypedDict):
    ErrorMessage: str
    ViewArn: str

class BatchGetViewInputRequestTypeDef(TypedDict):
    ViewArns: NotRequired[Sequence[str]]

class CreateIndexInputRequestTypeDef(TypedDict):
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class IncludedPropertyTypeDef(TypedDict):
    Name: str

class SearchFilterTypeDef(TypedDict):
    FilterString: str

class DeleteIndexInputRequestTypeDef(TypedDict):
    Arn: str

class DeleteViewInputRequestTypeDef(TypedDict):
    ViewArn: str

class OrgConfigurationTypeDef(TypedDict):
    AWSServiceAccessStatus: AWSServiceAccessStatusType
    ServiceLinkedRole: NotRequired[str]

class GetManagedViewInputRequestTypeDef(TypedDict):
    ManagedViewArn: str

class GetViewInputRequestTypeDef(TypedDict):
    ViewArn: str

IndexTypeDef = TypedDict(
    "IndexTypeDef",
    {
        "Arn": NotRequired[str],
        "Region": NotRequired[str],
        "Type": NotRequired[IndexTypeType],
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListIndexesForMembersInputRequestTypeDef(TypedDict):
    AccountIdList: Sequence[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

MemberIndexTypeDef = TypedDict(
    "MemberIndexTypeDef",
    {
        "AccountId": NotRequired[str],
        "Arn": NotRequired[str],
        "Region": NotRequired[str],
        "Type": NotRequired[IndexTypeType],
    },
)
ListIndexesInputRequestTypeDef = TypedDict(
    "ListIndexesInputRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "Regions": NotRequired[Sequence[str]],
        "Type": NotRequired[IndexTypeType],
    },
)

class ListManagedViewsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ServicePrincipal: NotRequired[str]

class ListSupportedResourceTypesInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class SupportedResourceTypeTypeDef(TypedDict):
    ResourceType: NotRequired[str]
    Service: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str

class ListViewsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ResourceCountTypeDef(TypedDict):
    Complete: NotRequired[bool]
    TotalResources: NotRequired[int]

class ResourcePropertyTypeDef(TypedDict):
    Data: NotRequired[dict[str, Any]]
    LastReportedAt: NotRequired[datetime]
    Name: NotRequired[str]

class SearchInputRequestTypeDef(TypedDict):
    QueryString: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ViewArn: NotRequired[str]

class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    Tags: NotRequired[Mapping[str, str]]

class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

UpdateIndexTypeInputRequestTypeDef = TypedDict(
    "UpdateIndexTypeInputRequestTypeDef",
    {
        "Arn": str,
        "Type": IndexTypeType,
    },
)

class AssociateDefaultViewOutputTypeDef(TypedDict):
    ViewArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateIndexOutputTypeDef(TypedDict):
    Arn: str
    CreatedAt: datetime
    State: IndexStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteIndexOutputTypeDef(TypedDict):
    Arn: str
    LastUpdatedAt: datetime
    State: IndexStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteViewOutputTypeDef(TypedDict):
    ViewArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetDefaultViewOutputTypeDef(TypedDict):
    ViewArn: str
    ResponseMetadata: ResponseMetadataTypeDef

GetIndexOutputTypeDef = TypedDict(
    "GetIndexOutputTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "ReplicatingFrom": list[str],
        "ReplicatingTo": list[str],
        "State": IndexStateType,
        "Tags": dict[str, str],
        "Type": IndexTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListManagedViewsOutputTypeDef(TypedDict):
    ManagedViews: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListViewsOutputTypeDef(TypedDict):
    Views: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

UpdateIndexTypeOutputTypeDef = TypedDict(
    "UpdateIndexTypeOutputTypeDef",
    {
        "Arn": str,
        "LastUpdatedAt": datetime,
        "State": IndexStateType,
        "Type": IndexTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateViewInputRequestTypeDef(TypedDict):
    ViewName: str
    ClientToken: NotRequired[str]
    Filters: NotRequired[SearchFilterTypeDef]
    IncludedProperties: NotRequired[Sequence[IncludedPropertyTypeDef]]
    Scope: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class ListResourcesInputRequestTypeDef(TypedDict):
    Filters: NotRequired[SearchFilterTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ViewArn: NotRequired[str]

class ManagedViewTypeDef(TypedDict):
    Filters: NotRequired[SearchFilterTypeDef]
    IncludedProperties: NotRequired[list[IncludedPropertyTypeDef]]
    LastUpdatedAt: NotRequired[datetime]
    ManagedViewArn: NotRequired[str]
    ManagedViewName: NotRequired[str]
    Owner: NotRequired[str]
    ResourcePolicy: NotRequired[str]
    Scope: NotRequired[str]
    TrustedService: NotRequired[str]
    Version: NotRequired[str]

class UpdateViewInputRequestTypeDef(TypedDict):
    ViewArn: str
    Filters: NotRequired[SearchFilterTypeDef]
    IncludedProperties: NotRequired[Sequence[IncludedPropertyTypeDef]]

class ViewTypeDef(TypedDict):
    Filters: NotRequired[SearchFilterTypeDef]
    IncludedProperties: NotRequired[list[IncludedPropertyTypeDef]]
    LastUpdatedAt: NotRequired[datetime]
    Owner: NotRequired[str]
    Scope: NotRequired[str]
    ViewArn: NotRequired[str]

class GetAccountLevelServiceConfigurationOutputTypeDef(TypedDict):
    OrgConfiguration: OrgConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListIndexesOutputTypeDef(TypedDict):
    Indexes: list[IndexTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListIndexesForMembersInputPaginateTypeDef(TypedDict):
    AccountIdList: Sequence[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListIndexesInputPaginateTypeDef = TypedDict(
    "ListIndexesInputPaginateTypeDef",
    {
        "Regions": NotRequired[Sequence[str]],
        "Type": NotRequired[IndexTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListManagedViewsInputPaginateTypeDef(TypedDict):
    ServicePrincipal: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourcesInputPaginateTypeDef(TypedDict):
    Filters: NotRequired[SearchFilterTypeDef]
    ViewArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSupportedResourceTypesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListViewsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchInputPaginateTypeDef(TypedDict):
    QueryString: str
    ViewArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIndexesForMembersOutputTypeDef(TypedDict):
    Indexes: list[MemberIndexTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSupportedResourceTypesOutputTypeDef(TypedDict):
    ResourceTypes: list[SupportedResourceTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ResourceTypeDef(TypedDict):
    Arn: NotRequired[str]
    LastReportedAt: NotRequired[datetime]
    OwningAccountId: NotRequired[str]
    Properties: NotRequired[list[ResourcePropertyTypeDef]]
    Region: NotRequired[str]
    ResourceType: NotRequired[str]
    Service: NotRequired[str]

class GetManagedViewOutputTypeDef(TypedDict):
    ManagedView: ManagedViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetViewOutputTypeDef(TypedDict):
    Errors: list[BatchGetViewErrorTypeDef]
    Views: list[ViewTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateViewOutputTypeDef(TypedDict):
    View: ViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetViewOutputTypeDef(TypedDict):
    Tags: dict[str, str]
    View: ViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateViewOutputTypeDef(TypedDict):
    View: ViewTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListResourcesOutputTypeDef(TypedDict):
    Resources: list[ResourceTypeDef]
    ViewArn: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SearchOutputTypeDef(TypedDict):
    Count: ResourceCountTypeDef
    Resources: list[ResourceTypeDef]
    ViewArn: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
