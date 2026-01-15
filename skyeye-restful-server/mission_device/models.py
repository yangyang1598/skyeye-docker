from random import choices
from django.db import models


# Create your models here.

class Camera(models.Model):
    AVAILABILITY_CHOICES = [
        ('고장', '고장'),
        ('파손', '파손'),
        ('기타', '기타'),
        ('분실', '분실'),
    ]
    NIGHT_VISION_CHOICES = [
        (None, '가능'),
        (1, '불가능'),
    ]
    serial_number = models.CharField(primary_key=True, max_length=100, help_text='카메라 일련번호')
    availability = models.CharField(max_length=100,choices=AVAILABILITY_CHOICES, blank=True, null=True, help_text='가용 가능 여부')
    remarks=models.CharField(max_length=100, blank=True, null=True, help_text='비고')
    maximum_angle_roll = models.IntegerField(blank=True, null=True, help_text='Roll 최대각')
    minimum_angle_roll = models.IntegerField(blank=True, null=True, help_text='Roll 최소각')
    maximum_angle_pitch = models.IntegerField(blank=True, null=True, help_text='Pitch 최대각')
    minimum_angle_pitch = models.IntegerField(blank=True, null=True, help_text='Pitch 최소각')
    maximum_angle_yaw = models.IntegerField(blank=True, null=True, help_text='Yaw 최대각')
    minimum_angle_yaw = models.IntegerField(blank=True, null=True, help_text='Yaw 최소각')
    zoom_magnification = models.IntegerField(blank=True, null=True, help_text='무게')
    night_vision = models.IntegerField(choices=NIGHT_VISION_CHOICES,blank=True, null=True, help_text='나이트 비전 가능 여부')
    protocol = models.IntegerField(blank=True, null=True, help_text='프로토콜 타입')

    class Meta:
        managed = False
        db_table = 'camera'


class Missiondevice(models.Model):
    AVAILABILITY_CHOICES = [
        ('고장', '고장'),
        ('파손', '파손'),
        ('기타', '기타'),
        ('분실', '분실'),
    ]
        
    serial_number = models.CharField(primary_key=True, max_length=100, help_text='임무 장치 일련번호')
    camera_serial_number = models.OneToOneField(Camera, models.DO_NOTHING, db_column='camera_serial_number',
                                                blank=True, null=True, help_text='카메라 일련번호') # ForeignKey / OneToOneField 임에 따라 Django가 자동으로 combo 설정
    availability = models.CharField(max_length=100, choices=AVAILABILITY_CHOICES, blank=True, null=True, help_text='가용 가능 여부') # choices 를 이용한 combo 구성
    remarks=models.CharField(max_length=100, blank=True, null=True, help_text='비고')
    # extended_sensor = models.CharField(max_length=100, blank=True, null=True, help_text='확장 센서')
    # communication_type = models.CharField(max_length=100, blank=True, null=True, help_text="통신방식")
    # mobile_service_company = models.CharField(max_length=100, blank=True, null=True, help_text='통신사')
    # weight = models.FloatField(blank=True, null=True, help_text='무게')
    # production_year = models.TextField(blank=True, null=True, help_text='제작 년도(1901-2155)')

    class Meta:
        managed = False
        db_table = 'missiondevice'


class MissiondeviceDataLog(models.Model):
    missiondevice_data_log_id = models.AutoField(verbose_name='id', primary_key=True, help_text='auto increment PK')
    missiondevice_serial_number = models.ForeignKey(Missiondevice, models.DO_NOTHING, db_index=True, db_column='missiondevice_serial_number', 
                                                    blank=True, null=True, help_text='임무 장치 일련번호')
    date = models.DateTimeField(blank=True, null=True, help_text='날짜', auto_now=True)
    latitude = models.FloatField(blank=True, null=True, help_text='위도')
    longitude = models.FloatField(blank=True, null=True, help_text='경도')
    roll = models.FloatField(blank=True, null=True, help_text=' Roll')
    pitch = models.FloatField(blank=True, null=True, help_text='Pitch')
    yaw = models.FloatField(blank=True, null=True, help_text='Yaw')
    camera_roll = models.FloatField(blank=True, null=True, help_text='카메라 Roll')
    camera_pitch = models.FloatField(blank=True, null=True, help_text='카메라 Pitch')
    camera_yaw = models.FloatField(blank=True, null=True, help_text='카메라 Yaw')
    camera_zoom = models.IntegerField(blank=True, null=True, help_text='카메라 Zoom')
    pressure = models.FloatField(blank=True, null=True, help_text='기압')
    altitude = models.FloatField(blank=True, null=True, help_text='고도')
    altitude2 = models.FloatField(blank=True, null=True, help_text='고도')
    altitude3 = models.FloatField(blank=True, null=True, help_text='고도')
    altitude4 = models.FloatField(blank=True, null=True, help_text='고도')
    temperature = models.FloatField(blank=True, null=True, help_text='온도')
    voltage = models.FloatField(blank=True, null=True, help_text='전압')
    rssi = models.IntegerField(db_column='rssi_lte', blank=True, null=True, help_text='무선통신 수신 감도')

    class Meta:
        managed = False
        indexes = [
            models.Index(fields=['date']),  # 'date' 필드에 인덱스 추가
        ]
        db_table = 'missiondevice_data_log'
