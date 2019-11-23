import ast
import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage, LocationSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route('/')
def index():
    return 'You call index()'


from func.search_spot import search_local_spot
@app.route('/push_sample')
def push_sample():
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
    from func.main import callback_area_code, callback_local_spot
    area_code = callback_area_code(event.message.text)
    spot = callback_local_spot(area_code)

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
    for spot in spots:
        # line_bot_api.reply_message(event.reply_token,
        #                            TextSendMessage(text=f'{spot.name}'
        #                                                 f'{spots}'
        #                                            ))

        line_bot_api.reply_message(event.reply_token,
                                   LocationSendMessage(type="location",
                                                       title=spot.name,
                                                       address=spot.address,
                                                       latitude=spot.lat,
                                                       longitude=spot.lon
                                                       ))


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
