"""
Type annotations for route53-recovery-control-config service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_control_config/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53_recovery_control_config.type_defs import RuleConfigTypeDef

    data: RuleConfigTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Mapping, Sequence

from .literals import RuleTypeType, StatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AssertionRuleTypeDef",
    "AssertionRuleUpdateTypeDef",
    "ClusterEndpointTypeDef",
    "ClusterTypeDef",
    "ControlPanelTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateControlPanelRequestRequestTypeDef",
    "CreateControlPanelResponseTypeDef",
    "CreateRoutingControlRequestRequestTypeDef",
    "CreateRoutingControlResponseTypeDef",
    "CreateSafetyRuleRequestRequestTypeDef",
    "CreateSafetyRuleResponseTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteControlPanelRequestRequestTypeDef",
    "DeleteRoutingControlRequestRequestTypeDef",
    "DeleteSafetyRuleRequestRequestTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeClusterRequestWaitTypeDef",
    "DescribeClusterResponseTypeDef",
    "DescribeControlPanelRequestRequestTypeDef",
    "DescribeControlPanelRequestWaitTypeDef",
    "DescribeControlPanelResponseTypeDef",
    "DescribeRoutingControlRequestRequestTypeDef",
    "DescribeRoutingControlRequestWaitTypeDef",
    "DescribeRoutingControlResponseTypeDef",
    "DescribeSafetyRuleRequestRequestTypeDef",
    "DescribeSafetyRuleResponseTypeDef",
    "GatingRuleTypeDef",
    "GatingRuleUpdateTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "ListAssociatedRoute53HealthChecksRequestPaginateTypeDef",
    "ListAssociatedRoute53HealthChecksRequestRequestTypeDef",
    "ListAssociatedRoute53HealthChecksResponseTypeDef",
    "ListClustersRequestPaginateTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListControlPanelsRequestPaginateTypeDef",
    "ListControlPanelsRequestRequestTypeDef",
    "ListControlPanelsResponseTypeDef",
    "ListRoutingControlsRequestPaginateTypeDef",
    "ListRoutingControlsRequestRequestTypeDef",
    "ListRoutingControlsResponseTypeDef",
    "ListSafetyRulesRequestPaginateTypeDef",
    "ListSafetyRulesRequestRequestTypeDef",
    "ListSafetyRulesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NewAssertionRuleTypeDef",
    "NewGatingRuleTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RoutingControlTypeDef",
    "RuleConfigTypeDef",
    "RuleTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateControlPanelRequestRequestTypeDef",
    "UpdateControlPanelResponseTypeDef",
    "UpdateRoutingControlRequestRequestTypeDef",
    "UpdateRoutingControlResponseTypeDef",
    "UpdateSafetyRuleRequestRequestTypeDef",
    "UpdateSafetyRuleResponseTypeDef",
    "WaiterConfigTypeDef",
)

RuleConfigTypeDef = TypedDict(
    "RuleConfigTypeDef",
    {
        "Inverted": bool,
        "Threshold": int,
        "Type": RuleTypeType,
    },
)

class AssertionRuleUpdateTypeDef(TypedDict):
    Name: str
    SafetyRuleArn: str
    WaitPeriodMs: int

class ClusterEndpointTypeDef(TypedDict):
    Endpoint: NotRequired[str]
    Region: NotRequired[str]

class ControlPanelTypeDef(TypedDict):
    ClusterArn: NotRequired[str]
    ControlPanelArn: NotRequired[str]
    DefaultControlPanel: NotRequired[bool]
    Name: NotRequired[str]
    RoutingControlCount: NotRequired[int]
    Status: NotRequired[StatusType]
    Owner: NotRequired[str]

class CreateClusterRequestRequestTypeDef(TypedDict):
    ClusterName: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateControlPanelRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    ControlPanelName: str
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class CreateRoutingControlRequestRequestTypeDef(TypedDict):
    ClusterArn: str
    RoutingControlName: str
    ClientToken: NotRequired[str]
    ControlPanelArn: NotRequired[str]

class RoutingControlTypeDef(TypedDict):
    ControlPanelArn: NotRequired[str]
    Name: NotRequired[str]
    RoutingControlArn: NotRequired[str]
    Status: NotRequired[StatusType]
    Owner: NotRequired[str]

class DeleteClusterRequestRequestTypeDef(TypedDict):
    ClusterArn: str

class DeleteControlPanelRequestRequestTypeDef(TypedDict):
    ControlPanelArn: str

class DeleteRoutingControlRequestRequestTypeDef(TypedDict):
    RoutingControlArn: str

class DeleteSafetyRuleRequestRequestTypeDef(TypedDict):
    SafetyRuleArn: str

class DescribeClusterRequestRequestTypeDef(TypedDict):
    ClusterArn: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeControlPanelRequestRequestTypeDef(TypedDict):
    ControlPanelArn: str

class DescribeRoutingControlRequestRequestTypeDef(TypedDict):
    RoutingControlArn: str

class DescribeSafetyRuleRequestRequestTypeDef(TypedDict):
    SafetyRuleArn: str

class GatingRuleUpdateTypeDef(TypedDict):
    Name: str
    SafetyRuleArn: str
    WaitPeriodMs: int

class GetResourcePolicyRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAssociatedRoute53HealthChecksRequestRequestTypeDef(TypedDict):
    RoutingControlArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListClustersRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListControlPanelsRequestRequestTypeDef(TypedDict):
    ClusterArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRoutingControlsRequestRequestTypeDef(TypedDict):
    ControlPanelArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListSafetyRulesRequestRequestTypeDef(TypedDict):
    ControlPanelArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateControlPanelRequestRequestTypeDef(TypedDict):
    ControlPanelArn: str
    ControlPanelName: str

class UpdateRoutingControlRequestRequestTypeDef(TypedDict):
    RoutingControlArn: str
    RoutingControlName: str

class AssertionRuleTypeDef(TypedDict):
    AssertedControls: list[str]
    ControlPanelArn: str
    Name: str
    RuleConfig: RuleConfigTypeDef
    SafetyRuleArn: str
    Status: StatusType
    WaitPeriodMs: int
    Owner: NotRequired[str]

class GatingRuleTypeDef(TypedDict):
    ControlPanelArn: str
    GatingControls: list[str]
    Name: str
    RuleConfig: RuleConfigTypeDef
    SafetyRuleArn: str
    Status: StatusType
    TargetControls: list[str]
    WaitPeriodMs: int
    Owner: NotRequired[str]

class NewAssertionRuleTypeDef(TypedDict):
    AssertedControls: Sequence[str]
    ControlPanelArn: str
    Name: str
    RuleConfig: RuleConfigTypeDef
    WaitPeriodMs: int

class NewGatingRuleTypeDef(TypedDict):
    ControlPanelArn: str
    GatingControls: Sequence[str]
    Name: str
    RuleConfig: RuleConfigTypeDef
    TargetControls: Sequence[str]
    WaitPeriodMs: int

class ClusterTypeDef(TypedDict):
    ClusterArn: NotRequired[str]
    ClusterEndpoints: NotRequired[list[ClusterEndpointTypeDef]]
    Name: NotRequired[str]
    Status: NotRequired[StatusType]
    Owner: NotRequired[str]

class CreateControlPanelResponseTypeDef(TypedDict):
    ControlPanel: ControlPanelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeControlPanelResponseTypeDef(TypedDict):
    ControlPanel: ControlPanelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyResponseTypeDef(TypedDict):
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssociatedRoute53HealthChecksResponseTypeDef(TypedDict):
    HealthCheckIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListControlPanelsResponseTypeDef(TypedDict):
    ControlPanels: list[ControlPanelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateControlPanelResponseTypeDef(TypedDict):
    ControlPanel: ControlPanelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRoutingControlResponseTypeDef(TypedDict):
    RoutingControl: RoutingControlTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeRoutingControlResponseTypeDef(TypedDict):
    RoutingControl: RoutingControlTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListRoutingControlsResponseTypeDef(TypedDict):
    RoutingControls: list[RoutingControlTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateRoutingControlResponseTypeDef(TypedDict):
    RoutingControl: RoutingControlTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeClusterRequestWaitTypeDef(TypedDict):
    ClusterArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeControlPanelRequestWaitTypeDef(TypedDict):
    ControlPanelArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeRoutingControlRequestWaitTypeDef(TypedDict):
    RoutingControlArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class UpdateSafetyRuleRequestRequestTypeDef(TypedDict):
    AssertionRuleUpdate: NotRequired[AssertionRuleUpdateTypeDef]
    GatingRuleUpdate: NotRequired[GatingRuleUpdateTypeDef]

class ListAssociatedRoute53HealthChecksRequestPaginateTypeDef(TypedDict):
    RoutingControlArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClustersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListControlPanelsRequestPaginateTypeDef(TypedDict):
    ClusterArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRoutingControlsRequestPaginateTypeDef(TypedDict):
    ControlPanelArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSafetyRulesRequestPaginateTypeDef(TypedDict):
    ControlPanelArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class CreateSafetyRuleResponseTypeDef(TypedDict):
    AssertionRule: AssertionRuleTypeDef
    GatingRule: GatingRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSafetyRuleResponseTypeDef(TypedDict):
    AssertionRule: AssertionRuleTypeDef
    GatingRule: GatingRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RuleTypeDef(TypedDict):
    ASSERTION: NotRequired[AssertionRuleTypeDef]
    GATING: NotRequired[GatingRuleTypeDef]

class UpdateSafetyRuleResponseTypeDef(TypedDict):
    AssertionRule: AssertionRuleTypeDef
    GatingRule: GatingRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSafetyRuleRequestRequestTypeDef(TypedDict):
    AssertionRule: NotRequired[NewAssertionRuleTypeDef]
    ClientToken: NotRequired[str]
    GatingRule: NotRequired[NewGatingRuleTypeDef]
    Tags: NotRequired[Mapping[str, str]]

class CreateClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeClusterResponseTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListClustersResponseTypeDef(TypedDict):
    Clusters: list[ClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListSafetyRulesResponseTypeDef(TypedDict):
    SafetyRules: list[RuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
