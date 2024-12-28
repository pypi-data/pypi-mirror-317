from entities.peer import Peer
from repositories.core import BaseRepository


class PeerRepository(BaseRepository):
    _entitie = Peer

    def get(self, name) -> Peer:
        return super().get(name)