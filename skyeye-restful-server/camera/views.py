from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db.models import Q
import logging

db_logger = logging.getLogger('db')


# Create your views here.
class CameraViewSet(viewsets.ModelViewSet):
    queryset = CameraView.objects.all()
    serializer_class = CameraViewSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            # 만약 `request.data['site']`가 필요하다면, 비어있을 때 에러 발생 가능
            site = request.data.get('site')  # 안전하게 가져오기
            if site:
                data = CameraView.objects.filter(site=site)
                data.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                # 기본 처리 (전체 삭제)
                CameraView.objects.all().delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


     # 최근 18초 데이터를 반환
    def list(self, request, *args, **kwargs):
        try:
            ten_seconds_ago = now() - timedelta(seconds=18)
            # 필드 이름을 `date`로 변경
            recent_data = self.queryset.filter(date__gte=ten_seconds_ago)
            serializer = self.get_serializer(recent_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            db_logger.exception(e)
            return Response({"error": "Unable to retrieve data"}, status=status.HTTP_400_BAD_REQUEST)

