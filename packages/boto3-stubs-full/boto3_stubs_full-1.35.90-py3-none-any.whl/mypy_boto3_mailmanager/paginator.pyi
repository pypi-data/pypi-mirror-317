"""
Type annotations for mailmanager service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mailmanager.client import MailManagerClient
    from mypy_boto3_mailmanager.paginator import (
        ListAddonInstancesPaginator,
        ListAddonSubscriptionsPaginator,
        ListArchiveExportsPaginator,
        ListArchiveSearchesPaginator,
        ListArchivesPaginator,
        ListIngressPointsPaginator,
        ListRelaysPaginator,
        ListRuleSetsPaginator,
        ListTrafficPoliciesPaginator,
    )

    session = Session()
    client: MailManagerClient = session.client("mailmanager")

    list_addon_instances_paginator: ListAddonInstancesPaginator = client.get_paginator("list_addon_instances")
    list_addon_subscriptions_paginator: ListAddonSubscriptionsPaginator = client.get_paginator("list_addon_subscriptions")
    list_archive_exports_paginator: ListArchiveExportsPaginator = client.get_paginator("list_archive_exports")
    list_archive_searches_paginator: ListArchiveSearchesPaginator = client.get_paginator("list_archive_searches")
    list_archives_paginator: ListArchivesPaginator = client.get_paginator("list_archives")
    list_ingress_points_paginator: ListIngressPointsPaginator = client.get_paginator("list_ingress_points")
    list_relays_paginator: ListRelaysPaginator = client.get_paginator("list_relays")
    list_rule_sets_paginator: ListRuleSetsPaginator = client.get_paginator("list_rule_sets")
    list_traffic_policies_paginator: ListTrafficPoliciesPaginator = client.get_paginator("list_traffic_policies")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAddonInstancesRequestPaginateTypeDef,
    ListAddonInstancesResponseTypeDef,
    ListAddonSubscriptionsRequestPaginateTypeDef,
    ListAddonSubscriptionsResponseTypeDef,
    ListArchiveExportsRequestPaginateTypeDef,
    ListArchiveExportsResponseTypeDef,
    ListArchiveSearchesRequestPaginateTypeDef,
    ListArchiveSearchesResponseTypeDef,
    ListArchivesRequestPaginateTypeDef,
    ListArchivesResponseTypeDef,
    ListIngressPointsRequestPaginateTypeDef,
    ListIngressPointsResponseTypeDef,
    ListRelaysRequestPaginateTypeDef,
    ListRelaysResponseTypeDef,
    ListRuleSetsRequestPaginateTypeDef,
    ListRuleSetsResponseTypeDef,
    ListTrafficPoliciesRequestPaginateTypeDef,
    ListTrafficPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAddonInstancesPaginator",
    "ListAddonSubscriptionsPaginator",
    "ListArchiveExportsPaginator",
    "ListArchiveSearchesPaginator",
    "ListArchivesPaginator",
    "ListIngressPointsPaginator",
    "ListRelaysPaginator",
    "ListRuleSetsPaginator",
    "ListTrafficPoliciesPaginator",
)

if TYPE_CHECKING:
    _ListAddonInstancesPaginatorBase = Paginator[ListAddonInstancesResponseTypeDef]
else:
    _ListAddonInstancesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAddonInstancesPaginator(_ListAddonInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonInstances.html#MailManager.Paginator.ListAddonInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listaddoninstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAddonInstancesRequestPaginateTypeDef]
    ) -> PageIterator[ListAddonInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonInstances.html#MailManager.Paginator.ListAddonInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listaddoninstancespaginator)
        """

if TYPE_CHECKING:
    _ListAddonSubscriptionsPaginatorBase = Paginator[ListAddonSubscriptionsResponseTypeDef]
