"""
Type annotations for iot1click-projects service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iot1click_projects.client import IoT1ClickProjectsClient
    from mypy_boto3_iot1click_projects.paginator import (
        ListPlacementsPaginator,
        ListProjectsPaginator,
    )

    session = Session()
    client: IoT1ClickProjectsClient = session.client("iot1click-projects")

    list_placements_paginator: ListPlacementsPaginator = client.get_paginator("list_placements")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListPlacementsRequestPaginateTypeDef,
    ListPlacementsResponseTypeDef,
    ListProjectsRequestPaginateTypeDef,
    ListProjectsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListPlacementsPaginator", "ListProjectsPaginator")


if TYPE_CHECKING:
    _ListPlacementsPaginatorBase = Paginator[ListPlacementsResponseTypeDef]
else:
    _ListPlacementsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPlacementsPaginator(_ListPlacementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/paginator/ListPlacements.html#IoT1ClickProjects.Paginator.ListPlacements)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/paginators/#listplacementspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlacementsRequestPaginateTypeDef]
    ) -> PageIterator[ListPlacementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/paginator/ListPlacements.html#IoT1ClickProjects.Paginator.ListPlacements.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/paginators/#listplacementspaginator)
        """


if TYPE_CHECKING:
    _ListProjectsPaginatorBase = Paginator[ListProjectsResponseTypeDef]
else:
    _ListProjectsPaginatorBase = Paginator  # type: ignore[assignment]


class ListProjectsPaginator(_ListProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/paginator/ListProjects.html#IoT1ClickProjects.Paginator.ListProjects)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/paginators/#listprojectspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectsRequestPaginateTypeDef]
    ) -> PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-projects/paginator/ListProjects.html#IoT1ClickProjects.Paginator.ListProjects.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot1click_projects/paginators/#listprojectspaginator)
        """
