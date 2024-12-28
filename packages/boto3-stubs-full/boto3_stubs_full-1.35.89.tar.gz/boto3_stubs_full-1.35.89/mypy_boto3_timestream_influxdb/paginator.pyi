"""
Type annotations for timestream-influxdb service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_timestream_influxdb.client import TimestreamInfluxDBClient
    from mypy_boto3_timestream_influxdb.paginator import (
        ListDbInstancesPaginator,
        ListDbParameterGroupsPaginator,
    )

    session = Session()
    client: TimestreamInfluxDBClient = session.client("timestream-influxdb")

    list_db_instances_paginator: ListDbInstancesPaginator = client.get_paginator("list_db_instances")
    list_db_parameter_groups_paginator: ListDbParameterGroupsPaginator = client.get_paginator("list_db_parameter_groups")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDbInstancesInputPaginateTypeDef,
    ListDbInstancesOutputTypeDef,
    ListDbParameterGroupsInputPaginateTypeDef,
    ListDbParameterGroupsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDbInstancesPaginator", "ListDbParameterGroupsPaginator")

if TYPE_CHECKING:
    _ListDbInstancesPaginatorBase = Paginator[ListDbInstancesOutputTypeDef]
else:
    _ListDbInstancesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDbInstancesPaginator(_ListDbInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbInstances.html#TimestreamInfluxDB.Paginator.ListDbInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/paginators/#listdbinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbInstancesInputPaginateTypeDef]
    ) -> PageIterator[ListDbInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbInstances.html#TimestreamInfluxDB.Paginator.ListDbInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/paginators/#listdbinstancespaginator)
        """

if TYPE_CHECKING:
    _ListDbParameterGroupsPaginatorBase = Paginator[ListDbParameterGroupsOutputTypeDef]
else:
    _ListDbParameterGroupsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDbParameterGroupsPaginator(_ListDbParameterGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbParameterGroups.html#TimestreamInfluxDB.Paginator.ListDbParameterGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/paginators/#listdbparametergroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDbParameterGroupsInputPaginateTypeDef]
    ) -> PageIterator[ListDbParameterGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb/paginator/ListDbParameterGroups.html#TimestreamInfluxDB.Paginator.ListDbParameterGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_influxdb/paginators/#listdbparametergroupspaginator)
        """
