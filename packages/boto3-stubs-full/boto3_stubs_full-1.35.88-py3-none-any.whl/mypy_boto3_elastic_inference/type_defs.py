"""
Type annotations for elastic-inference service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/type_defs/)

Usage::

    ```python
    from mypy_boto3_elastic_inference.type_defs import AcceleratorTypeOfferingTypeDef

    data: AcceleratorTypeOfferingTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Mapping, Sequence

from .literals import LocationTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AcceleratorTypeOfferingTypeDef",
    "AcceleratorTypeTypeDef",
    "DescribeAcceleratorOfferingsRequestRequestTypeDef",
    "DescribeAcceleratorOfferingsResponseTypeDef",
    "DescribeAcceleratorTypesResponseTypeDef",
    "DescribeAcceleratorsRequestPaginateTypeDef",
    "DescribeAcceleratorsRequestRequestTypeDef",
    "DescribeAcceleratorsResponseTypeDef",
    "ElasticInferenceAcceleratorHealthTypeDef",
    "ElasticInferenceAcceleratorTypeDef",
    "FilterTypeDef",
    "KeyValuePairTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "MemoryInfoTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
)


class AcceleratorTypeOfferingTypeDef(TypedDict):
    acceleratorType: NotRequired[str]
    locationType: NotRequired[LocationTypeType]
    location: NotRequired[str]


class KeyValuePairTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[int]


class MemoryInfoTypeDef(TypedDict):
    sizeInMiB: NotRequired[int]


class DescribeAcceleratorOfferingsRequestRequestTypeDef(TypedDict):
    locationType: LocationTypeType
    acceleratorTypes: NotRequired[Sequence[str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class FilterTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[Sequence[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ElasticInferenceAcceleratorHealthTypeDef(TypedDict):
    status: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class AcceleratorTypeTypeDef(TypedDict):
    acceleratorTypeName: NotRequired[str]
    memoryInfo: NotRequired[MemoryInfoTypeDef]
    throughputInfo: NotRequired[list[KeyValuePairTypeDef]]


class DescribeAcceleratorOfferingsResponseTypeDef(TypedDict):
    acceleratorTypeOfferings: list[AcceleratorTypeOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResultTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAcceleratorsRequestRequestTypeDef(TypedDict):
    acceleratorIds: NotRequired[Sequence[str]]
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeAcceleratorsRequestPaginateTypeDef(TypedDict):
    acceleratorIds: NotRequired[Sequence[str]]
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ElasticInferenceAcceleratorTypeDef(TypedDict):
    acceleratorHealth: NotRequired[ElasticInferenceAcceleratorHealthTypeDef]
    acceleratorType: NotRequired[str]
    acceleratorId: NotRequired[str]
    availabilityZone: NotRequired[str]
    attachedResource: NotRequired[str]


class DescribeAcceleratorTypesResponseTypeDef(TypedDict):
    acceleratorTypes: list[AcceleratorTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAcceleratorsResponseTypeDef(TypedDict):
    acceleratorSet: list[ElasticInferenceAcceleratorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
