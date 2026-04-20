from django_eventstream import send_event
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def messages(request, channels_id):

    text = request.data

    if not text:
        return Response({"message": "INVALID_PAYLOAD"}, status=400)

    send_event(channels_id, 'message', text, request.user)
    return Response({"message": "SEND_SUCCESS"})
