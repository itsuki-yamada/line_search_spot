from .search_spot import search_area_code, search_town


def callback_area_code(area_code: str) -> str:
    area = search_area_code(area_code)
    towns = search_town(area)
    list_towns = [town.name for town in towns]
    return ','.join(list_towns)
