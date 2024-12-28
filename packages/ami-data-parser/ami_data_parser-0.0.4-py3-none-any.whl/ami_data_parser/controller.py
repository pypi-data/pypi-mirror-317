from ami_data_parser.entities.queue import Queue
from ami_data_parser.factories.peer_factory import get_peers
from ami_data_parser.factories.queue_factory import get_queues
from ami_data_parser.parser.hint_parser import HintParser
from ami_data_parser.parser.queue_parser import QueueParser
from ami_data_parser.repositories.peer_repository import PeerRepository
from ami_data_parser.repositories.queue_repository import QueueRepository


class Controller:

    def __init__(self):
        self._hint_parser = HintParser()
        self._queue_parser = QueueParser()
        self._peer_repository = PeerRepository()
        self._queue_repository = QueueRepository()

    def get(self, entity_key: str, entity_type: str):

        if entity_type == 'peer':
            return self._peer_repository.get(entity_key)
        
        elif entity_type == 'queue':
            return self._queue_repository.get(entity_key)
        
        raise TypeError(f'Invalid type: {entity_type}')

    def peer_update(self, received_data: list) -> list:
        data = []
        parser_data = self._hint_parser.get_data(received_data)
        peers_data = get_peers(parser_data)
        self._peer_repository.set(
            peers_data
        )
        peers_diff = self._peer_repository.diff()

        for peer, event in peers_diff:
            
            if event == 'removed':
                peer_dict = {'peername': peer, 'type': 'peer'}
            
            else:
                peer_dict = vars(self._peer_repository.get(peer))
            
            peer_dict['event'] = event
            data.append(peer_dict)
        
            
        return data

    def queue_update(self, received_data: list) -> list:
        data = []
        parser_data = self._queue_parser.get_data(received_data)
        queues_data = get_queues(parser_data)
        self._queue_repository.set(
            queues_data
        )
        queues_diff = self._queue_repository.diff()

        for queue, event in queues_diff:

            if event == 'removed':
                queue_dict = {'queuename': queue, 'type': 'queue'}
            
            else:
                queue_data: Queue = self._queue_repository.get(queue)
                queue_dict = queue_data.get_dict()

            queue_dict['event'] = event
            data.append(queue_dict)
        
        return data
        