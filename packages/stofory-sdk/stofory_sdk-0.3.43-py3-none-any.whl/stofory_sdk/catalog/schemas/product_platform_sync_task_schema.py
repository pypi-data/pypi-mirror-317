from datetime import datetime
from typing import Annotated, Dict, Any

from litestar.params import Parameter
from msgspec import Struct

from stofory_sdk.catalog.models.enums import SyncTaskStatus, SyncTaskType
from stofory_sdk.catalog.schemas import ProductPlatformResponse


class TaskMetaChange(Struct):
    table_name: str
    id: int
    operation: SyncTaskType


class TaskMeta(Struct):
    product_platform: ProductPlatformResponse
    changes: list[TaskMetaChange]


class ProductPlatformSyncTaskCreateRequest(Struct, forbid_unknown_fields=True):
    product_platform_id: Annotated[int, Parameter(title="Product Platform ID")]
    task_type: Annotated[
        SyncTaskType,
        Parameter(
            title="Task Type",
            description="The task type."
        )
    ]
    task_meta: Annotated[
        TaskMeta | None,
        Parameter(
            required=False,
            title="Task Meta",
            description="The task meta."
        )
    ]
    status: Annotated[
        SyncTaskStatus,
        Parameter(
            title="Status",
            description="The status."
        )
    ]
    routing_keys: Annotated[
        list[str],
        Parameter(
            title="Routing Keys",
            description="The consumer queue`s routing keys."
        )
    ] = []
    sub_statuses: Annotated[
        Dict[str, SyncTaskStatus],
        Parameter(
            title="Sub Statuses",
            description="The sub statuses."
        )
    ] = {}
    sub_infos: Annotated[
        Dict[str, str],
        Parameter(
            title="Sub Infos",
            description="The sub infos."
        )
    ] = {}
    info: Annotated[
        str | None,
        Parameter(
            required=False,
            title="Info",
            description="The info."
        )
    ] = None


class ProductPlatformSyncTaskUpdateRequest(Struct, forbid_unknown_fields=True):
    task_type: Annotated[
        SyncTaskType,
        Parameter(
            title="Task Type",
            description="The task type."
        )
    ]
    task_meta: Annotated[
        TaskMeta | None,
        Parameter(
            title="Task Meta",
            description="The task meta."
        )
    ]
    routing_keys: Annotated[
        list[str],
        Parameter(
            title="Routing Keys",
            description="The consumer queue`s routing keys."
        )
    ]
    sub_statuses: Annotated[
        Dict[str, SyncTaskStatus],
        Parameter(
            title="Sub Statuses",
            description="The sub statuses."
        )
    ]
    sub_infos: Annotated[
        Dict[str, str],
        Parameter(
            title="Sub Infos",
            description="The sub infos."
        )
    ]
    status: Annotated[
        SyncTaskStatus,
        Parameter(
            title="Status",
            description="The status."
        )
    ]
    info: Annotated[
        str | None,
        Parameter(
            title="Info",
            description="The info."
        )
    ]


class ProductPlatformSyncTaskResponse(Struct):
    id: Annotated[int, Parameter(title="ID")]
    product_platform_id: Annotated[int, Parameter(title="Product Platform ID")]
    task_type: Annotated[
        SyncTaskType,
        Parameter(
            title="Task Type",
            description="The task type."
        )
    ]
    task_meta: Annotated[
        TaskMeta | None,
        Parameter(
            title="Task Meta",
            description="The task meta."
        )
    ]
    routing_keys: Annotated[
        list[str],
        Parameter(
            title="Routing Keys",
            description="The consumer queue`s routing keys."
        )
    ]
    sub_statuses: Annotated[
        Dict[str, SyncTaskStatus],
        Parameter(
            title="Sub Statuses",
            description="The sub statuses."
        )
    ]
    sub_infos: Annotated[
        Dict[str, str],
        Parameter(
            title="Sub Infos",
            description="The sub infos."
        )
    ]
    status: Annotated[
        SyncTaskStatus,
        Parameter(
            title="Status",
            description="The status."
        )
    ]
    info: Annotated[
        str | None,
        Parameter(
            required=False,
            title="Info",
            description="The info."
        )
    ]

    created_at: Annotated[datetime, Parameter(title="Created At")]
    updated_at: Annotated[datetime, Parameter(title="Updated At")]
