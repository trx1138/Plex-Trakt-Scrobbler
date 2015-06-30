from plugin.sync.core.task.state.plex_ import SyncStatePlex
from plugin.sync.core.task.state.trakt_ import SyncStateTrakt

import logging

log = logging.getLogger(__name__)


class SyncState(object):
    def __init__(self, task):
        self.task = task

        self.plex = SyncStatePlex(self)
        self.trakt = SyncStateTrakt(self)

    def flush(self):
        log.debug('Flushing caches...')

        self.trakt.flush()
