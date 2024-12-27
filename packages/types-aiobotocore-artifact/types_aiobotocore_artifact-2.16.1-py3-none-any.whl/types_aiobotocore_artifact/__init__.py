"""
Main interface for artifact service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_artifact import (
        ArtifactClient,
        Client,
        ListCustomerAgreementsPaginator,
        ListReportsPaginator,
    )

    session = get_session()
    async with session.create_client("artifact") as client:
        client: ArtifactClient
        ...


    list_customer_agreements_paginator: ListCustomerAgreementsPaginator = client.get_paginator("list_customer_agreements")
    list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import ArtifactClient
from .paginator import ListCustomerAgreementsPaginator, ListReportsPaginator

Client = ArtifactClient


__all__ = ("ArtifactClient", "Client", "ListCustomerAgreementsPaginator", "ListReportsPaginator")
