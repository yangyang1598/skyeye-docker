from django.db import models
from skyeye.models import Site

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
    zoom_magnification = models.IntegerField(blank=True, null=True, help_text='Zoom 배율')
    night_vision = models.IntegerField(choices=NIGHT_VISION_CHOICES,blank=True, null=True, help_text='나이트 비전 가능 여부')
    protocol = models.IntegerField(blank=True, null=True, help_text='프로토콜 타입')

    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Camera'
        managed = True
        db_table = 'camera'

class CameraView(models.Model):
    camera_view_id = models.AutoField(verbose_name='id', primary_key=True, help_text='auto increment PK')
    site = models.ForeignKey(Site, models.DO_NOTHING, db_column='site_id', help_text='사이트 번호')
    date = models.DateTimeField(blank=True, null=True, help_text='날짜', auto_now=True)
    latitude = models.CharField(max_length=100,blank=True, null=True, help_text='위도')
    longitude = models.CharField(max_length=100,blank=True, null=True, help_text='경도')
    cardinal_direction = models.CharField(max_length=100, blank=True, null=True, help_text='방위')

    class Meta:
        indexes = [
            models.Index(fields=['site', '-date']),
        ]
        managed = False
        db_table = 'camera_view'
        verbose_name = 'Camera view'
        verbose_name_plural = 'Camera view'