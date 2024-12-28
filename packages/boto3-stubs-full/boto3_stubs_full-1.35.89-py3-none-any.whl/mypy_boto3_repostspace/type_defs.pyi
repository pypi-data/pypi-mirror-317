"""
Type annotations for repostspace service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_repostspace/type_defs/)

Usage::

    ```python
    from mypy_boto3_repostspace.type_defs import BatchAddRoleInputRequestTypeDef

    data: BatchAddRoleInputRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Mapping, Sequence

from .literals import ConfigurationStatusType, RoleType, TierLevelType, VanityDomainStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BatchAddRoleInputRequestTypeDef",
    "BatchAddRoleOutputTypeDef",
    "BatchErrorTypeDef",
    "BatchRemoveRoleInputRequestTypeDef",
    "BatchRemoveRoleOutputTypeDef",
    "CreateSpaceInputRequestTypeDef",
    "CreateSpaceOutputTypeDef",
    "DeleteSpaceInputRequestTypeDef",
    "DeregisterAdminInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetSpaceInputRequestTypeDef",
    "GetSpaceOutputTypeDef",
    "ListSpacesInputPaginateTypeDef",
    "ListSpacesInputRequestTypeDef",
    "ListSpacesOutputTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RegisterAdminInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SendInvitesInputRequestTypeDef",
    "SpaceDataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateSpaceInputRequestTypeDef",
)

class BatchAddRoleInputRequestTypeDef(TypedDict):
    accessorIds: Sequence[str]
    role: RoleType
    spaceId: str

class BatchErrorTypeDef(TypedDict):
    accessorId: str
    error: int
    message: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchRemoveRoleInputRequestTypeDef(TypedDict):
    accessorIds: Sequence[str]
    role: RoleType
    spaceId: str

class CreateSpaceInputRequestTypeDef(TypedDict):
    name: str
    subdomain: str
    tier: TierLevelType
    description: NotRequired[str]
    roleArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    userKMSKey: NotRequired[str]

class DeleteSpaceInputRequestTypeDef(TypedDict):
    spaceId: str

class DeregisterAdminInputRequestTypeDef(TypedDict):
    adminId: str
    spaceId: str

class GetSpaceInputRequestTypeDef(TypedDict):
    spaceId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListSpacesInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SpaceDataTypeDef(TypedDict):
    arn: str
    configurationStatus: ConfigurationStatusType
    createDateTime: datetime
    name: str
    randomDomain: str
    spaceId: str
    status: str
    storageLimit: int
    tier: TierLevelType
    vanityDomain: str
    vanityDomainStatus: VanityDomainStatusType
    contentSize: NotRequired[int]
    deleteDateTime: NotRequired[datetime]
    description: NotRequired[str]
    userCount: NotRequired[int]
    userKMSKey: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str

class RegisterAdminInputRequestTypeDef(TypedDict):
    adminId: str
    spaceId: str

class SendInvitesInputRequestTypeDef(TypedDict):
    accessorIds: Sequence[str]
    body: str
    spaceId: str
    title: str

class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateSpaceInputRequestTypeDef(TypedDict):
    spaceId: str
    description: NotRequired[str]
    roleArn: NotRequired[str]
    tier: NotRequired[TierLevelType]

class BatchAddRoleOutputTypeDef(TypedDict):
    addedAccessorIds: list[str]
    errors: list[BatchErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchRemoveRoleOutputTypeDef(TypedDict):
    errors: list[BatchErrorTypeDef]
    removedAccessorIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSpaceOutputTypeDef(TypedDict):
    spaceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetSpaceOutputTypeDef(TypedDict):
    arn: str
    clientId: str
    configurationStatus: ConfigurationStatusType
    contentSize: int
    createDateTime: datetime
    customerRoleArn: str
    deleteDateTime: datetime
    description: str
    groupAdmins: list[str]
    name: str
    randomDomain: str
    roles: dict[str, list[RoleType]]
    spaceId: str
    status: str
    storageLimit: int
    tier: TierLevelType
    userAdmins: list[str]
    userCount: int
    userKMSKey: str
    vanityDomain: str
    vanityDomainStatus: VanityDomainStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListSpacesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSpacesOutputTypeDef(TypedDict):
    spaces: list[SpaceDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
