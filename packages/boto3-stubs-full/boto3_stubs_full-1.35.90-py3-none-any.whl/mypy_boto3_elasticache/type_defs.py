"""
Type annotations for elasticache service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticache/type_defs/)

Usage::

    ```python
    from mypy_boto3_elasticache.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence, Union

from .literals import (
    AuthenticationTypeType,
    AuthTokenUpdateStatusType,
    AuthTokenUpdateStrategyTypeType,
    AutomaticFailoverStatusType,
    AZModeType,
    ChangeTypeType,
    ClusterModeType,
    DataTieringStatusType,
    DestinationTypeType,
    InputAuthenticationTypeType,
    IpDiscoveryType,
    LogDeliveryConfigurationStatusType,
    LogFormatType,
    LogTypeType,
    MultiAZStatusType,
    NetworkTypeType,
    NodeUpdateInitiatedByType,
    NodeUpdateStatusType,
    OutpostModeType,
    PendingAutomaticFailoverStatusType,
    ServiceUpdateSeverityType,
    ServiceUpdateStatusType,
    SlaMetType,
    SourceTypeType,
    TransitEncryptionModeType,
    UpdateActionStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AddTagsToResourceMessageRequestTypeDef",
    "AllowedNodeTypeModificationsMessageTypeDef",
    "AuthenticationModeTypeDef",
    "AuthenticationTypeDef",
    "AuthorizeCacheSecurityGroupIngressMessageRequestTypeDef",
    "AuthorizeCacheSecurityGroupIngressResultTypeDef",
    "AvailabilityZoneTypeDef",
    "BatchApplyUpdateActionMessageRequestTypeDef",
    "BatchStopUpdateActionMessageRequestTypeDef",
    "CacheClusterMessageTypeDef",
    "CacheClusterTypeDef",
    "CacheEngineVersionMessageTypeDef",
    "CacheEngineVersionTypeDef",
    "CacheNodeTypeDef",
    "CacheNodeTypeSpecificParameterTypeDef",
    "CacheNodeTypeSpecificValueTypeDef",
    "CacheNodeUpdateStatusTypeDef",
    "CacheParameterGroupDetailsTypeDef",
    "CacheParameterGroupNameMessageTypeDef",
    "CacheParameterGroupStatusTypeDef",
    "CacheParameterGroupTypeDef",
    "CacheParameterGroupsMessageTypeDef",
    "CacheSecurityGroupMembershipTypeDef",
    "CacheSecurityGroupMessageTypeDef",
    "CacheSecurityGroupTypeDef",
    "CacheSubnetGroupMessageTypeDef",
    "CacheSubnetGroupTypeDef",
    "CacheUsageLimitsTypeDef",
    "CloudWatchLogsDestinationDetailsTypeDef",
    "CompleteMigrationMessageRequestTypeDef",
    "CompleteMigrationResponseTypeDef",
    "ConfigureShardTypeDef",
    "CopyServerlessCacheSnapshotRequestRequestTypeDef",
    "CopyServerlessCacheSnapshotResponseTypeDef",
    "CopySnapshotMessageRequestTypeDef",
    "CopySnapshotResultTypeDef",
    "CreateCacheClusterMessageRequestTypeDef",
    "CreateCacheClusterResultTypeDef",
    "CreateCacheParameterGroupMessageRequestTypeDef",
    "CreateCacheParameterGroupResultTypeDef",
    "CreateCacheSecurityGroupMessageRequestTypeDef",
    "CreateCacheSecurityGroupResultTypeDef",
    "CreateCacheSubnetGroupMessageRequestTypeDef",
    "CreateCacheSubnetGroupResultTypeDef",
    "CreateGlobalReplicationGroupMessageRequestTypeDef",
    "CreateGlobalReplicationGroupResultTypeDef",
    "CreateReplicationGroupMessageRequestTypeDef",
    "CreateReplicationGroupResultTypeDef",
    "CreateServerlessCacheRequestRequestTypeDef",
    "CreateServerlessCacheResponseTypeDef",
    "CreateServerlessCacheSnapshotRequestRequestTypeDef",
    "CreateServerlessCacheSnapshotResponseTypeDef",
    "CreateSnapshotMessageRequestTypeDef",
    "CreateSnapshotResultTypeDef",
    "CreateUserGroupMessageRequestTypeDef",
    "CreateUserMessageRequestTypeDef",
    "CustomerNodeEndpointTypeDef",
    "DataStorageTypeDef",
    "DecreaseNodeGroupsInGlobalReplicationGroupMessageRequestTypeDef",
    "DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef",
    "DecreaseReplicaCountMessageRequestTypeDef",
    "DecreaseReplicaCountResultTypeDef",
    "DeleteCacheClusterMessageRequestTypeDef",
    "DeleteCacheClusterResultTypeDef",
    "DeleteCacheParameterGroupMessageRequestTypeDef",
    "DeleteCacheSecurityGroupMessageRequestTypeDef",
    "DeleteCacheSubnetGroupMessageRequestTypeDef",
    "DeleteGlobalReplicationGroupMessageRequestTypeDef",
    "DeleteGlobalReplicationGroupResultTypeDef",
    "DeleteReplicationGroupMessageRequestTypeDef",
    "DeleteReplicationGroupResultTypeDef",
    "DeleteServerlessCacheRequestRequestTypeDef",
    "DeleteServerlessCacheResponseTypeDef",
    "DeleteServerlessCacheSnapshotRequestRequestTypeDef",
    "DeleteServerlessCacheSnapshotResponseTypeDef",
    "DeleteSnapshotMessageRequestTypeDef",
    "DeleteSnapshotResultTypeDef",
    "DeleteUserGroupMessageRequestTypeDef",
    "DeleteUserMessageRequestTypeDef",
    "DescribeCacheClustersMessagePaginateTypeDef",
    "DescribeCacheClustersMessageRequestTypeDef",
    "DescribeCacheClustersMessageWaitTypeDef",
    "DescribeCacheEngineVersionsMessagePaginateTypeDef",
    "DescribeCacheEngineVersionsMessageRequestTypeDef",
    "DescribeCacheParameterGroupsMessagePaginateTypeDef",
    "DescribeCacheParameterGroupsMessageRequestTypeDef",
    "DescribeCacheParametersMessagePaginateTypeDef",
    "DescribeCacheParametersMessageRequestTypeDef",
    "DescribeCacheSecurityGroupsMessagePaginateTypeDef",
    "DescribeCacheSecurityGroupsMessageRequestTypeDef",
    "DescribeCacheSubnetGroupsMessagePaginateTypeDef",
    "DescribeCacheSubnetGroupsMessageRequestTypeDef",
    "DescribeEngineDefaultParametersMessagePaginateTypeDef",
    "DescribeEngineDefaultParametersMessageRequestTypeDef",
    "DescribeEngineDefaultParametersResultTypeDef",
    "DescribeEventsMessagePaginateTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeGlobalReplicationGroupsMessagePaginateTypeDef",
    "DescribeGlobalReplicationGroupsMessageRequestTypeDef",
    "DescribeGlobalReplicationGroupsResultTypeDef",
    "DescribeReplicationGroupsMessagePaginateTypeDef",
    "DescribeReplicationGroupsMessageRequestTypeDef",
    "DescribeReplicationGroupsMessageWaitTypeDef",
    "DescribeReservedCacheNodesMessagePaginateTypeDef",
    "DescribeReservedCacheNodesMessageRequestTypeDef",
    "DescribeReservedCacheNodesOfferingsMessagePaginateTypeDef",
    "DescribeReservedCacheNodesOfferingsMessageRequestTypeDef",
    "DescribeServerlessCacheSnapshotsRequestPaginateTypeDef",
    "DescribeServerlessCacheSnapshotsRequestRequestTypeDef",
    "DescribeServerlessCacheSnapshotsResponseTypeDef",
    "DescribeServerlessCachesRequestPaginateTypeDef",
    "DescribeServerlessCachesRequestRequestTypeDef",
    "DescribeServerlessCachesResponseTypeDef",
    "DescribeServiceUpdatesMessagePaginateTypeDef",
    "DescribeServiceUpdatesMessageRequestTypeDef",
    "DescribeSnapshotsListMessageTypeDef",
    "DescribeSnapshotsMessagePaginateTypeDef",
    "DescribeSnapshotsMessageRequestTypeDef",
    "DescribeUpdateActionsMessagePaginateTypeDef",
    "DescribeUpdateActionsMessageRequestTypeDef",
    "DescribeUserGroupsMessagePaginateTypeDef",
    "DescribeUserGroupsMessageRequestTypeDef",
    "DescribeUserGroupsResultTypeDef",
    "DescribeUsersMessagePaginateTypeDef",
    "DescribeUsersMessageRequestTypeDef",
    "DescribeUsersResultTypeDef",
    "DestinationDetailsTypeDef",
    "DisassociateGlobalReplicationGroupMessageRequestTypeDef",
    "DisassociateGlobalReplicationGroupResultTypeDef",
    "EC2SecurityGroupTypeDef",
    "ECPUPerSecondTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointTypeDef",
    "EngineDefaultsTypeDef",
    "EventTypeDef",
    "EventsMessageTypeDef",
    "ExportServerlessCacheSnapshotRequestRequestTypeDef",
    "ExportServerlessCacheSnapshotResponseTypeDef",
    "FailoverGlobalReplicationGroupMessageRequestTypeDef",
    "FailoverGlobalReplicationGroupResultTypeDef",
    "FilterTypeDef",
    "GlobalNodeGroupTypeDef",
    "GlobalReplicationGroupInfoTypeDef",
    "GlobalReplicationGroupMemberTypeDef",
    "GlobalReplicationGroupTypeDef",
    "IncreaseNodeGroupsInGlobalReplicationGroupMessageRequestTypeDef",
    "IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef",
    "IncreaseReplicaCountMessageRequestTypeDef",
    "IncreaseReplicaCountResultTypeDef",
    "KinesisFirehoseDestinationDetailsTypeDef",
    "ListAllowedNodeTypeModificationsMessageRequestTypeDef",
    "ListTagsForResourceMessageRequestTypeDef",
    "LogDeliveryConfigurationRequestTypeDef",
    "LogDeliveryConfigurationTypeDef",
    "ModifyCacheClusterMessageRequestTypeDef",
    "ModifyCacheClusterResultTypeDef",
    "ModifyCacheParameterGroupMessageRequestTypeDef",
    "ModifyCacheSubnetGroupMessageRequestTypeDef",
    "ModifyCacheSubnetGroupResultTypeDef",
    "ModifyGlobalReplicationGroupMessageRequestTypeDef",
    "ModifyGlobalReplicationGroupResultTypeDef",
    "ModifyReplicationGroupMessageRequestTypeDef",
    "ModifyReplicationGroupResultTypeDef",
    "ModifyReplicationGroupShardConfigurationMessageRequestTypeDef",
    "ModifyReplicationGroupShardConfigurationResultTypeDef",
    "ModifyServerlessCacheRequestRequestTypeDef",
    "ModifyServerlessCacheResponseTypeDef",
    "ModifyUserGroupMessageRequestTypeDef",
    "ModifyUserMessageRequestTypeDef",
    "NodeGroupConfigurationOutputTypeDef",
    "NodeGroupConfigurationTypeDef",
    "NodeGroupConfigurationUnionTypeDef",
    "NodeGroupMemberTypeDef",
    "NodeGroupMemberUpdateStatusTypeDef",
    "NodeGroupTypeDef",
    "NodeGroupUpdateStatusTypeDef",
    "NodeSnapshotTypeDef",
    "NotificationConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterNameValueTypeDef",
    "ParameterTypeDef",
    "PendingLogDeliveryConfigurationTypeDef",
    "PendingModifiedValuesTypeDef",
    "ProcessedUpdateActionTypeDef",
    "PurchaseReservedCacheNodesOfferingMessageRequestTypeDef",
    "PurchaseReservedCacheNodesOfferingResultTypeDef",
    "RebalanceSlotsInGlobalReplicationGroupMessageRequestTypeDef",
    "RebalanceSlotsInGlobalReplicationGroupResultTypeDef",
    "RebootCacheClusterMessageRequestTypeDef",
    "RebootCacheClusterResultTypeDef",
    "RecurringChargeTypeDef",
    "RegionalConfigurationTypeDef",
    "RemoveTagsFromResourceMessageRequestTypeDef",
    "ReplicationGroupMessageTypeDef",
    "ReplicationGroupPendingModifiedValuesTypeDef",
    "ReplicationGroupTypeDef",
    "ReservedCacheNodeMessageTypeDef",
    "ReservedCacheNodeTypeDef",
    "ReservedCacheNodesOfferingMessageTypeDef",
    "ReservedCacheNodesOfferingTypeDef",
    "ResetCacheParameterGroupMessageRequestTypeDef",
    "ReshardingConfigurationTypeDef",
    "ReshardingStatusTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeCacheSecurityGroupIngressMessageRequestTypeDef",
    "RevokeCacheSecurityGroupIngressResultTypeDef",
    "SecurityGroupMembershipTypeDef",
    "ServerlessCacheConfigurationTypeDef",
    "ServerlessCacheSnapshotTypeDef",
    "ServerlessCacheTypeDef",
    "ServiceUpdateTypeDef",
    "ServiceUpdatesMessageTypeDef",
    "SlotMigrationTypeDef",
    "SnapshotTypeDef",
    "StartMigrationMessageRequestTypeDef",
    "StartMigrationResponseTypeDef",
    "SubnetOutpostTypeDef",
    "SubnetTypeDef",
    "TagListMessageTypeDef",
    "TagTypeDef",
    "TestFailoverMessageRequestTypeDef",
    "TestFailoverResultTypeDef",
    "TestMigrationMessageRequestTypeDef",
    "TestMigrationResponseTypeDef",
    "TimeRangeFilterTypeDef",
    "TimestampTypeDef",
    "UnprocessedUpdateActionTypeDef",
    "UpdateActionResultsMessageTypeDef",
    "UpdateActionTypeDef",
    "UpdateActionsMessageTypeDef",
    "UserGroupPendingChangesTypeDef",
    "UserGroupResponseTypeDef",
    "UserGroupTypeDef",
    "UserGroupsUpdateStatusTypeDef",
    "UserResponseTypeDef",
    "UserTypeDef",
    "WaiterConfigTypeDef",
)


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


AuthenticationModeTypeDef = TypedDict(
    "AuthenticationModeTypeDef",
    {
        "Type": NotRequired[InputAuthenticationTypeType],
        "Passwords": NotRequired[Sequence[str]],
    },
)
AuthenticationTypeDef = TypedDict(
    "AuthenticationTypeDef",
    {
        "Type": NotRequired[AuthenticationTypeType],
        "PasswordCount": NotRequired[int],
    },
)


class AuthorizeCacheSecurityGroupIngressMessageRequestTypeDef(TypedDict):
    CacheSecurityGroupName: str
    EC2SecurityGroupName: str
    EC2SecurityGroupOwnerId: str


class AvailabilityZoneTypeDef(TypedDict):
    Name: NotRequired[str]


class BatchApplyUpdateActionMessageRequestTypeDef(TypedDict):
    ServiceUpdateName: str
    ReplicationGroupIds: NotRequired[Sequence[str]]
    CacheClusterIds: NotRequired[Sequence[str]]


class BatchStopUpdateActionMessageRequestTypeDef(TypedDict):
    ServiceUpdateName: str
    ReplicationGroupIds: NotRequired[Sequence[str]]
    CacheClusterIds: NotRequired[Sequence[str]]


class CacheParameterGroupStatusTypeDef(TypedDict):
    CacheParameterGroupName: NotRequired[str]
    ParameterApplyStatus: NotRequired[str]
    CacheNodeIdsToReboot: NotRequired[list[str]]


class CacheSecurityGroupMembershipTypeDef(TypedDict):
    CacheSecurityGroupName: NotRequired[str]
    Status: NotRequired[str]


class EndpointTypeDef(TypedDict):
    Address: NotRequired[str]
    Port: NotRequired[int]


class NotificationConfigurationTypeDef(TypedDict):
    TopicArn: NotRequired[str]
    TopicStatus: NotRequired[str]


class SecurityGroupMembershipTypeDef(TypedDict):
    SecurityGroupId: NotRequired[str]
    Status: NotRequired[str]


class CacheEngineVersionTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    CacheParameterGroupFamily: NotRequired[str]
    CacheEngineDescription: NotRequired[str]
    CacheEngineVersionDescription: NotRequired[str]


class CacheNodeTypeSpecificValueTypeDef(TypedDict):
    CacheNodeType: NotRequired[str]
    Value: NotRequired[str]


class CacheNodeUpdateStatusTypeDef(TypedDict):
    CacheNodeId: NotRequired[str]
    NodeUpdateStatus: NotRequired[NodeUpdateStatusType]
    NodeDeletionDate: NotRequired[datetime]
    NodeUpdateStartDate: NotRequired[datetime]
    NodeUpdateEndDate: NotRequired[datetime]
    NodeUpdateInitiatedBy: NotRequired[NodeUpdateInitiatedByType]
    NodeUpdateInitiatedDate: NotRequired[datetime]
    NodeUpdateStatusModifiedDate: NotRequired[datetime]


class ParameterTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    ParameterValue: NotRequired[str]
    Description: NotRequired[str]
    Source: NotRequired[str]
    DataType: NotRequired[str]
    AllowedValues: NotRequired[str]
    IsModifiable: NotRequired[bool]
    MinimumEngineVersion: NotRequired[str]
    ChangeType: NotRequired[ChangeTypeType]


class CacheParameterGroupTypeDef(TypedDict):
    CacheParameterGroupName: NotRequired[str]
    CacheParameterGroupFamily: NotRequired[str]
    Description: NotRequired[str]
    IsGlobal: NotRequired[bool]
    ARN: NotRequired[str]


class EC2SecurityGroupTypeDef(TypedDict):
    Status: NotRequired[str]
    EC2SecurityGroupName: NotRequired[str]
    EC2SecurityGroupOwnerId: NotRequired[str]


class DataStorageTypeDef(TypedDict):
    Unit: Literal["GB"]
    Maximum: NotRequired[int]
    Minimum: NotRequired[int]


class ECPUPerSecondTypeDef(TypedDict):
    Maximum: NotRequired[int]
    Minimum: NotRequired[int]


class CloudWatchLogsDestinationDetailsTypeDef(TypedDict):
    LogGroup: NotRequired[str]


class CompleteMigrationMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    Force: NotRequired[bool]


class ConfigureShardTypeDef(TypedDict):
    NodeGroupId: str
    NewReplicaCount: int
    PreferredAvailabilityZones: NotRequired[Sequence[str]]
    PreferredOutpostArns: NotRequired[Sequence[str]]


class CreateGlobalReplicationGroupMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupIdSuffix: str
    PrimaryReplicationGroupId: str
    GlobalReplicationGroupDescription: NotRequired[str]


class CustomerNodeEndpointTypeDef(TypedDict):
    Address: NotRequired[str]
    Port: NotRequired[int]


class DecreaseNodeGroupsInGlobalReplicationGroupMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupId: str
    NodeGroupCount: int
    ApplyImmediately: bool
    GlobalNodeGroupsToRemove: NotRequired[Sequence[str]]
    GlobalNodeGroupsToRetain: NotRequired[Sequence[str]]


class DeleteCacheClusterMessageRequestTypeDef(TypedDict):
    CacheClusterId: str
    FinalSnapshotIdentifier: NotRequired[str]


class DeleteCacheParameterGroupMessageRequestTypeDef(TypedDict):
    CacheParameterGroupName: str


class DeleteCacheSecurityGroupMessageRequestTypeDef(TypedDict):
    CacheSecurityGroupName: str


class DeleteCacheSubnetGroupMessageRequestTypeDef(TypedDict):
    CacheSubnetGroupName: str


class DeleteGlobalReplicationGroupMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupId: str
    RetainPrimaryReplicationGroup: bool


class DeleteReplicationGroupMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    RetainPrimaryCluster: NotRequired[bool]
    FinalSnapshotIdentifier: NotRequired[str]


class DeleteServerlessCacheRequestRequestTypeDef(TypedDict):
    ServerlessCacheName: str
    FinalSnapshotName: NotRequired[str]


class DeleteServerlessCacheSnapshotRequestRequestTypeDef(TypedDict):
    ServerlessCacheSnapshotName: str


class DeleteSnapshotMessageRequestTypeDef(TypedDict):
    SnapshotName: str


class DeleteUserGroupMessageRequestTypeDef(TypedDict):
    UserGroupId: str


class DeleteUserMessageRequestTypeDef(TypedDict):
    UserId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeCacheClustersMessageRequestTypeDef(TypedDict):
    CacheClusterId: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    ShowCacheNodeInfo: NotRequired[bool]
    ShowCacheClustersNotInReplicationGroups: NotRequired[bool]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeCacheEngineVersionsMessageRequestTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    CacheParameterGroupFamily: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    DefaultOnly: NotRequired[bool]


class DescribeCacheParameterGroupsMessageRequestTypeDef(TypedDict):
    CacheParameterGroupName: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeCacheParametersMessageRequestTypeDef(TypedDict):
    CacheParameterGroupName: str
    Source: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeCacheSecurityGroupsMessageRequestTypeDef(TypedDict):
    CacheSecurityGroupName: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeCacheSubnetGroupsMessageRequestTypeDef(TypedDict):
    CacheSubnetGroupName: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEngineDefaultParametersMessageRequestTypeDef(TypedDict):
    CacheParameterGroupFamily: str
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class DescribeGlobalReplicationGroupsMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupId: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    ShowMemberInfo: NotRequired[bool]


class DescribeReplicationGroupsMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeReservedCacheNodesMessageRequestTypeDef(TypedDict):
    ReservedCacheNodeId: NotRequired[str]
    ReservedCacheNodesOfferingId: NotRequired[str]
    CacheNodeType: NotRequired[str]
    Duration: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeReservedCacheNodesOfferingsMessageRequestTypeDef(TypedDict):
    ReservedCacheNodesOfferingId: NotRequired[str]
    CacheNodeType: NotRequired[str]
    Duration: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeServerlessCacheSnapshotsRequestRequestTypeDef(TypedDict):
    ServerlessCacheName: NotRequired[str]
    ServerlessCacheSnapshotName: NotRequired[str]
    SnapshotType: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeServerlessCachesRequestRequestTypeDef(TypedDict):
    ServerlessCacheName: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeServiceUpdatesMessageRequestTypeDef(TypedDict):
    ServiceUpdateName: NotRequired[str]
    ServiceUpdateStatus: NotRequired[Sequence[ServiceUpdateStatusType]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeSnapshotsMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    CacheClusterId: NotRequired[str]
    SnapshotName: NotRequired[str]
    SnapshotSource: NotRequired[str]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]
    ShowNodeGroupConfig: NotRequired[bool]


class DescribeUserGroupsMessageRequestTypeDef(TypedDict):
    UserGroupId: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class FilterTypeDef(TypedDict):
    Name: str
    Values: Sequence[str]


class KinesisFirehoseDestinationDetailsTypeDef(TypedDict):
    DeliveryStream: NotRequired[str]


class DisassociateGlobalReplicationGroupMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupId: str
    ReplicationGroupId: str
    ReplicationGroupRegion: str


class EventTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    Message: NotRequired[str]
    Date: NotRequired[datetime]


class ExportServerlessCacheSnapshotRequestRequestTypeDef(TypedDict):
    ServerlessCacheSnapshotName: str
    S3BucketName: str


class FailoverGlobalReplicationGroupMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupId: str
    PrimaryRegion: str
    PrimaryReplicationGroupId: str


class GlobalNodeGroupTypeDef(TypedDict):
    GlobalNodeGroupId: NotRequired[str]
    Slots: NotRequired[str]


class GlobalReplicationGroupInfoTypeDef(TypedDict):
    GlobalReplicationGroupId: NotRequired[str]
    GlobalReplicationGroupMemberRole: NotRequired[str]


class GlobalReplicationGroupMemberTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    ReplicationGroupRegion: NotRequired[str]
    Role: NotRequired[str]
    AutomaticFailover: NotRequired[AutomaticFailoverStatusType]
    Status: NotRequired[str]


class ListAllowedNodeTypeModificationsMessageRequestTypeDef(TypedDict):
    CacheClusterId: NotRequired[str]
    ReplicationGroupId: NotRequired[str]


class ListTagsForResourceMessageRequestTypeDef(TypedDict):
    ResourceName: str


class ParameterNameValueTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    ParameterValue: NotRequired[str]


class ModifyCacheSubnetGroupMessageRequestTypeDef(TypedDict):
    CacheSubnetGroupName: str
    CacheSubnetGroupDescription: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]


class ModifyGlobalReplicationGroupMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupId: str
    ApplyImmediately: bool
    CacheNodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    CacheParameterGroupName: NotRequired[str]
    GlobalReplicationGroupDescription: NotRequired[str]
    AutomaticFailoverEnabled: NotRequired[bool]


class ReshardingConfigurationTypeDef(TypedDict):
    NodeGroupId: NotRequired[str]
    PreferredAvailabilityZones: NotRequired[Sequence[str]]


class ModifyUserGroupMessageRequestTypeDef(TypedDict):
    UserGroupId: str
    UserIdsToAdd: NotRequired[Sequence[str]]
    UserIdsToRemove: NotRequired[Sequence[str]]
    Engine: NotRequired[str]


class NodeGroupConfigurationOutputTypeDef(TypedDict):
    NodeGroupId: NotRequired[str]
    Slots: NotRequired[str]
    ReplicaCount: NotRequired[int]
    PrimaryAvailabilityZone: NotRequired[str]
    ReplicaAvailabilityZones: NotRequired[list[str]]
    PrimaryOutpostArn: NotRequired[str]
    ReplicaOutpostArns: NotRequired[list[str]]


class NodeGroupConfigurationTypeDef(TypedDict):
    NodeGroupId: NotRequired[str]
    Slots: NotRequired[str]
    ReplicaCount: NotRequired[int]
    PrimaryAvailabilityZone: NotRequired[str]
    ReplicaAvailabilityZones: NotRequired[Sequence[str]]
    PrimaryOutpostArn: NotRequired[str]
    ReplicaOutpostArns: NotRequired[Sequence[str]]


class NodeGroupMemberUpdateStatusTypeDef(TypedDict):
    CacheClusterId: NotRequired[str]
    CacheNodeId: NotRequired[str]
    NodeUpdateStatus: NotRequired[NodeUpdateStatusType]
    NodeDeletionDate: NotRequired[datetime]
    NodeUpdateStartDate: NotRequired[datetime]
    NodeUpdateEndDate: NotRequired[datetime]
    NodeUpdateInitiatedBy: NotRequired[NodeUpdateInitiatedByType]
    NodeUpdateInitiatedDate: NotRequired[datetime]
    NodeUpdateStatusModifiedDate: NotRequired[datetime]


class ProcessedUpdateActionTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    CacheClusterId: NotRequired[str]
    ServiceUpdateName: NotRequired[str]
    UpdateActionStatus: NotRequired[UpdateActionStatusType]


class RebalanceSlotsInGlobalReplicationGroupMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupId: str
    ApplyImmediately: bool


class RebootCacheClusterMessageRequestTypeDef(TypedDict):
    CacheClusterId: str
    CacheNodeIdsToReboot: Sequence[str]


class RecurringChargeTypeDef(TypedDict):
    RecurringChargeAmount: NotRequired[float]
    RecurringChargeFrequency: NotRequired[str]


class RemoveTagsFromResourceMessageRequestTypeDef(TypedDict):
    ResourceName: str
    TagKeys: Sequence[str]


class UserGroupsUpdateStatusTypeDef(TypedDict):
    UserGroupIdsToAdd: NotRequired[list[str]]
    UserGroupIdsToRemove: NotRequired[list[str]]


class SlotMigrationTypeDef(TypedDict):
    ProgressPercentage: NotRequired[float]


class RevokeCacheSecurityGroupIngressMessageRequestTypeDef(TypedDict):
    CacheSecurityGroupName: str
    EC2SecurityGroupName: str
    EC2SecurityGroupOwnerId: str


class ServerlessCacheConfigurationTypeDef(TypedDict):
    ServerlessCacheName: NotRequired[str]
    Engine: NotRequired[str]
    MajorEngineVersion: NotRequired[str]


class ServiceUpdateTypeDef(TypedDict):
    ServiceUpdateName: NotRequired[str]
    ServiceUpdateReleaseDate: NotRequired[datetime]
    ServiceUpdateEndDate: NotRequired[datetime]
    ServiceUpdateSeverity: NotRequired[ServiceUpdateSeverityType]
    ServiceUpdateRecommendedApplyByDate: NotRequired[datetime]
    ServiceUpdateStatus: NotRequired[ServiceUpdateStatusType]
    ServiceUpdateDescription: NotRequired[str]
    ServiceUpdateType: NotRequired[Literal["security-update"]]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    AutoUpdateAfterRecommendedApplyByDate: NotRequired[bool]
    EstimatedUpdateTime: NotRequired[str]


class SubnetOutpostTypeDef(TypedDict):
    SubnetOutpostArn: NotRequired[str]


class TestFailoverMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    NodeGroupId: str


class UnprocessedUpdateActionTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    CacheClusterId: NotRequired[str]
    ServiceUpdateName: NotRequired[str]
    ErrorType: NotRequired[str]
    ErrorMessage: NotRequired[str]


class UserGroupPendingChangesTypeDef(TypedDict):
    UserIdsToRemove: NotRequired[list[str]]
    UserIdsToAdd: NotRequired[list[str]]


class AddTagsToResourceMessageRequestTypeDef(TypedDict):
    ResourceName: str
    Tags: Sequence[TagTypeDef]


class CopyServerlessCacheSnapshotRequestRequestTypeDef(TypedDict):
    SourceServerlessCacheSnapshotName: str
    TargetServerlessCacheSnapshotName: str
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CopySnapshotMessageRequestTypeDef(TypedDict):
    SourceSnapshotName: str
    TargetSnapshotName: str
    TargetBucket: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateCacheParameterGroupMessageRequestTypeDef(TypedDict):
    CacheParameterGroupName: str
    CacheParameterGroupFamily: str
    Description: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateCacheSecurityGroupMessageRequestTypeDef(TypedDict):
    CacheSecurityGroupName: str
    Description: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateCacheSubnetGroupMessageRequestTypeDef(TypedDict):
    CacheSubnetGroupName: str
    CacheSubnetGroupDescription: str
    SubnetIds: Sequence[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateServerlessCacheSnapshotRequestRequestTypeDef(TypedDict):
    ServerlessCacheSnapshotName: str
    ServerlessCacheName: str
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateSnapshotMessageRequestTypeDef(TypedDict):
    SnapshotName: str
    ReplicationGroupId: NotRequired[str]
    CacheClusterId: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateUserGroupMessageRequestTypeDef(TypedDict):
    UserGroupId: str
    Engine: str
    UserIds: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class PurchaseReservedCacheNodesOfferingMessageRequestTypeDef(TypedDict):
    ReservedCacheNodesOfferingId: str
    ReservedCacheNodeId: NotRequired[str]
    CacheNodeCount: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]


class AllowedNodeTypeModificationsMessageTypeDef(TypedDict):
    ScaleUpModifications: list[str]
    ScaleDownModifications: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class CacheParameterGroupNameMessageTypeDef(TypedDict):
    CacheParameterGroupName: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class TagListMessageTypeDef(TypedDict):
    TagList: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserMessageRequestTypeDef(TypedDict):
    UserId: str
    UserName: str
    Engine: str
    AccessString: str
    Passwords: NotRequired[Sequence[str]]
    NoPasswordRequired: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    AuthenticationMode: NotRequired[AuthenticationModeTypeDef]


class ModifyUserMessageRequestTypeDef(TypedDict):
    UserId: str
    AccessString: NotRequired[str]
    AppendAccessString: NotRequired[str]
    Passwords: NotRequired[Sequence[str]]
    NoPasswordRequired: NotRequired[bool]
    AuthenticationMode: NotRequired[AuthenticationModeTypeDef]
    Engine: NotRequired[str]


class UserResponseTypeDef(TypedDict):
    UserId: str
    UserName: str
    Status: str
    Engine: str
    MinimumEngineVersion: str
    AccessString: str
    UserGroupIds: list[str]
    Authentication: AuthenticationTypeDef
    ARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UserTypeDef(TypedDict):
    UserId: NotRequired[str]
    UserName: NotRequired[str]
    Status: NotRequired[str]
    Engine: NotRequired[str]
    MinimumEngineVersion: NotRequired[str]
    AccessString: NotRequired[str]
    UserGroupIds: NotRequired[list[str]]
    Authentication: NotRequired[AuthenticationTypeDef]
    ARN: NotRequired[str]


class CacheNodeTypeDef(TypedDict):
    CacheNodeId: NotRequired[str]
    CacheNodeStatus: NotRequired[str]
    CacheNodeCreateTime: NotRequired[datetime]
    Endpoint: NotRequired[EndpointTypeDef]
    ParameterGroupStatus: NotRequired[str]
    SourceCacheNodeId: NotRequired[str]
    CustomerAvailabilityZone: NotRequired[str]
    CustomerOutpostArn: NotRequired[str]


class NodeGroupMemberTypeDef(TypedDict):
    CacheClusterId: NotRequired[str]
    CacheNodeId: NotRequired[str]
    ReadEndpoint: NotRequired[EndpointTypeDef]
    PreferredAvailabilityZone: NotRequired[str]
    PreferredOutpostArn: NotRequired[str]
    CurrentRole: NotRequired[str]


class CacheEngineVersionMessageTypeDef(TypedDict):
    Marker: str
    CacheEngineVersions: list[CacheEngineVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CacheNodeTypeSpecificParameterTypeDef(TypedDict):
    ParameterName: NotRequired[str]
    Description: NotRequired[str]
    Source: NotRequired[str]
    DataType: NotRequired[str]
    AllowedValues: NotRequired[str]
    IsModifiable: NotRequired[bool]
    MinimumEngineVersion: NotRequired[str]
    CacheNodeTypeSpecificValues: NotRequired[list[CacheNodeTypeSpecificValueTypeDef]]
    ChangeType: NotRequired[ChangeTypeType]


class CacheParameterGroupsMessageTypeDef(TypedDict):
    Marker: str
    CacheParameterGroups: list[CacheParameterGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCacheParameterGroupResultTypeDef(TypedDict):
    CacheParameterGroup: CacheParameterGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CacheSecurityGroupTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    CacheSecurityGroupName: NotRequired[str]
    Description: NotRequired[str]
    EC2SecurityGroups: NotRequired[list[EC2SecurityGroupTypeDef]]
    ARN: NotRequired[str]


class CacheUsageLimitsTypeDef(TypedDict):
    DataStorage: NotRequired[DataStorageTypeDef]
    ECPUPerSecond: NotRequired[ECPUPerSecondTypeDef]


class DecreaseReplicaCountMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    ApplyImmediately: bool
    NewReplicaCount: NotRequired[int]
    ReplicaConfiguration: NotRequired[Sequence[ConfigureShardTypeDef]]
    ReplicasToRemove: NotRequired[Sequence[str]]


class IncreaseReplicaCountMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    ApplyImmediately: bool
    NewReplicaCount: NotRequired[int]
    ReplicaConfiguration: NotRequired[Sequence[ConfigureShardTypeDef]]


class StartMigrationMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    CustomerNodeEndpointList: Sequence[CustomerNodeEndpointTypeDef]


class TestMigrationMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    CustomerNodeEndpointList: Sequence[CustomerNodeEndpointTypeDef]


class DescribeCacheClustersMessagePaginateTypeDef(TypedDict):
    CacheClusterId: NotRequired[str]
    ShowCacheNodeInfo: NotRequired[bool]
    ShowCacheClustersNotInReplicationGroups: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCacheEngineVersionsMessagePaginateTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    CacheParameterGroupFamily: NotRequired[str]
    DefaultOnly: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCacheParameterGroupsMessagePaginateTypeDef(TypedDict):
    CacheParameterGroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCacheParametersMessagePaginateTypeDef(TypedDict):
    CacheParameterGroupName: str
    Source: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCacheSecurityGroupsMessagePaginateTypeDef(TypedDict):
    CacheSecurityGroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCacheSubnetGroupsMessagePaginateTypeDef(TypedDict):
    CacheSubnetGroupName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEngineDefaultParametersMessagePaginateTypeDef(TypedDict):
    CacheParameterGroupFamily: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeGlobalReplicationGroupsMessagePaginateTypeDef(TypedDict):
    GlobalReplicationGroupId: NotRequired[str]
    ShowMemberInfo: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplicationGroupsMessagePaginateTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReservedCacheNodesMessagePaginateTypeDef(TypedDict):
    ReservedCacheNodeId: NotRequired[str]
    ReservedCacheNodesOfferingId: NotRequired[str]
    CacheNodeType: NotRequired[str]
    Duration: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReservedCacheNodesOfferingsMessagePaginateTypeDef(TypedDict):
    ReservedCacheNodesOfferingId: NotRequired[str]
    CacheNodeType: NotRequired[str]
    Duration: NotRequired[str]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeServerlessCacheSnapshotsRequestPaginateTypeDef(TypedDict):
    ServerlessCacheName: NotRequired[str]
    ServerlessCacheSnapshotName: NotRequired[str]
    SnapshotType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeServerlessCachesRequestPaginateTypeDef(TypedDict):
    ServerlessCacheName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeServiceUpdatesMessagePaginateTypeDef(TypedDict):
    ServiceUpdateName: NotRequired[str]
    ServiceUpdateStatus: NotRequired[Sequence[ServiceUpdateStatusType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSnapshotsMessagePaginateTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    CacheClusterId: NotRequired[str]
    SnapshotName: NotRequired[str]
    SnapshotSource: NotRequired[str]
    ShowNodeGroupConfig: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeUserGroupsMessagePaginateTypeDef(TypedDict):
    UserGroupId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCacheClustersMessageWaitTypeDef(TypedDict):
    CacheClusterId: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    ShowCacheNodeInfo: NotRequired[bool]
    ShowCacheClustersNotInReplicationGroups: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeReplicationGroupsMessageWaitTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEventsMessagePaginateTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEventsMessageRequestTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[SourceTypeType]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class TimeRangeFilterTypeDef(TypedDict):
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]


class DescribeUsersMessagePaginateTypeDef(TypedDict):
    Engine: NotRequired[str]
    UserId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeUsersMessageRequestTypeDef(TypedDict):
    Engine: NotRequired[str]
    UserId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DestinationDetailsTypeDef(TypedDict):
    CloudWatchLogsDetails: NotRequired[CloudWatchLogsDestinationDetailsTypeDef]
    KinesisFirehoseDetails: NotRequired[KinesisFirehoseDestinationDetailsTypeDef]


class EventsMessageTypeDef(TypedDict):
    Marker: str
    Events: list[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GlobalReplicationGroupTypeDef(TypedDict):
    GlobalReplicationGroupId: NotRequired[str]
    GlobalReplicationGroupDescription: NotRequired[str]
    Status: NotRequired[str]
    CacheNodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    Members: NotRequired[list[GlobalReplicationGroupMemberTypeDef]]
    ClusterEnabled: NotRequired[bool]
    GlobalNodeGroups: NotRequired[list[GlobalNodeGroupTypeDef]]
    AuthTokenEnabled: NotRequired[bool]
    TransitEncryptionEnabled: NotRequired[bool]
    AtRestEncryptionEnabled: NotRequired[bool]
    ARN: NotRequired[str]


class ModifyCacheParameterGroupMessageRequestTypeDef(TypedDict):
    CacheParameterGroupName: str
    ParameterNameValues: Sequence[ParameterNameValueTypeDef]


class ResetCacheParameterGroupMessageRequestTypeDef(TypedDict):
    CacheParameterGroupName: str
    ResetAllParameters: NotRequired[bool]
    ParameterNameValues: NotRequired[Sequence[ParameterNameValueTypeDef]]


class ModifyReplicationGroupShardConfigurationMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    NodeGroupCount: int
    ApplyImmediately: bool
    ReshardingConfiguration: NotRequired[Sequence[ReshardingConfigurationTypeDef]]
    NodeGroupsToRemove: NotRequired[Sequence[str]]
    NodeGroupsToRetain: NotRequired[Sequence[str]]


class RegionalConfigurationTypeDef(TypedDict):
    ReplicationGroupId: str
    ReplicationGroupRegion: str
    ReshardingConfiguration: Sequence[ReshardingConfigurationTypeDef]


class NodeSnapshotTypeDef(TypedDict):
    CacheClusterId: NotRequired[str]
    NodeGroupId: NotRequired[str]
    CacheNodeId: NotRequired[str]
    NodeGroupConfiguration: NotRequired[NodeGroupConfigurationOutputTypeDef]
    CacheSize: NotRequired[str]
    CacheNodeCreateTime: NotRequired[datetime]
    SnapshotCreateTime: NotRequired[datetime]


NodeGroupConfigurationUnionTypeDef = Union[
    NodeGroupConfigurationTypeDef, NodeGroupConfigurationOutputTypeDef
]


class NodeGroupUpdateStatusTypeDef(TypedDict):
    NodeGroupId: NotRequired[str]
    NodeGroupMemberUpdateStatus: NotRequired[list[NodeGroupMemberUpdateStatusTypeDef]]


class ReservedCacheNodeTypeDef(TypedDict):
    ReservedCacheNodeId: NotRequired[str]
    ReservedCacheNodesOfferingId: NotRequired[str]
    CacheNodeType: NotRequired[str]
    StartTime: NotRequired[datetime]
    Duration: NotRequired[int]
    FixedPrice: NotRequired[float]
    UsagePrice: NotRequired[float]
    CacheNodeCount: NotRequired[int]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    State: NotRequired[str]
    RecurringCharges: NotRequired[list[RecurringChargeTypeDef]]
    ReservationARN: NotRequired[str]


class ReservedCacheNodesOfferingTypeDef(TypedDict):
    ReservedCacheNodesOfferingId: NotRequired[str]
    CacheNodeType: NotRequired[str]
    Duration: NotRequired[int]
    FixedPrice: NotRequired[float]
    UsagePrice: NotRequired[float]
    ProductDescription: NotRequired[str]
    OfferingType: NotRequired[str]
    RecurringCharges: NotRequired[list[RecurringChargeTypeDef]]


class ReshardingStatusTypeDef(TypedDict):
    SlotMigration: NotRequired[SlotMigrationTypeDef]


class ServerlessCacheSnapshotTypeDef(TypedDict):
    ServerlessCacheSnapshotName: NotRequired[str]
    ARN: NotRequired[str]
    KmsKeyId: NotRequired[str]
    SnapshotType: NotRequired[str]
    Status: NotRequired[str]
    CreateTime: NotRequired[datetime]
    ExpiryTime: NotRequired[datetime]
    BytesUsedForCache: NotRequired[str]
    ServerlessCacheConfiguration: NotRequired[ServerlessCacheConfigurationTypeDef]


class ServiceUpdatesMessageTypeDef(TypedDict):
    Marker: str
    ServiceUpdates: list[ServiceUpdateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SubnetTypeDef(TypedDict):
    SubnetIdentifier: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[AvailabilityZoneTypeDef]
    SubnetOutpost: NotRequired[SubnetOutpostTypeDef]
    SupportedNetworkTypes: NotRequired[list[NetworkTypeType]]


class UpdateActionResultsMessageTypeDef(TypedDict):
    ProcessedUpdateActions: list[ProcessedUpdateActionTypeDef]
    UnprocessedUpdateActions: list[UnprocessedUpdateActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UserGroupResponseTypeDef(TypedDict):
    UserGroupId: str
    Status: str
    Engine: str
    UserIds: list[str]
    MinimumEngineVersion: str
    PendingChanges: UserGroupPendingChangesTypeDef
    ReplicationGroups: list[str]
    ServerlessCaches: list[str]
    ARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UserGroupTypeDef(TypedDict):
    UserGroupId: NotRequired[str]
    Status: NotRequired[str]
    Engine: NotRequired[str]
    UserIds: NotRequired[list[str]]
    MinimumEngineVersion: NotRequired[str]
    PendingChanges: NotRequired[UserGroupPendingChangesTypeDef]
    ReplicationGroups: NotRequired[list[str]]
    ServerlessCaches: NotRequired[list[str]]
    ARN: NotRequired[str]


class DescribeUsersResultTypeDef(TypedDict):
    Users: list[UserTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class NodeGroupTypeDef(TypedDict):
    NodeGroupId: NotRequired[str]
    Status: NotRequired[str]
    PrimaryEndpoint: NotRequired[EndpointTypeDef]
    ReaderEndpoint: NotRequired[EndpointTypeDef]
    Slots: NotRequired[str]
    NodeGroupMembers: NotRequired[list[NodeGroupMemberTypeDef]]


class CacheParameterGroupDetailsTypeDef(TypedDict):
    Marker: str
    Parameters: list[ParameterTypeDef]
    CacheNodeTypeSpecificParameters: list[CacheNodeTypeSpecificParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EngineDefaultsTypeDef(TypedDict):
    CacheParameterGroupFamily: NotRequired[str]
    Marker: NotRequired[str]
    Parameters: NotRequired[list[ParameterTypeDef]]
    CacheNodeTypeSpecificParameters: NotRequired[list[CacheNodeTypeSpecificParameterTypeDef]]


class AuthorizeCacheSecurityGroupIngressResultTypeDef(TypedDict):
    CacheSecurityGroup: CacheSecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CacheSecurityGroupMessageTypeDef(TypedDict):
    Marker: str
    CacheSecurityGroups: list[CacheSecurityGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCacheSecurityGroupResultTypeDef(TypedDict):
    CacheSecurityGroup: CacheSecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RevokeCacheSecurityGroupIngressResultTypeDef(TypedDict):
    CacheSecurityGroup: CacheSecurityGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateServerlessCacheRequestRequestTypeDef(TypedDict):
    ServerlessCacheName: str
    Engine: str
    Description: NotRequired[str]
    MajorEngineVersion: NotRequired[str]
    CacheUsageLimits: NotRequired[CacheUsageLimitsTypeDef]
    KmsKeyId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    SnapshotArnsToRestore: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    UserGroupId: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]
    SnapshotRetentionLimit: NotRequired[int]
    DailySnapshotTime: NotRequired[str]


class ModifyServerlessCacheRequestRequestTypeDef(TypedDict):
    ServerlessCacheName: str
    Description: NotRequired[str]
    CacheUsageLimits: NotRequired[CacheUsageLimitsTypeDef]
    RemoveUserGroup: NotRequired[bool]
    UserGroupId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    SnapshotRetentionLimit: NotRequired[int]
    DailySnapshotTime: NotRequired[str]
    Engine: NotRequired[str]
    MajorEngineVersion: NotRequired[str]


class ServerlessCacheTypeDef(TypedDict):
    ServerlessCacheName: NotRequired[str]
    Description: NotRequired[str]
    CreateTime: NotRequired[datetime]
    Status: NotRequired[str]
    Engine: NotRequired[str]
    MajorEngineVersion: NotRequired[str]
    FullEngineVersion: NotRequired[str]
    CacheUsageLimits: NotRequired[CacheUsageLimitsTypeDef]
    KmsKeyId: NotRequired[str]
    SecurityGroupIds: NotRequired[list[str]]
    Endpoint: NotRequired[EndpointTypeDef]
    ReaderEndpoint: NotRequired[EndpointTypeDef]
    ARN: NotRequired[str]
    UserGroupId: NotRequired[str]
    SubnetIds: NotRequired[list[str]]
    SnapshotRetentionLimit: NotRequired[int]
    DailySnapshotTime: NotRequired[str]


class DescribeUpdateActionsMessagePaginateTypeDef(TypedDict):
    ServiceUpdateName: NotRequired[str]
    ReplicationGroupIds: NotRequired[Sequence[str]]
    CacheClusterIds: NotRequired[Sequence[str]]
    Engine: NotRequired[str]
    ServiceUpdateStatus: NotRequired[Sequence[ServiceUpdateStatusType]]
    ServiceUpdateTimeRange: NotRequired[TimeRangeFilterTypeDef]
    UpdateActionStatus: NotRequired[Sequence[UpdateActionStatusType]]
    ShowNodeLevelUpdateStatus: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeUpdateActionsMessageRequestTypeDef(TypedDict):
    ServiceUpdateName: NotRequired[str]
    ReplicationGroupIds: NotRequired[Sequence[str]]
    CacheClusterIds: NotRequired[Sequence[str]]
    Engine: NotRequired[str]
    ServiceUpdateStatus: NotRequired[Sequence[ServiceUpdateStatusType]]
    ServiceUpdateTimeRange: NotRequired[TimeRangeFilterTypeDef]
    UpdateActionStatus: NotRequired[Sequence[UpdateActionStatusType]]
    ShowNodeLevelUpdateStatus: NotRequired[bool]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class LogDeliveryConfigurationRequestTypeDef(TypedDict):
    LogType: NotRequired[LogTypeType]
    DestinationType: NotRequired[DestinationTypeType]
    DestinationDetails: NotRequired[DestinationDetailsTypeDef]
    LogFormat: NotRequired[LogFormatType]
    Enabled: NotRequired[bool]


class LogDeliveryConfigurationTypeDef(TypedDict):
    LogType: NotRequired[LogTypeType]
    DestinationType: NotRequired[DestinationTypeType]
    DestinationDetails: NotRequired[DestinationDetailsTypeDef]
    LogFormat: NotRequired[LogFormatType]
    Status: NotRequired[LogDeliveryConfigurationStatusType]
    Message: NotRequired[str]


class PendingLogDeliveryConfigurationTypeDef(TypedDict):
    LogType: NotRequired[LogTypeType]
    DestinationType: NotRequired[DestinationTypeType]
    DestinationDetails: NotRequired[DestinationDetailsTypeDef]
    LogFormat: NotRequired[LogFormatType]


class CreateGlobalReplicationGroupResultTypeDef(TypedDict):
    GlobalReplicationGroup: GlobalReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef(TypedDict):
    GlobalReplicationGroup: GlobalReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGlobalReplicationGroupResultTypeDef(TypedDict):
    GlobalReplicationGroup: GlobalReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGlobalReplicationGroupsResultTypeDef(TypedDict):
    Marker: str
    GlobalReplicationGroups: list[GlobalReplicationGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateGlobalReplicationGroupResultTypeDef(TypedDict):
    GlobalReplicationGroup: GlobalReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FailoverGlobalReplicationGroupResultTypeDef(TypedDict):
    GlobalReplicationGroup: GlobalReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef(TypedDict):
    GlobalReplicationGroup: GlobalReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyGlobalReplicationGroupResultTypeDef(TypedDict):
    GlobalReplicationGroup: GlobalReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RebalanceSlotsInGlobalReplicationGroupResultTypeDef(TypedDict):
    GlobalReplicationGroup: GlobalReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IncreaseNodeGroupsInGlobalReplicationGroupMessageRequestTypeDef(TypedDict):
    GlobalReplicationGroupId: str
    NodeGroupCount: int
    ApplyImmediately: bool
    RegionalConfigurations: NotRequired[Sequence[RegionalConfigurationTypeDef]]


class SnapshotTypeDef(TypedDict):
    SnapshotName: NotRequired[str]
    ReplicationGroupId: NotRequired[str]
    ReplicationGroupDescription: NotRequired[str]
    CacheClusterId: NotRequired[str]
    SnapshotStatus: NotRequired[str]
    SnapshotSource: NotRequired[str]
    CacheNodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    NumCacheNodes: NotRequired[int]
    PreferredAvailabilityZone: NotRequired[str]
    PreferredOutpostArn: NotRequired[str]
    CacheClusterCreateTime: NotRequired[datetime]
    PreferredMaintenanceWindow: NotRequired[str]
    TopicArn: NotRequired[str]
    Port: NotRequired[int]
    CacheParameterGroupName: NotRequired[str]
    CacheSubnetGroupName: NotRequired[str]
    VpcId: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    SnapshotRetentionLimit: NotRequired[int]
    SnapshotWindow: NotRequired[str]
    NumNodeGroups: NotRequired[int]
    AutomaticFailover: NotRequired[AutomaticFailoverStatusType]
    NodeSnapshots: NotRequired[list[NodeSnapshotTypeDef]]
    KmsKeyId: NotRequired[str]
    ARN: NotRequired[str]
    DataTiering: NotRequired[DataTieringStatusType]


class UpdateActionTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    CacheClusterId: NotRequired[str]
    ServiceUpdateName: NotRequired[str]
    ServiceUpdateReleaseDate: NotRequired[datetime]
    ServiceUpdateSeverity: NotRequired[ServiceUpdateSeverityType]
    ServiceUpdateStatus: NotRequired[ServiceUpdateStatusType]
    ServiceUpdateRecommendedApplyByDate: NotRequired[datetime]
    ServiceUpdateType: NotRequired[Literal["security-update"]]
    UpdateActionAvailableDate: NotRequired[datetime]
    UpdateActionStatus: NotRequired[UpdateActionStatusType]
    NodesUpdated: NotRequired[str]
    UpdateActionStatusModifiedDate: NotRequired[datetime]
    SlaMet: NotRequired[SlaMetType]
    NodeGroupUpdateStatus: NotRequired[list[NodeGroupUpdateStatusTypeDef]]
    CacheNodeUpdateStatus: NotRequired[list[CacheNodeUpdateStatusTypeDef]]
    EstimatedUpdateTime: NotRequired[str]
    Engine: NotRequired[str]


class PurchaseReservedCacheNodesOfferingResultTypeDef(TypedDict):
    ReservedCacheNode: ReservedCacheNodeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ReservedCacheNodeMessageTypeDef(TypedDict):
    Marker: str
    ReservedCacheNodes: list[ReservedCacheNodeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ReservedCacheNodesOfferingMessageTypeDef(TypedDict):
    Marker: str
    ReservedCacheNodesOfferings: list[ReservedCacheNodesOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CopyServerlessCacheSnapshotResponseTypeDef(TypedDict):
    ServerlessCacheSnapshot: ServerlessCacheSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateServerlessCacheSnapshotResponseTypeDef(TypedDict):
    ServerlessCacheSnapshot: ServerlessCacheSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteServerlessCacheSnapshotResponseTypeDef(TypedDict):
    ServerlessCacheSnapshot: ServerlessCacheSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeServerlessCacheSnapshotsResponseTypeDef(TypedDict):
    ServerlessCacheSnapshots: list[ServerlessCacheSnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ExportServerlessCacheSnapshotResponseTypeDef(TypedDict):
    ServerlessCacheSnapshot: ServerlessCacheSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CacheSubnetGroupTypeDef(TypedDict):
    CacheSubnetGroupName: NotRequired[str]
    CacheSubnetGroupDescription: NotRequired[str]
    VpcId: NotRequired[str]
    Subnets: NotRequired[list[SubnetTypeDef]]
    ARN: NotRequired[str]
    SupportedNetworkTypes: NotRequired[list[NetworkTypeType]]


class DescribeUserGroupsResultTypeDef(TypedDict):
    UserGroups: list[UserGroupTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEngineDefaultParametersResultTypeDef(TypedDict):
    EngineDefaults: EngineDefaultsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateServerlessCacheResponseTypeDef(TypedDict):
    ServerlessCache: ServerlessCacheTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteServerlessCacheResponseTypeDef(TypedDict):
    ServerlessCache: ServerlessCacheTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeServerlessCachesResponseTypeDef(TypedDict):
    ServerlessCaches: list[ServerlessCacheTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyServerlessCacheResponseTypeDef(TypedDict):
    ServerlessCache: ServerlessCacheTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCacheClusterMessageRequestTypeDef(TypedDict):
    CacheClusterId: str
    ReplicationGroupId: NotRequired[str]
    AZMode: NotRequired[AZModeType]
    PreferredAvailabilityZone: NotRequired[str]
    PreferredAvailabilityZones: NotRequired[Sequence[str]]
    NumCacheNodes: NotRequired[int]
    CacheNodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    CacheParameterGroupName: NotRequired[str]
    CacheSubnetGroupName: NotRequired[str]
    CacheSecurityGroupNames: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SnapshotArns: NotRequired[Sequence[str]]
    SnapshotName: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    Port: NotRequired[int]
    NotificationTopicArn: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    SnapshotRetentionLimit: NotRequired[int]
    SnapshotWindow: NotRequired[str]
    AuthToken: NotRequired[str]
    OutpostMode: NotRequired[OutpostModeType]
    PreferredOutpostArn: NotRequired[str]
    PreferredOutpostArns: NotRequired[Sequence[str]]
    LogDeliveryConfigurations: NotRequired[Sequence[LogDeliveryConfigurationRequestTypeDef]]
    TransitEncryptionEnabled: NotRequired[bool]
    NetworkType: NotRequired[NetworkTypeType]
    IpDiscovery: NotRequired[IpDiscoveryType]


class CreateReplicationGroupMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    ReplicationGroupDescription: str
    GlobalReplicationGroupId: NotRequired[str]
    PrimaryClusterId: NotRequired[str]
    AutomaticFailoverEnabled: NotRequired[bool]
    MultiAZEnabled: NotRequired[bool]
    NumCacheClusters: NotRequired[int]
    PreferredCacheClusterAZs: NotRequired[Sequence[str]]
    NumNodeGroups: NotRequired[int]
    ReplicasPerNodeGroup: NotRequired[int]
    NodeGroupConfiguration: NotRequired[Sequence[NodeGroupConfigurationUnionTypeDef]]
    CacheNodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    CacheParameterGroupName: NotRequired[str]
    CacheSubnetGroupName: NotRequired[str]
    CacheSecurityGroupNames: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SnapshotArns: NotRequired[Sequence[str]]
    SnapshotName: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    Port: NotRequired[int]
    NotificationTopicArn: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    SnapshotRetentionLimit: NotRequired[int]
    SnapshotWindow: NotRequired[str]
    AuthToken: NotRequired[str]
    TransitEncryptionEnabled: NotRequired[bool]
    AtRestEncryptionEnabled: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    UserGroupIds: NotRequired[Sequence[str]]
    LogDeliveryConfigurations: NotRequired[Sequence[LogDeliveryConfigurationRequestTypeDef]]
    DataTieringEnabled: NotRequired[bool]
    NetworkType: NotRequired[NetworkTypeType]
    IpDiscovery: NotRequired[IpDiscoveryType]
    TransitEncryptionMode: NotRequired[TransitEncryptionModeType]
    ClusterMode: NotRequired[ClusterModeType]
    ServerlessCacheSnapshotName: NotRequired[str]


class ModifyCacheClusterMessageRequestTypeDef(TypedDict):
    CacheClusterId: str
    NumCacheNodes: NotRequired[int]
    CacheNodeIdsToRemove: NotRequired[Sequence[str]]
    AZMode: NotRequired[AZModeType]
    NewAvailabilityZones: NotRequired[Sequence[str]]
    CacheSecurityGroupNames: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    PreferredMaintenanceWindow: NotRequired[str]
    NotificationTopicArn: NotRequired[str]
    CacheParameterGroupName: NotRequired[str]
    NotificationTopicStatus: NotRequired[str]
    ApplyImmediately: NotRequired[bool]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    SnapshotRetentionLimit: NotRequired[int]
    SnapshotWindow: NotRequired[str]
    CacheNodeType: NotRequired[str]
    AuthToken: NotRequired[str]
    AuthTokenUpdateStrategy: NotRequired[AuthTokenUpdateStrategyTypeType]
    LogDeliveryConfigurations: NotRequired[Sequence[LogDeliveryConfigurationRequestTypeDef]]
    IpDiscovery: NotRequired[IpDiscoveryType]


class ModifyReplicationGroupMessageRequestTypeDef(TypedDict):
    ReplicationGroupId: str
    ReplicationGroupDescription: NotRequired[str]
    PrimaryClusterId: NotRequired[str]
    SnapshottingClusterId: NotRequired[str]
    AutomaticFailoverEnabled: NotRequired[bool]
    MultiAZEnabled: NotRequired[bool]
    NodeGroupId: NotRequired[str]
    CacheSecurityGroupNames: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    PreferredMaintenanceWindow: NotRequired[str]
    NotificationTopicArn: NotRequired[str]
    CacheParameterGroupName: NotRequired[str]
    NotificationTopicStatus: NotRequired[str]
    ApplyImmediately: NotRequired[bool]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    SnapshotRetentionLimit: NotRequired[int]
    SnapshotWindow: NotRequired[str]
    CacheNodeType: NotRequired[str]
    AuthToken: NotRequired[str]
    AuthTokenUpdateStrategy: NotRequired[AuthTokenUpdateStrategyTypeType]
    UserGroupIdsToAdd: NotRequired[Sequence[str]]
    UserGroupIdsToRemove: NotRequired[Sequence[str]]
    RemoveUserGroups: NotRequired[bool]
    LogDeliveryConfigurations: NotRequired[Sequence[LogDeliveryConfigurationRequestTypeDef]]
    IpDiscovery: NotRequired[IpDiscoveryType]
    TransitEncryptionEnabled: NotRequired[bool]
    TransitEncryptionMode: NotRequired[TransitEncryptionModeType]
    ClusterMode: NotRequired[ClusterModeType]


class PendingModifiedValuesTypeDef(TypedDict):
    NumCacheNodes: NotRequired[int]
    CacheNodeIdsToRemove: NotRequired[list[str]]
    EngineVersion: NotRequired[str]
    CacheNodeType: NotRequired[str]
    AuthTokenStatus: NotRequired[AuthTokenUpdateStatusType]
    LogDeliveryConfigurations: NotRequired[list[PendingLogDeliveryConfigurationTypeDef]]
    TransitEncryptionEnabled: NotRequired[bool]
    TransitEncryptionMode: NotRequired[TransitEncryptionModeType]


class ReplicationGroupPendingModifiedValuesTypeDef(TypedDict):
    PrimaryClusterId: NotRequired[str]
    AutomaticFailoverStatus: NotRequired[PendingAutomaticFailoverStatusType]
    Resharding: NotRequired[ReshardingStatusTypeDef]
    AuthTokenStatus: NotRequired[AuthTokenUpdateStatusType]
    UserGroups: NotRequired[UserGroupsUpdateStatusTypeDef]
    LogDeliveryConfigurations: NotRequired[list[PendingLogDeliveryConfigurationTypeDef]]
    TransitEncryptionEnabled: NotRequired[bool]
    TransitEncryptionMode: NotRequired[TransitEncryptionModeType]
    ClusterMode: NotRequired[ClusterModeType]


class CopySnapshotResultTypeDef(TypedDict):
    Snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSnapshotResultTypeDef(TypedDict):
    Snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSnapshotResultTypeDef(TypedDict):
    Snapshot: SnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSnapshotsListMessageTypeDef(TypedDict):
    Marker: str
    Snapshots: list[SnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateActionsMessageTypeDef(TypedDict):
    Marker: str
    UpdateActions: list[UpdateActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CacheSubnetGroupMessageTypeDef(TypedDict):
    Marker: str
    CacheSubnetGroups: list[CacheSubnetGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCacheSubnetGroupResultTypeDef(TypedDict):
    CacheSubnetGroup: CacheSubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyCacheSubnetGroupResultTypeDef(TypedDict):
    CacheSubnetGroup: CacheSubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CacheClusterTypeDef(TypedDict):
    CacheClusterId: NotRequired[str]
    ConfigurationEndpoint: NotRequired[EndpointTypeDef]
    ClientDownloadLandingPage: NotRequired[str]
    CacheNodeType: NotRequired[str]
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    CacheClusterStatus: NotRequired[str]
    NumCacheNodes: NotRequired[int]
    PreferredAvailabilityZone: NotRequired[str]
    PreferredOutpostArn: NotRequired[str]
    CacheClusterCreateTime: NotRequired[datetime]
    PreferredMaintenanceWindow: NotRequired[str]
    PendingModifiedValues: NotRequired[PendingModifiedValuesTypeDef]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    CacheSecurityGroups: NotRequired[list[CacheSecurityGroupMembershipTypeDef]]
    CacheParameterGroup: NotRequired[CacheParameterGroupStatusTypeDef]
    CacheSubnetGroupName: NotRequired[str]
    CacheNodes: NotRequired[list[CacheNodeTypeDef]]
    AutoMinorVersionUpgrade: NotRequired[bool]
    SecurityGroups: NotRequired[list[SecurityGroupMembershipTypeDef]]
    ReplicationGroupId: NotRequired[str]
    SnapshotRetentionLimit: NotRequired[int]
    SnapshotWindow: NotRequired[str]
    AuthTokenEnabled: NotRequired[bool]
    AuthTokenLastModifiedDate: NotRequired[datetime]
    TransitEncryptionEnabled: NotRequired[bool]
    AtRestEncryptionEnabled: NotRequired[bool]
    ARN: NotRequired[str]
    ReplicationGroupLogDeliveryEnabled: NotRequired[bool]
    LogDeliveryConfigurations: NotRequired[list[LogDeliveryConfigurationTypeDef]]
    NetworkType: NotRequired[NetworkTypeType]
    IpDiscovery: NotRequired[IpDiscoveryType]
    TransitEncryptionMode: NotRequired[TransitEncryptionModeType]


class ReplicationGroupTypeDef(TypedDict):
    ReplicationGroupId: NotRequired[str]
    Description: NotRequired[str]
    GlobalReplicationGroupInfo: NotRequired[GlobalReplicationGroupInfoTypeDef]
    Status: NotRequired[str]
    PendingModifiedValues: NotRequired[ReplicationGroupPendingModifiedValuesTypeDef]
    MemberClusters: NotRequired[list[str]]
    NodeGroups: NotRequired[list[NodeGroupTypeDef]]
    SnapshottingClusterId: NotRequired[str]
    AutomaticFailover: NotRequired[AutomaticFailoverStatusType]
    MultiAZ: NotRequired[MultiAZStatusType]
    ConfigurationEndpoint: NotRequired[EndpointTypeDef]
    SnapshotRetentionLimit: NotRequired[int]
    SnapshotWindow: NotRequired[str]
    ClusterEnabled: NotRequired[bool]
    CacheNodeType: NotRequired[str]
    AuthTokenEnabled: NotRequired[bool]
    AuthTokenLastModifiedDate: NotRequired[datetime]
    TransitEncryptionEnabled: NotRequired[bool]
    AtRestEncryptionEnabled: NotRequired[bool]
    MemberClustersOutpostArns: NotRequired[list[str]]
    KmsKeyId: NotRequired[str]
    ARN: NotRequired[str]
    UserGroupIds: NotRequired[list[str]]
    LogDeliveryConfigurations: NotRequired[list[LogDeliveryConfigurationTypeDef]]
    ReplicationGroupCreateTime: NotRequired[datetime]
    DataTiering: NotRequired[DataTieringStatusType]
    AutoMinorVersionUpgrade: NotRequired[bool]
    NetworkType: NotRequired[NetworkTypeType]
    IpDiscovery: NotRequired[IpDiscoveryType]
    TransitEncryptionMode: NotRequired[TransitEncryptionModeType]
    ClusterMode: NotRequired[ClusterModeType]
    Engine: NotRequired[str]


class CacheClusterMessageTypeDef(TypedDict):
    Marker: str
    CacheClusters: list[CacheClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCacheClusterResultTypeDef(TypedDict):
    CacheCluster: CacheClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCacheClusterResultTypeDef(TypedDict):
    CacheCluster: CacheClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyCacheClusterResultTypeDef(TypedDict):
    CacheCluster: CacheClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RebootCacheClusterResultTypeDef(TypedDict):
    CacheCluster: CacheClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CompleteMigrationResponseTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateReplicationGroupResultTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DecreaseReplicaCountResultTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteReplicationGroupResultTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IncreaseReplicaCountResultTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyReplicationGroupResultTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyReplicationGroupShardConfigurationResultTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ReplicationGroupMessageTypeDef(TypedDict):
    Marker: str
    ReplicationGroups: list[ReplicationGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartMigrationResponseTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TestFailoverResultTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TestMigrationResponseTypeDef(TypedDict):
    ReplicationGroup: ReplicationGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
