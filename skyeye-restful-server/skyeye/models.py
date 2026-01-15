from django.db import models
from mission_device.models import Missiondevice
from helikite.models import Helikite
from winch.models import Winch


# Create your models here.
class Site(models.Model):
    site_id = models.IntegerField(primary_key=True, help_text='auto increment PK')
    name = models.CharField(unique=True, max_length=100, blank=True, null=True, help_text='장소명')
    installation_date = models.DateField(blank=True, null=True, help_text='설치 날짜')
    helikite_serial_number = models.OneToOneField(Helikite, models.DO_NOTHING, db_column='helikite_serial_number',
                                                   blank=True, null=True, help_text='설치된 헬리카이트 일련번호')
    gcs_serial_number = models.CharField(unique=True, max_length=100, blank=True, null=True, help_text='gcs')
    missiondevice_serial_number = models.OneToOneField(Missiondevice, models.DO_NOTHING, db_column='missiondevice_serial_number',
                                                       blank=True, null=True, help_text='설치된 임무장비 일련번호')
    winch_serial_number = models.OneToOneField(Winch, models.DO_NOTHING, db_column='winch_serial_number',
                                                blank=True, null=True, help_text='설치된 윈치 일련번호')
    missiondevice_pressure_offset=models.FloatField(blank=False, null=False, default=0, help_text='임무장비 기압 오프셋')
    winch_pressure_offset=models.FloatField(blank=False, null=False, default=0, help_text='윈치 기압 오프셋')
    missiondevice_altitude_low = models.FloatField(blank=True, null=True, help_text='임무장치 고도 하한')
    winch_tetherline_angle_high = models.FloatField(blank=True, null=True, help_text='윈치 티더선 각도 상한')
    winch_tetherline_angle_low = models.FloatField(blank=True, null=True, help_text='윈치 티더선 각도 하한')
    alarm = models.SmallIntegerField(blank=False, null=False, default=0, help_text='위험 상황 알림 여부')
    state = models.SmallIntegerField(blank=False, null=False, default=0, help_text='데이터 수신 상태')
    
    class Meta:
        managed = False
        db_table = 'site'

class Poi(models.Model):
    date = models.DateTimeField(primary_key=True, auto_now=True, help_text="기본키")
    poi_id = models.IntegerField(help_text='지점 번호')
    site = models.ForeignKey(Site, models.DO_NOTHING, db_column='site_id', help_text='사이트 번호')
    latitude = models.FloatField(blank=True, null=True, help_text='위도')
    longitude = models.FloatField(blank=True, null=True, help_text='경도')
    altitude = models.FloatField(blank=True, null=True, help_text='고도')
    zoom_level = models.IntegerField(blank=True, null=True, help_text='줌레벨')

    class Meta:
        managed = False
        db_table = 'poi'
