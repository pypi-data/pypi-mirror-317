"""
Main interface for notifications service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_notifications import (
        Client,
        ListChannelsPaginator,
        ListEventRulesPaginator,
        ListNotificationConfigurationsPaginator,
        ListNotificationEventsPaginator,
        ListNotificationHubsPaginator,
        UserNotificationsClient,
    )

    session = get_session()
    async with session.create_client("notifications") as client:
        client: UserNotificationsClient
        ...


    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_event_rules_paginator: ListEventRulesPaginator = client.get_paginator("list_event_rules")
    list_notification_configurations_paginator: ListNotificationConfigurationsPaginator = client.get_paginator("list_notification_configurations")
    list_notification_events_paginator: ListNotificationEventsPaginator = client.get_paginator("list_notification_events")
    list_notification_hubs_paginator: ListNotificationHubsPaginator = client.get_paginator("list_notification_hubs")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import UserNotificationsClient
from .paginator import (
    ListChannelsPaginator,
    ListEventRulesPaginator,
    ListNotificationConfigurationsPaginator,
    ListNotificationEventsPaginator,
    ListNotificationHubsPaginator,
)

Client = UserNotificationsClient

__all__ = (
    "Client",
    "ListChannelsPaginator",
    "ListEventRulesPaginator",
    "ListNotificationConfigurationsPaginator",
    "ListNotificationEventsPaginator",
    "ListNotificationHubsPaginator",
    "UserNotificationsClient",
)
