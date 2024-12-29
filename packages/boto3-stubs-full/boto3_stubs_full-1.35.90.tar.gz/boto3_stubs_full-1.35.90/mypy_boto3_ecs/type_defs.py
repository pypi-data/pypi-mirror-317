"""
Type annotations for ecs service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/type_defs/)

Usage::

    ```python
    from mypy_boto3_ecs.type_defs import AttachmentStateChangeTypeDef

    data: AttachmentStateChangeTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    AgentUpdateStatusType,
    ApplicationProtocolType,
    AssignPublicIpType,
    AvailabilityZoneRebalancingType,
    CapacityProviderStatusType,
    CapacityProviderUpdateStatusType,
    ClusterFieldType,
    CompatibilityType,
    ConnectivityType,
    ContainerConditionType,
    ContainerInstanceFieldType,
    ContainerInstanceStatusType,
    CPUArchitectureType,
    DeploymentControllerTypeType,
    DeploymentRolloutStateType,
    DesiredStatusType,
    DeviceCgroupPermissionType,
    EFSAuthorizationConfigIAMType,
    EFSTransitEncryptionType,
    ExecuteCommandLoggingType,
    FirelensConfigurationTypeType,
    HealthStatusType,
    InstanceHealthCheckStateType,
    IpcModeType,
    LaunchTypeType,
    LogDriverType,
    ManagedDrainingType,
    ManagedScalingStatusType,
    ManagedTerminationProtectionType,
    NetworkModeType,
    OSFamilyType,
    PidModeType,
    PlacementConstraintTypeType,
    PlacementStrategyTypeType,
    PropagateTagsType,
    ResourceTypeType,
    SchedulingStrategyType,
    ScopeType,
    ServiceDeploymentRollbackMonitorsStatusType,
    ServiceDeploymentStatusType,
    SettingNameType,
    SettingTypeType,
    SortOrderType,
    StabilityStatusType,
    TaskDefinitionFamilyStatusType,
    TaskDefinitionStatusType,
    TaskFilesystemTypeType,
    TaskStopCodeType,
    TransportProtocolType,
    UlimitNameType,
    VersionConsistencyType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AttachmentStateChangeTypeDef",
    "AttachmentTypeDef",
    "AttributeTypeDef",
    "AutoScalingGroupProviderTypeDef",
    "AutoScalingGroupProviderUpdateTypeDef",
    "AwsVpcConfigurationOutputTypeDef",
    "AwsVpcConfigurationTypeDef",
    "AwsVpcConfigurationUnionTypeDef",
    "CapacityProviderStrategyItemTypeDef",
    "CapacityProviderTypeDef",
    "ClusterConfigurationTypeDef",
    "ClusterServiceConnectDefaultsRequestTypeDef",
    "ClusterServiceConnectDefaultsTypeDef",
    "ClusterSettingTypeDef",
    "ClusterTypeDef",
    "ContainerDefinitionOutputTypeDef",
    "ContainerDefinitionTypeDef",
    "ContainerDefinitionUnionTypeDef",
    "ContainerDependencyTypeDef",
    "ContainerImageTypeDef",
    "ContainerInstanceHealthStatusTypeDef",
    "ContainerInstanceTypeDef",
    "ContainerOverrideOutputTypeDef",
    "ContainerOverrideTypeDef",
    "ContainerOverrideUnionTypeDef",
    "ContainerRestartPolicyOutputTypeDef",
    "ContainerRestartPolicyTypeDef",
    "ContainerRestartPolicyUnionTypeDef",
    "ContainerStateChangeTypeDef",
    "ContainerTypeDef",
    "CreateCapacityProviderRequestRequestTypeDef",
    "CreateCapacityProviderResponseTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "CreateServiceResponseTypeDef",
    "CreateTaskSetRequestRequestTypeDef",
    "CreateTaskSetResponseTypeDef",
    "CreatedAtTypeDef",
    "DeleteAccountSettingRequestRequestTypeDef",
    "DeleteAccountSettingResponseTypeDef",
    "DeleteAttributesRequestRequestTypeDef",
    "DeleteAttributesResponseTypeDef",
    "DeleteCapacityProviderRequestRequestTypeDef",
    "DeleteCapacityProviderResponseTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "DeleteServiceResponseTypeDef",
    "DeleteTaskDefinitionsRequestRequestTypeDef",
    "DeleteTaskDefinitionsResponseTypeDef",
    "DeleteTaskSetRequestRequestTypeDef",
    "DeleteTaskSetResponseTypeDef",
    "DeploymentAlarmsOutputTypeDef",
    "DeploymentAlarmsTypeDef",
    "DeploymentAlarmsUnionTypeDef",
    "DeploymentCircuitBreakerTypeDef",
    "DeploymentConfigurationOutputTypeDef",
    "DeploymentConfigurationTypeDef",
    "DeploymentControllerTypeDef",
    "DeploymentEphemeralStorageTypeDef",
    "DeploymentTypeDef",
    "DeregisterContainerInstanceRequestRequestTypeDef",
    "DeregisterContainerInstanceResponseTypeDef",
    "DeregisterTaskDefinitionRequestRequestTypeDef",
    "DeregisterTaskDefinitionResponseTypeDef",
    "DescribeCapacityProvidersRequestRequestTypeDef",
    "DescribeCapacityProvidersResponseTypeDef",
    "DescribeClustersRequestRequestTypeDef",
    "DescribeClustersResponseTypeDef",
    "DescribeContainerInstancesRequestRequestTypeDef",
    "DescribeContainerInstancesResponseTypeDef",
    "DescribeServiceDeploymentsRequestRequestTypeDef",
    "DescribeServiceDeploymentsResponseTypeDef",
    "DescribeServiceRevisionsRequestRequestTypeDef",
    "DescribeServiceRevisionsResponseTypeDef",
    "DescribeServicesRequestRequestTypeDef",
    "DescribeServicesRequestWaitTypeDef",
    "DescribeServicesResponseTypeDef",
    "DescribeTaskDefinitionRequestRequestTypeDef",
    "DescribeTaskDefinitionResponseTypeDef",
    "DescribeTaskSetsRequestRequestTypeDef",
    "DescribeTaskSetsResponseTypeDef",
    "DescribeTasksRequestRequestTypeDef",
    "DescribeTasksRequestWaitTypeDef",
    "DescribeTasksResponseTypeDef",
    "DeviceOutputTypeDef",
    "DeviceTypeDef",
    "DeviceUnionTypeDef",
    "DiscoverPollEndpointRequestRequestTypeDef",
    "DiscoverPollEndpointResponseTypeDef",
    "DockerVolumeConfigurationOutputTypeDef",
    "DockerVolumeConfigurationTypeDef",
    "DockerVolumeConfigurationUnionTypeDef",
    "EBSTagSpecificationOutputTypeDef",
    "EBSTagSpecificationTypeDef",
    "EBSTagSpecificationUnionTypeDef",
    "EFSAuthorizationConfigTypeDef",
    "EFSVolumeConfigurationTypeDef",
    "EnvironmentFileTypeDef",
    "EphemeralStorageTypeDef",
    "ExecuteCommandConfigurationTypeDef",
    "ExecuteCommandLogConfigurationTypeDef",
    "ExecuteCommandRequestRequestTypeDef",
    "ExecuteCommandResponseTypeDef",
    "FSxWindowsFileServerAuthorizationConfigTypeDef",
    "FSxWindowsFileServerVolumeConfigurationTypeDef",
    "FailureTypeDef",
    "FirelensConfigurationOutputTypeDef",
    "FirelensConfigurationTypeDef",
    "FirelensConfigurationUnionTypeDef",
    "GetTaskProtectionRequestRequestTypeDef",
    "GetTaskProtectionResponseTypeDef",
    "HealthCheckOutputTypeDef",
    "HealthCheckTypeDef",
    "HealthCheckUnionTypeDef",
    "HostEntryTypeDef",
    "HostVolumePropertiesTypeDef",
    "InferenceAcceleratorOverrideTypeDef",
    "InferenceAcceleratorTypeDef",
    "InstanceHealthCheckResultTypeDef",
    "KernelCapabilitiesOutputTypeDef",
    "KernelCapabilitiesTypeDef",
    "KernelCapabilitiesUnionTypeDef",
    "KeyValuePairTypeDef",
    "LinuxParametersOutputTypeDef",
    "LinuxParametersTypeDef",
    "LinuxParametersUnionTypeDef",
    "ListAccountSettingsRequestPaginateTypeDef",
    "ListAccountSettingsRequestRequestTypeDef",
    "ListAccountSettingsResponseTypeDef",
    "ListAttributesRequestPaginateTypeDef",
    "ListAttributesRequestRequestTypeDef",
    "ListAttributesResponseTypeDef",
    "ListClustersRequestPaginateTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListContainerInstancesRequestPaginateTypeDef",
    "ListContainerInstancesRequestRequestTypeDef",
    "ListContainerInstancesResponseTypeDef",
    "ListServiceDeploymentsRequestRequestTypeDef",
    "ListServiceDeploymentsResponseTypeDef",
    "ListServicesByNamespaceRequestPaginateTypeDef",
    "ListServicesByNamespaceRequestRequestTypeDef",
    "ListServicesByNamespaceResponseTypeDef",
    "ListServicesRequestPaginateTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTaskDefinitionFamiliesRequestPaginateTypeDef",
    "ListTaskDefinitionFamiliesRequestRequestTypeDef",
    "ListTaskDefinitionFamiliesResponseTypeDef",
    "ListTaskDefinitionsRequestPaginateTypeDef",
    "ListTaskDefinitionsRequestRequestTypeDef",
    "ListTaskDefinitionsResponseTypeDef",
    "ListTasksRequestPaginateTypeDef",
    "ListTasksRequestRequestTypeDef",
    "ListTasksResponseTypeDef",
    "LoadBalancerTypeDef",
    "LogConfigurationOutputTypeDef",
    "LogConfigurationTypeDef",
    "LogConfigurationUnionTypeDef",
    "ManagedAgentStateChangeTypeDef",
    "ManagedAgentTypeDef",
    "ManagedScalingTypeDef",
    "ManagedStorageConfigurationTypeDef",
    "MountPointTypeDef",
    "NetworkBindingTypeDef",
    "NetworkConfigurationOutputTypeDef",
    "NetworkConfigurationTypeDef",
    "NetworkInterfaceTypeDef",
    "PaginatorConfigTypeDef",
    "PlacementConstraintTypeDef",
    "PlacementStrategyTypeDef",
    "PlatformDeviceTypeDef",
    "PortMappingTypeDef",
    "ProtectedTaskTypeDef",
    "ProxyConfigurationOutputTypeDef",
    "ProxyConfigurationTypeDef",
    "PutAccountSettingDefaultRequestRequestTypeDef",
    "PutAccountSettingDefaultResponseTypeDef",
    "PutAccountSettingRequestRequestTypeDef",
    "PutAccountSettingResponseTypeDef",
    "PutAttributesRequestRequestTypeDef",
    "PutAttributesResponseTypeDef",
    "PutClusterCapacityProvidersRequestRequestTypeDef",
    "PutClusterCapacityProvidersResponseTypeDef",
    "RegisterContainerInstanceRequestRequestTypeDef",
    "RegisterContainerInstanceResponseTypeDef",
    "RegisterTaskDefinitionRequestRequestTypeDef",
    "RegisterTaskDefinitionResponseTypeDef",
    "RepositoryCredentialsTypeDef",
    "ResourceOutputTypeDef",
    "ResourceRequirementTypeDef",
    "ResourceTypeDef",
    "ResourceUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RollbackTypeDef",
    "RunTaskRequestRequestTypeDef",
    "RunTaskResponseTypeDef",
    "RuntimePlatformTypeDef",
    "ScaleTypeDef",
    "SecretTypeDef",
    "ServiceConnectClientAliasTypeDef",
    "ServiceConnectConfigurationOutputTypeDef",
    "ServiceConnectConfigurationTypeDef",
    "ServiceConnectServiceOutputTypeDef",
    "ServiceConnectServiceResourceTypeDef",
    "ServiceConnectServiceTypeDef",
    "ServiceConnectServiceUnionTypeDef",
    "ServiceConnectTlsCertificateAuthorityTypeDef",
    "ServiceConnectTlsConfigurationTypeDef",
    "ServiceDeploymentAlarmsTypeDef",
    "ServiceDeploymentBriefTypeDef",
    "ServiceDeploymentCircuitBreakerTypeDef",
    "ServiceDeploymentTypeDef",
    "ServiceEventTypeDef",
    "ServiceManagedEBSVolumeConfigurationOutputTypeDef",
    "ServiceManagedEBSVolumeConfigurationTypeDef",
    "ServiceManagedEBSVolumeConfigurationUnionTypeDef",
    "ServiceRegistryTypeDef",
    "ServiceRevisionSummaryTypeDef",
    "ServiceRevisionTypeDef",
    "ServiceTypeDef",
    "ServiceVolumeConfigurationOutputTypeDef",
    "ServiceVolumeConfigurationTypeDef",
    "ServiceVolumeConfigurationUnionTypeDef",
    "SessionTypeDef",
    "SettingTypeDef",
    "StartTaskRequestRequestTypeDef",
    "StartTaskResponseTypeDef",
    "StopTaskRequestRequestTypeDef",
    "StopTaskResponseTypeDef",
    "SubmitAttachmentStateChangesRequestRequestTypeDef",
    "SubmitAttachmentStateChangesResponseTypeDef",
    "SubmitContainerStateChangeRequestRequestTypeDef",
    "SubmitContainerStateChangeResponseTypeDef",
    "SubmitTaskStateChangeRequestRequestTypeDef",
    "SubmitTaskStateChangeResponseTypeDef",
    "SystemControlTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TaskDefinitionPlacementConstraintTypeDef",
    "TaskDefinitionTypeDef",
    "TaskEphemeralStorageTypeDef",
    "TaskManagedEBSVolumeConfigurationTypeDef",
    "TaskManagedEBSVolumeTerminationPolicyTypeDef",
    "TaskOverrideOutputTypeDef",
    "TaskOverrideTypeDef",
    "TaskSetTypeDef",
    "TaskTypeDef",
    "TaskVolumeConfigurationTypeDef",
    "TimeoutConfigurationTypeDef",
    "TimestampTypeDef",
    "TmpfsOutputTypeDef",
    "TmpfsTypeDef",
    "TmpfsUnionTypeDef",
    "UlimitTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateCapacityProviderRequestRequestTypeDef",
    "UpdateCapacityProviderResponseTypeDef",
    "UpdateClusterRequestRequestTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateClusterSettingsRequestRequestTypeDef",
    "UpdateClusterSettingsResponseTypeDef",
    "UpdateContainerAgentRequestRequestTypeDef",
    "UpdateContainerAgentResponseTypeDef",
    "UpdateContainerInstancesStateRequestRequestTypeDef",
    "UpdateContainerInstancesStateResponseTypeDef",
    "UpdateServicePrimaryTaskSetRequestRequestTypeDef",
    "UpdateServicePrimaryTaskSetResponseTypeDef",
    "UpdateServiceRequestRequestTypeDef",
    "UpdateServiceResponseTypeDef",
    "UpdateTaskProtectionRequestRequestTypeDef",
    "UpdateTaskProtectionResponseTypeDef",
    "UpdateTaskSetRequestRequestTypeDef",
    "UpdateTaskSetResponseTypeDef",
    "VersionInfoTypeDef",
    "VolumeFromTypeDef",
    "VolumeOutputTypeDef",
    "VolumeTypeDef",
    "VolumeUnionTypeDef",
    "VpcLatticeConfigurationTypeDef",
    "WaiterConfigTypeDef",
)


class AttachmentStateChangeTypeDef(TypedDict):
    attachmentArn: str
    status: str


class KeyValuePairTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]


class AttributeTypeDef(TypedDict):
    name: str
    value: NotRequired[str]
    targetType: NotRequired[Literal["container-instance"]]
    targetId: NotRequired[str]


class ManagedScalingTypeDef(TypedDict):
    status: NotRequired[ManagedScalingStatusType]
    targetCapacity: NotRequired[int]
    minimumScalingStepSize: NotRequired[int]
    maximumScalingStepSize: NotRequired[int]
    instanceWarmupPeriod: NotRequired[int]


class AwsVpcConfigurationOutputTypeDef(TypedDict):
    subnets: list[str]
    securityGroups: NotRequired[list[str]]
    assignPublicIp: NotRequired[AssignPublicIpType]


class AwsVpcConfigurationTypeDef(TypedDict):
    subnets: Sequence[str]
    securityGroups: NotRequired[Sequence[str]]
    assignPublicIp: NotRequired[AssignPublicIpType]


class CapacityProviderStrategyItemTypeDef(TypedDict):
    capacityProvider: str
    weight: NotRequired[int]
    base: NotRequired[int]


class TagTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]


class ManagedStorageConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]
    fargateEphemeralStorageKmsKeyId: NotRequired[str]


class ClusterServiceConnectDefaultsRequestTypeDef(TypedDict):
    namespace: str


class ClusterServiceConnectDefaultsTypeDef(TypedDict):
    namespace: NotRequired[str]


class ClusterSettingTypeDef(TypedDict):
    name: NotRequired[Literal["containerInsights"]]
    value: NotRequired[str]


class ContainerDependencyTypeDef(TypedDict):
    containerName: str
    condition: ContainerConditionType


class ContainerRestartPolicyOutputTypeDef(TypedDict):
    enabled: bool
    ignoredExitCodes: NotRequired[list[int]]
    restartAttemptPeriod: NotRequired[int]


EnvironmentFileTypeDef = TypedDict(
    "EnvironmentFileTypeDef",
    {
        "value": str,
        "type": Literal["s3"],
    },
)
FirelensConfigurationOutputTypeDef = TypedDict(
    "FirelensConfigurationOutputTypeDef",
    {
        "type": FirelensConfigurationTypeType,
        "options": NotRequired[dict[str, str]],
    },
)


class HealthCheckOutputTypeDef(TypedDict):
    command: list[str]
    interval: NotRequired[int]
    timeout: NotRequired[int]
    retries: NotRequired[int]
    startPeriod: NotRequired[int]


class HostEntryTypeDef(TypedDict):
    hostname: str
    ipAddress: str


class MountPointTypeDef(TypedDict):
    sourceVolume: NotRequired[str]
    containerPath: NotRequired[str]
    readOnly: NotRequired[bool]


class PortMappingTypeDef(TypedDict):
    containerPort: NotRequired[int]
    hostPort: NotRequired[int]
    protocol: NotRequired[TransportProtocolType]
    name: NotRequired[str]
    appProtocol: NotRequired[ApplicationProtocolType]
    containerPortRange: NotRequired[str]


class RepositoryCredentialsTypeDef(TypedDict):
    credentialsParameter: str


ResourceRequirementTypeDef = TypedDict(
    "ResourceRequirementTypeDef",
    {
        "value": str,
        "type": ResourceTypeType,
    },
)


class SecretTypeDef(TypedDict):
    name: str
    valueFrom: str


class SystemControlTypeDef(TypedDict):
    namespace: NotRequired[str]
    value: NotRequired[str]


class UlimitTypeDef(TypedDict):
    name: UlimitNameType
    softLimit: int
    hardLimit: int


class VolumeFromTypeDef(TypedDict):
    sourceContainer: NotRequired[str]
    readOnly: NotRequired[bool]


class ContainerImageTypeDef(TypedDict):
    containerName: NotRequired[str]
    imageDigest: NotRequired[str]
    image: NotRequired[str]


InstanceHealthCheckResultTypeDef = TypedDict(
    "InstanceHealthCheckResultTypeDef",
    {
        "type": NotRequired[Literal["CONTAINER_RUNTIME"]],
        "status": NotRequired[InstanceHealthCheckStateType],
        "lastUpdated": NotRequired[datetime],
        "lastStatusChange": NotRequired[datetime],
    },
)
ResourceOutputTypeDef = TypedDict(
    "ResourceOutputTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "doubleValue": NotRequired[float],
        "longValue": NotRequired[int],
        "integerValue": NotRequired[int],
        "stringSetValue": NotRequired[list[str]],
    },
)


class VersionInfoTypeDef(TypedDict):
    agentVersion: NotRequired[str]
    agentHash: NotRequired[str]
    dockerVersion: NotRequired[str]


class ContainerRestartPolicyTypeDef(TypedDict):
    enabled: bool
    ignoredExitCodes: NotRequired[Sequence[int]]
    restartAttemptPeriod: NotRequired[int]


class NetworkBindingTypeDef(TypedDict):
    bindIP: NotRequired[str]
    containerPort: NotRequired[int]
    hostPort: NotRequired[int]
    protocol: NotRequired[TransportProtocolType]
    containerPortRange: NotRequired[str]
    hostPortRange: NotRequired[str]


class ManagedAgentTypeDef(TypedDict):
    lastStartedAt: NotRequired[datetime]
    name: NotRequired[Literal["ExecuteCommandAgent"]]
    reason: NotRequired[str]
    lastStatus: NotRequired[str]


class NetworkInterfaceTypeDef(TypedDict):
    attachmentId: NotRequired[str]
    privateIpv4Address: NotRequired[str]
    ipv6Address: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


DeploymentControllerTypeDef = TypedDict(
    "DeploymentControllerTypeDef",
    {
        "type": DeploymentControllerTypeType,
    },
)


class LoadBalancerTypeDef(TypedDict):
    targetGroupArn: NotRequired[str]
    loadBalancerName: NotRequired[str]
    containerName: NotRequired[str]
    containerPort: NotRequired[int]


PlacementConstraintTypeDef = TypedDict(
    "PlacementConstraintTypeDef",
    {
        "type": NotRequired[PlacementConstraintTypeType],
        "expression": NotRequired[str],
    },
)
PlacementStrategyTypeDef = TypedDict(
    "PlacementStrategyTypeDef",
    {
        "type": NotRequired[PlacementStrategyTypeType],
        "field": NotRequired[str],
    },
)


class ServiceRegistryTypeDef(TypedDict):
    registryArn: NotRequired[str]
    port: NotRequired[int]
    containerName: NotRequired[str]
    containerPort: NotRequired[int]


class VpcLatticeConfigurationTypeDef(TypedDict):
    roleArn: str
    targetGroupArn: str
    portName: str


class ScaleTypeDef(TypedDict):
    value: NotRequired[float]
    unit: NotRequired[Literal["PERCENT"]]


TimestampTypeDef = Union[datetime, str]


class DeleteAccountSettingRequestRequestTypeDef(TypedDict):
    name: SettingNameType
    principalArn: NotRequired[str]


SettingTypeDef = TypedDict(
    "SettingTypeDef",
    {
        "name": NotRequired[SettingNameType],
        "value": NotRequired[str],
        "principalArn": NotRequired[str],
        "type": NotRequired[SettingTypeType],
    },
)


class DeleteCapacityProviderRequestRequestTypeDef(TypedDict):
    capacityProvider: str


class DeleteClusterRequestRequestTypeDef(TypedDict):
    cluster: str


class DeleteServiceRequestRequestTypeDef(TypedDict):
    service: str
    cluster: NotRequired[str]
    force: NotRequired[bool]


class DeleteTaskDefinitionsRequestRequestTypeDef(TypedDict):
    taskDefinitions: Sequence[str]


class FailureTypeDef(TypedDict):
    arn: NotRequired[str]
    reason: NotRequired[str]
    detail: NotRequired[str]


class DeleteTaskSetRequestRequestTypeDef(TypedDict):
    cluster: str
    service: str
    taskSet: str
    force: NotRequired[bool]


class DeploymentAlarmsOutputTypeDef(TypedDict):
    alarmNames: list[str]
    rollback: bool
    enable: bool


class DeploymentAlarmsTypeDef(TypedDict):
    alarmNames: Sequence[str]
    rollback: bool
    enable: bool


class DeploymentCircuitBreakerTypeDef(TypedDict):
    enable: bool
    rollback: bool


class DeploymentEphemeralStorageTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]


class ServiceConnectServiceResourceTypeDef(TypedDict):
    discoveryName: NotRequired[str]
    discoveryArn: NotRequired[str]


class DeregisterContainerInstanceRequestRequestTypeDef(TypedDict):
    containerInstance: str
    cluster: NotRequired[str]
    force: NotRequired[bool]


class DeregisterTaskDefinitionRequestRequestTypeDef(TypedDict):
    taskDefinition: str


class DescribeCapacityProvidersRequestRequestTypeDef(TypedDict):
    capacityProviders: NotRequired[Sequence[str]]
    include: NotRequired[Sequence[Literal["TAGS"]]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeClustersRequestRequestTypeDef(TypedDict):
    clusters: NotRequired[Sequence[str]]
    include: NotRequired[Sequence[ClusterFieldType]]


class DescribeContainerInstancesRequestRequestTypeDef(TypedDict):
    containerInstances: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[ContainerInstanceFieldType]]


class DescribeServiceDeploymentsRequestRequestTypeDef(TypedDict):
    serviceDeploymentArns: Sequence[str]


class DescribeServiceRevisionsRequestRequestTypeDef(TypedDict):
    serviceRevisionArns: Sequence[str]


class DescribeServicesRequestRequestTypeDef(TypedDict):
    services: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeTaskDefinitionRequestRequestTypeDef(TypedDict):
    taskDefinition: str
    include: NotRequired[Sequence[Literal["TAGS"]]]


class DescribeTaskSetsRequestRequestTypeDef(TypedDict):
    cluster: str
    service: str
    taskSets: NotRequired[Sequence[str]]
    include: NotRequired[Sequence[Literal["TAGS"]]]


class DescribeTasksRequestRequestTypeDef(TypedDict):
    tasks: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]


class DeviceOutputTypeDef(TypedDict):
    hostPath: str
    containerPath: NotRequired[str]
    permissions: NotRequired[list[DeviceCgroupPermissionType]]


class DeviceTypeDef(TypedDict):
    hostPath: str
    containerPath: NotRequired[str]
    permissions: NotRequired[Sequence[DeviceCgroupPermissionType]]


class DiscoverPollEndpointRequestRequestTypeDef(TypedDict):
    containerInstance: NotRequired[str]
    cluster: NotRequired[str]


class DockerVolumeConfigurationOutputTypeDef(TypedDict):
    scope: NotRequired[ScopeType]
    autoprovision: NotRequired[bool]
    driver: NotRequired[str]
    driverOpts: NotRequired[dict[str, str]]
    labels: NotRequired[dict[str, str]]


class DockerVolumeConfigurationTypeDef(TypedDict):
    scope: NotRequired[ScopeType]
    autoprovision: NotRequired[bool]
    driver: NotRequired[str]
    driverOpts: NotRequired[Mapping[str, str]]
    labels: NotRequired[Mapping[str, str]]


class EFSAuthorizationConfigTypeDef(TypedDict):
    accessPointId: NotRequired[str]
    iam: NotRequired[EFSAuthorizationConfigIAMType]


class EphemeralStorageTypeDef(TypedDict):
    sizeInGiB: int


class ExecuteCommandLogConfigurationTypeDef(TypedDict):
    cloudWatchLogGroupName: NotRequired[str]
    cloudWatchEncryptionEnabled: NotRequired[bool]
    s3BucketName: NotRequired[str]
    s3EncryptionEnabled: NotRequired[bool]
    s3KeyPrefix: NotRequired[str]


class ExecuteCommandRequestRequestTypeDef(TypedDict):
    command: str
    interactive: bool
    task: str
    cluster: NotRequired[str]
    container: NotRequired[str]


class SessionTypeDef(TypedDict):
    sessionId: NotRequired[str]
    streamUrl: NotRequired[str]
    tokenValue: NotRequired[str]


class FSxWindowsFileServerAuthorizationConfigTypeDef(TypedDict):
    credentialsParameter: str
    domain: str


FirelensConfigurationTypeDef = TypedDict(
    "FirelensConfigurationTypeDef",
    {
        "type": FirelensConfigurationTypeType,
        "options": NotRequired[Mapping[str, str]],
    },
)


class GetTaskProtectionRequestRequestTypeDef(TypedDict):
    cluster: str
    tasks: NotRequired[Sequence[str]]


class ProtectedTaskTypeDef(TypedDict):
    taskArn: NotRequired[str]
    protectionEnabled: NotRequired[bool]
    expirationDate: NotRequired[datetime]


class HealthCheckTypeDef(TypedDict):
    command: Sequence[str]
    interval: NotRequired[int]
    timeout: NotRequired[int]
    retries: NotRequired[int]
    startPeriod: NotRequired[int]


class HostVolumePropertiesTypeDef(TypedDict):
    sourcePath: NotRequired[str]


class InferenceAcceleratorOverrideTypeDef(TypedDict):
    deviceName: NotRequired[str]
    deviceType: NotRequired[str]


class InferenceAcceleratorTypeDef(TypedDict):
    deviceName: str
    deviceType: str


class KernelCapabilitiesOutputTypeDef(TypedDict):
    add: NotRequired[list[str]]
    drop: NotRequired[list[str]]


class KernelCapabilitiesTypeDef(TypedDict):
    add: NotRequired[Sequence[str]]
    drop: NotRequired[Sequence[str]]


class TmpfsOutputTypeDef(TypedDict):
    containerPath: str
    size: int
    mountOptions: NotRequired[list[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAccountSettingsRequestRequestTypeDef(TypedDict):
    name: NotRequired[SettingNameType]
    value: NotRequired[str]
    principalArn: NotRequired[str]
    effectiveSettings: NotRequired[bool]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAttributesRequestRequestTypeDef(TypedDict):
    targetType: Literal["container-instance"]
    cluster: NotRequired[str]
    attributeName: NotRequired[str]
    attributeValue: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListClustersRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ListContainerInstancesRequestRequestTypeDef = TypedDict(
    "ListContainerInstancesRequestRequestTypeDef",
    {
        "cluster": NotRequired[str],
        "filter": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "status": NotRequired[ContainerInstanceStatusType],
    },
)


class ServiceDeploymentBriefTypeDef(TypedDict):
    serviceDeploymentArn: NotRequired[str]
    serviceArn: NotRequired[str]
    clusterArn: NotRequired[str]
    startedAt: NotRequired[datetime]
    createdAt: NotRequired[datetime]
    finishedAt: NotRequired[datetime]
    targetServiceRevisionArn: NotRequired[str]
    status: NotRequired[ServiceDeploymentStatusType]
    statusReason: NotRequired[str]


class ListServicesByNamespaceRequestRequestTypeDef(TypedDict):
    namespace: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListServicesRequestRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    launchType: NotRequired[LaunchTypeType]
    schedulingStrategy: NotRequired[SchedulingStrategyType]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class ListTaskDefinitionFamiliesRequestRequestTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    status: NotRequired[TaskDefinitionFamilyStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListTaskDefinitionsRequestRequestTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    status: NotRequired[TaskDefinitionStatusType]
    sort: NotRequired[SortOrderType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListTasksRequestRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    containerInstance: NotRequired[str]
    family: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    startedBy: NotRequired[str]
    serviceName: NotRequired[str]
    desiredStatus: NotRequired[DesiredStatusType]
    launchType: NotRequired[LaunchTypeType]


class ManagedAgentStateChangeTypeDef(TypedDict):
    containerName: str
    managedAgentName: Literal["ExecuteCommandAgent"]
    status: str
    reason: NotRequired[str]


PlatformDeviceTypeDef = TypedDict(
    "PlatformDeviceTypeDef",
    {
        "id": str,
        "type": Literal["GPU"],
    },
)


class PutAccountSettingDefaultRequestRequestTypeDef(TypedDict):
    name: SettingNameType
    value: str


class PutAccountSettingRequestRequestTypeDef(TypedDict):
    name: SettingNameType
    value: str
    principalArn: NotRequired[str]


class RuntimePlatformTypeDef(TypedDict):
    cpuArchitecture: NotRequired[CPUArchitectureType]
    operatingSystemFamily: NotRequired[OSFamilyType]


TaskDefinitionPlacementConstraintTypeDef = TypedDict(
    "TaskDefinitionPlacementConstraintTypeDef",
    {
        "type": NotRequired[Literal["memberOf"]],
        "expression": NotRequired[str],
    },
)
ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "doubleValue": NotRequired[float],
        "longValue": NotRequired[int],
        "integerValue": NotRequired[int],
        "stringSetValue": NotRequired[Sequence[str]],
    },
)


class RollbackTypeDef(TypedDict):
    reason: NotRequired[str]
    startedAt: NotRequired[datetime]
    serviceRevisionArn: NotRequired[str]


class ServiceConnectClientAliasTypeDef(TypedDict):
    port: int
    dnsName: NotRequired[str]


class TimeoutConfigurationTypeDef(TypedDict):
    idleTimeoutSeconds: NotRequired[int]
    perRequestTimeoutSeconds: NotRequired[int]


class ServiceConnectTlsCertificateAuthorityTypeDef(TypedDict):
    awsPcaAuthorityArn: NotRequired[str]


class ServiceDeploymentAlarmsTypeDef(TypedDict):
    status: NotRequired[ServiceDeploymentRollbackMonitorsStatusType]
    alarmNames: NotRequired[list[str]]
    triggeredAlarmNames: NotRequired[list[str]]


class ServiceDeploymentCircuitBreakerTypeDef(TypedDict):
    status: NotRequired[ServiceDeploymentRollbackMonitorsStatusType]
    failureCount: NotRequired[int]
    threshold: NotRequired[int]


class ServiceRevisionSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    requestedTaskCount: NotRequired[int]
    runningTaskCount: NotRequired[int]
    pendingTaskCount: NotRequired[int]


ServiceEventTypeDef = TypedDict(
    "ServiceEventTypeDef",
    {
        "id": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "message": NotRequired[str],
    },
)


class StopTaskRequestRequestTypeDef(TypedDict):
    task: str
    cluster: NotRequired[str]
    reason: NotRequired[str]


class TaskEphemeralStorageTypeDef(TypedDict):
    sizeInGiB: NotRequired[int]
    kmsKeyId: NotRequired[str]


class TaskManagedEBSVolumeTerminationPolicyTypeDef(TypedDict):
    deleteOnTermination: bool


class TmpfsTypeDef(TypedDict):
    containerPath: str
    size: int
    mountOptions: NotRequired[Sequence[str]]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateContainerAgentRequestRequestTypeDef(TypedDict):
    containerInstance: str
    cluster: NotRequired[str]


class UpdateContainerInstancesStateRequestRequestTypeDef(TypedDict):
    containerInstances: Sequence[str]
    status: ContainerInstanceStatusType
    cluster: NotRequired[str]


class UpdateServicePrimaryTaskSetRequestRequestTypeDef(TypedDict):
    cluster: str
    service: str
    primaryTaskSet: str


class UpdateTaskProtectionRequestRequestTypeDef(TypedDict):
    cluster: str
    tasks: Sequence[str]
    protectionEnabled: bool
    expiresInMinutes: NotRequired[int]


class SubmitAttachmentStateChangesRequestRequestTypeDef(TypedDict):
    attachments: Sequence[AttachmentStateChangeTypeDef]
    cluster: NotRequired[str]


AttachmentTypeDef = TypedDict(
    "AttachmentTypeDef",
    {
        "id": NotRequired[str],
        "type": NotRequired[str],
        "status": NotRequired[str],
        "details": NotRequired[list[KeyValuePairTypeDef]],
    },
)
ProxyConfigurationOutputTypeDef = TypedDict(
    "ProxyConfigurationOutputTypeDef",
    {
        "containerName": str,
        "type": NotRequired[Literal["APPMESH"]],
        "properties": NotRequired[list[KeyValuePairTypeDef]],
    },
)
ProxyConfigurationTypeDef = TypedDict(
    "ProxyConfigurationTypeDef",
    {
        "containerName": str,
        "type": NotRequired[Literal["APPMESH"]],
        "properties": NotRequired[Sequence[KeyValuePairTypeDef]],
    },
)


class DeleteAttributesRequestRequestTypeDef(TypedDict):
    attributes: Sequence[AttributeTypeDef]
    cluster: NotRequired[str]


class PutAttributesRequestRequestTypeDef(TypedDict):
    attributes: Sequence[AttributeTypeDef]
    cluster: NotRequired[str]


class AutoScalingGroupProviderTypeDef(TypedDict):
    autoScalingGroupArn: str
    managedScaling: NotRequired[ManagedScalingTypeDef]
    managedTerminationProtection: NotRequired[ManagedTerminationProtectionType]
    managedDraining: NotRequired[ManagedDrainingType]


class AutoScalingGroupProviderUpdateTypeDef(TypedDict):
    managedScaling: NotRequired[ManagedScalingTypeDef]
    managedTerminationProtection: NotRequired[ManagedTerminationProtectionType]
    managedDraining: NotRequired[ManagedDrainingType]


class NetworkConfigurationOutputTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationOutputTypeDef]


AwsVpcConfigurationUnionTypeDef = Union[
    AwsVpcConfigurationTypeDef, AwsVpcConfigurationOutputTypeDef
]


class PutClusterCapacityProvidersRequestRequestTypeDef(TypedDict):
    cluster: str
    capacityProviders: Sequence[str]
    defaultCapacityProviderStrategy: Sequence[CapacityProviderStrategyItemTypeDef]


class EBSTagSpecificationOutputTypeDef(TypedDict):
    resourceType: Literal["volume"]
    tags: NotRequired[list[TagTypeDef]]
    propagateTags: NotRequired[PropagateTagsType]


class EBSTagSpecificationTypeDef(TypedDict):
    resourceType: Literal["volume"]
    tags: NotRequired[Sequence[TagTypeDef]]
    propagateTags: NotRequired[PropagateTagsType]


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class UpdateClusterSettingsRequestRequestTypeDef(TypedDict):
    cluster: str
    settings: Sequence[ClusterSettingTypeDef]


class ContainerOverrideOutputTypeDef(TypedDict):
    name: NotRequired[str]
    command: NotRequired[list[str]]
    environment: NotRequired[list[KeyValuePairTypeDef]]
    environmentFiles: NotRequired[list[EnvironmentFileTypeDef]]
    cpu: NotRequired[int]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    resourceRequirements: NotRequired[list[ResourceRequirementTypeDef]]


class ContainerOverrideTypeDef(TypedDict):
    name: NotRequired[str]
    command: NotRequired[Sequence[str]]
    environment: NotRequired[Sequence[KeyValuePairTypeDef]]
    environmentFiles: NotRequired[Sequence[EnvironmentFileTypeDef]]
    cpu: NotRequired[int]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    resourceRequirements: NotRequired[Sequence[ResourceRequirementTypeDef]]


class LogConfigurationOutputTypeDef(TypedDict):
    logDriver: LogDriverType
    options: NotRequired[dict[str, str]]
    secretOptions: NotRequired[list[SecretTypeDef]]


class LogConfigurationTypeDef(TypedDict):
    logDriver: LogDriverType
    options: NotRequired[Mapping[str, str]]
    secretOptions: NotRequired[Sequence[SecretTypeDef]]


class ContainerInstanceHealthStatusTypeDef(TypedDict):
    overallStatus: NotRequired[InstanceHealthCheckStateType]
    details: NotRequired[list[InstanceHealthCheckResultTypeDef]]


ContainerRestartPolicyUnionTypeDef = Union[
    ContainerRestartPolicyTypeDef, ContainerRestartPolicyOutputTypeDef
]


class ContainerStateChangeTypeDef(TypedDict):
    containerName: NotRequired[str]
    imageDigest: NotRequired[str]
    runtimeId: NotRequired[str]
    exitCode: NotRequired[int]
    networkBindings: NotRequired[Sequence[NetworkBindingTypeDef]]
    reason: NotRequired[str]
    status: NotRequired[str]


class SubmitContainerStateChangeRequestRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    task: NotRequired[str]
    containerName: NotRequired[str]
    runtimeId: NotRequired[str]
    status: NotRequired[str]
    exitCode: NotRequired[int]
    reason: NotRequired[str]
    networkBindings: NotRequired[Sequence[NetworkBindingTypeDef]]


class ContainerTypeDef(TypedDict):
    containerArn: NotRequired[str]
    taskArn: NotRequired[str]
    name: NotRequired[str]
    image: NotRequired[str]
    imageDigest: NotRequired[str]
    runtimeId: NotRequired[str]
    lastStatus: NotRequired[str]
    exitCode: NotRequired[int]
    reason: NotRequired[str]
    networkBindings: NotRequired[list[NetworkBindingTypeDef]]
    networkInterfaces: NotRequired[list[NetworkInterfaceTypeDef]]
    healthStatus: NotRequired[HealthStatusType]
    managedAgents: NotRequired[list[ManagedAgentTypeDef]]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    memoryReservation: NotRequired[str]
    gpuIds: NotRequired[list[str]]


class DeleteAttributesResponseTypeDef(TypedDict):
    attributes: list[AttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DiscoverPollEndpointResponseTypeDef(TypedDict):
    endpoint: str
    telemetryEndpoint: str
    serviceConnectEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAttributesResponseTypeDef(TypedDict):
    attributes: list[AttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListClustersResponseTypeDef(TypedDict):
    clusterArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListContainerInstancesResponseTypeDef(TypedDict):
    containerInstanceArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListServicesByNamespaceResponseTypeDef(TypedDict):
    serviceArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListServicesResponseTypeDef(TypedDict):
    serviceArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListTaskDefinitionFamiliesResponseTypeDef(TypedDict):
    families: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTaskDefinitionsResponseTypeDef(TypedDict):
    taskDefinitionArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTasksResponseTypeDef(TypedDict):
    taskArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PutAttributesResponseTypeDef(TypedDict):
    attributes: list[AttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SubmitAttachmentStateChangesResponseTypeDef(TypedDict):
    acknowledgment: str
    ResponseMetadata: ResponseMetadataTypeDef


class SubmitContainerStateChangeResponseTypeDef(TypedDict):
    acknowledgment: str
    ResponseMetadata: ResponseMetadataTypeDef


class SubmitTaskStateChangeResponseTypeDef(TypedDict):
    acknowledgment: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTaskSetRequestRequestTypeDef(TypedDict):
    cluster: str
    service: str
    taskSet: str
    scale: ScaleTypeDef


class CreatedAtTypeDef(TypedDict):
    before: NotRequired[TimestampTypeDef]
    after: NotRequired[TimestampTypeDef]


class DeleteAccountSettingResponseTypeDef(TypedDict):
    setting: SettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccountSettingsResponseTypeDef(TypedDict):
    settings: list[SettingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PutAccountSettingDefaultResponseTypeDef(TypedDict):
    setting: SettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutAccountSettingResponseTypeDef(TypedDict):
    setting: SettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DeploymentAlarmsUnionTypeDef = Union[DeploymentAlarmsTypeDef, DeploymentAlarmsOutputTypeDef]


class DeploymentConfigurationOutputTypeDef(TypedDict):
    deploymentCircuitBreaker: NotRequired[DeploymentCircuitBreakerTypeDef]
    maximumPercent: NotRequired[int]
    minimumHealthyPercent: NotRequired[int]
    alarms: NotRequired[DeploymentAlarmsOutputTypeDef]


class DescribeServicesRequestWaitTypeDef(TypedDict):
    services: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeTasksRequestWaitTypeDef(TypedDict):
    tasks: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


DeviceUnionTypeDef = Union[DeviceTypeDef, DeviceOutputTypeDef]
DockerVolumeConfigurationUnionTypeDef = Union[
    DockerVolumeConfigurationTypeDef, DockerVolumeConfigurationOutputTypeDef
]


class EFSVolumeConfigurationTypeDef(TypedDict):
    fileSystemId: str
    rootDirectory: NotRequired[str]
    transitEncryption: NotRequired[EFSTransitEncryptionType]
    transitEncryptionPort: NotRequired[int]
    authorizationConfig: NotRequired[EFSAuthorizationConfigTypeDef]


class ExecuteCommandConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]
    logging: NotRequired[ExecuteCommandLoggingType]
    logConfiguration: NotRequired[ExecuteCommandLogConfigurationTypeDef]


class ExecuteCommandResponseTypeDef(TypedDict):
    clusterArn: str
    containerArn: str
    containerName: str
    interactive: bool
    session: SessionTypeDef
    taskArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class FSxWindowsFileServerVolumeConfigurationTypeDef(TypedDict):
    fileSystemId: str
    rootDirectory: str
    authorizationConfig: FSxWindowsFileServerAuthorizationConfigTypeDef


FirelensConfigurationUnionTypeDef = Union[
    FirelensConfigurationTypeDef, FirelensConfigurationOutputTypeDef
]


class GetTaskProtectionResponseTypeDef(TypedDict):
    protectedTasks: list[ProtectedTaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTaskProtectionResponseTypeDef(TypedDict):
    protectedTasks: list[ProtectedTaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


HealthCheckUnionTypeDef = Union[HealthCheckTypeDef, HealthCheckOutputTypeDef]
KernelCapabilitiesUnionTypeDef = Union[KernelCapabilitiesTypeDef, KernelCapabilitiesOutputTypeDef]


class LinuxParametersOutputTypeDef(TypedDict):
    capabilities: NotRequired[KernelCapabilitiesOutputTypeDef]
    devices: NotRequired[list[DeviceOutputTypeDef]]
    initProcessEnabled: NotRequired[bool]
    sharedMemorySize: NotRequired[int]
    tmpfs: NotRequired[list[TmpfsOutputTypeDef]]
    maxSwap: NotRequired[int]
    swappiness: NotRequired[int]


class ListAccountSettingsRequestPaginateTypeDef(TypedDict):
    name: NotRequired[SettingNameType]
    value: NotRequired[str]
    principalArn: NotRequired[str]
    effectiveSettings: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAttributesRequestPaginateTypeDef(TypedDict):
    targetType: Literal["container-instance"]
    cluster: NotRequired[str]
    attributeName: NotRequired[str]
    attributeValue: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClustersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListContainerInstancesRequestPaginateTypeDef = TypedDict(
    "ListContainerInstancesRequestPaginateTypeDef",
    {
        "cluster": NotRequired[str],
        "filter": NotRequired[str],
        "status": NotRequired[ContainerInstanceStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListServicesByNamespaceRequestPaginateTypeDef(TypedDict):
    namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServicesRequestPaginateTypeDef(TypedDict):
    cluster: NotRequired[str]
    launchType: NotRequired[LaunchTypeType]
    schedulingStrategy: NotRequired[SchedulingStrategyType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTaskDefinitionFamiliesRequestPaginateTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    status: NotRequired[TaskDefinitionFamilyStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTaskDefinitionsRequestPaginateTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    status: NotRequired[TaskDefinitionStatusType]
    sort: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTasksRequestPaginateTypeDef(TypedDict):
    cluster: NotRequired[str]
    containerInstance: NotRequired[str]
    family: NotRequired[str]
    startedBy: NotRequired[str]
    serviceName: NotRequired[str]
    desiredStatus: NotRequired[DesiredStatusType]
    launchType: NotRequired[LaunchTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListServiceDeploymentsResponseTypeDef(TypedDict):
    serviceDeployments: list[ServiceDeploymentBriefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ResourceUnionTypeDef = Union[ResourceTypeDef, ResourceOutputTypeDef]


class ServiceConnectTlsConfigurationTypeDef(TypedDict):
    issuerCertificateAuthority: ServiceConnectTlsCertificateAuthorityTypeDef
    kmsKey: NotRequired[str]
    roleArn: NotRequired[str]


TmpfsUnionTypeDef = Union[TmpfsTypeDef, TmpfsOutputTypeDef]


class CapacityProviderTypeDef(TypedDict):
    capacityProviderArn: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[CapacityProviderStatusType]
    autoScalingGroupProvider: NotRequired[AutoScalingGroupProviderTypeDef]
    updateStatus: NotRequired[CapacityProviderUpdateStatusType]
    updateStatusReason: NotRequired[str]
    tags: NotRequired[list[TagTypeDef]]


class CreateCapacityProviderRequestRequestTypeDef(TypedDict):
    name: str
    autoScalingGroupProvider: AutoScalingGroupProviderTypeDef
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateCapacityProviderRequestRequestTypeDef(TypedDict):
    name: str
    autoScalingGroupProvider: AutoScalingGroupProviderUpdateTypeDef


TaskSetTypeDef = TypedDict(
    "TaskSetTypeDef",
    {
        "id": NotRequired[str],
        "taskSetArn": NotRequired[str],
        "serviceArn": NotRequired[str],
        "clusterArn": NotRequired[str],
        "startedBy": NotRequired[str],
        "externalId": NotRequired[str],
        "status": NotRequired[str],
        "taskDefinition": NotRequired[str],
        "computedDesiredCount": NotRequired[int],
        "pendingCount": NotRequired[int],
        "runningCount": NotRequired[int],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "launchType": NotRequired[LaunchTypeType],
        "capacityProviderStrategy": NotRequired[list[CapacityProviderStrategyItemTypeDef]],
        "platformVersion": NotRequired[str],
        "platformFamily": NotRequired[str],
        "networkConfiguration": NotRequired[NetworkConfigurationOutputTypeDef],
        "loadBalancers": NotRequired[list[LoadBalancerTypeDef]],
        "serviceRegistries": NotRequired[list[ServiceRegistryTypeDef]],
        "scale": NotRequired[ScaleTypeDef],
        "stabilityStatus": NotRequired[StabilityStatusType],
        "stabilityStatusAt": NotRequired[datetime],
        "tags": NotRequired[list[TagTypeDef]],
        "fargateEphemeralStorage": NotRequired[DeploymentEphemeralStorageTypeDef],
    },
)


class NetworkConfigurationTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationUnionTypeDef]


class ServiceManagedEBSVolumeConfigurationOutputTypeDef(TypedDict):
    roleArn: str
    encrypted: NotRequired[bool]
    kmsKeyId: NotRequired[str]
    volumeType: NotRequired[str]
    sizeInGiB: NotRequired[int]
    snapshotId: NotRequired[str]
    iops: NotRequired[int]
    throughput: NotRequired[int]
    tagSpecifications: NotRequired[list[EBSTagSpecificationOutputTypeDef]]
    filesystemType: NotRequired[TaskFilesystemTypeType]


EBSTagSpecificationUnionTypeDef = Union[
    EBSTagSpecificationTypeDef, EBSTagSpecificationOutputTypeDef
]


class TaskOverrideOutputTypeDef(TypedDict):
    containerOverrides: NotRequired[list[ContainerOverrideOutputTypeDef]]
    cpu: NotRequired[str]
    inferenceAcceleratorOverrides: NotRequired[list[InferenceAcceleratorOverrideTypeDef]]
    executionRoleArn: NotRequired[str]
    memory: NotRequired[str]
    taskRoleArn: NotRequired[str]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]


ContainerOverrideUnionTypeDef = Union[ContainerOverrideTypeDef, ContainerOverrideOutputTypeDef]
LogConfigurationUnionTypeDef = Union[LogConfigurationTypeDef, LogConfigurationOutputTypeDef]


class ContainerInstanceTypeDef(TypedDict):
    containerInstanceArn: NotRequired[str]
    ec2InstanceId: NotRequired[str]
    capacityProviderName: NotRequired[str]
    version: NotRequired[int]
    versionInfo: NotRequired[VersionInfoTypeDef]
    remainingResources: NotRequired[list[ResourceOutputTypeDef]]
    registeredResources: NotRequired[list[ResourceOutputTypeDef]]
    status: NotRequired[str]
    statusReason: NotRequired[str]
    agentConnected: NotRequired[bool]
    runningTasksCount: NotRequired[int]
    pendingTasksCount: NotRequired[int]
    agentUpdateStatus: NotRequired[AgentUpdateStatusType]
    attributes: NotRequired[list[AttributeTypeDef]]
    registeredAt: NotRequired[datetime]
    attachments: NotRequired[list[AttachmentTypeDef]]
    tags: NotRequired[list[TagTypeDef]]
    healthStatus: NotRequired[ContainerInstanceHealthStatusTypeDef]


class SubmitTaskStateChangeRequestRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    task: NotRequired[str]
    status: NotRequired[str]
    reason: NotRequired[str]
    containers: NotRequired[Sequence[ContainerStateChangeTypeDef]]
    attachments: NotRequired[Sequence[AttachmentStateChangeTypeDef]]
    managedAgents: NotRequired[Sequence[ManagedAgentStateChangeTypeDef]]
    pullStartedAt: NotRequired[TimestampTypeDef]
    pullStoppedAt: NotRequired[TimestampTypeDef]
    executionStoppedAt: NotRequired[TimestampTypeDef]


class ListServiceDeploymentsRequestRequestTypeDef(TypedDict):
    service: str
    cluster: NotRequired[str]
    status: NotRequired[Sequence[ServiceDeploymentStatusType]]
    createdAt: NotRequired[CreatedAtTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class DeploymentConfigurationTypeDef(TypedDict):
    deploymentCircuitBreaker: NotRequired[DeploymentCircuitBreakerTypeDef]
    maximumPercent: NotRequired[int]
    minimumHealthyPercent: NotRequired[int]
    alarms: NotRequired[DeploymentAlarmsUnionTypeDef]


class ServiceDeploymentTypeDef(TypedDict):
    serviceDeploymentArn: NotRequired[str]
    serviceArn: NotRequired[str]
    clusterArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    finishedAt: NotRequired[datetime]
    stoppedAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    sourceServiceRevisions: NotRequired[list[ServiceRevisionSummaryTypeDef]]
    targetServiceRevision: NotRequired[ServiceRevisionSummaryTypeDef]
    status: NotRequired[ServiceDeploymentStatusType]
    statusReason: NotRequired[str]
    deploymentConfiguration: NotRequired[DeploymentConfigurationOutputTypeDef]
    rollback: NotRequired[RollbackTypeDef]
    deploymentCircuitBreaker: NotRequired[ServiceDeploymentCircuitBreakerTypeDef]
    alarms: NotRequired[ServiceDeploymentAlarmsTypeDef]


class ClusterConfigurationTypeDef(TypedDict):
    executeCommandConfiguration: NotRequired[ExecuteCommandConfigurationTypeDef]
    managedStorageConfiguration: NotRequired[ManagedStorageConfigurationTypeDef]


class VolumeOutputTypeDef(TypedDict):
    name: NotRequired[str]
    host: NotRequired[HostVolumePropertiesTypeDef]
    dockerVolumeConfiguration: NotRequired[DockerVolumeConfigurationOutputTypeDef]
    efsVolumeConfiguration: NotRequired[EFSVolumeConfigurationTypeDef]
    fsxWindowsFileServerVolumeConfiguration: NotRequired[
        FSxWindowsFileServerVolumeConfigurationTypeDef
    ]
    configuredAtLaunch: NotRequired[bool]


class VolumeTypeDef(TypedDict):
    name: NotRequired[str]
    host: NotRequired[HostVolumePropertiesTypeDef]
    dockerVolumeConfiguration: NotRequired[DockerVolumeConfigurationUnionTypeDef]
    efsVolumeConfiguration: NotRequired[EFSVolumeConfigurationTypeDef]
    fsxWindowsFileServerVolumeConfiguration: NotRequired[
        FSxWindowsFileServerVolumeConfigurationTypeDef
    ]
    configuredAtLaunch: NotRequired[bool]


class ContainerDefinitionOutputTypeDef(TypedDict):
    name: NotRequired[str]
    image: NotRequired[str]
    repositoryCredentials: NotRequired[RepositoryCredentialsTypeDef]
    cpu: NotRequired[int]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    links: NotRequired[list[str]]
    portMappings: NotRequired[list[PortMappingTypeDef]]
    essential: NotRequired[bool]
    restartPolicy: NotRequired[ContainerRestartPolicyOutputTypeDef]
    entryPoint: NotRequired[list[str]]
    command: NotRequired[list[str]]
    environment: NotRequired[list[KeyValuePairTypeDef]]
    environmentFiles: NotRequired[list[EnvironmentFileTypeDef]]
    mountPoints: NotRequired[list[MountPointTypeDef]]
    volumesFrom: NotRequired[list[VolumeFromTypeDef]]
    linuxParameters: NotRequired[LinuxParametersOutputTypeDef]
    secrets: NotRequired[list[SecretTypeDef]]
    dependsOn: NotRequired[list[ContainerDependencyTypeDef]]
    startTimeout: NotRequired[int]
    stopTimeout: NotRequired[int]
    versionConsistency: NotRequired[VersionConsistencyType]
    hostname: NotRequired[str]
    user: NotRequired[str]
    workingDirectory: NotRequired[str]
    disableNetworking: NotRequired[bool]
    privileged: NotRequired[bool]
    readonlyRootFilesystem: NotRequired[bool]
    dnsServers: NotRequired[list[str]]
    dnsSearchDomains: NotRequired[list[str]]
    extraHosts: NotRequired[list[HostEntryTypeDef]]
    dockerSecurityOptions: NotRequired[list[str]]
    interactive: NotRequired[bool]
    pseudoTerminal: NotRequired[bool]
    dockerLabels: NotRequired[dict[str, str]]
    ulimits: NotRequired[list[UlimitTypeDef]]
    logConfiguration: NotRequired[LogConfigurationOutputTypeDef]
    healthCheck: NotRequired[HealthCheckOutputTypeDef]
    systemControls: NotRequired[list[SystemControlTypeDef]]
    resourceRequirements: NotRequired[list[ResourceRequirementTypeDef]]
    firelensConfiguration: NotRequired[FirelensConfigurationOutputTypeDef]
    credentialSpecs: NotRequired[list[str]]


class RegisterContainerInstanceRequestRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    instanceIdentityDocument: NotRequired[str]
    instanceIdentityDocumentSignature: NotRequired[str]
    totalResources: NotRequired[Sequence[ResourceUnionTypeDef]]
    versionInfo: NotRequired[VersionInfoTypeDef]
    containerInstanceArn: NotRequired[str]
    attributes: NotRequired[Sequence[AttributeTypeDef]]
    platformDevices: NotRequired[Sequence[PlatformDeviceTypeDef]]
    tags: NotRequired[Sequence[TagTypeDef]]


class ServiceConnectServiceOutputTypeDef(TypedDict):
    portName: str
    discoveryName: NotRequired[str]
    clientAliases: NotRequired[list[ServiceConnectClientAliasTypeDef]]
    ingressPortOverride: NotRequired[int]
    timeout: NotRequired[TimeoutConfigurationTypeDef]
    tls: NotRequired[ServiceConnectTlsConfigurationTypeDef]


class ServiceConnectServiceTypeDef(TypedDict):
    portName: str
    discoveryName: NotRequired[str]
    clientAliases: NotRequired[Sequence[ServiceConnectClientAliasTypeDef]]
    ingressPortOverride: NotRequired[int]
    timeout: NotRequired[TimeoutConfigurationTypeDef]
    tls: NotRequired[ServiceConnectTlsConfigurationTypeDef]


class LinuxParametersTypeDef(TypedDict):
    capabilities: NotRequired[KernelCapabilitiesUnionTypeDef]
    devices: NotRequired[Sequence[DeviceUnionTypeDef]]
    initProcessEnabled: NotRequired[bool]
    sharedMemorySize: NotRequired[int]
    tmpfs: NotRequired[Sequence[TmpfsUnionTypeDef]]
    maxSwap: NotRequired[int]
    swappiness: NotRequired[int]


class CreateCapacityProviderResponseTypeDef(TypedDict):
    capacityProvider: CapacityProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCapacityProviderResponseTypeDef(TypedDict):
    capacityProvider: CapacityProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCapacityProvidersResponseTypeDef(TypedDict):
    capacityProviders: list[CapacityProviderTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateCapacityProviderResponseTypeDef(TypedDict):
    capacityProvider: CapacityProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTaskSetResponseTypeDef(TypedDict):
    taskSet: TaskSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTaskSetResponseTypeDef(TypedDict):
    taskSet: TaskSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTaskSetsResponseTypeDef(TypedDict):
    taskSets: list[TaskSetTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateServicePrimaryTaskSetResponseTypeDef(TypedDict):
    taskSet: TaskSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTaskSetResponseTypeDef(TypedDict):
    taskSet: TaskSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTaskSetRequestRequestTypeDef(TypedDict):
    service: str
    cluster: str
    taskDefinition: str
    externalId: NotRequired[str]
    networkConfiguration: NotRequired[NetworkConfigurationTypeDef]
    loadBalancers: NotRequired[Sequence[LoadBalancerTypeDef]]
    serviceRegistries: NotRequired[Sequence[ServiceRegistryTypeDef]]
    launchType: NotRequired[LaunchTypeType]
    capacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    platformVersion: NotRequired[str]
    scale: NotRequired[ScaleTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class ServiceVolumeConfigurationOutputTypeDef(TypedDict):
    name: str
    managedEBSVolume: NotRequired[ServiceManagedEBSVolumeConfigurationOutputTypeDef]


class ServiceManagedEBSVolumeConfigurationTypeDef(TypedDict):
    roleArn: str
    encrypted: NotRequired[bool]
    kmsKeyId: NotRequired[str]
    volumeType: NotRequired[str]
    sizeInGiB: NotRequired[int]
    snapshotId: NotRequired[str]
    iops: NotRequired[int]
    throughput: NotRequired[int]
    tagSpecifications: NotRequired[Sequence[EBSTagSpecificationUnionTypeDef]]
    filesystemType: NotRequired[TaskFilesystemTypeType]


class TaskManagedEBSVolumeConfigurationTypeDef(TypedDict):
    roleArn: str
    encrypted: NotRequired[bool]
    kmsKeyId: NotRequired[str]
    volumeType: NotRequired[str]
    sizeInGiB: NotRequired[int]
    snapshotId: NotRequired[str]
    iops: NotRequired[int]
    throughput: NotRequired[int]
    tagSpecifications: NotRequired[Sequence[EBSTagSpecificationUnionTypeDef]]
    terminationPolicy: NotRequired[TaskManagedEBSVolumeTerminationPolicyTypeDef]
    filesystemType: NotRequired[TaskFilesystemTypeType]


class TaskTypeDef(TypedDict):
    attachments: NotRequired[list[AttachmentTypeDef]]
    attributes: NotRequired[list[AttributeTypeDef]]
    availabilityZone: NotRequired[str]
    capacityProviderName: NotRequired[str]
    clusterArn: NotRequired[str]
    connectivity: NotRequired[ConnectivityType]
    connectivityAt: NotRequired[datetime]
    containerInstanceArn: NotRequired[str]
    containers: NotRequired[list[ContainerTypeDef]]
    cpu: NotRequired[str]
    createdAt: NotRequired[datetime]
    desiredStatus: NotRequired[str]
    enableExecuteCommand: NotRequired[bool]
    executionStoppedAt: NotRequired[datetime]
    group: NotRequired[str]
    healthStatus: NotRequired[HealthStatusType]
    inferenceAccelerators: NotRequired[list[InferenceAcceleratorTypeDef]]
    lastStatus: NotRequired[str]
    launchType: NotRequired[LaunchTypeType]
    memory: NotRequired[str]
    overrides: NotRequired[TaskOverrideOutputTypeDef]
    platformVersion: NotRequired[str]
    platformFamily: NotRequired[str]
    pullStartedAt: NotRequired[datetime]
    pullStoppedAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    startedBy: NotRequired[str]
    stopCode: NotRequired[TaskStopCodeType]
    stoppedAt: NotRequired[datetime]
    stoppedReason: NotRequired[str]
    stoppingAt: NotRequired[datetime]
    tags: NotRequired[list[TagTypeDef]]
    taskArn: NotRequired[str]
    taskDefinitionArn: NotRequired[str]
    version: NotRequired[int]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]
    fargateEphemeralStorage: NotRequired[TaskEphemeralStorageTypeDef]


class TaskOverrideTypeDef(TypedDict):
    containerOverrides: NotRequired[Sequence[ContainerOverrideUnionTypeDef]]
    cpu: NotRequired[str]
    inferenceAcceleratorOverrides: NotRequired[Sequence[InferenceAcceleratorOverrideTypeDef]]
    executionRoleArn: NotRequired[str]
    memory: NotRequired[str]
    taskRoleArn: NotRequired[str]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]


class DeregisterContainerInstanceResponseTypeDef(TypedDict):
    containerInstance: ContainerInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeContainerInstancesResponseTypeDef(TypedDict):
    containerInstances: list[ContainerInstanceTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterContainerInstanceResponseTypeDef(TypedDict):
    containerInstance: ContainerInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContainerAgentResponseTypeDef(TypedDict):
    containerInstance: ContainerInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContainerInstancesStateResponseTypeDef(TypedDict):
    containerInstances: list[ContainerInstanceTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeServiceDeploymentsResponseTypeDef(TypedDict):
    serviceDeployments: list[ServiceDeploymentTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ClusterTypeDef(TypedDict):
    clusterArn: NotRequired[str]
    clusterName: NotRequired[str]
    configuration: NotRequired[ClusterConfigurationTypeDef]
    status: NotRequired[str]
    registeredContainerInstancesCount: NotRequired[int]
    runningTasksCount: NotRequired[int]
    pendingTasksCount: NotRequired[int]
    activeServicesCount: NotRequired[int]
    statistics: NotRequired[list[KeyValuePairTypeDef]]
    tags: NotRequired[list[TagTypeDef]]
    settings: NotRequired[list[ClusterSettingTypeDef]]
    capacityProviders: NotRequired[list[str]]
    defaultCapacityProviderStrategy: NotRequired[list[CapacityProviderStrategyItemTypeDef]]
    attachments: NotRequired[list[AttachmentTypeDef]]
    attachmentsStatus: NotRequired[str]
    serviceConnectDefaults: NotRequired[ClusterServiceConnectDefaultsTypeDef]


class CreateClusterRequestRequestTypeDef(TypedDict):
    clusterName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    settings: NotRequired[Sequence[ClusterSettingTypeDef]]
    configuration: NotRequired[ClusterConfigurationTypeDef]
    capacityProviders: NotRequired[Sequence[str]]
    defaultCapacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    serviceConnectDefaults: NotRequired[ClusterServiceConnectDefaultsRequestTypeDef]


class UpdateClusterRequestRequestTypeDef(TypedDict):
    cluster: str
    settings: NotRequired[Sequence[ClusterSettingTypeDef]]
    configuration: NotRequired[ClusterConfigurationTypeDef]
    serviceConnectDefaults: NotRequired[ClusterServiceConnectDefaultsRequestTypeDef]


VolumeUnionTypeDef = Union[VolumeTypeDef, VolumeOutputTypeDef]


class TaskDefinitionTypeDef(TypedDict):
    taskDefinitionArn: NotRequired[str]
    containerDefinitions: NotRequired[list[ContainerDefinitionOutputTypeDef]]
    family: NotRequired[str]
    taskRoleArn: NotRequired[str]
    executionRoleArn: NotRequired[str]
    networkMode: NotRequired[NetworkModeType]
    revision: NotRequired[int]
    volumes: NotRequired[list[VolumeOutputTypeDef]]
    status: NotRequired[TaskDefinitionStatusType]
    requiresAttributes: NotRequired[list[AttributeTypeDef]]
    placementConstraints: NotRequired[list[TaskDefinitionPlacementConstraintTypeDef]]
    compatibilities: NotRequired[list[CompatibilityType]]
    runtimePlatform: NotRequired[RuntimePlatformTypeDef]
    requiresCompatibilities: NotRequired[list[CompatibilityType]]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    inferenceAccelerators: NotRequired[list[InferenceAcceleratorTypeDef]]
    pidMode: NotRequired[PidModeType]
    ipcMode: NotRequired[IpcModeType]
    proxyConfiguration: NotRequired[ProxyConfigurationOutputTypeDef]
    registeredAt: NotRequired[datetime]
    deregisteredAt: NotRequired[datetime]
    registeredBy: NotRequired[str]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]
    enableFaultInjection: NotRequired[bool]


class ServiceConnectConfigurationOutputTypeDef(TypedDict):
    enabled: bool
    namespace: NotRequired[str]
    services: NotRequired[list[ServiceConnectServiceOutputTypeDef]]
    logConfiguration: NotRequired[LogConfigurationOutputTypeDef]


ServiceConnectServiceUnionTypeDef = Union[
    ServiceConnectServiceTypeDef, ServiceConnectServiceOutputTypeDef
]
LinuxParametersUnionTypeDef = Union[LinuxParametersTypeDef, LinuxParametersOutputTypeDef]
ServiceManagedEBSVolumeConfigurationUnionTypeDef = Union[
    ServiceManagedEBSVolumeConfigurationTypeDef, ServiceManagedEBSVolumeConfigurationOutputTypeDef
]


class TaskVolumeConfigurationTypeDef(TypedDict):
    name: str
    managedEBSVolume: NotRequired[TaskManagedEBSVolumeConfigurationTypeDef]


class DescribeTasksResponseTypeDef(TypedDict):
    tasks: list[TaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RunTaskResponseTypeDef(TypedDict):
    tasks: list[TaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartTaskResponseTypeDef(TypedDict):
    tasks: list[TaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StopTaskResponseTypeDef(TypedDict):
    task: TaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClustersResponseTypeDef(TypedDict):
    clusters: list[ClusterTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutClusterCapacityProvidersResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterSettingsResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTaskDefinitionsResponseTypeDef(TypedDict):
    taskDefinitions: list[TaskDefinitionTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeregisterTaskDefinitionResponseTypeDef(TypedDict):
    taskDefinition: TaskDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTaskDefinitionResponseTypeDef(TypedDict):
    taskDefinition: TaskDefinitionTypeDef
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterTaskDefinitionResponseTypeDef(TypedDict):
    taskDefinition: TaskDefinitionTypeDef
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "id": NotRequired[str],
        "status": NotRequired[str],
        "taskDefinition": NotRequired[str],
        "desiredCount": NotRequired[int],
        "pendingCount": NotRequired[int],
        "runningCount": NotRequired[int],
        "failedTasks": NotRequired[int],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "capacityProviderStrategy": NotRequired[list[CapacityProviderStrategyItemTypeDef]],
        "launchType": NotRequired[LaunchTypeType],
        "platformVersion": NotRequired[str],
        "platformFamily": NotRequired[str],
        "networkConfiguration": NotRequired[NetworkConfigurationOutputTypeDef],
        "rolloutState": NotRequired[DeploymentRolloutStateType],
        "rolloutStateReason": NotRequired[str],
        "serviceConnectConfiguration": NotRequired[ServiceConnectConfigurationOutputTypeDef],
        "serviceConnectResources": NotRequired[list[ServiceConnectServiceResourceTypeDef]],
        "volumeConfigurations": NotRequired[list[ServiceVolumeConfigurationOutputTypeDef]],
        "fargateEphemeralStorage": NotRequired[DeploymentEphemeralStorageTypeDef],
        "vpcLatticeConfigurations": NotRequired[list[VpcLatticeConfigurationTypeDef]],
    },
)


class ServiceRevisionTypeDef(TypedDict):
    serviceRevisionArn: NotRequired[str]
    serviceArn: NotRequired[str]
    clusterArn: NotRequired[str]
    taskDefinition: NotRequired[str]
    capacityProviderStrategy: NotRequired[list[CapacityProviderStrategyItemTypeDef]]
    launchType: NotRequired[LaunchTypeType]
    platformVersion: NotRequired[str]
    platformFamily: NotRequired[str]
    loadBalancers: NotRequired[list[LoadBalancerTypeDef]]
    serviceRegistries: NotRequired[list[ServiceRegistryTypeDef]]
    networkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    containerImages: NotRequired[list[ContainerImageTypeDef]]
    guardDutyEnabled: NotRequired[bool]
    serviceConnectConfiguration: NotRequired[ServiceConnectConfigurationOutputTypeDef]
    volumeConfigurations: NotRequired[list[ServiceVolumeConfigurationOutputTypeDef]]
    fargateEphemeralStorage: NotRequired[DeploymentEphemeralStorageTypeDef]
    createdAt: NotRequired[datetime]
    vpcLatticeConfigurations: NotRequired[list[VpcLatticeConfigurationTypeDef]]


class ServiceConnectConfigurationTypeDef(TypedDict):
    enabled: bool
    namespace: NotRequired[str]
    services: NotRequired[Sequence[ServiceConnectServiceUnionTypeDef]]
    logConfiguration: NotRequired[LogConfigurationUnionTypeDef]


class ContainerDefinitionTypeDef(TypedDict):
    name: NotRequired[str]
    image: NotRequired[str]
    repositoryCredentials: NotRequired[RepositoryCredentialsTypeDef]
    cpu: NotRequired[int]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    links: NotRequired[Sequence[str]]
    portMappings: NotRequired[Sequence[PortMappingTypeDef]]
    essential: NotRequired[bool]
    restartPolicy: NotRequired[ContainerRestartPolicyUnionTypeDef]
    entryPoint: NotRequired[Sequence[str]]
    command: NotRequired[Sequence[str]]
    environment: NotRequired[Sequence[KeyValuePairTypeDef]]
    environmentFiles: NotRequired[Sequence[EnvironmentFileTypeDef]]
    mountPoints: NotRequired[Sequence[MountPointTypeDef]]
    volumesFrom: NotRequired[Sequence[VolumeFromTypeDef]]
    linuxParameters: NotRequired[LinuxParametersUnionTypeDef]
    secrets: NotRequired[Sequence[SecretTypeDef]]
    dependsOn: NotRequired[Sequence[ContainerDependencyTypeDef]]
    startTimeout: NotRequired[int]
    stopTimeout: NotRequired[int]
    versionConsistency: NotRequired[VersionConsistencyType]
    hostname: NotRequired[str]
    user: NotRequired[str]
    workingDirectory: NotRequired[str]
    disableNetworking: NotRequired[bool]
    privileged: NotRequired[bool]
    readonlyRootFilesystem: NotRequired[bool]
    dnsServers: NotRequired[Sequence[str]]
    dnsSearchDomains: NotRequired[Sequence[str]]
    extraHosts: NotRequired[Sequence[HostEntryTypeDef]]
    dockerSecurityOptions: NotRequired[Sequence[str]]
    interactive: NotRequired[bool]
    pseudoTerminal: NotRequired[bool]
    dockerLabels: NotRequired[Mapping[str, str]]
    ulimits: NotRequired[Sequence[UlimitTypeDef]]
    logConfiguration: NotRequired[LogConfigurationUnionTypeDef]
    healthCheck: NotRequired[HealthCheckUnionTypeDef]
    systemControls: NotRequired[Sequence[SystemControlTypeDef]]
    resourceRequirements: NotRequired[Sequence[ResourceRequirementTypeDef]]
    firelensConfiguration: NotRequired[FirelensConfigurationUnionTypeDef]
    credentialSpecs: NotRequired[Sequence[str]]


class ServiceVolumeConfigurationTypeDef(TypedDict):
    name: str
    managedEBSVolume: NotRequired[ServiceManagedEBSVolumeConfigurationUnionTypeDef]


class RunTaskRequestRequestTypeDef(TypedDict):
    taskDefinition: str
    capacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    cluster: NotRequired[str]
    count: NotRequired[int]
    enableECSManagedTags: NotRequired[bool]
    enableExecuteCommand: NotRequired[bool]
    group: NotRequired[str]
    launchType: NotRequired[LaunchTypeType]
    networkConfiguration: NotRequired[NetworkConfigurationTypeDef]
    overrides: NotRequired[TaskOverrideTypeDef]
    placementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    placementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    platformVersion: NotRequired[str]
    propagateTags: NotRequired[PropagateTagsType]
    referenceId: NotRequired[str]
    startedBy: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientToken: NotRequired[str]
    volumeConfigurations: NotRequired[Sequence[TaskVolumeConfigurationTypeDef]]


class StartTaskRequestRequestTypeDef(TypedDict):
    containerInstances: Sequence[str]
    taskDefinition: str
    cluster: NotRequired[str]
    enableECSManagedTags: NotRequired[bool]
    enableExecuteCommand: NotRequired[bool]
    group: NotRequired[str]
    networkConfiguration: NotRequired[NetworkConfigurationTypeDef]
    overrides: NotRequired[TaskOverrideTypeDef]
    propagateTags: NotRequired[PropagateTagsType]
    referenceId: NotRequired[str]
    startedBy: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    volumeConfigurations: NotRequired[Sequence[TaskVolumeConfigurationTypeDef]]


class ServiceTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    serviceName: NotRequired[str]
    clusterArn: NotRequired[str]
    loadBalancers: NotRequired[list[LoadBalancerTypeDef]]
    serviceRegistries: NotRequired[list[ServiceRegistryTypeDef]]
    status: NotRequired[str]
    desiredCount: NotRequired[int]
    runningCount: NotRequired[int]
    pendingCount: NotRequired[int]
    launchType: NotRequired[LaunchTypeType]
    capacityProviderStrategy: NotRequired[list[CapacityProviderStrategyItemTypeDef]]
    platformVersion: NotRequired[str]
    platformFamily: NotRequired[str]
    taskDefinition: NotRequired[str]
    deploymentConfiguration: NotRequired[DeploymentConfigurationOutputTypeDef]
    taskSets: NotRequired[list[TaskSetTypeDef]]
    deployments: NotRequired[list[DeploymentTypeDef]]
    roleArn: NotRequired[str]
    events: NotRequired[list[ServiceEventTypeDef]]
    createdAt: NotRequired[datetime]
    placementConstraints: NotRequired[list[PlacementConstraintTypeDef]]
    placementStrategy: NotRequired[list[PlacementStrategyTypeDef]]
    networkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    healthCheckGracePeriodSeconds: NotRequired[int]
    schedulingStrategy: NotRequired[SchedulingStrategyType]
    deploymentController: NotRequired[DeploymentControllerTypeDef]
    tags: NotRequired[list[TagTypeDef]]
    createdBy: NotRequired[str]
    enableECSManagedTags: NotRequired[bool]
    propagateTags: NotRequired[PropagateTagsType]
    enableExecuteCommand: NotRequired[bool]
    availabilityZoneRebalancing: NotRequired[AvailabilityZoneRebalancingType]


class DescribeServiceRevisionsResponseTypeDef(TypedDict):
    serviceRevisions: list[ServiceRevisionTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


ContainerDefinitionUnionTypeDef = Union[
    ContainerDefinitionTypeDef, ContainerDefinitionOutputTypeDef
]
ServiceVolumeConfigurationUnionTypeDef = Union[
    ServiceVolumeConfigurationTypeDef, ServiceVolumeConfigurationOutputTypeDef
]


class UpdateServiceRequestRequestTypeDef(TypedDict):
    service: str
    cluster: NotRequired[str]
    desiredCount: NotRequired[int]
    taskDefinition: NotRequired[str]
    capacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    deploymentConfiguration: NotRequired[DeploymentConfigurationTypeDef]
    availabilityZoneRebalancing: NotRequired[AvailabilityZoneRebalancingType]
    networkConfiguration: NotRequired[NetworkConfigurationTypeDef]
    placementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    placementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    platformVersion: NotRequired[str]
    forceNewDeployment: NotRequired[bool]
    healthCheckGracePeriodSeconds: NotRequired[int]
    enableExecuteCommand: NotRequired[bool]
    enableECSManagedTags: NotRequired[bool]
    loadBalancers: NotRequired[Sequence[LoadBalancerTypeDef]]
    propagateTags: NotRequired[PropagateTagsType]
    serviceRegistries: NotRequired[Sequence[ServiceRegistryTypeDef]]
    serviceConnectConfiguration: NotRequired[ServiceConnectConfigurationTypeDef]
    volumeConfigurations: NotRequired[Sequence[ServiceVolumeConfigurationTypeDef]]
    vpcLatticeConfigurations: NotRequired[Sequence[VpcLatticeConfigurationTypeDef]]


class CreateServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeServicesResponseTypeDef(TypedDict):
    services: list[ServiceTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterTaskDefinitionRequestRequestTypeDef(TypedDict):
    family: str
    containerDefinitions: Sequence[ContainerDefinitionUnionTypeDef]
    taskRoleArn: NotRequired[str]
    executionRoleArn: NotRequired[str]
    networkMode: NotRequired[NetworkModeType]
    volumes: NotRequired[Sequence[VolumeUnionTypeDef]]
    placementConstraints: NotRequired[Sequence[TaskDefinitionPlacementConstraintTypeDef]]
    requiresCompatibilities: NotRequired[Sequence[CompatibilityType]]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    pidMode: NotRequired[PidModeType]
    ipcMode: NotRequired[IpcModeType]
    proxyConfiguration: NotRequired[ProxyConfigurationTypeDef]
    inferenceAccelerators: NotRequired[Sequence[InferenceAcceleratorTypeDef]]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]
    runtimePlatform: NotRequired[RuntimePlatformTypeDef]
    enableFaultInjection: NotRequired[bool]


class CreateServiceRequestRequestTypeDef(TypedDict):
    serviceName: str
    cluster: NotRequired[str]
    taskDefinition: NotRequired[str]
    availabilityZoneRebalancing: NotRequired[AvailabilityZoneRebalancingType]
    loadBalancers: NotRequired[Sequence[LoadBalancerTypeDef]]
    serviceRegistries: NotRequired[Sequence[ServiceRegistryTypeDef]]
    desiredCount: NotRequired[int]
    clientToken: NotRequired[str]
    launchType: NotRequired[LaunchTypeType]
    capacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    platformVersion: NotRequired[str]
    role: NotRequired[str]
    deploymentConfiguration: NotRequired[DeploymentConfigurationTypeDef]
    placementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    placementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    networkConfiguration: NotRequired[NetworkConfigurationTypeDef]
    healthCheckGracePeriodSeconds: NotRequired[int]
    schedulingStrategy: NotRequired[SchedulingStrategyType]
    deploymentController: NotRequired[DeploymentControllerTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    enableECSManagedTags: NotRequired[bool]
    propagateTags: NotRequired[PropagateTagsType]
    enableExecuteCommand: NotRequired[bool]
    serviceConnectConfiguration: NotRequired[ServiceConnectConfigurationTypeDef]
    volumeConfigurations: NotRequired[Sequence[ServiceVolumeConfigurationUnionTypeDef]]
    vpcLatticeConfigurations: NotRequired[Sequence[VpcLatticeConfigurationTypeDef]]
