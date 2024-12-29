"""
Type annotations for connectcases service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_connectcases.client import ConnectCasesClient
    from mypy_boto3_connectcases.paginator import (
        SearchCasesPaginator,
        SearchRelatedItemsPaginator,
    )

    session = Session()
    client: ConnectCasesClient = session.client("connectcases")

    search_cases_paginator: SearchCasesPaginator = client.get_paginator("search_cases")
    search_related_items_paginator: SearchRelatedItemsPaginator = client.get_paginator("search_related_items")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    SearchCasesRequestPaginateTypeDef,
    SearchCasesResponseTypeDef,
    SearchRelatedItemsRequestPaginateTypeDef,
    SearchRelatedItemsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SearchCasesPaginator", "SearchRelatedItemsPaginator")

if TYPE_CHECKING:
    _SearchCasesPaginatorBase = Paginator[SearchCasesResponseTypeDef]
else:
    _SearchCasesPaginatorBase = Paginator  # type: ignore[assignment]

class SearchCasesPaginator(_SearchCasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchCases.html#ConnectCases.Paginator.SearchCases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/#searchcasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchCasesRequestPaginateTypeDef]
    ) -> PageIterator[SearchCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchCases.html#ConnectCases.Paginator.SearchCases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/#searchcasespaginator)
        """

if TYPE_CHECKING:
    _SearchRelatedItemsPaginatorBase = Paginator[SearchRelatedItemsResponseTypeDef]
else:
    _SearchRelatedItemsPaginatorBase = Paginator  # type: ignore[assignment]

class SearchRelatedItemsPaginator(_SearchRelatedItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchRelatedItems.html#ConnectCases.Paginator.SearchRelatedItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/#searchrelateditemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchRelatedItemsRequestPaginateTypeDef]
    ) -> PageIterator[SearchRelatedItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchRelatedItems.html#ConnectCases.Paginator.SearchRelatedItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connectcases/paginators/#searchrelateditemspaginator)
        """
