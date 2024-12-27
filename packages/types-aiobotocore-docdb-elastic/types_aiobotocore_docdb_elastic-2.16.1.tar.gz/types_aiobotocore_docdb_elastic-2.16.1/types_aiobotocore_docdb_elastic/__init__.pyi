"""
Main interface for docdb-elastic service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_docdb_elastic import (
        Client,
        DocDBElasticClient,
        ListClusterSnapshotsPaginator,
        ListClustersPaginator,
        ListPendingMaintenanceActionsPaginator,
    )

    session = get_session()
    async with session.create_client("docdb-elastic") as client:
        client: DocDBElasticClient
        ...


    list_cluster_snapshots_paginator: ListClusterSnapshotsPaginator = client.get_paginator("list_cluster_snapshots")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_pending_maintenance_actions_paginator: ListPendingMaintenanceActionsPaginator = client.get_paginator("list_pending_maintenance_actions")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import DocDBElasticClient
from .paginator import (
    ListClusterSnapshotsPaginator,
    ListClustersPaginator,
    ListPendingMaintenanceActionsPaginator,
)

Client = DocDBElasticClient

__all__ = (
    "Client",
    "DocDBElasticClient",
    "ListClusterSnapshotsPaginator",
    "ListClustersPaginator",
    "ListPendingMaintenanceActionsPaginator",
)
