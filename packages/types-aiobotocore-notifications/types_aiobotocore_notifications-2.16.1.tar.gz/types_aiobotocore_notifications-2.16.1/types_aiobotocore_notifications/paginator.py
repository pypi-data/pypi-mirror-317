"""
Type annotations for notifications service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_notifications.client import UserNotificationsClient
    from types_aiobotocore_notifications.paginator import (
        ListChannelsPaginator,
        ListEventRulesPaginator,
        ListNotificationConfigurationsPaginator,
        ListNotificationEventsPaginator,
        ListNotificationHubsPaginator,
    )

    session = get_session()
    with session.create_client("notifications") as client:
        client: UserNotificationsClient

        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_event_rules_paginator: ListEventRulesPaginator = client.get_paginator("list_event_rules")
        list_notification_configurations_paginator: ListNotificationConfigurationsPaginator = client.get_paginator("list_notification_configurations")
        list_notification_events_paginator: ListNotificationEventsPaginator = client.get_paginator("list_notification_events")
        list_notification_hubs_paginator: ListNotificationHubsPaginator = client.get_paginator("list_notification_hubs")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChannelsRequestPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListEventRulesRequestPaginateTypeDef,
    ListEventRulesResponseTypeDef,
    ListNotificationConfigurationsRequestPaginateTypeDef,
    ListNotificationConfigurationsResponseTypeDef,
    ListNotificationEventsRequestPaginateTypeDef,
    ListNotificationEventsResponseTypeDef,
    ListNotificationHubsRequestPaginateTypeDef,
    ListNotificationHubsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChannelsPaginator",
    "ListEventRulesPaginator",
    "ListNotificationConfigurationsPaginator",
    "ListNotificationEventsPaginator",
    "ListNotificationHubsPaginator",
)


if TYPE_CHECKING:
    _ListChannelsPaginatorBase = AioPaginator[ListChannelsResponseTypeDef]
else:
    _ListChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelsPaginator(_ListChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListChannels.html#UserNotifications.Paginator.ListChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listchannelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListChannels.html#UserNotifications.Paginator.ListChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listchannelspaginator)
        """


if TYPE_CHECKING:
    _ListEventRulesPaginatorBase = AioPaginator[ListEventRulesResponseTypeDef]
else:
    _ListEventRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventRulesPaginator(_ListEventRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListEventRules.html#UserNotifications.Paginator.ListEventRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listeventrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListEventRules.html#UserNotifications.Paginator.ListEventRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listeventrulespaginator)
        """


if TYPE_CHECKING:
    _ListNotificationConfigurationsPaginatorBase = AioPaginator[
        ListNotificationConfigurationsResponseTypeDef
    ]
else:
    _ListNotificationConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNotificationConfigurationsPaginator(_ListNotificationConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationConfigurations.html#UserNotifications.Paginator.ListNotificationConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationConfigurations.html#UserNotifications.Paginator.ListNotificationConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListNotificationEventsPaginatorBase = AioPaginator[ListNotificationEventsResponseTypeDef]
else:
    _ListNotificationEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNotificationEventsPaginator(_ListNotificationEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationEvents.html#UserNotifications.Paginator.ListNotificationEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationEvents.html#UserNotifications.Paginator.ListNotificationEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationeventspaginator)
        """


if TYPE_CHECKING:
    _ListNotificationHubsPaginatorBase = AioPaginator[ListNotificationHubsResponseTypeDef]
else:
    _ListNotificationHubsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNotificationHubsPaginator(_ListNotificationHubsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationHubs.html#UserNotifications.Paginator.ListNotificationHubs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationhubspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationHubsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationHubsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/paginator/ListNotificationHubs.html#UserNotifications.Paginator.ListNotificationHubs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/paginators/#listnotificationhubspaginator)
        """
