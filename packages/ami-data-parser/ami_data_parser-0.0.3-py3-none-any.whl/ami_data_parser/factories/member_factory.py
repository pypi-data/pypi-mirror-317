from ami_data_parser.entities import Member


def get_members(data: list) -> list:
    return [
        Member(**item)
        for item in data
    ]