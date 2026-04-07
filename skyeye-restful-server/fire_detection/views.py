from .serializers import DetectionSerializer
from .models import Detection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import logging
from django.core.mail.message import EmailMessage
from server import settings
from skyeye.models import Site
from rest_framework.authtoken.models import Token
import datetime
from django_eventstream import send_event
import json

db_logger = logging.getLogger('db')


class DetectionView(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = request.headers['Authorization'].split()
            
            if len(token) == 2:
                token_key = token[1]
            else:
                db_logger.exception("Token Null")
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            try:
                token = Token.objects.get(key=token_key)

            except Token.DoesNotExist as e:
                db_logger.exception(e)
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            if not token.user.is_anonymous:
                user = token.user
                try:
                    
                    serializer.save()
                    
                except Exception as e:
                    # 실패 시 예외 로그 기록
                    db_logger.exception("Error during saving detection data and sending email: {}".format(e))
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(status=status.HTTP_201_CREATED)
            else:
                # 데이터 유효성 검사 실패 로그
                db_logger.warning("Invalid data received in detection request")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
