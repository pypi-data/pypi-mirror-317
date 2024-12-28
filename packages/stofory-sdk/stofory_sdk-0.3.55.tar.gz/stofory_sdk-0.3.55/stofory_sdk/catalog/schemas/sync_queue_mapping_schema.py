from datetime import datetime
from typing import Annotated

from litestar.params import Parameter
from msgspec import Struct, Meta

from stofory_sdk.catalog.models.enums import SyncTaskType, SyncTaskPriority


class SyncQueueMappingCreateRequest(Struct, forbid_unknown_fields=True):
    priority: Annotated[SyncTaskPriority, Parameter(title="Priority", description="The priority of the sync task.")]
    consumer: Annotated[str, Parameter(title="Consumer Name", description="The prefix of the consumer."), Meta(min_length=1)]
    table_names: Annotated[list[str], Parameter(title="Table Names", description="The names of the tables."), Meta(min_length=1)]
    operation: Annotated[SyncTaskType, Parameter(title="Operation", description="The operation of the sync task.")]


class SyncQueueMappingUpdateRequest(Struct, forbid_unknown_fields=True):
    priority: Annotated[SyncTaskPriority, Parameter(title="Priority", description="The priority of the sync task.")]
    consumer: Annotated[str, Parameter(title="Consumer Name", description="The prefix of the consumer."), Meta(min_length=1)]
    table_names: Annotated[list[str], Parameter(title="Table Names", description="The names of the tables."), Meta(min_length=1)]
    operation: Annotated[SyncTaskType, Parameter(title="Operation", description="The operation of the sync task.")]


class SyncQueueMappingResponse(Struct):
    id: int
    priority: SyncTaskPriority
    consumer: str
    table_names: list[str]
    operation: SyncTaskType

    created_at: datetime
    updated_at: datetime
