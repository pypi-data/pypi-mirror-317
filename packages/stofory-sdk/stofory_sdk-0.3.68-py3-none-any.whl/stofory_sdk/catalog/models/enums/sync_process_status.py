import enum


class SyncProcessStatus(enum.Enum):
    NOT_EXTERNAL = 'PLATFORM IS NOT EXTERNAL'
    NOT_SYNCED = 'NOT SYNCED'
    SYNCED = 'SYNCED'
    SYNCING = 'SYNCING'
    FAILED = 'FAILED'
