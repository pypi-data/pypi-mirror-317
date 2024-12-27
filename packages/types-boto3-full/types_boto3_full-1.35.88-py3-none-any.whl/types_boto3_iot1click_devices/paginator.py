"""
Type annotations for iot1click-devices service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot1click_devices/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_iot1click_devices.client import IoT1ClickDevicesServiceClient
    from types_boto3_iot1click_devices.paginator import (
        ListDeviceEventsPaginator,
        ListDevicesPaginator,
    )

    session = Session()
    client: IoT1ClickDevicesServiceClient = session.client("iot1click-devices")

    list_device_events_paginator: ListDeviceEventsPaginator = client.get_paginator("list_device_events")
    list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDeviceEventsRequestPaginateTypeDef,
    ListDeviceEventsResponseTypeDef,
    ListDevicesRequestPaginateTypeDef,
    ListDevicesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListDeviceEventsPaginator", "ListDevicesPaginator")


if TYPE_CHECKING:
    _ListDeviceEventsPaginatorBase = Paginator[ListDeviceEventsResponseTypeDef]
else:
    _ListDeviceEventsPaginatorBase = Paginator  # type: ignore[assignment]


class ListDeviceEventsPaginator(_ListDeviceEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/paginator/ListDeviceEvents.html#IoT1ClickDevicesService.Paginator.ListDeviceEvents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot1click_devices/paginators/#listdeviceeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeviceEventsRequestPaginateTypeDef]
    ) -> PageIterator[ListDeviceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/paginator/ListDeviceEvents.html#IoT1ClickDevicesService.Paginator.ListDeviceEvents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot1click_devices/paginators/#listdeviceeventspaginator)
        """


if TYPE_CHECKING:
    _ListDevicesPaginatorBase = Paginator[ListDevicesResponseTypeDef]
else:
    _ListDevicesPaginatorBase = Paginator  # type: ignore[assignment]


class ListDevicesPaginator(_ListDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/paginator/ListDevices.html#IoT1ClickDevicesService.Paginator.ListDevices)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot1click_devices/paginators/#listdevicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicesRequestPaginateTypeDef]
    ) -> PageIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices/paginator/ListDevices.html#IoT1ClickDevicesService.Paginator.ListDevices.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot1click_devices/paginators/#listdevicespaginator)
        """
