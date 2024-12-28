"""
Type annotations for route53-recovery-cluster service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_cluster/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53_recovery_cluster.type_defs import GetRoutingControlStateRequestRequestTypeDef

    data: GetRoutingControlStateRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Sequence

from .literals import RoutingControlStateType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetRoutingControlStateRequestRequestTypeDef",
    "GetRoutingControlStateResponseTypeDef",
    "ListRoutingControlsRequestPaginateTypeDef",
    "ListRoutingControlsRequestRequestTypeDef",
    "ListRoutingControlsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RoutingControlTypeDef",
    "UpdateRoutingControlStateEntryTypeDef",
    "UpdateRoutingControlStateRequestRequestTypeDef",
    "UpdateRoutingControlStatesRequestRequestTypeDef",
)

class GetRoutingControlStateRequestRequestTypeDef(TypedDict):
    RoutingControlArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListRoutingControlsRequestRequestTypeDef(TypedDict):
    ControlPanelArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class RoutingControlTypeDef(TypedDict):
    ControlPanelArn: NotRequired[str]
    ControlPanelName: NotRequired[str]
    RoutingControlArn: NotRequired[str]
    RoutingControlName: NotRequired[str]
    RoutingControlState: NotRequired[RoutingControlStateType]
    Owner: NotRequired[str]

class UpdateRoutingControlStateEntryTypeDef(TypedDict):
    RoutingControlArn: str
    RoutingControlState: RoutingControlStateType

class UpdateRoutingControlStateRequestRequestTypeDef(TypedDict):
    RoutingControlArn: str
    RoutingControlState: RoutingControlStateType
    SafetyRulesToOverride: NotRequired[Sequence[str]]

class GetRoutingControlStateResponseTypeDef(TypedDict):
    RoutingControlArn: str
    RoutingControlState: RoutingControlStateType
    RoutingControlName: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListRoutingControlsRequestPaginateTypeDef(TypedDict):
    ControlPanelArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRoutingControlsResponseTypeDef(TypedDict):
    RoutingControls: list[RoutingControlTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateRoutingControlStatesRequestRequestTypeDef(TypedDict):
    UpdateRoutingControlStateEntries: Sequence[UpdateRoutingControlStateEntryTypeDef]
    SafetyRulesToOverride: NotRequired[Sequence[str]]
