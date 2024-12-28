from entities.peer import Peer


def get_peers(data: list) -> list:
    return [
        Peer(**item)
        for item in data
    ]