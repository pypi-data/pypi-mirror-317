from entities.queue import Queue


def get_queues(data: list) -> list:
    return [
        Queue(**item)
        for item in data
    ]