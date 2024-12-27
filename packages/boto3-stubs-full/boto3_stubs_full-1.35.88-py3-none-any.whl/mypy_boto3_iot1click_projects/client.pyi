"""
Type annotations for iot1click-projects service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iot1click_projects.client import IoT1ClickProjectsClient

    session = Session()
    client: IoT1ClickProjectsClient = session.client("iot1click-projects")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListPlacementsPaginator, ListProjectsPaginator
from .type_defs import (
    AssociateDeviceWithPlacementRequestRequestTypeDef,
    CreatePlacementRequestRequestTypeDef,
    CreateProjectRequestRequestTypeDef,
    DeletePlacementRequestRequestTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DescribePlacementRequestRequestTypeDef,
    DescribePlacementResponseTypeDef,
    DescribeProjectRequestRequestTypeDef,
    DescribeProjectResponseTypeDef,
    DisassociateDeviceFromPlacementRequestRequestTypeDef,
    GetDevicesInPlacementRequestRequestTypeDef,
    GetDevicesInPlacementResponseTypeDef,
    ListPlacementsRequestRequestTypeDef,
    ListPlacementsResponseTypeDef,
    ListProjectsRequestRequestTypeDef,
    ListProjectsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdatePlacementRequestRequestTypeDef,
    UpdateProjectRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("IoT1ClickProjectsClient",)

class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    InternalFailureException: type[BotocoreClientError]
    InvalidRequestException: type[BotocoreClientError]
    ResourceConflictException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    TooManyRequestsException: type[BotocoreClientError]

class IoT1ClickProjectsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects.html#IoT1ClickProjects.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoT1ClickProjectsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects.html#IoT1ClickProjects.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#generate_presigned_url)
        """

    def associate_device_with_placement(
        self, **kwargs: Unpack[AssociateDeviceWithPlacementRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Associates a physical device with a placement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/associate_device_with_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#associate_device_with_placement)
        """

    def create_placement(
        self, **kwargs: Unpack[CreatePlacementRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates an empty placement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/create_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#create_placement)
        """

    def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates an empty project with a placement template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/create_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#create_project)
        """

    def delete_placement(
        self, **kwargs: Unpack[DeletePlacementRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a placement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/delete_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#delete_placement)
        """

    def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/delete_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#delete_project)
        """

    def describe_placement(
        self, **kwargs: Unpack[DescribePlacementRequestRequestTypeDef]
    ) -> DescribePlacementResponseTypeDef:
        """
        Describes a placement in a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/describe_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#describe_placement)
        """

    def describe_project(
        self, **kwargs: Unpack[DescribeProjectRequestRequestTypeDef]
    ) -> DescribeProjectResponseTypeDef:
        """
        Returns an object describing a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/describe_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#describe_project)
        """

    def disassociate_device_from_placement(
        self, **kwargs: Unpack[DisassociateDeviceFromPlacementRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes a physical device from a placement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/disassociate_device_from_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#disassociate_device_from_placement)
        """

    def get_devices_in_placement(
        self, **kwargs: Unpack[GetDevicesInPlacementRequestRequestTypeDef]
    ) -> GetDevicesInPlacementResponseTypeDef:
        """
        Returns an object enumerating the devices in a placement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/get_devices_in_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#get_devices_in_placement)
        """

    def list_placements(
        self, **kwargs: Unpack[ListPlacementsRequestRequestTypeDef]
    ) -> ListPlacementsResponseTypeDef:
        """
        Lists the placement(s) of a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/list_placements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#list_placements)
        """

    def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestRequestTypeDef]
    ) -> ListProjectsResponseTypeDef:
        """
        Lists the AWS IoT 1-Click project(s) associated with your AWS account and
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/list_projects.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#list_projects)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata key/value pairs) which you have assigned to the
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Creates or modifies tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes one or more tags (metadata key/value pairs) from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#untag_resource)
        """

    def update_placement(
        self, **kwargs: Unpack[UpdatePlacementRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates a placement with the given attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/update_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#update_placement)
        """

    def update_project(
        self, **kwargs: Unpack[UpdateProjectRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates a project associated with your AWS account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/update_project.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#update_project)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_placements"]
    ) -> ListPlacementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_projects"]
    ) -> ListProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/client/#get_paginator)
        """
