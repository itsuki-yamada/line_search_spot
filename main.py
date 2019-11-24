import ast
import os
import random

import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage, LocationSendMessage, RichMenu, \
    RichMenuSize, RichMenuArea, RichMenuBounds, URIAction, Action, LocationAction

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route('/')
def index():
    return 'You call index()'


@app.route('/push_sample')
def push_sample():
    from func.search_spot import search_local_spot
    """プッシュメッセージを送る"""
    user_id = os.environ['USER_ID']
    line_bot_api.push_message(user_id, TextSendMessage(text='Hello World!'))
    spot = search_local_spot(kwargs={'lat': 39.928829, 'lon': 141.003034, })
    line_bot_api.push_message(user_id, LocationSendMessage(type="location",
                                                           title=spot.name,
                                                           address=spot.address,
                                                           latitude=spot.lat,
                                                           longitude=spot.lon
                                                           ))

    return 'OK'


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    from func.search_spot import search_area_code, search_local_spot
    area_code = search_area_code(event.message.text)
    spot = random.choice([town for town in search_local_spot(area_code)])

    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=f'{event.message.text}'
                                                    f'{event.message.id}\n'
                                               ),
                               TextSendMessage(text=f'******市町村******\n'
                                                    f'{area_code}\n'),
                               TextSendMessage(text=f'******レストラン******\n'
                                                    f'{spot}'))


@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    from func.search_spot import search_local_spot
    location_dict = ast.literal_eval(str(event.message))
    spots = search_local_spot(kwargs={'lat': location_dict['latitude'], 'lon': location_dict["longitude"]})
    spot = random.choice([sp for sp in spots])

    line_bot_api.reply_message(event.reply_token,
                               LocationSendMessage(type="location",
                                                   title=spot.name,
                                                   address=spot.address,
                                                   latitude=spot.lat,
                                                   longitude=spot.lon
                                                   ))


@app.route('/richmenu', methods=['GET'])
def rich_menu():
    text_dict = {'type': 'location', 'label': 'location'}

    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=True,
        name="rich_menu",
        chat_bar_text="Tap here",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=1250, height=1686),
                action=LocationAction(**text_dict)
            )
            # RichMenuArea(
            #     bounds=RichMenuBounds(x=1250, y=0, width=1250, height=1686),
            #     action=URIAction(label='Go to line.me', uri='https://line.me'))
        ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    # url = 'https://api.line.me/v2/bot/richmenu'
    # header = {'Authorization': os.environ['ACCESS_TOKEN'], 'Content-Type': 'json'}
    # res = requests.post(url=url, headers=header,data=rich_menu_id)
    with open('line_rich_menu.001.jpeg', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, 'image/jpeg', f)
    # content = line_bot_api.get_rich_menu_image( rich_menu_id)
    # with open('.', 'wb') as fd:
    #     for chunk in content.iter_content():
    #         fd.write(chunk)
    requests.delete('https://api.line.me/v2/bot/user/all/richmenu')
    line_bot_api.set_default_rich_menu(rich_menu_id)
    print(rich_menu_id)
    print(rich_menu_to_create)

    return 'hoge'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
