from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from datetime import timedelta
from .serializers import *
from .models import *
from skyeye.models import *
from winch.models import *
from notification.send import warning_notification, job_daily_notification #, site_winch_temperature

import logging
import math
import time

db_logger = logging.getLogger('db')

# Create your views here.
class MissionDeviceViewSet(viewsets.ModelViewSet):
    queryset = Missiondevice.objects.all()
    serializer_class = MissionDeviceSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("임무장비", serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            name = request.GET['name']
            data = Missiondevice.objects.filter(serial_number=name).last()
            if data != None:
                serializer = MissionDeviceSerializer(data)
                # print("임무장비 데이터 GCS 전송", serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                db_logger.exception(status.HTTP_404_NOT_FOUND)
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


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

class MissionDeviceDataLogViewSet(viewsets.ModelViewSet):
    queryset = MissiondeviceDataLog.objects.all()
    serializer_class = MissionDeviceDataLogSerializer
    global warning_notification_send_time,queryset_site
    warning_notification_send_time = {}
    queryset_site = Site.objects.values_list('name', 'missiondevice_serial_number')
    print(queryset_site)
    for site in queryset_site:
        warning_notification_send_time[site[0]] = time.time()
        #if not site[0] in site_winch_temperature:
        #    morning_9am = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
        #    data = WinchDataLog.objects.filter(winch_serial_number=site[1], temperature__isnull=False, pressure__isnull=False, date__gte = morning_9am - timedelta(minutes=5)).last()
        #    site_winch_temperature[site[0]] = data.temperature if data != None else None
        #    print(f'site_winch_temperature[{site[0]}] = {site_winch_temperature[site[0]]}')

    def create(self, request):
        global warning_notification_send_time
        #global site_winch_temperature
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                pressure = data.get('pressure')
                site = Site.objects.filter(missiondevice_serial_number=data.get('missiondevice_serial_number'), winch_serial_number__isnull=False).last()
                
                if pressure != None and site != None :
                    winchDataLog = WinchDataLog.objects.filter(winch_serial_number=site.winch_serial_number, temperature__isnull=False, pressure__isnull=False, date__gte = timezone.now() - timedelta(minutes=5)).last()
                    if winchDataLog != None:
                        altitude_low = site.missiondevice_altitude_low
                        pressure -= site.missiondevice_pressure_offset-site.winch_pressure_offset
                        altitude = round((winchDataLog.temperature / -0.0065) * math.log(pressure / winchDataLog.pressure), 2)
                        altitude2 = round(44330 * (1 - (pressure / winchDataLog.pressure)**0.1903), 2)
                        altitude3 = round((winchDataLog.temperature / 0.0065) * math.log(winchDataLog.pressure / pressure), 2)
                        #if site_winch_temperature[site.name] == None:
                        #    site_winch_temperature[site.name] = winchDataLog.temperature
                        #    print(f'site_winch_temperature[{site.name}] = {site_winch_temperature[site.name]}')

                        #altitude4 = round((site_winch_temperature[site.name] / 0.0065) * math.log(winchDataLog.pressure / pressure), 2)
                        
                        tether_angle_low=site.winch_tetherline_angle_low
                        tether_angle_high=site.winch_tetherline_angle_high
                        winch_tether_angle=winchDataLog.tetherline_angle
                        
                        if altitude != None:
                            serializer = MissiondeviceDataLog(**data, altitude = altitude, altitude2= altitude2, altitude3 = altitude3)#, altitude4 = altitude4)
                        send_time = time.time()-warning_notification_send_time[site.name]
                        
                        if 600 <= send_time:
                            if site.alarm == 1:
                                # print(f'site.name : {site.name}')
                                if warning_notification(site.site_id, site.name, altitude, altitude_low, winch_tether_angle, tether_angle_high, tether_angle_low):
                                    warning_notification_send_time[site.name] = time.time()

                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"Error: {e}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        try:
            name = request.GET['name']
            data = MissiondeviceDataLog.objects.filter(missiondevice_serial_number=name).last()
            if data != None:
                serializer = MissionDeviceDataLogSerializer(data)
                # print("임무장비 데이터 GCS 전송", serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                db_logger.exception(status.HTTP_404_NOT_FOUND)
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
def check_site(data):
    
    global queryset_site,warning_notification_send_time
    try:
        DB_queryset_site = Site.objects.values_list('name', 'missiondevice_serial_number') #사이트 내용이 추가/삭제/변경시 새로 값 사이트값을 받아옴
        print(DB_queryset_site,queryset_site)
        db_dict = dict(DB_queryset_site)
        site_dict = dict(queryset_site)

        # 비교 결과 계산
        added = {key: db_dict[key] for key in db_dict if key not in site_dict}  # 추가된 값
        removed = {key: site_dict[key] for key in site_dict if key not in db_dict}  # 삭제된 값
        modified = {
            key: db_dict[key]
            for key in db_dict
            if key in site_dict and site_dict[key] != db_dict[key]
        }  # 수정된 값
        
        # 실제 수정된 값은 삭제된 키와 추가된 키가 아닌, 값이 변경된 키만 포함
        for key in modified:
            if key in removed:
                del removed[key]
            if key in added:
                del added[key]

        # warning_notification_send_time 업데이트
        # 추가된 값 처리
        for key in added:
            warning_notification_send_time[key] = time.time()

        # 삭제된 값 처리
        for key in removed:
            warning_notification_send_time.pop(key, None)

        # 수정된 값 처리
        for key in modified:
            warning_notification_send_time[key] = time.time()

        queryset_site=DB_queryset_site
    except Exception as e:
        db_logger.exception(e)