"""
Type annotations for oam service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_oam/type_defs/)

Usage::

    ```python
    from mypy_boto3_oam.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Mapping, Sequence

from .literals import ResourceTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CreateLinkInputRequestTypeDef",
    "CreateLinkOutputTypeDef",
    "CreateSinkInputRequestTypeDef",
    "CreateSinkOutputTypeDef",
    "DeleteLinkInputRequestTypeDef",
    "DeleteSinkInputRequestTypeDef",
    "GetLinkInputRequestTypeDef",
    "GetLinkOutputTypeDef",
    "GetSinkInputRequestTypeDef",
    "GetSinkOutputTypeDef",
    "GetSinkPolicyInputRequestTypeDef",
    "GetSinkPolicyOutputTypeDef",
    "LinkConfigurationTypeDef",
    "ListAttachedLinksInputPaginateTypeDef",
    "ListAttachedLinksInputRequestTypeDef",
    "ListAttachedLinksItemTypeDef",
    "ListAttachedLinksOutputTypeDef",
    "ListLinksInputPaginateTypeDef",
    "ListLinksInputRequestTypeDef",
    "ListLinksItemTypeDef",
    "ListLinksOutputTypeDef",
    "ListSinksInputPaginateTypeDef",
    "ListSinksInputRequestTypeDef",
    "ListSinksItemTypeDef",
    "ListSinksOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "LogGroupConfigurationTypeDef",
    "MetricConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PutSinkPolicyInputRequestTypeDef",
    "PutSinkPolicyOutputTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateLinkInputRequestTypeDef",
    "UpdateLinkOutputTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateSinkInputRequestTypeDef(TypedDict):
    Name: str
    Tags: NotRequired[Mapping[str, str]]

class DeleteLinkInputRequestTypeDef(TypedDict):
    Identifier: str

class DeleteSinkInputRequestTypeDef(TypedDict):
    Identifier: str

class GetLinkInputRequestTypeDef(TypedDict):
    Identifier: str

class GetSinkInputRequestTypeDef(TypedDict):
    Identifier: str

class GetSinkPolicyInputRequestTypeDef(TypedDict):
    SinkIdentifier: str

class LogGroupConfigurationTypeDef(TypedDict):
    Filter: str

class MetricConfigurationTypeDef(TypedDict):
    Filter: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAttachedLinksInputRequestTypeDef(TypedDict):
    SinkIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListAttachedLinksItemTypeDef(TypedDict):
    Label: NotRequired[str]
    LinkArn: NotRequired[str]
    ResourceTypes: NotRequired[list[str]]

class ListLinksInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListLinksItemTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Label: NotRequired[str]
    ResourceTypes: NotRequired[list[str]]
    SinkArn: NotRequired[str]

class ListSinksInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListSinksItemTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]

class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str

class PutSinkPolicyInputRequestTypeDef(TypedDict):
    Policy: str
    SinkIdentifier: str

class TagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class CreateSinkOutputTypeDef(TypedDict):
    Arn: str
    Id: str
    Name: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSinkOutputTypeDef(TypedDict):
    Arn: str
    Id: str
    Name: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSinkPolicyOutputTypeDef(TypedDict):
    Policy: str
    SinkArn: str
    SinkId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutSinkPolicyOutputTypeDef(TypedDict):
    Policy: str
    SinkArn: str
    SinkId: str
    ResponseMetadata: ResponseMetadataTypeDef

class LinkConfigurationTypeDef(TypedDict):
    LogGroupConfiguration: NotRequired[LogGroupConfigurationTypeDef]
    MetricConfiguration: NotRequired[MetricConfigurationTypeDef]

class ListAttachedLinksInputPaginateTypeDef(TypedDict):
    SinkIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLinksInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSinksInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAttachedLinksOutputTypeDef(TypedDict):
    Items: list[ListAttachedLinksItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListLinksOutputTypeDef(TypedDict):
    Items: list[ListLinksItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSinksOutputTypeDef(TypedDict):
    Items: list[ListSinksItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateLinkInputRequestTypeDef(TypedDict):
    LabelTemplate: str
    ResourceTypes: Sequence[ResourceTypeType]
    SinkIdentifier: str
    LinkConfiguration: NotRequired[LinkConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]

class CreateLinkOutputTypeDef(TypedDict):
    Arn: str
    Id: str
    Label: str
    LabelTemplate: str
    LinkConfiguration: LinkConfigurationTypeDef
    ResourceTypes: list[str]
    SinkArn: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetLinkOutputTypeDef(TypedDict):
    Arn: str
    Id: str
    Label: str
    LabelTemplate: str
    LinkConfiguration: LinkConfigurationTypeDef
    ResourceTypes: list[str]
    SinkArn: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLinkInputRequestTypeDef(TypedDict):
    Identifier: str
    ResourceTypes: Sequence[ResourceTypeType]
    LinkConfiguration: NotRequired[LinkConfigurationTypeDef]

class UpdateLinkOutputTypeDef(TypedDict):
    Arn: str
    Id: str
    Label: str
    LabelTemplate: str
    LinkConfiguration: LinkConfigurationTypeDef
    ResourceTypes: list[str]
    SinkArn: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
