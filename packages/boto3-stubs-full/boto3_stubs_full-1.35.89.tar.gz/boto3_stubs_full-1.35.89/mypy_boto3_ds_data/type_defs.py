"""
Type annotations for ds-data service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ds_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_ds_data.type_defs import AddGroupMemberRequestRequestTypeDef

    data: AddGroupMemberRequestRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Mapping, Sequence, Union

from .literals import GroupScopeType, GroupTypeType, MemberTypeType, UpdateTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AddGroupMemberRequestRequestTypeDef",
    "AttributeValueOutputTypeDef",
    "AttributeValueTypeDef",
    "AttributeValueUnionTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "CreateGroupResultTypeDef",
    "CreateUserRequestRequestTypeDef",
    "CreateUserResultTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeGroupResultTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "DescribeUserResultTypeDef",
    "DisableUserRequestRequestTypeDef",
    "GroupSummaryTypeDef",
    "GroupTypeDef",
    "ListGroupMembersRequestPaginateTypeDef",
    "ListGroupMembersRequestRequestTypeDef",
    "ListGroupMembersResultTypeDef",
    "ListGroupsForMemberRequestPaginateTypeDef",
    "ListGroupsForMemberRequestRequestTypeDef",
    "ListGroupsForMemberResultTypeDef",
    "ListGroupsRequestPaginateTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResultTypeDef",
    "ListUsersRequestPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListUsersResultTypeDef",
    "MemberTypeDef",
    "PaginatorConfigTypeDef",
    "RemoveGroupMemberRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SearchGroupsRequestPaginateTypeDef",
    "SearchGroupsRequestRequestTypeDef",
    "SearchGroupsResultTypeDef",
    "SearchUsersRequestPaginateTypeDef",
    "SearchUsersRequestRequestTypeDef",
    "SearchUsersResultTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UserSummaryTypeDef",
    "UserTypeDef",
)


class AddGroupMemberRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    GroupName: str
    MemberName: str
    ClientToken: NotRequired[str]
    MemberRealm: NotRequired[str]


class AttributeValueOutputTypeDef(TypedDict):
    BOOL: NotRequired[bool]
    N: NotRequired[int]
    S: NotRequired[str]
    SS: NotRequired[list[str]]


class AttributeValueTypeDef(TypedDict):
    BOOL: NotRequired[bool]
    N: NotRequired[int]
    S: NotRequired[str]
    SS: NotRequired[Sequence[str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteGroupRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    ClientToken: NotRequired[str]


class DeleteUserRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    ClientToken: NotRequired[str]


class DescribeGroupRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    OtherAttributes: NotRequired[Sequence[str]]
    Realm: NotRequired[str]


class DescribeUserRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    OtherAttributes: NotRequired[Sequence[str]]
    Realm: NotRequired[str]


class DisableUserRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    ClientToken: NotRequired[str]


class GroupSummaryTypeDef(TypedDict):
    GroupScope: GroupScopeType
    GroupType: GroupTypeType
    SAMAccountName: str
    SID: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListGroupMembersRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    MaxResults: NotRequired[int]
    MemberRealm: NotRequired[str]
    NextToken: NotRequired[str]
    Realm: NotRequired[str]


class MemberTypeDef(TypedDict):
    MemberType: MemberTypeType
    SAMAccountName: str
    SID: str


class ListGroupsForMemberRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    MaxResults: NotRequired[int]
    MemberRealm: NotRequired[str]
    NextToken: NotRequired[str]
    Realm: NotRequired[str]


class ListGroupsRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Realm: NotRequired[str]


class ListUsersRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Realm: NotRequired[str]


class UserSummaryTypeDef(TypedDict):
    Enabled: bool
    SAMAccountName: str
    SID: str
    GivenName: NotRequired[str]
    Surname: NotRequired[str]


class RemoveGroupMemberRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    GroupName: str
    MemberName: str
    ClientToken: NotRequired[str]
    MemberRealm: NotRequired[str]


class SearchGroupsRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SearchAttributes: Sequence[str]
    SearchString: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Realm: NotRequired[str]


class SearchUsersRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SearchAttributes: Sequence[str]
    SearchString: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Realm: NotRequired[str]


class GroupTypeDef(TypedDict):
    SAMAccountName: str
    DistinguishedName: NotRequired[str]
    GroupScope: NotRequired[GroupScopeType]
    GroupType: NotRequired[GroupTypeType]
    OtherAttributes: NotRequired[dict[str, AttributeValueOutputTypeDef]]
    SID: NotRequired[str]


class UserTypeDef(TypedDict):
    SAMAccountName: str
    DistinguishedName: NotRequired[str]
    EmailAddress: NotRequired[str]
    Enabled: NotRequired[bool]
    GivenName: NotRequired[str]
    OtherAttributes: NotRequired[dict[str, AttributeValueOutputTypeDef]]
    SID: NotRequired[str]
    Surname: NotRequired[str]
    UserPrincipalName: NotRequired[str]


AttributeValueUnionTypeDef = Union[AttributeValueTypeDef, AttributeValueOutputTypeDef]


class CreateUserRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    ClientToken: NotRequired[str]
    EmailAddress: NotRequired[str]
    GivenName: NotRequired[str]
    OtherAttributes: NotRequired[Mapping[str, AttributeValueTypeDef]]
    Surname: NotRequired[str]


class UpdateGroupRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    ClientToken: NotRequired[str]
    GroupScope: NotRequired[GroupScopeType]
    GroupType: NotRequired[GroupTypeType]
    OtherAttributes: NotRequired[Mapping[str, AttributeValueTypeDef]]
    UpdateType: NotRequired[UpdateTypeType]


class UpdateUserRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    ClientToken: NotRequired[str]
    EmailAddress: NotRequired[str]
    GivenName: NotRequired[str]
    OtherAttributes: NotRequired[Mapping[str, AttributeValueTypeDef]]
    Surname: NotRequired[str]
    UpdateType: NotRequired[UpdateTypeType]


class CreateGroupResultTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    SID: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserResultTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    SID: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGroupResultTypeDef(TypedDict):
    DirectoryId: str
    DistinguishedName: str
    GroupScope: GroupScopeType
    GroupType: GroupTypeType
    OtherAttributes: dict[str, AttributeValueOutputTypeDef]
    Realm: str
    SAMAccountName: str
    SID: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUserResultTypeDef(TypedDict):
    DirectoryId: str
    DistinguishedName: str
    EmailAddress: str
    Enabled: bool
    GivenName: str
    OtherAttributes: dict[str, AttributeValueOutputTypeDef]
    Realm: str
    SAMAccountName: str
    SID: str
    Surname: str
    UserPrincipalName: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupsForMemberResultTypeDef(TypedDict):
    DirectoryId: str
    Groups: list[GroupSummaryTypeDef]
    MemberRealm: str
    Realm: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGroupsResultTypeDef(TypedDict):
    DirectoryId: str
    Groups: list[GroupSummaryTypeDef]
    Realm: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListGroupMembersRequestPaginateTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    MemberRealm: NotRequired[str]
    Realm: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsForMemberRequestPaginateTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    MemberRealm: NotRequired[str]
    Realm: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsRequestPaginateTypeDef(TypedDict):
    DirectoryId: str
    Realm: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsersRequestPaginateTypeDef(TypedDict):
    DirectoryId: str
    Realm: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchGroupsRequestPaginateTypeDef(TypedDict):
    DirectoryId: str
    SearchAttributes: Sequence[str]
    SearchString: str
    Realm: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchUsersRequestPaginateTypeDef(TypedDict):
    DirectoryId: str
    SearchAttributes: Sequence[str]
    SearchString: str
    Realm: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupMembersResultTypeDef(TypedDict):
    DirectoryId: str
    MemberRealm: str
    Members: list[MemberTypeDef]
    Realm: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUsersResultTypeDef(TypedDict):
    DirectoryId: str
    Realm: str
    Users: list[UserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchGroupsResultTypeDef(TypedDict):
    DirectoryId: str
    Groups: list[GroupTypeDef]
    Realm: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchUsersResultTypeDef(TypedDict):
    DirectoryId: str
    Realm: str
    Users: list[UserTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateGroupRequestRequestTypeDef(TypedDict):
    DirectoryId: str
    SAMAccountName: str
    ClientToken: NotRequired[str]
    GroupScope: NotRequired[GroupScopeType]
    GroupType: NotRequired[GroupTypeType]
    OtherAttributes: NotRequired[Mapping[str, AttributeValueUnionTypeDef]]
