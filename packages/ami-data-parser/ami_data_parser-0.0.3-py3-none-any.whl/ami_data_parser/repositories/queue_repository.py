from ami_data_parser.entities import Queue
from ami_data_parser.repositories import BaseRepository


class QueueRepository(BaseRepository):
    _entitie = Queue

    def get(self, name) -> Queue:
        return super().get(name)