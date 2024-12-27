"""
Type annotations for backup-gateway service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup_gateway/type_defs/)

Usage::

    ```python
    from mypy_boto3_backup_gateway.type_defs import AssociateGatewayToServerInputRequestTypeDef

    data: AssociateGatewayToServerInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Sequence, Union

from .literals import HypervisorStateType, SyncMetadataStatusType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AssociateGatewayToServerInputRequestTypeDef",
    "AssociateGatewayToServerOutputTypeDef",
    "BandwidthRateLimitIntervalOutputTypeDef",
    "BandwidthRateLimitIntervalTypeDef",
    "BandwidthRateLimitIntervalUnionTypeDef",
    "CreateGatewayInputRequestTypeDef",
    "CreateGatewayOutputTypeDef",
    "DeleteGatewayInputRequestTypeDef",
    "DeleteGatewayOutputTypeDef",
    "DeleteHypervisorInputRequestTypeDef",
    "DeleteHypervisorOutputTypeDef",
    "DisassociateGatewayFromServerInputRequestTypeDef",
    "DisassociateGatewayFromServerOutputTypeDef",
    "GatewayDetailsTypeDef",
    "GatewayTypeDef",
    "GetBandwidthRateLimitScheduleInputRequestTypeDef",
    "GetBandwidthRateLimitScheduleOutputTypeDef",
    "GetGatewayInputRequestTypeDef",
    "GetGatewayOutputTypeDef",
    "GetHypervisorInputRequestTypeDef",
    "GetHypervisorOutputTypeDef",
    "GetHypervisorPropertyMappingsInputRequestTypeDef",
    "GetHypervisorPropertyMappingsOutputTypeDef",
    "GetVirtualMachineInputRequestTypeDef",
    "GetVirtualMachineOutputTypeDef",
    "HypervisorDetailsTypeDef",
    "HypervisorTypeDef",
    "ImportHypervisorConfigurationInputRequestTypeDef",
    "ImportHypervisorConfigurationOutputTypeDef",
    "ListGatewaysInputPaginateTypeDef",
    "ListGatewaysInputRequestTypeDef",
    "ListGatewaysOutputTypeDef",
    "ListHypervisorsInputPaginateTypeDef",
    "ListHypervisorsInputRequestTypeDef",
    "ListHypervisorsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListVirtualMachinesInputPaginateTypeDef",
    "ListVirtualMachinesInputRequestTypeDef",
    "ListVirtualMachinesOutputTypeDef",
    "MaintenanceStartTimeTypeDef",
    "PaginatorConfigTypeDef",
    "PutBandwidthRateLimitScheduleInputRequestTypeDef",
    "PutBandwidthRateLimitScheduleOutputTypeDef",
    "PutHypervisorPropertyMappingsInputRequestTypeDef",
    "PutHypervisorPropertyMappingsOutputTypeDef",
    "PutMaintenanceStartTimeInputRequestTypeDef",
    "PutMaintenanceStartTimeOutputTypeDef",
    "ResponseMetadataTypeDef",
    "StartVirtualMachinesMetadataSyncInputRequestTypeDef",
    "StartVirtualMachinesMetadataSyncOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "TagResourceOutputTypeDef",
    "TagTypeDef",
    "TestHypervisorConfigurationInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UntagResourceOutputTypeDef",
    "UpdateGatewayInformationInputRequestTypeDef",
    "UpdateGatewayInformationOutputTypeDef",
    "UpdateGatewaySoftwareNowInputRequestTypeDef",
    "UpdateGatewaySoftwareNowOutputTypeDef",
    "UpdateHypervisorInputRequestTypeDef",
    "UpdateHypervisorOutputTypeDef",
    "VirtualMachineDetailsTypeDef",
    "VirtualMachineTypeDef",
    "VmwareTagTypeDef",
    "VmwareToAwsTagMappingTypeDef",
)


class AssociateGatewayToServerInputRequestTypeDef(TypedDict):
    GatewayArn: str
    ServerArn: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class BandwidthRateLimitIntervalOutputTypeDef(TypedDict):
    DaysOfWeek: list[int]
    EndHourOfDay: int
    EndMinuteOfHour: int
    StartHourOfDay: int
    StartMinuteOfHour: int
    AverageUploadRateLimitInBitsPerSec: NotRequired[int]


class BandwidthRateLimitIntervalTypeDef(TypedDict):
    DaysOfWeek: Sequence[int]
    EndHourOfDay: int
    EndMinuteOfHour: int
    StartHourOfDay: int
    StartMinuteOfHour: int
    AverageUploadRateLimitInBitsPerSec: NotRequired[int]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class DeleteGatewayInputRequestTypeDef(TypedDict):
    GatewayArn: str


class DeleteHypervisorInputRequestTypeDef(TypedDict):
    HypervisorArn: str


class DisassociateGatewayFromServerInputRequestTypeDef(TypedDict):
    GatewayArn: str


class MaintenanceStartTimeTypeDef(TypedDict):
    HourOfDay: int
    MinuteOfHour: int
    DayOfMonth: NotRequired[int]
    DayOfWeek: NotRequired[int]


class GatewayTypeDef(TypedDict):
    GatewayArn: NotRequired[str]
    GatewayDisplayName: NotRequired[str]
    GatewayType: NotRequired[Literal["BACKUP_VM"]]
    HypervisorId: NotRequired[str]
    LastSeenTime: NotRequired[datetime]


class GetBandwidthRateLimitScheduleInputRequestTypeDef(TypedDict):
    GatewayArn: str


class GetGatewayInputRequestTypeDef(TypedDict):
    GatewayArn: str


class GetHypervisorInputRequestTypeDef(TypedDict):
    HypervisorArn: str


class HypervisorDetailsTypeDef(TypedDict):
    Host: NotRequired[str]
    HypervisorArn: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    LastSuccessfulMetadataSyncTime: NotRequired[datetime]
    LatestMetadataSyncStatus: NotRequired[SyncMetadataStatusType]
    LatestMetadataSyncStatusMessage: NotRequired[str]
    LogGroupArn: NotRequired[str]
    Name: NotRequired[str]
    State: NotRequired[HypervisorStateType]


class GetHypervisorPropertyMappingsInputRequestTypeDef(TypedDict):
    HypervisorArn: str


class VmwareToAwsTagMappingTypeDef(TypedDict):
    AwsTagKey: str
    AwsTagValue: str
    VmwareCategory: str
    VmwareTagName: str


class GetVirtualMachineInputRequestTypeDef(TypedDict):
    ResourceArn: str


class HypervisorTypeDef(TypedDict):
    Host: NotRequired[str]
    HypervisorArn: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    Name: NotRequired[str]
    State: NotRequired[HypervisorStateType]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListGatewaysInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListHypervisorsInputRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    ResourceArn: str


class ListVirtualMachinesInputRequestTypeDef(TypedDict):
    HypervisorArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class VirtualMachineTypeDef(TypedDict):
    HostName: NotRequired[str]
    HypervisorId: NotRequired[str]
    LastBackupDate: NotRequired[datetime]
    Name: NotRequired[str]
    Path: NotRequired[str]
    ResourceArn: NotRequired[str]


class PutMaintenanceStartTimeInputRequestTypeDef(TypedDict):
    GatewayArn: str
    HourOfDay: int
    MinuteOfHour: int
    DayOfMonth: NotRequired[int]
    DayOfWeek: NotRequired[int]


class StartVirtualMachinesMetadataSyncInputRequestTypeDef(TypedDict):
    HypervisorArn: str


class TestHypervisorConfigurationInputRequestTypeDef(TypedDict):
    GatewayArn: str
    Host: str
    Password: NotRequired[str]
    Username: NotRequired[str]


class UntagResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


class UpdateGatewayInformationInputRequestTypeDef(TypedDict):
    GatewayArn: str
    GatewayDisplayName: NotRequired[str]


class UpdateGatewaySoftwareNowInputRequestTypeDef(TypedDict):
    GatewayArn: str


class UpdateHypervisorInputRequestTypeDef(TypedDict):
    HypervisorArn: str
    Host: NotRequired[str]
    LogGroupArn: NotRequired[str]
    Name: NotRequired[str]
    Password: NotRequired[str]
    Username: NotRequired[str]


class VmwareTagTypeDef(TypedDict):
    VmwareCategory: NotRequired[str]
    VmwareTagDescription: NotRequired[str]
    VmwareTagName: NotRequired[str]


class AssociateGatewayToServerOutputTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGatewayOutputTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGatewayOutputTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteHypervisorOutputTypeDef(TypedDict):
    HypervisorArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateGatewayFromServerOutputTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ImportHypervisorConfigurationOutputTypeDef(TypedDict):
    HypervisorArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutBandwidthRateLimitScheduleOutputTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutHypervisorPropertyMappingsOutputTypeDef(TypedDict):
    HypervisorArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class PutMaintenanceStartTimeOutputTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartVirtualMachinesMetadataSyncOutputTypeDef(TypedDict):
    HypervisorArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceOutputTypeDef(TypedDict):
    ResourceARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UntagResourceOutputTypeDef(TypedDict):
    ResourceARN: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGatewayInformationOutputTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateGatewaySoftwareNowOutputTypeDef(TypedDict):
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHypervisorOutputTypeDef(TypedDict):
    HypervisorArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetBandwidthRateLimitScheduleOutputTypeDef(TypedDict):
    BandwidthRateLimitIntervals: list[BandwidthRateLimitIntervalOutputTypeDef]
    GatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef


BandwidthRateLimitIntervalUnionTypeDef = Union[
    BandwidthRateLimitIntervalTypeDef, BandwidthRateLimitIntervalOutputTypeDef
]


class CreateGatewayInputRequestTypeDef(TypedDict):
    ActivationKey: str
    GatewayDisplayName: str
    GatewayType: Literal["BACKUP_VM"]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ImportHypervisorConfigurationInputRequestTypeDef(TypedDict):
    Host: str
    Name: str
    KmsKeyArn: NotRequired[str]
    Password: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Username: NotRequired[str]


class ListTagsForResourceOutputTypeDef(TypedDict):
    ResourceArn: str
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceInputRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class GatewayDetailsTypeDef(TypedDict):
    GatewayArn: NotRequired[str]
    GatewayDisplayName: NotRequired[str]
    GatewayType: NotRequired[Literal["BACKUP_VM"]]
    HypervisorId: NotRequired[str]
    LastSeenTime: NotRequired[datetime]
    MaintenanceStartTime: NotRequired[MaintenanceStartTimeTypeDef]
    NextUpdateAvailabilityTime: NotRequired[datetime]
    VpcEndpoint: NotRequired[str]


class ListGatewaysOutputTypeDef(TypedDict):
    Gateways: list[GatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetHypervisorOutputTypeDef(TypedDict):
    Hypervisor: HypervisorDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetHypervisorPropertyMappingsOutputTypeDef(TypedDict):
    HypervisorArn: str
    IamRoleArn: str
    VmwareToAwsTagMappings: list[VmwareToAwsTagMappingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutHypervisorPropertyMappingsInputRequestTypeDef(TypedDict):
    HypervisorArn: str
    IamRoleArn: str
    VmwareToAwsTagMappings: Sequence[VmwareToAwsTagMappingTypeDef]


class ListHypervisorsOutputTypeDef(TypedDict):
    Hypervisors: list[HypervisorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGatewaysInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHypervisorsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVirtualMachinesInputPaginateTypeDef(TypedDict):
    HypervisorArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVirtualMachinesOutputTypeDef(TypedDict):
    VirtualMachines: list[VirtualMachineTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class VirtualMachineDetailsTypeDef(TypedDict):
    HostName: NotRequired[str]
    HypervisorId: NotRequired[str]
    LastBackupDate: NotRequired[datetime]
    Name: NotRequired[str]
    Path: NotRequired[str]
    ResourceArn: NotRequired[str]
    VmwareTags: NotRequired[list[VmwareTagTypeDef]]


class PutBandwidthRateLimitScheduleInputRequestTypeDef(TypedDict):
    BandwidthRateLimitIntervals: Sequence[BandwidthRateLimitIntervalUnionTypeDef]
    GatewayArn: str


class GetGatewayOutputTypeDef(TypedDict):
    Gateway: GatewayDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetVirtualMachineOutputTypeDef(TypedDict):
    VirtualMachine: VirtualMachineDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
