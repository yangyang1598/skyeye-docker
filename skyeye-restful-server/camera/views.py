from rest_framework import viewsets
from rest_framework.decorators import action
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

    @action(detail=False, methods=['delete'])
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


     # 최근 20초이내 최신 데이터를 반환
    def list(self, request, *args, **kwargs):
        try:
            site = request.query_params.get('site')

            if not site:
                return Response(
                    {"error": "site parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            site = int(site)
            threshold_time = now() - timedelta(seconds=20)

            latest_data = (self.queryset.filter(site_id=site, date__gte=threshold_time).order_by('-date').first())
            if not latest_data:
                return Response({"message": "No data found"}, status=status.HTTP_204_NO_CONTENT)

            serializer = self.get_serializer(latest_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            db_logger.exception(e)
            return Response(
                {"error": "Unable to retrieve data"},
                status=status.HTTP_400_BAD_REQUEST
            )
