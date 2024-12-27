"""
Main interface for socialmessaging service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_socialmessaging import (
        Client,
        EndUserMessagingSocialClient,
        ListLinkedWhatsAppBusinessAccountsPaginator,
    )

    session = get_session()
    async with session.create_client("socialmessaging") as client:
        client: EndUserMessagingSocialClient
        ...


    list_linked_whatsapp_business_accounts_paginator: ListLinkedWhatsAppBusinessAccountsPaginator = client.get_paginator("list_linked_whatsapp_business_accounts")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import EndUserMessagingSocialClient
from .paginator import ListLinkedWhatsAppBusinessAccountsPaginator

Client = EndUserMessagingSocialClient

__all__ = ("Client", "EndUserMessagingSocialClient", "ListLinkedWhatsAppBusinessAccountsPaginator")
