from entities.queue import Queue
from repositories.core import BaseRepository


class QueueRepository(BaseRepository):
    _entitie = Queue

    def get(self, name) -> Queue:
        return super().get(name)