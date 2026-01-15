from django.http import JsonResponse, HttpResponse
from django_eventstream import send_event, get_current_event_id
from rest_framework import status
from rest_framework.authtoken.models import Token
import logging
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User

db_logger = logging.getLogger('db')


@csrf_exempt
def messages(request, channels_id):
    # if request.method == 'GET':
    #     event_count = get_current_event_id(['channels-{}'.format(channels_id)])
    #     print("channels_id: ", channels_id)
    #     print("event_count: ", event_count)
    #
    #     text = request.GET['text']
    #     print(text)
    #
    #     send_event('channels-{}'.format(channels_id), 'message', text)
    #     return HttpResponse(text, content_type='application/json')
    if request.method == 'POST':
        try:  # Apache 에서 문제 발생 원인 파악 X
            token = request.headers['Authorization'].split()
            if len(token) == 2:
                token_key = token[1]
            else:
                db_logger.exception("Token Null")
                return JsonResponse({"message": "Token Null"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                token = Token.objects.get(key=token_key)
            except Token.DoesNotExist as e:
                db_logger.exception(e)
                return JsonResponse({"message": "TOKEN_ERROR"}, status=status.HTTP_401_UNAUTHORIZED)

            if token.user != 'AnonyMousUser':
                user = User.objects.get(username=token.user)
                text = request.POST['text']
                send_event('channels-{}'.format(channels_id), 'message', text, user)

                return JsonResponse({'message': 'SEND_SUCCESS'}, status=status.HTTP_200_OK)
        except KeyError:
            db_logger.exception(KeyError)
            return JsonResponse({"message": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            db_logger.exception(e)
            return JsonResponse({"message": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
