from django.db import models
from mission_device.models import Missiondevice
from winch.models import Winch


# Create your models here.
class Site(models.Model):
    site_id = models.IntegerField(primary_key=True, help_text='auto increment PK')
    name = models.CharField(unique=True, max_length=100, blank=True, null=True, help_text='장소명')
    installation_date = models.DateField(blank=True, null=True, help_text='설치 날짜')
    missiondevice_serial_number = models.OneToOneField(Missiondevice, models.DO_NOTHING, db_column='missiondevice_serial_number',
                                                       blank=True, null=True, help_text='설치된 임무장비 일련번호')
    winch_serial_number = models.OneToOneField(Winch, models.DO_NOTHING, db_column='winch_serial_number',
                                                blank=True, null=True, help_text='설치된 윈치 일련번호')
    video_stream_url = models.CharField(max_length=200, blank=True, null=True, help_text='비디오 스트림 URL')
    missiondevice_pressure_offset=models.FloatField(blank=False, null=False, default=0, help_text='임무장비 기압 오프셋')
    winch_pressure_offset=models.FloatField(blank=False, null=False, default=0, help_text='윈치 기압 오프셋')
    missiondevice_altitude_low = models.FloatField(blank=True, null=True, help_text='임무장치 고도 하한')
    winch_tetherline_angle_high = models.FloatField(blank=True, null=True, help_text='윈치 티더선 각도 상한')
    winch_tetherline_angle_low = models.FloatField(blank=True, null=True, help_text='윈치 티더선 각도 하한')
    alarm = models.SmallIntegerField(blank=False, null=False, default=0, help_text='위험 상황 알림 여부')
    state = models.SmallIntegerField(blank=False, null=False, default=0, help_text='데이터 수신 상태')
    
    class Meta:
        managed = True
        db_table = 'site'

class Poi(models.Model):
    id = models.AutoField(primary_key=True, help_text='auto increment PK')
    date = models.DateTimeField(auto_now=True, help_text="날짜")
    name = models.CharField(max_length=100, blank=True, null=True, help_text='지점명')
    site = models.ForeignKey(Site, on_delete=models.CASCADE, db_column='site_id', help_text='사이트 번호')
    latitude = models.FloatField(blank=True, null=True, help_text='위도')
    longitude = models.FloatField(blank=True, null=True, help_text='경도')
    altitude = models.FloatField(blank=True, null=True, help_text='고도')
    zoom_level = models.IntegerField(blank=True, null=True, help_text='줌레벨')
    dwell_seconds = models.IntegerField(blank=False, null=False, default=20, help_text='체류 시간(초)')
    pitch = models.FloatField(blank=True, null=True, help_text='Pitch')
    order = models.IntegerField(blank=True, null=True, help_text='순서')

    def save(self, *args, **kwargs):
        if self.order is None:
            last = Poi.objects.filter(site=self.site).order_by('-order').first()
            self.order = 1 if not last else last.order + 1
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'poi'


class Scan360Config(models.Model):
    id = models.AutoField(primary_key=True, help_text='auto increment PK')
    site = models.OneToOneField(Site, on_delete=models.CASCADE, db_column='site_id', related_name="scan360", help_text='사이트 번호')
    step_angle = models.FloatField(blank=True, null=True, help_text='회전 각도')
    pitch = models.FloatField(blank=True, null=True, help_text='Pitch')
    zoom_level = models.IntegerField(blank=True, null=True, help_text='줌레벨')
    dwell_seconds = models.IntegerField(blank=False, null=False, default=20, help_text='체류 시간(초)')
    class Meta:
        managed = True
        db_table = 'scan360_config'
