"""
Type annotations for ssm-contacts service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm_contacts.type_defs import AcceptPageRequestRequestTypeDef

    data: AcceptPageRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence, Union

from .literals import (
    AcceptCodeValidationType,
    AcceptTypeType,
    ActivationStatusType,
    ChannelTypeType,
    ContactTypeType,
    DayOfWeekType,
    ReceiptTypeType,
    ShiftTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AcceptPageRequestRequestTypeDef",
    "ActivateContactChannelRequestRequestTypeDef",
    "ChannelTargetInfoTypeDef",
    "ContactChannelAddressTypeDef",
    "ContactChannelTypeDef",
    "ContactTargetInfoTypeDef",
    "ContactTypeDef",
    "CoverageTimeTypeDef",
    "CreateContactChannelRequestRequestTypeDef",
    "CreateContactChannelResultTypeDef",
    "CreateContactRequestRequestTypeDef",
    "CreateContactResultTypeDef",
    "CreateRotationOverrideRequestRequestTypeDef",
    "CreateRotationOverrideResultTypeDef",
    "CreateRotationRequestRequestTypeDef",
    "CreateRotationResultTypeDef",
    "DeactivateContactChannelRequestRequestTypeDef",
    "DeleteContactChannelRequestRequestTypeDef",
    "DeleteContactRequestRequestTypeDef",
    "DeleteRotationOverrideRequestRequestTypeDef",
    "DeleteRotationRequestRequestTypeDef",
    "DescribeEngagementRequestRequestTypeDef",
    "DescribeEngagementResultTypeDef",
    "DescribePageRequestRequestTypeDef",
    "DescribePageResultTypeDef",
    "EngagementTypeDef",
    "GetContactChannelRequestRequestTypeDef",
    "GetContactChannelResultTypeDef",
    "GetContactPolicyRequestRequestTypeDef",
    "GetContactPolicyResultTypeDef",
    "GetContactRequestRequestTypeDef",
    "GetContactResultTypeDef",
    "GetRotationOverrideRequestRequestTypeDef",
    "GetRotationOverrideResultTypeDef",
    "GetRotationRequestRequestTypeDef",
    "GetRotationResultTypeDef",
    "HandOffTimeTypeDef",
    "ListContactChannelsRequestPaginateTypeDef",
    "ListContactChannelsRequestRequestTypeDef",
    "ListContactChannelsResultTypeDef",
    "ListContactsRequestPaginateTypeDef",
    "ListContactsRequestRequestTypeDef",
    "ListContactsResultTypeDef",
    "ListEngagementsRequestPaginateTypeDef",
    "ListEngagementsRequestRequestTypeDef",
    "ListEngagementsResultTypeDef",
    "ListPageReceiptsRequestPaginateTypeDef",
    "ListPageReceiptsRequestRequestTypeDef",
    "ListPageReceiptsResultTypeDef",
    "ListPageResolutionsRequestPaginateTypeDef",
    "ListPageResolutionsRequestRequestTypeDef",
    "ListPageResolutionsResultTypeDef",
    "ListPagesByContactRequestPaginateTypeDef",
    "ListPagesByContactRequestRequestTypeDef",
    "ListPagesByContactResultTypeDef",
    "ListPagesByEngagementRequestPaginateTypeDef",
    "ListPagesByEngagementRequestRequestTypeDef",
    "ListPagesByEngagementResultTypeDef",
    "ListPreviewRotationShiftsRequestPaginateTypeDef",
    "ListPreviewRotationShiftsRequestRequestTypeDef",
    "ListPreviewRotationShiftsResultTypeDef",
    "ListRotationOverridesRequestPaginateTypeDef",
    "ListRotationOverridesRequestRequestTypeDef",
    "ListRotationOverridesResultTypeDef",
    "ListRotationShiftsRequestPaginateTypeDef",
    "ListRotationShiftsRequestRequestTypeDef",
    "ListRotationShiftsResultTypeDef",
    "ListRotationsRequestPaginateTypeDef",
    "ListRotationsRequestRequestTypeDef",
    "ListRotationsResultTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "MonthlySettingTypeDef",
    "PageTypeDef",
    "PaginatorConfigTypeDef",
    "PlanOutputTypeDef",
    "PlanTypeDef",
    "PreviewOverrideTypeDef",
    "PutContactPolicyRequestRequestTypeDef",
    "ReceiptTypeDef",
    "RecurrenceSettingsOutputTypeDef",
    "RecurrenceSettingsTypeDef",
    "ResolutionContactTypeDef",
    "ResponseMetadataTypeDef",
    "RotationOverrideTypeDef",
    "RotationShiftTypeDef",
    "RotationTypeDef",
    "SendActivationCodeRequestRequestTypeDef",
    "ShiftDetailsTypeDef",
    "StageOutputTypeDef",
    "StageTypeDef",
    "StageUnionTypeDef",
    "StartEngagementRequestRequestTypeDef",
    "StartEngagementResultTypeDef",
    "StopEngagementRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TargetTypeDef",
    "TimeRangeTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateContactChannelRequestRequestTypeDef",
    "UpdateContactRequestRequestTypeDef",
    "UpdateRotationRequestRequestTypeDef",
    "WeeklySettingTypeDef",
)


class AcceptPageRequestRequestTypeDef(TypedDict):
    PageId: str
    AcceptType: AcceptTypeType
    AcceptCode: str
    ContactChannelId: NotRequired[str]
    Note: NotRequired[str]
    AcceptCodeValidation: NotRequired[AcceptCodeValidationType]


class ActivateContactChannelRequestRequestTypeDef(TypedDict):
    ContactChannelId: str
    ActivationCode: str


class ChannelTargetInfoTypeDef(TypedDict):
    ContactChannelId: str
    RetryIntervalInMinutes: NotRequired[int]


class ContactChannelAddressTypeDef(TypedDict):
    SimpleAddress: NotRequired[str]


class ContactTargetInfoTypeDef(TypedDict):
    IsEssential: bool
    ContactId: NotRequired[str]


ContactTypeDef = TypedDict(
    "ContactTypeDef",
    {
        "ContactArn": str,
        "Alias": str,
        "Type": ContactTypeType,
        "DisplayName": NotRequired[str],
    },
)


class HandOffTimeTypeDef(TypedDict):
    HourOfDay: int
    MinuteOfHour: int


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class DeactivateContactChannelRequestRequestTypeDef(TypedDict):
    ContactChannelId: str


class DeleteContactChannelRequestRequestTypeDef(TypedDict):
    ContactChannelId: str


class DeleteContactRequestRequestTypeDef(TypedDict):
    ContactId: str


class DeleteRotationOverrideRequestRequestTypeDef(TypedDict):
    RotationId: str
    RotationOverrideId: str


class DeleteRotationRequestRequestTypeDef(TypedDict):
    RotationId: str


class DescribeEngagementRequestRequestTypeDef(TypedDict):
    EngagementId: str


class DescribePageRequestRequestTypeDef(TypedDict):
    PageId: str


class EngagementTypeDef(TypedDict):
    EngagementArn: str
    ContactArn: str
    Sender: str
    IncidentId: NotRequired[str]
    StartTime: NotRequired[datetime]
    StopTime: NotRequired[datetime]


class GetContactChannelRequestRequestTypeDef(TypedDict):
    ContactChannelId: str


class GetContactPolicyRequestRequestTypeDef(TypedDict):
    ContactArn: str


class GetContactRequestRequestTypeDef(TypedDict):
    ContactId: str


class GetRotationOverrideRequestRequestTypeDef(TypedDict):
    RotationId: str
    RotationOverrideId: str


class GetRotationRequestRequestTypeDef(TypedDict):
    RotationId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListContactChannelsRequestRequestTypeDef(TypedDict):
    ContactId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


ListContactsRequestRequestTypeDef = TypedDict(
    "ListContactsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "AliasPrefix": NotRequired[str],
        "Type": NotRequired[ContactTypeType],
    },
)


class ListPageReceiptsRequestRequestTypeDef(TypedDict):
    PageId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ReceiptTypeDef(TypedDict):
    ReceiptType: ReceiptTypeType
    ReceiptTime: datetime
    ContactChannelArn: NotRequired[str]
    ReceiptInfo: NotRequired[str]


class ListPageResolutionsRequestRequestTypeDef(TypedDict):
    PageId: str
    NextToken: NotRequired[str]


ResolutionContactTypeDef = TypedDict(
    "ResolutionContactTypeDef",
    {
        "ContactArn": str,
        "Type": ContactTypeType,
        "StageIndex": NotRequired[int],
    },
)


class ListPagesByContactRequestRequestTypeDef(TypedDict):
    ContactId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PageTypeDef(TypedDict):
    PageArn: str
    EngagementArn: str
    ContactArn: str
    Sender: str
    IncidentId: NotRequired[str]
    SentTime: NotRequired[datetime]
    DeliveryTime: NotRequired[datetime]
    ReadTime: NotRequired[datetime]


class ListPagesByEngagementRequestRequestTypeDef(TypedDict):
    EngagementId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class RotationOverrideTypeDef(TypedDict):
    RotationOverrideId: str
    NewContactIds: list[str]
    StartTime: datetime
    EndTime: datetime
    CreateTime: datetime


class ListRotationsRequestRequestTypeDef(TypedDict):
    RotationNamePrefix: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str


class PutContactPolicyRequestRequestTypeDef(TypedDict):
    ContactArn: str
    Policy: str


class ShiftDetailsTypeDef(TypedDict):
    OverriddenContactIds: list[str]


class SendActivationCodeRequestRequestTypeDef(TypedDict):
    ContactChannelId: str


class StartEngagementRequestRequestTypeDef(TypedDict):
    ContactId: str
    Sender: str
    Subject: str
    Content: str
    PublicSubject: NotRequired[str]
    PublicContent: NotRequired[str]
    IncidentId: NotRequired[str]
    IdempotencyToken: NotRequired[str]


class StopEngagementRequestRequestTypeDef(TypedDict):
    EngagementId: str
    Reason: NotRequired[str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]


ContactChannelTypeDef = TypedDict(
    "ContactChannelTypeDef",
    {
        "ContactChannelArn": str,
        "ContactArn": str,
        "Name": str,
        "DeliveryAddress": ContactChannelAddressTypeDef,
        "ActivationStatus": ActivationStatusType,
        "Type": NotRequired[ChannelTypeType],
    },
)
CreateContactChannelRequestRequestTypeDef = TypedDict(
    "CreateContactChannelRequestRequestTypeDef",
    {
        "ContactId": str,
        "Name": str,
        "Type": ChannelTypeType,
        "DeliveryAddress": ContactChannelAddressTypeDef,
        "DeferActivation": NotRequired[bool],
        "IdempotencyToken": NotRequired[str],
    },
)


class UpdateContactChannelRequestRequestTypeDef(TypedDict):
    ContactChannelId: str
    Name: NotRequired[str]
    DeliveryAddress: NotRequired[ContactChannelAddressTypeDef]


class TargetTypeDef(TypedDict):
    ChannelTargetInfo: NotRequired[ChannelTargetInfoTypeDef]
    ContactTargetInfo: NotRequired[ContactTargetInfoTypeDef]


class CoverageTimeTypeDef(TypedDict):
    Start: NotRequired[HandOffTimeTypeDef]
    End: NotRequired[HandOffTimeTypeDef]


class MonthlySettingTypeDef(TypedDict):
    DayOfMonth: int
    HandOffTime: HandOffTimeTypeDef


class WeeklySettingTypeDef(TypedDict):
    DayOfWeek: DayOfWeekType
    HandOffTime: HandOffTimeTypeDef


class CreateContactChannelResultTypeDef(TypedDict):
    ContactChannelArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContactResultTypeDef(TypedDict):
    ContactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRotationOverrideResultTypeDef(TypedDict):
    RotationOverrideId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRotationResultTypeDef(TypedDict):
    RotationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEngagementResultTypeDef(TypedDict):
    ContactArn: str
    EngagementArn: str
    Sender: str
    Subject: str
    Content: str
    PublicSubject: str
    PublicContent: str
    IncidentId: str
    StartTime: datetime
    StopTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePageResultTypeDef(TypedDict):
    PageArn: str
    EngagementArn: str
    ContactArn: str
    Sender: str
    Subject: str
    Content: str
    PublicSubject: str
    PublicContent: str
    IncidentId: str
    SentTime: datetime
    ReadTime: datetime
    DeliveryTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


GetContactChannelResultTypeDef = TypedDict(
    "GetContactChannelResultTypeDef",
    {
        "ContactArn": str,
        "ContactChannelArn": str,
        "Name": str,
        "Type": ChannelTypeType,
        "DeliveryAddress": ContactChannelAddressTypeDef,
        "ActivationStatus": ActivationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetContactPolicyResultTypeDef(TypedDict):
    ContactArn: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRotationOverrideResultTypeDef(TypedDict):
    RotationOverrideId: str
    RotationArn: str
    NewContactIds: list[str]
    StartTime: datetime
    EndTime: datetime
    CreateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListContactsResultTypeDef(TypedDict):
    Contacts: list[ContactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartEngagementResultTypeDef(TypedDict):
    EngagementArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResultTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]


class CreateRotationOverrideRequestRequestTypeDef(TypedDict):
    RotationId: str
    NewContactIds: Sequence[str]
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    IdempotencyToken: NotRequired[str]


class ListRotationOverridesRequestRequestTypeDef(TypedDict):
    RotationId: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListRotationShiftsRequestRequestTypeDef(TypedDict):
    RotationId: str
    EndTime: TimestampTypeDef
    StartTime: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class PreviewOverrideTypeDef(TypedDict):
    NewMembers: NotRequired[Sequence[str]]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]


class TimeRangeTypeDef(TypedDict):
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]


class ListEngagementsResultTypeDef(TypedDict):
    Engagements: list[EngagementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListContactChannelsRequestPaginateTypeDef(TypedDict):
    ContactId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListContactsRequestPaginateTypeDef = TypedDict(
    "ListContactsRequestPaginateTypeDef",
    {
        "AliasPrefix": NotRequired[str],
        "Type": NotRequired[ContactTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListPageReceiptsRequestPaginateTypeDef(TypedDict):
    PageId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPageResolutionsRequestPaginateTypeDef(TypedDict):
    PageId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPagesByContactRequestPaginateTypeDef(TypedDict):
    ContactId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPagesByEngagementRequestPaginateTypeDef(TypedDict):
    EngagementId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRotationOverridesRequestPaginateTypeDef(TypedDict):
    RotationId: str
    StartTime: TimestampTypeDef
    EndTime: TimestampTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRotationShiftsRequestPaginateTypeDef(TypedDict):
    RotationId: str
    EndTime: TimestampTypeDef
    StartTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRotationsRequestPaginateTypeDef(TypedDict):
    RotationNamePrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPageReceiptsResultTypeDef(TypedDict):
    Receipts: list[ReceiptTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPageResolutionsResultTypeDef(TypedDict):
    PageResolutions: list[ResolutionContactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPagesByContactResultTypeDef(TypedDict):
    Pages: list[PageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPagesByEngagementResultTypeDef(TypedDict):
    Pages: list[PageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRotationOverridesResultTypeDef(TypedDict):
    RotationOverrides: list[RotationOverrideTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


RotationShiftTypeDef = TypedDict(
    "RotationShiftTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
        "ContactIds": NotRequired[list[str]],
        "Type": NotRequired[ShiftTypeType],
        "ShiftDetails": NotRequired[ShiftDetailsTypeDef],
    },
)


class ListContactChannelsResultTypeDef(TypedDict):
    ContactChannels: list[ContactChannelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StageOutputTypeDef(TypedDict):
    DurationInMinutes: int
    Targets: list[TargetTypeDef]


class StageTypeDef(TypedDict):
    DurationInMinutes: int
    Targets: Sequence[TargetTypeDef]


class RecurrenceSettingsOutputTypeDef(TypedDict):
    NumberOfOnCalls: int
    RecurrenceMultiplier: int
    MonthlySettings: NotRequired[list[MonthlySettingTypeDef]]
    WeeklySettings: NotRequired[list[WeeklySettingTypeDef]]
    DailySettings: NotRequired[list[HandOffTimeTypeDef]]
    ShiftCoverages: NotRequired[dict[DayOfWeekType, list[CoverageTimeTypeDef]]]


class RecurrenceSettingsTypeDef(TypedDict):
    NumberOfOnCalls: int
    RecurrenceMultiplier: int
    MonthlySettings: NotRequired[Sequence[MonthlySettingTypeDef]]
    WeeklySettings: NotRequired[Sequence[WeeklySettingTypeDef]]
    DailySettings: NotRequired[Sequence[HandOffTimeTypeDef]]
    ShiftCoverages: NotRequired[Mapping[DayOfWeekType, Sequence[CoverageTimeTypeDef]]]


class ListEngagementsRequestPaginateTypeDef(TypedDict):
    IncidentId: NotRequired[str]
    TimeRangeValue: NotRequired[TimeRangeTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEngagementsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    IncidentId: NotRequired[str]
    TimeRangeValue: NotRequired[TimeRangeTypeDef]


class ListPreviewRotationShiftsResultTypeDef(TypedDict):
    RotationShifts: list[RotationShiftTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRotationShiftsResultTypeDef(TypedDict):
    RotationShifts: list[RotationShiftTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PlanOutputTypeDef(TypedDict):
    Stages: NotRequired[list[StageOutputTypeDef]]
    RotationIds: NotRequired[list[str]]


StageUnionTypeDef = Union[StageTypeDef, StageOutputTypeDef]


class GetRotationResultTypeDef(TypedDict):
    RotationArn: str
    Name: str
    ContactIds: list[str]
    StartTime: datetime
    TimeZoneId: str
    Recurrence: RecurrenceSettingsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RotationTypeDef(TypedDict):
    RotationArn: str
    Name: str
    ContactIds: NotRequired[list[str]]
    StartTime: NotRequired[datetime]
    TimeZoneId: NotRequired[str]
    Recurrence: NotRequired[RecurrenceSettingsOutputTypeDef]


class CreateRotationRequestRequestTypeDef(TypedDict):
    Name: str
    ContactIds: Sequence[str]
    TimeZoneId: str
    Recurrence: RecurrenceSettingsTypeDef
    StartTime: NotRequired[TimestampTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    IdempotencyToken: NotRequired[str]


class ListPreviewRotationShiftsRequestPaginateTypeDef(TypedDict):
    EndTime: TimestampTypeDef
    Members: Sequence[str]
    TimeZoneId: str
    Recurrence: RecurrenceSettingsTypeDef
    RotationStartTime: NotRequired[TimestampTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    Overrides: NotRequired[Sequence[PreviewOverrideTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPreviewRotationShiftsRequestRequestTypeDef(TypedDict):
    EndTime: TimestampTypeDef
    Members: Sequence[str]
    TimeZoneId: str
    Recurrence: RecurrenceSettingsTypeDef
    RotationStartTime: NotRequired[TimestampTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    Overrides: NotRequired[Sequence[PreviewOverrideTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class UpdateRotationRequestRequestTypeDef(TypedDict):
    RotationId: str
    Recurrence: RecurrenceSettingsTypeDef
    ContactIds: NotRequired[Sequence[str]]
    StartTime: NotRequired[TimestampTypeDef]
    TimeZoneId: NotRequired[str]


GetContactResultTypeDef = TypedDict(
    "GetContactResultTypeDef",
    {
        "ContactArn": str,
        "Alias": str,
        "DisplayName": str,
        "Type": ContactTypeType,
        "Plan": PlanOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class PlanTypeDef(TypedDict):
    Stages: NotRequired[Sequence[StageUnionTypeDef]]
    RotationIds: NotRequired[Sequence[str]]


class ListRotationsResultTypeDef(TypedDict):
    Rotations: list[RotationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CreateContactRequestRequestTypeDef = TypedDict(
    "CreateContactRequestRequestTypeDef",
    {
        "Alias": str,
        "Type": ContactTypeType,
        "Plan": PlanTypeDef,
        "DisplayName": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "IdempotencyToken": NotRequired[str],
    },
)


class UpdateContactRequestRequestTypeDef(TypedDict):
    ContactId: str
    DisplayName: NotRequired[str]
    Plan: NotRequired[PlanTypeDef]
