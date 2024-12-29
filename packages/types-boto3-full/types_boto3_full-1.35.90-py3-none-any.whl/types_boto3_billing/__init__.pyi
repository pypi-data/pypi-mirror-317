"""
Main interface for billing service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_billing import (
        BillingClient,
        Client,
        ListBillingViewsPaginator,
        ListSourceViewsForBillingViewPaginator,
    )

    session = Session()
    client: BillingClient = session.client("billing")

    list_billing_views_paginator: ListBillingViewsPaginator = client.get_paginator("list_billing_views")
    list_source_views_for_billing_view_paginator: ListSourceViewsForBillingViewPaginator = client.get_paginator("list_source_views_for_billing_view")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import BillingClient
from .paginator import ListBillingViewsPaginator, ListSourceViewsForBillingViewPaginator

Client = BillingClient

__all__ = (
    "BillingClient",
    "Client",
    "ListBillingViewsPaginator",
    "ListSourceViewsForBillingViewPaginator",
)
