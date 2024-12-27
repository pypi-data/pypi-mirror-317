"""
Main interface for geo-routes service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_geo_routes import (
        Client,
        LocationServiceRoutesV2Client,
    )

    session = get_session()
    async with session.create_client("geo-routes") as client:
        client: LocationServiceRoutesV2Client
        ...

    ```

Copyright 2024 Vlad Emelianov
"""

from .client import LocationServiceRoutesV2Client

Client = LocationServiceRoutesV2Client


__all__ = ("Client", "LocationServiceRoutesV2Client")
