from func.search_spot import search_area_code, search_town, search_local_spot


def callback_area_code(area_code: str) -> str:
    area = search_area_code(area_code)
    towns = search_town(area)
    list_towns = [town.name for town in towns]
    return ','.join(list_towns)


def callback_local_spot(area_code='0', **kwargs) -> str:
    if 'lat' in kwargs['kwargs'] and 'lon' in kwargs['kwargs']:
        restaurant_list = [res.name for res in search_local_spot(kwargs={'lat': kwargs['kwargs']['lat'],
                                                                         'lon': kwargs['kwargs']['lon']})]
    else:
        restaurant_list = {res.name for res in search_local_spot(area_code)}
    return '\n'.join(restaurant_list)


def main():
    area_name = '岩手県'
    area_code = callback_area_code(area_name)
    print(area_code)
    print(callback_local_spot(kwargs={'lat': 39.928829, 'lon': 141.003034}))


if __name__ == '__main__':
    main()
