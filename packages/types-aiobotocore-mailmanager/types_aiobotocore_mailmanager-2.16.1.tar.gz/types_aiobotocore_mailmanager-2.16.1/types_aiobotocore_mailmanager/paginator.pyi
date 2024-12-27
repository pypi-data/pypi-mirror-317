"""
Type annotations for mailmanager service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mailmanager.client import MailManagerClient
    from types_aiobotocore_mailmanager.paginator import (
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

    session = get_session()
    with session.create_client("mailmanager") as client:
        client: MailManagerClient

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

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _ListAddonInstancesPaginatorBase = AioPaginator[ListAddonInstancesResponseTypeDef]
else:
    _ListAddonInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAddonInstancesPaginator(_ListAddonInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonInstances.html#MailManager.Paginator.ListAddonInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listaddoninstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAddonInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAddonInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonInstances.html#MailManager.Paginator.ListAddonInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listaddoninstancespaginator)
        """

if TYPE_CHECKING:
    _ListAddonSubscriptionsPaginatorBase = AioPaginator[ListAddonSubscriptionsResponseTypeDef]
else:
    _ListAddonSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAddonSubscriptionsPaginator(_ListAddonSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonSubscriptions.html#MailManager.Paginator.ListAddonSubscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listaddonsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAddonSubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAddonSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListAddonSubscriptions.html#MailManager.Paginator.ListAddonSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listaddonsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _ListArchiveExportsPaginatorBase = AioPaginator[ListArchiveExportsResponseTypeDef]
else:
    _ListArchiveExportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListArchiveExportsPaginator(_ListArchiveExportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveExports.html#MailManager.Paginator.ListArchiveExports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchiveexportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArchiveExportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListArchiveExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveExports.html#MailManager.Paginator.ListArchiveExports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchiveexportspaginator)
        """

if TYPE_CHECKING:
    _ListArchiveSearchesPaginatorBase = AioPaginator[ListArchiveSearchesResponseTypeDef]
else:
    _ListArchiveSearchesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListArchiveSearchesPaginator(_ListArchiveSearchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveSearches.html#MailManager.Paginator.ListArchiveSearches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchivesearchespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArchiveSearchesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListArchiveSearchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchiveSearches.html#MailManager.Paginator.ListArchiveSearches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchivesearchespaginator)
        """

if TYPE_CHECKING:
    _ListArchivesPaginatorBase = AioPaginator[ListArchivesResponseTypeDef]
else:
    _ListArchivesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListArchivesPaginator(_ListArchivesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchives.html#MailManager.Paginator.ListArchives)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchivespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArchivesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListArchivesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListArchives.html#MailManager.Paginator.ListArchives.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listarchivespaginator)
        """

if TYPE_CHECKING:
    _ListIngressPointsPaginatorBase = AioPaginator[ListIngressPointsResponseTypeDef]
else:
    _ListIngressPointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIngressPointsPaginator(_ListIngressPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListIngressPoints.html#MailManager.Paginator.ListIngressPoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listingresspointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngressPointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIngressPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListIngressPoints.html#MailManager.Paginator.ListIngressPoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listingresspointspaginator)
        """

if TYPE_CHECKING:
    _ListRelaysPaginatorBase = AioPaginator[ListRelaysResponseTypeDef]
else:
    _ListRelaysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRelaysPaginator(_ListRelaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRelays.html#MailManager.Paginator.ListRelays)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listrelayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRelaysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRelaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRelays.html#MailManager.Paginator.ListRelays.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listrelayspaginator)
        """

if TYPE_CHECKING:
    _ListRuleSetsPaginatorBase = AioPaginator[ListRuleSetsResponseTypeDef]
else:
    _ListRuleSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRuleSetsPaginator(_ListRuleSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRuleSets.html#MailManager.Paginator.ListRuleSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listrulesetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRuleSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListRuleSets.html#MailManager.Paginator.ListRuleSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listrulesetspaginator)
        """

if TYPE_CHECKING:
    _ListTrafficPoliciesPaginatorBase = AioPaginator[ListTrafficPoliciesResponseTypeDef]
else:
    _ListTrafficPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrafficPoliciesPaginator(_ListTrafficPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListTrafficPolicies.html#MailManager.Paginator.ListTrafficPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listtrafficpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrafficPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrafficPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/paginator/ListTrafficPolicies.html#MailManager.Paginator.ListTrafficPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/paginators/#listtrafficpoliciespaginator)
        """
