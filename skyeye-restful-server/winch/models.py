from django.db import models


# Create your models here.
class Winch(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=100, help_text='윈치 일련번호')
    primary_sensor = models.CharField(max_length=100, blank=True, null=True, help_text='기본 센서')
    extended_sensor = models.CharField(max_length=100, blank=True, null=True, help_text='확장 센서')
    tetherline_length = models.FloatField(blank=True, null=True, help_text='티더선 전체 길이')
    tetherline_limit_tension = models.FloatField(blank=True, null=True, help_text='티더선 한계 장력')
    production_year = models.IntegerField(blank=True, null=True, help_text='제작 년도(1901-2155)')

    class Meta:
        managed = False
        db_table = 'winch'


class WinchDataLog(models.Model):
    winch_data_log_id = models.AutoField(verbose_name='id', primary_key=True, help_text='auto increment PK')
    winch_serial_number = models.ForeignKey(Winch, models.DO_NOTHING, db_column='winch_serial_number', blank=True, null=True, help_text='윈치 일련번호')
    date = models.DateTimeField(blank=True, null=True, help_text='날짜', auto_now=True)
    latitude = models.FloatField(blank=True, null=True, help_text='위도')
    longitude = models.FloatField(blank=True, null=True, help_text='경도')
    main_power_voltage = models.FloatField(blank=True, null=True, help_text='메인 전원 전압')
    tetherline_voltage = models.FloatField(blank=True, null=True, help_text='티더선 전압')
    main_power_electric_current = models.FloatField(blank=True, null=True, help_text='메인 전원 전류')
    tetherline_electric_current = models.FloatField(blank=True, null=True, help_text='티더선 전류')
    mechanical_brake_operation = models.IntegerField(blank=True, null=True, help_text='기계식 브레이크 동작 여부')
    electronic_brake_operation = models.IntegerField(blank=True, null=True, help_text='전자식 브레이크 동작 여부')
    tetherline_length = models.FloatField(blank=True, null=True, help_text='티더선 길이')
    tetherline_angle = models.FloatField(blank=True, null=True, help_text='티더선 각도')
    tetherline_tension = models.FloatField(blank=True, null=True, help_text='티더선 장력')
    pressure = models.FloatField(blank=True, null=True, help_text='기압')
    temperature = models.FloatField(blank=True, null=True, help_text='온도')
    wind_direction = models.CharField(max_length=100, blank=True, null=True, help_text='풍향')
    wind_speed = models.FloatField(blank=True, null=True, help_text='풍속')
    rain = models.IntegerField(blank=True, null=True, help_text='강우')
    rssi = models.IntegerField(db_column='rssi_lte', blank=True, null=True, help_text='무선통신 수신 감도')

    class Meta:
        managed = False
        db_table = 'winch_data_log'