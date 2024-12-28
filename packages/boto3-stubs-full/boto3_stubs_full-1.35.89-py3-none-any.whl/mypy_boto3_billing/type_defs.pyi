"""
Type annotations for billing service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_billing/type_defs/)

Usage::

    ```python
    from mypy_boto3_billing.type_defs import TimestampTypeDef

    data: TimestampTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence, Union

from .literals import BillingViewTypeType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ActiveTimeRangeTypeDef",
    "BillingViewElementTypeDef",
    "BillingViewListElementTypeDef",
    "CreateBillingViewRequestRequestTypeDef",
    "CreateBillingViewResponseTypeDef",
    "DeleteBillingViewRequestRequestTypeDef",
    "DeleteBillingViewResponseTypeDef",
    "DimensionValuesOutputTypeDef",
    "DimensionValuesTypeDef",
    "DimensionValuesUnionTypeDef",
    "ExpressionOutputTypeDef",
    "ExpressionTypeDef",
    "GetBillingViewRequestRequestTypeDef",
    "GetBillingViewResponseTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "ListBillingViewsRequestPaginateTypeDef",
    "ListBillingViewsRequestRequestTypeDef",
    "ListBillingViewsResponseTypeDef",
    "ListSourceViewsForBillingViewRequestPaginateTypeDef",
    "ListSourceViewsForBillingViewRequestRequestTypeDef",
    "ListSourceViewsForBillingViewResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResourceTagTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagValuesOutputTypeDef",
    "TagValuesTypeDef",
    "TagValuesUnionTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBillingViewRequestRequestTypeDef",
    "UpdateBillingViewResponseTypeDef",
)

TimestampTypeDef = Union[datetime, str]

class BillingViewListElementTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    ownerAccountId: NotRequired[str]
    billingViewType: NotRequired[BillingViewTypeType]

class ResourceTagTypeDef(TypedDict):
    key: str
    value: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteBillingViewRequestRequestTypeDef(TypedDict):
    arn: str

class DimensionValuesOutputTypeDef(TypedDict):
    key: Literal["LINKED_ACCOUNT"]
    values: list[str]

class DimensionValuesTypeDef(TypedDict):
    key: Literal["LINKED_ACCOUNT"]
    values: Sequence[str]

class TagValuesOutputTypeDef(TypedDict):
    key: str
    values: list[str]

class GetBillingViewRequestRequestTypeDef(TypedDict):
    arn: str

class GetResourcePolicyRequestRequestTypeDef(TypedDict):
    resourceArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListSourceViewsForBillingViewRequestRequestTypeDef(TypedDict):
    arn: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class TagValuesTypeDef(TypedDict):
    key: str
    values: Sequence[str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    resourceTagKeys: Sequence[str]

class ActiveTimeRangeTypeDef(TypedDict):
    activeAfterInclusive: TimestampTypeDef
    activeBeforeInclusive: TimestampTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    resourceTags: Sequence[ResourceTagTypeDef]

class CreateBillingViewResponseTypeDef(TypedDict):
    arn: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBillingViewResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyResponseTypeDef(TypedDict):
    resourceArn: str
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListBillingViewsResponseTypeDef(TypedDict):
    billingViews: list[BillingViewListElementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSourceViewsForBillingViewResponseTypeDef(TypedDict):
    sourceViews: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    resourceTags: list[ResourceTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBillingViewResponseTypeDef(TypedDict):
    arn: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

DimensionValuesUnionTypeDef = Union[DimensionValuesTypeDef, DimensionValuesOutputTypeDef]

class ExpressionOutputTypeDef(TypedDict):
    dimensions: NotRequired[DimensionValuesOutputTypeDef]
    tags: NotRequired[TagValuesOutputTypeDef]

class ListSourceViewsForBillingViewRequestPaginateTypeDef(TypedDict):
    arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

TagValuesUnionTypeDef = Union[TagValuesTypeDef, TagValuesOutputTypeDef]

class ListBillingViewsRequestPaginateTypeDef(TypedDict):
    activeTimeRange: NotRequired[ActiveTimeRangeTypeDef]
    arns: NotRequired[Sequence[str]]
    billingViewTypes: NotRequired[Sequence[BillingViewTypeType]]
    ownerAccountId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBillingViewsRequestRequestTypeDef(TypedDict):
    activeTimeRange: NotRequired[ActiveTimeRangeTypeDef]
    arns: NotRequired[Sequence[str]]
    billingViewTypes: NotRequired[Sequence[BillingViewTypeType]]
    ownerAccountId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class BillingViewElementTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    billingViewType: NotRequired[BillingViewTypeType]
    ownerAccountId: NotRequired[str]
    dataFilterExpression: NotRequired[ExpressionOutputTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ExpressionTypeDef(TypedDict):
    dimensions: NotRequired[DimensionValuesUnionTypeDef]
    tags: NotRequired[TagValuesUnionTypeDef]

class GetBillingViewResponseTypeDef(TypedDict):
    billingView: BillingViewElementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBillingViewRequestRequestTypeDef(TypedDict):
    name: str
    sourceViews: Sequence[str]
    description: NotRequired[str]
    dataFilterExpression: NotRequired[ExpressionTypeDef]
    clientToken: NotRequired[str]
    resourceTags: NotRequired[Sequence[ResourceTagTypeDef]]

class UpdateBillingViewRequestRequestTypeDef(TypedDict):
    arn: str
    name: NotRequired[str]
    description: NotRequired[str]
    dataFilterExpression: NotRequired[ExpressionTypeDef]
