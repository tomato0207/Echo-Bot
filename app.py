from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    MessagingApi,
    Configuration,
    ApiClient,
    ReplyMessageRequest,
    TextMessage,
    Emoji,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselColumn,
    CarouselTemplate,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    TextMessageContent
)

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@line_handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    text = event.message.text  # 取得使用者輸入的文字
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text == '指令':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="目前實作指令:\n嗨\n表情符號\n貼圖\n圖片\n影片\n音訊\n位置\n確認\n按鈕\n社群")]
                )
            )

        if text == '嗨':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="你好啊!")]
                )
            )
        elif text == '表情符號':
            emojis = [
                Emoji(index=0,productId="5ac21184040ab15980c9b43a",emojiId="007"),
                Emoji(index=7,productId="5ac21184040ab15980c9b43a",emojiId="007")
            ]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='$tomato$',emojis=emojis)]
                )
            )
        elif text == '貼圖':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[StickerMessage(package_id="789",stickerId="10855")]
                )
            )
        elif text == '圖片':
            url = request.url_root + '/static/head.png'
            url = url.replace("http","https")
            app.logger.info("url="+url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(originalContentUrl=url,previewImageUrl=url)
                    ]
                )
            )
        elif text == '影片':
            url = request.url_root + '/static/video.mp4'
            url = url.replace("http","https")
            app.logger.info("url="+url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        VideoMessage(originalContentUrl=url,previewImageUrl=url)
                    ]
                )
            )
        elif text == '音訊':
            url = request.url_root + '/static/music.mp3'
            url = url.replace("http","https")
            app.logger.info("url="+url)
            duration = 50000
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        AudioMessage(originalContentUrl=url,duration=duration)
                    ]
                )
            )
        elif text == '位置':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        LocationMessage(title='聯合大學',address="miaoli",latitude=24.539064469251663,longitude=120.79169716864828)
                    ]
                )
            )
        elif text == '確認':
            confirm_template = ConfirmTemplate(
                text='寫作業了沒',
                actions=[
                    MessageAction(label='是',text='是!'),
                    MessageAction(label='否',text='否!')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Confirm alt text',
                template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        elif text == '按鈕':
            url = request.url_root + '/static/head.png'
            url= url.replace("http","https")
            app.logger.info("url="+url)
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title='按鈕測試',
                text='回傳測試',
                actions=[
                    URIAction(label='連結',uri='https://www.facebook.com/todayplay'),
                    PostbackAction(label='回傳值',data='ping',displayText='傳了'),
                    MessageAction(label='傳"哈囉"',text='哈囉'),
                    DatetimePickerAction(label="選擇時間",data="時間",mode="datetime")
                ])
            template_message=TemplateMessage(
                alt_text="This is a button template",
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        elif text == '社群':
            url = request.url_root+'/static'
            url = url.replace("http","https")
            app.logger.info("url="+url)
            image_carousel_template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=url+'/facebook.jpg',
                        action=URIAction(
                            label='前往FB',
                            uri='https://www.facebook.com/todayplay'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=url+'/ig.jpg',
                        action=URIAction(
                            label='前往IG',
                            uri='https://www.instagram.com/tomato__0207/'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=url+'/youtube.png',
                        action=URIAction(
                            label='前往YT',
                            uri='https://www.youtube.com/@tomatopiano2121'
                        )
                    ),
                ]
            )

            image_carousel_message = TemplateMessage(
                alt_text='圖片輪播範本',
                template=image_carousel_template
            )

            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[image_carousel_message]
            ))
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@line_handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got {event.type} event')

if __name__ == "__main__":
    app.run(port=8000)