else:
    _ListAddonSubscriptionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAddonSubscriptionsPaginator(_ListAddonSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonSubscriptions.html#MailManager.Paginator.ListAddonSubscriptions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listaddonsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAddonSubscriptionsRequestPaginateTypeDef]
    ) -> PageIterator[ListAddonSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonSubscriptions.html#MailManager.Paginator.ListAddonSubscriptions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listaddonsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _ListArchiveExportsPaginatorBase = Paginator[ListArchiveExportsResponseTypeDef]
else:
    _ListArchiveExportsPaginatorBase = Paginator  # type: ignore[assignment]

class ListArchiveExportsPaginator(_ListArchiveExportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveExports.html#MailManager.Paginator.ListArchiveExports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listarchiveexportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArchiveExportsRequestPaginateTypeDef]
    ) -> PageIterator[ListArchiveExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveExports.html#MailManager.Paginator.ListArchiveExports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listarchiveexportspaginator)
        """

if TYPE_CHECKING:
    _ListArchiveSearchesPaginatorBase = Paginator[ListArchiveSearchesResponseTypeDef]
else:
    _ListArchiveSearchesPaginatorBase = Paginator  # type: ignore[assignment]

class ListArchiveSearchesPaginator(_ListArchiveSearchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveSearches.html#MailManager.Paginator.ListArchiveSearches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listarchivesearchespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArchiveSearchesRequestPaginateTypeDef]
    ) -> PageIterator[ListArchiveSearchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveSearches.html#MailManager.Paginator.ListArchiveSearches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listarchivesearchespaginator)
        """

if TYPE_CHECKING:
    _ListArchivesPaginatorBase = Paginator[ListArchivesResponseTypeDef]
else:
    _ListArchivesPaginatorBase = Paginator  # type: ignore[assignment]

class ListArchivesPaginator(_ListArchivesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchives.html#MailManager.Paginator.ListArchives)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listarchivespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArchivesRequestPaginateTypeDef]
    ) -> PageIterator[ListArchivesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchives.html#MailManager.Paginator.ListArchives.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listarchivespaginator)
        """

if TYPE_CHECKING:
    _ListIngressPointsPaginatorBase = Paginator[ListIngressPointsResponseTypeDef]
else:
    _ListIngressPointsPaginatorBase = Paginator  # type: ignore[assignment]

class ListIngressPointsPaginator(_ListIngressPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListIngressPoints.html#MailManager.Paginator.ListIngressPoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listingresspointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngressPointsRequestPaginateTypeDef]
    ) -> PageIterator[ListIngressPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListIngressPoints.html#MailManager.Paginator.ListIngressPoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listingresspointspaginator)
        """

if TYPE_CHECKING:
    _ListRelaysPaginatorBase = Paginator[ListRelaysResponseTypeDef]
else:
    _ListRelaysPaginatorBase = Paginator  # type: ignore[assignment]

class ListRelaysPaginator(_ListRelaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRelays.html#MailManager.Paginator.ListRelays)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listrelayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRelaysRequestPaginateTypeDef]
    ) -> PageIterator[ListRelaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRelays.html#MailManager.Paginator.ListRelays.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listrelayspaginator)
        """

if TYPE_CHECKING:
    _ListRuleSetsPaginatorBase = Paginator[ListRuleSetsResponseTypeDef]
else:
    _ListRuleSetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListRuleSetsPaginator(_ListRuleSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRuleSets.html#MailManager.Paginator.ListRuleSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listrulesetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleSetsRequestPaginateTypeDef]
    ) -> PageIterator[ListRuleSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRuleSets.html#MailManager.Paginator.ListRuleSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listrulesetspaginator)
        """

if TYPE_CHECKING:
    _ListTrafficPoliciesPaginatorBase = Paginator[ListTrafficPoliciesResponseTypeDef]
else:
    _ListTrafficPoliciesPaginatorBase = Paginator  # type: ignore[assignment]

class ListTrafficPoliciesPaginator(_ListTrafficPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListTrafficPolicies.html#MailManager.Paginator.ListTrafficPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listtrafficpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrafficPoliciesRequestPaginateTypeDef]
    ) -> PageIterator[ListTrafficPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListTrafficPolicies.html#MailManager.Paginator.ListTrafficPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mailmanager/paginators/#listtrafficpoliciespaginator)
        """
