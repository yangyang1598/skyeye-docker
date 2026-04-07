from django.db import models


# Create your models here.
class Winch(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=100, help_text='윈치 일련번호')
    tetherline_length = models.FloatField(blank=True, null=True, help_text='티더선 전체 길이')
    router = models.CharField(max_length=100, blank=True, null=True, help_text='윈치 연결 라우터(통신사 정보 포함)')    
    brake_operations=models.CharField(max_length=100, blank=True, null=True, help_text='브레이크 방식')

    class Meta:
        managed = True
        db_table = 'winch'


class WinchDataLog(models.Model):
    winch_data_log_id = models.AutoField(verbose_name='id', primary_key=True, help_text='auto increment PK')
    winch_serial_number = models.ForeignKey(Winch, models.DO_NOTHING, db_column='winch_serial_number', blank=True, null=True, help_text='윈치 일련번호')
    date = models.DateTimeField(blank=True, null=True, help_text='날짜', auto_now=True)
    latitude = models.FloatField(blank=True, null=True, help_text='위도')
    longitude = models.FloatField(blank=True, null=True, help_text='경도')
    tetherline_length = models.FloatField(blank=True, null=True, help_text='티더선 길이')
    tetherline_angle = models.FloatField(blank=True, null=True, help_text='티더선 각도')
    tetherline_tension = models.FloatField(blank=True, null=True, help_text='티더선 장력')
    pressure = models.FloatField(blank=True, null=True, help_text='기압')
    temperature = models.FloatField(blank=True, null=True, help_text='온도')

    class Meta:
        managed = True
        db_table = 'winch_data_log'