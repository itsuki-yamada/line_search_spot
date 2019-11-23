import os
import random

import requests

from class_spot import AreaCode, Restaurant


def search_area_code(area_name: str) -> str:
    """
    Area_code_dbからAREA_CODEを取得する
    市町村名が入っていた場合は国土交通省APIを使用して取得をする
    :param area_name:
    :param str:
    :return: str
    """
    pref_dict = {'北海道': '01',
                 '青森県': '02',
                 '岩手県': '03',
                 '宮城県': '04',
                 '秋田県': '05',
                 '山形県': '06',
                 '福島県': '07',
                 '茨城県': '08',
                 '栃木県': '09',
                 '群馬県': '10',
                 '埼玉県': '11',
                 '千葉県': '12',
                 '東京都': '13',
                 '神奈川県': '14',
                 '新潟県': '15',
                 '富山県': '16',
                 '石川県': '17',
                 '福井県': '18',
                 '山梨県': '19',
                 '長野県': '20',
                 '岐阜県': '21',
                 '静岡県': '22',
                 '愛知県': '23',
                 '三重県': '24',
                 '滋賀県': '25',
                 '京都府': '26',
                 '大阪府': '27',
                 '兵庫県': '28',
                 '奈良県': '29',
                 '和歌山県': '30',
                 '鳥取県': '31',
                 '島根県': '32',
                 '岡山県': '33',
                 '広島県': '34',
                 '山口県': '35',
                 '徳島県': '36',
                 '香川県': '37',
                 '愛媛県': '38',
                 '高知県': '39',
                 '福岡県': '40',
                 '佐賀県': '41',
                 '長崎県': '42',
                 '熊本県': '43',
                 '大分県': '44',
                 '宮崎県': '45',
                 '鹿児島県': '46',
                 '沖縄県': '47'}
    return pref_dict[area_name]


def search_town(area_code: str) -> list:
    param = {'area': area_code}
    towns = requests.get('https://www.land.mlit.go.jp/webland/api/CitySearch?', params=param).json()['data']
    for town in towns:
        yield AreaCode(id=town['id'],
                       name=town['name'])


def search_local_spot(area_code='0', **kwargs):
    appid = os.environ['YAHOO_APPID']
    output = 'json'
    ac = area_code
    url = 'https://map.yahooapis.jp/search/local/V1/localSearch'
    sort = ['rating', 'score', 'hybrid', 'review', 'kana', 'price', 'dist', 'geo', 'match']

    # TODO:リファクタリングすべし
    # locationがあるときはparamを変更
    if 'lat' in kwargs['kwargs'] and 'lon' in kwargs['kwargs']:
        param = {'appid': appid,
                 'results': 30,
                 'output': output,
                 'device': 'mobile',
                 'gc': '01',
                 'sort': random.choice(sort),
                 'lat': kwargs['kwargs']['lat'],
                 'lon': kwargs['kwargs']['lon'],
                 'dist': 20,
                 # 'coupon': True
                 'image': True
                 }

    else:
        param = {'appid': appid,
                 'results': 30,
                 'output': output,
                 'ac': ac,
                 'device': 'mobile',
                 'gc': '01',
                 'sort': random.choice(sort)
                 }
    restaurants_dict = requests.get(url=url, params=param).json()
    if 'Feature' in restaurants_dict:
        for restaurant in restaurants_dict['Feature']:
            location = restaurant['Geometry']['Coordinates'].split(',')
            res = Restaurant(
                id=restaurant['Property']['Uid'],
                name=restaurant['Name'],
                ac=restaurant['Property']['GovernmentCode'],
                address=restaurant['Property']['Address'],
                lat=float(location[1]),
                lon=float(location[0]),
            )
            if 'Coupon' in restaurant['Property']:
                if len(restaurant['Property']['Coupon']) > 0:
                    res.edit_mobile_url(restaurant['Property']['Coupon'][0]['SmartPhoneUrl'])
                    res.edit_image(restaurant['Property']['Coupon'][0]['Image1'])
            if 'Station' in restaurant['Property']:
                if len(restaurant['Property']['Station']) > 0:
                    res.edit_access(restaurant['Property']['Station'][0])
            yield res
    else:
        return ['レストランが見つかりませんでした。']


def main():
    print(search_local_spot(kwargs={'lat': None, 'lon': None}))
    for spot in search_local_spot('0', kwargs={'lat': 39.928829, 'lon': 141.003034, }):
        print(spot.name)
        print(spot.lat)
        print(spot.lon)
        print(spot.image)


if __name__ == '__main__':
    main()
