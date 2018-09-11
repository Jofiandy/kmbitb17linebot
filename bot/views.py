from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()
        except LineBotApiError:
            return HttpResponseBadRequest()

        return HttpResponse()

OtherMessage = 'Maaf Keyword yang Anda input tidak valid'

def reply_message(event, reply):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if (text.lower() == 'hai'):
        reply_message(event, 'It works')
    else:
        reply_message(event, OtherMessage)