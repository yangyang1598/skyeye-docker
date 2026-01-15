from .serializers import DetectionSerializer
from .models import Detection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import logging
from django.core.mail.message import EmailMessage
from server import settings
from accounts.models import User
from rest_framework.authtoken.models import Token
import datetime


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
                # print(token.user)
            except Token.DoesNotExist as e:
                db_logger.exception(e)
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            if not token.user.is_anonymous:
                user = User.objects.get(username=token.user)
                image = request.FILES['image']
                # print(image)
                # print(user.email)
                # print(image.name)
                # print(user.username)
                if user.username=="양진현" or user.username=="test_server":
                
                    mountain_name="백두"
                else:
                    mountain_name=" "
                
                detection_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                subject = "[화재 알림] 금일 {}경 {}산 산불 발생 img:{}".format(detection_time,mountain_name,image.name)
                to = [user.email]
                message = "금일 {}경 산불 발생".format(detection_time)
                try:
                    # mail = EmailMessage(subject=subject, body=message, to=to, from_email=settings.EMAIL_HOST_USER)
                    # mail.attach(image.name, image.read(), image.content_type)
                    # mail.send()
                    serializer.save(user=request.user)
                    db_logger.info("Detection data saved and email sent successfully to {}".format(user.email))

                except Exception as e:
                    # 실패 시 예외 로그 기록
                    db_logger.exception("Error during saving detection data and sending email: {}".format(e))
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(status=status.HTTP_201_CREATED)
            else:
                # 데이터 유효성 검사 실패 로그
                db_logger.warning("Invalid data received in detection request")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
