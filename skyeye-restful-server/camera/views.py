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
from django.utils import timezone

db_logger = logging.getLogger('db')

# Create your views here.
class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
class CameraViewViewSet(viewsets.ModelViewSet):
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

            # 현재 서버의 KST(한국시간)를 가져옵니다. (예: 10시 05분 49초)
            local_time = timezone.localtime()
            
            # DB(외부 장비 등)에는 KST 시간이 timezone 없이 저장되지만, 
            # Django(USE_TZ=True)는 DB의 시간을 UTC로 취급하여 9시간의 오차가 발생하고 있었습니다.
            # 이를 해결하기 위해 KST 시간의 시/분/초 그대로를 UTC 객체로 덮어은워 쿼리에 사용합니다.
            db_current_time = local_time.replace(tzinfo=timezone.utc)
            db_threshold_time = db_current_time - timedelta(seconds=20)

            # 정확히 최근 20초 이내의 KST 시간에 생성된 데이터만 필터링
            latest_data = (self.queryset.filter(
                site_id=site, 
                date__gte=db_threshold_time,
                date__lte=db_current_time
            ).order_by('-date').first())
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
