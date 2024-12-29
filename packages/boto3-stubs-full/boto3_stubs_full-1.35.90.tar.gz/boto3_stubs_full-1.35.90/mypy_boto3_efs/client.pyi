"""
Type annotations for efs service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_efs.client import EFSClient

    session = Session()
    client: EFSClient = session.client("efs")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeAccessPointsPaginator,
    DescribeFileSystemsPaginator,
    DescribeMountTargetsPaginator,
    DescribeReplicationConfigurationsPaginator,
    DescribeTagsPaginator,
)
from .type_defs import (
    AccessPointDescriptionResponseTypeDef,
    BackupPolicyDescriptionTypeDef,
    CreateAccessPointRequestRequestTypeDef,
    CreateFileSystemRequestRequestTypeDef,
    CreateMountTargetRequestRequestTypeDef,
    CreateReplicationConfigurationRequestRequestTypeDef,
    CreateTagsRequestRequestTypeDef,
    DeleteAccessPointRequestRequestTypeDef,
    DeleteFileSystemPolicyRequestRequestTypeDef,
    DeleteFileSystemRequestRequestTypeDef,
    DeleteMountTargetRequestRequestTypeDef,
    DeleteReplicationConfigurationRequestRequestTypeDef,
    DeleteTagsRequestRequestTypeDef,
    DescribeAccessPointsRequestRequestTypeDef,
    DescribeAccessPointsResponseTypeDef,
    DescribeAccountPreferencesRequestRequestTypeDef,
    DescribeAccountPreferencesResponseTypeDef,
    DescribeBackupPolicyRequestRequestTypeDef,
    DescribeFileSystemPolicyRequestRequestTypeDef,
    DescribeFileSystemsRequestRequestTypeDef,
    DescribeFileSystemsResponseTypeDef,
    DescribeLifecycleConfigurationRequestRequestTypeDef,
    DescribeMountTargetSecurityGroupsRequestRequestTypeDef,
    DescribeMountTargetSecurityGroupsResponseTypeDef,
    DescribeMountTargetsRequestRequestTypeDef,
    DescribeMountTargetsResponseTypeDef,
    DescribeReplicationConfigurationsRequestRequestTypeDef,
    DescribeReplicationConfigurationsResponseTypeDef,
    DescribeTagsRequestRequestTypeDef,
    DescribeTagsResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    FileSystemDescriptionResponseTypeDef,
    FileSystemPolicyDescriptionTypeDef,
    FileSystemProtectionDescriptionResponseTypeDef,
    LifecycleConfigurationDescriptionTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ModifyMountTargetSecurityGroupsRequestRequestTypeDef,
    MountTargetDescriptionResponseTypeDef,
    PutAccountPreferencesRequestRequestTypeDef,
    PutAccountPreferencesResponseTypeDef,
    PutBackupPolicyRequestRequestTypeDef,
    PutFileSystemPolicyRequestRequestTypeDef,
    PutLifecycleConfigurationRequestRequestTypeDef,
    ReplicationConfigurationDescriptionResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateFileSystemProtectionRequestRequestTypeDef,
    UpdateFileSystemRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("EFSClient",)

class Exceptions(BaseClientExceptions):
    AccessPointAlreadyExists: type[BotocoreClientError]
    AccessPointLimitExceeded: type[BotocoreClientError]
    AccessPointNotFound: type[BotocoreClientError]
    AvailabilityZonesMismatch: type[BotocoreClientError]
    BadRequest: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    DependencyTimeout: type[BotocoreClientError]
    FileSystemAlreadyExists: type[BotocoreClientError]
    FileSystemInUse: type[BotocoreClientError]
    FileSystemLimitExceeded: type[BotocoreClientError]
    FileSystemNotFound: type[BotocoreClientError]
    IncorrectFileSystemLifeCycleState: type[BotocoreClientError]
    IncorrectMountTargetState: type[BotocoreClientError]
    InsufficientThroughputCapacity: type[BotocoreClientError]
    InternalServerError: type[BotocoreClientError]
    InvalidPolicyException: type[BotocoreClientError]
    IpAddressInUse: type[BotocoreClientError]
    MountTargetConflict: type[BotocoreClientError]
    MountTargetNotFound: type[BotocoreClientError]
    NetworkInterfaceLimitExceeded: type[BotocoreClientError]
    NoFreeAddressesInSubnet: type[BotocoreClientError]
    PolicyNotFound: type[BotocoreClientError]
    ReplicationAlreadyExists: type[BotocoreClientError]
    ReplicationNotFound: type[BotocoreClientError]
    SecurityGroupLimitExceeded: type[BotocoreClientError]
    SecurityGroupNotFound: type[BotocoreClientError]
    SubnetNotFound: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ThroughputLimitExceeded: type[BotocoreClientError]
    TooManyRequests: type[BotocoreClientError]
    UnsupportedAvailabilityZone: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class EFSClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EFSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#generate_presigned_url)
        """

    def create_access_point(
        self, **kwargs: Unpack[CreateAccessPointRequestRequestTypeDef]
    ) -> AccessPointDescriptionResponseTypeDef:
        """
        Creates an EFS access point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/create_access_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#create_access_point)
        """

    def create_file_system(
        self, **kwargs: Unpack[CreateFileSystemRequestRequestTypeDef]
    ) -> FileSystemDescriptionResponseTypeDef:
        """
        Creates a new, empty file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/create_file_system.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#create_file_system)
        """

    def create_mount_target(
        self, **kwargs: Unpack[CreateMountTargetRequestRequestTypeDef]
    ) -> MountTargetDescriptionResponseTypeDef:
        """
        Creates a mount target for a file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/create_mount_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#create_mount_target)
        """

    def create_replication_configuration(
        self, **kwargs: Unpack[CreateReplicationConfigurationRequestRequestTypeDef]
    ) -> ReplicationConfigurationDescriptionResponseTypeDef:
        """
        Creates a replication conﬁguration to either a new or existing EFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/create_replication_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#create_replication_configuration)
        """

    def create_tags(
        self, **kwargs: Unpack[CreateTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        DEPRECATED - <code>CreateTags</code> is deprecated and not maintained.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/create_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#create_tags)
        """

    def delete_access_point(
        self, **kwargs: Unpack[DeleteAccessPointRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified access point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/delete_access_point.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#delete_access_point)
        """

    def delete_file_system(
        self, **kwargs: Unpack[DeleteFileSystemRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a file system, permanently severing access to its contents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/delete_file_system.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#delete_file_system)
        """

    def delete_file_system_policy(
        self, **kwargs: Unpack[DeleteFileSystemPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the <code>FileSystemPolicy</code> for the specified file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/delete_file_system_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#delete_file_system_policy)
        """

    def delete_mount_target(
        self, **kwargs: Unpack[DeleteMountTargetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified mount target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/delete_mount_target.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#delete_mount_target)
        """

    def delete_replication_configuration(
        self, **kwargs: Unpack[DeleteReplicationConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a replication configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/delete_replication_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#delete_replication_configuration)
        """

    def delete_tags(
        self, **kwargs: Unpack[DeleteTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        DEPRECATED - <code>DeleteTags</code> is deprecated and not maintained.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/delete_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#delete_tags)
        """

    def describe_access_points(
        self, **kwargs: Unpack[DescribeAccessPointsRequestRequestTypeDef]
    ) -> DescribeAccessPointsResponseTypeDef:
        """
        Returns the description of a specific Amazon EFS access point if the
        <code>AccessPointId</code> is provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_access_points.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_access_points)
        """

    def describe_account_preferences(
        self, **kwargs: Unpack[DescribeAccountPreferencesRequestRequestTypeDef]
    ) -> DescribeAccountPreferencesResponseTypeDef:
        """
        Returns the account preferences settings for the Amazon Web Services account
        associated with the user making the request, in the current Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_account_preferences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_account_preferences)
        """

    def describe_backup_policy(
        self, **kwargs: Unpack[DescribeBackupPolicyRequestRequestTypeDef]
    ) -> BackupPolicyDescriptionTypeDef:
        """
        Returns the backup policy for the specified EFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_backup_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_backup_policy)
        """

    def describe_file_system_policy(
        self, **kwargs: Unpack[DescribeFileSystemPolicyRequestRequestTypeDef]
    ) -> FileSystemPolicyDescriptionTypeDef:
        """
        Returns the <code>FileSystemPolicy</code> for the specified EFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_file_system_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_file_system_policy)
        """

    def describe_file_systems(
        self, **kwargs: Unpack[DescribeFileSystemsRequestRequestTypeDef]
    ) -> DescribeFileSystemsResponseTypeDef:
        """
        Returns the description of a specific Amazon EFS file system if either the file
        system <code>CreationToken</code> or the <code>FileSystemId</code> is provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_file_systems.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_file_systems)
        """

    def describe_lifecycle_configuration(
        self, **kwargs: Unpack[DescribeLifecycleConfigurationRequestRequestTypeDef]
    ) -> LifecycleConfigurationDescriptionTypeDef:
        """
        Returns the current <code>LifecycleConfiguration</code> object for the
        specified Amazon EFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_lifecycle_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_lifecycle_configuration)
        """

    def describe_mount_target_security_groups(
        self, **kwargs: Unpack[DescribeMountTargetSecurityGroupsRequestRequestTypeDef]
    ) -> DescribeMountTargetSecurityGroupsResponseTypeDef:
        """
        Returns the security groups currently in effect for a mount target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_mount_target_security_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_mount_target_security_groups)
        """

    def describe_mount_targets(
        self, **kwargs: Unpack[DescribeMountTargetsRequestRequestTypeDef]
    ) -> DescribeMountTargetsResponseTypeDef:
        """
        Returns the descriptions of all the current mount targets, or a specific mount
        target, for a file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_mount_targets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_mount_targets)
        """

    def describe_replication_configurations(
        self, **kwargs: Unpack[DescribeReplicationConfigurationsRequestRequestTypeDef]
    ) -> DescribeReplicationConfigurationsResponseTypeDef:
        """
        Retrieves the replication configuration for a specific file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_replication_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_replication_configurations)
        """

    def describe_tags(
        self, **kwargs: Unpack[DescribeTagsRequestRequestTypeDef]
    ) -> DescribeTagsResponseTypeDef:
        """
        DEPRECATED - The <code>DescribeTags</code> action is deprecated and not
        maintained.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/describe_tags.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#describe_tags)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags for a top-level EFS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#list_tags_for_resource)
        """

    def modify_mount_target_security_groups(
        self, **kwargs: Unpack[ModifyMountTargetSecurityGroupsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the set of security groups in effect for a mount target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/modify_mount_target_security_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#modify_mount_target_security_groups)
        """

    def put_account_preferences(
        self, **kwargs: Unpack[PutAccountPreferencesRequestRequestTypeDef]
    ) -> PutAccountPreferencesResponseTypeDef:
        """
        Use this operation to set the account preference in the current Amazon Web
        Services Region to use long 17 character (63 bit) or short 8 character (32 bit)
        resource IDs for new EFS file system and mount target resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/put_account_preferences.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#put_account_preferences)
        """

    def put_backup_policy(
        self, **kwargs: Unpack[PutBackupPolicyRequestRequestTypeDef]
    ) -> BackupPolicyDescriptionTypeDef:
        """
        Updates the file system's backup policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/put_backup_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#put_backup_policy)
        """

    def put_file_system_policy(
        self, **kwargs: Unpack[PutFileSystemPolicyRequestRequestTypeDef]
    ) -> FileSystemPolicyDescriptionTypeDef:
        """
        Applies an Amazon EFS <code>FileSystemPolicy</code> to an Amazon EFS file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/put_file_system_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#put_file_system_policy)
        """

    def put_lifecycle_configuration(
        self, **kwargs: Unpack[PutLifecycleConfigurationRequestRequestTypeDef]
    ) -> LifecycleConfigurationDescriptionTypeDef:
        """
        Use this action to manage storage for your file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/put_lifecycle_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#put_lifecycle_configuration)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a tag for an EFS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from an EFS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#untag_resource)
        """

    def update_file_system(
        self, **kwargs: Unpack[UpdateFileSystemRequestRequestTypeDef]
    ) -> FileSystemDescriptionResponseTypeDef:
        """
        Updates the throughput mode or the amount of provisioned throughput of an
        existing file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/update_file_system.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#update_file_system)
        """

    def update_file_system_protection(
        self, **kwargs: Unpack[UpdateFileSystemProtectionRequestRequestTypeDef]
    ) -> FileSystemProtectionDescriptionResponseTypeDef:
        """
        Updates protection on the file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/update_file_system_protection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#update_file_system_protection)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_access_points"]
    ) -> DescribeAccessPointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_file_systems"]
    ) -> DescribeFileSystemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_mount_targets"]
    ) -> DescribeMountTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_replication_configurations"]
    ) -> DescribeReplicationConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_tags"]
    ) -> DescribeTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_efs/client/#get_paginator)
        """
