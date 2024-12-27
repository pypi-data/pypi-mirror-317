"""
Main interface for invoicing service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_invoicing import (
        Client,
        InvoicingClient,
        ListInvoiceUnitsPaginator,
    )

    session = get_session()
    async with session.create_client("invoicing") as client:
        client: InvoicingClient
        ...


    list_invoice_units_paginator: ListInvoiceUnitsPaginator = client.get_paginator("list_invoice_units")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import InvoicingClient
from .paginator import ListInvoiceUnitsPaginator

Client = InvoicingClient


__all__ = ("Client", "InvoicingClient", "ListInvoiceUnitsPaginator")
