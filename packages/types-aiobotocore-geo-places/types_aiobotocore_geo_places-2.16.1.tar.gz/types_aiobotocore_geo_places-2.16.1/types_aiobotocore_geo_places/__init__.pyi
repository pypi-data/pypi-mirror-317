"""
Main interface for geo-places service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_geo_places import (
        Client,
        LocationServicePlacesV2Client,
    )

    session = get_session()
    async with session.create_client("geo-places") as client:
        client: LocationServicePlacesV2Client
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LocationServicePlacesV2Client

Client = LocationServicePlacesV2Client

__all__ = ("Client", "LocationServicePlacesV2Client")
