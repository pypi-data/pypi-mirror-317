from ami_data_parser.entities import Peer


def get_peers(data: list) -> list:
    return [
        Peer(**item)
        for item in data
    ]