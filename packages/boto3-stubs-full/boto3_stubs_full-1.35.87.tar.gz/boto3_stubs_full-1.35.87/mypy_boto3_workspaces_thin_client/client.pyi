"""
Type annotations for workspaces-thin-client service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_workspaces_thin_client.client import WorkSpacesThinClientClient

    session = Session()
    client: WorkSpacesThinClientClient = session.client("workspaces-thin-client")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListDevicesPaginator, ListEnvironmentsPaginator, ListSoftwareSetsPaginator
from .type_defs import (
    CreateEnvironmentRequestRequestTypeDef,
    CreateEnvironmentResponseTypeDef,
    DeleteDeviceRequestRequestTypeDef,
    DeleteEnvironmentRequestRequestTypeDef,
    DeregisterDeviceRequestRequestTypeDef,
    GetDeviceRequestRequestTypeDef,
    GetDeviceResponseTypeDef,
    GetEnvironmentRequestRequestTypeDef,
    GetEnvironmentResponseTypeDef,
    GetSoftwareSetRequestRequestTypeDef,
    GetSoftwareSetResponseTypeDef,
    ListDevicesRequestRequestTypeDef,
    ListDevicesResponseTypeDef,
    ListEnvironmentsRequestRequestTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListSoftwareSetsRequestRequestTypeDef,
    ListSoftwareSetsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDeviceRequestRequestTypeDef,
    UpdateDeviceResponseTypeDef,
    UpdateEnvironmentRequestRequestTypeDef,
    UpdateEnvironmentResponseTypeDef,
    UpdateSoftwareSetRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("WorkSpacesThinClientClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class WorkSpacesThinClientClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client.html#WorkSpacesThinClient.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkSpacesThinClientClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client.html#WorkSpacesThinClient.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#generate_presigned_url)
        """

    def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentRequestRequestTypeDef]
    ) -> CreateEnvironmentResponseTypeDef:
        """
        Creates an environment for your thin client devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/create_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#create_environment)
        """

    def delete_device(self, **kwargs: Unpack[DeleteDeviceRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes a thin client device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/delete_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#delete_device)
        """

    def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/delete_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#delete_environment)
        """

    def deregister_device(
        self, **kwargs: Unpack[DeregisterDeviceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deregisters a thin client device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/deregister_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#deregister_device)
        """

    def get_device(
        self, **kwargs: Unpack[GetDeviceRequestRequestTypeDef]
    ) -> GetDeviceResponseTypeDef:
        """
        Returns information for a thin client device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/get_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#get_device)
        """

    def get_environment(
        self, **kwargs: Unpack[GetEnvironmentRequestRequestTypeDef]
    ) -> GetEnvironmentResponseTypeDef:
        """
        Returns information for an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/get_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#get_environment)
        """

    def get_software_set(
        self, **kwargs: Unpack[GetSoftwareSetRequestRequestTypeDef]
    ) -> GetSoftwareSetResponseTypeDef:
        """
        Returns information for a software set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/get_software_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#get_software_set)
        """

    def list_devices(
        self, **kwargs: Unpack[ListDevicesRequestRequestTypeDef]
    ) -> ListDevicesResponseTypeDef:
        """
        Returns a list of thin client devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/list_devices.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#list_devices)
        """

    def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsRequestRequestTypeDef]
    ) -> ListEnvironmentsResponseTypeDef:
        """
        Returns a list of environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/list_environments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#list_environments)
        """

    def list_software_sets(
        self, **kwargs: Unpack[ListSoftwareSetsRequestRequestTypeDef]
    ) -> ListSoftwareSetsResponseTypeDef:
        """
        Returns a list of software sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/list_software_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#list_software_sets)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes a tag or tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#untag_resource)
        """

    def update_device(
        self, **kwargs: Unpack[UpdateDeviceRequestRequestTypeDef]
    ) -> UpdateDeviceResponseTypeDef:
        """
        Updates a thin client device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/update_device.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#update_device)
        """

    def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentRequestRequestTypeDef]
    ) -> UpdateEnvironmentResponseTypeDef:
        """
        Updates an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/update_environment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#update_environment)
        """

    def update_software_set(
        self, **kwargs: Unpack[UpdateSoftwareSetRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates a software set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/update_software_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#update_software_set)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_devices"]
    ) -> ListDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_software_sets"]
    ) -> ListSoftwareSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-thin-client/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workspaces_thin_client/client/#get_paginator)
        """
