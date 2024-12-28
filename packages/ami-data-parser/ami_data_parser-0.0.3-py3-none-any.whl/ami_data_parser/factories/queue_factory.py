from ami_data_parser.entities import Queue


def get_queues(data: list) -> list:
    return [
        Queue(**item)
        for item in data
    ]