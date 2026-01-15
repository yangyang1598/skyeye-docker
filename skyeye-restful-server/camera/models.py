from django.db import models
from skyeye.models import Site

# Create your models here.
class CameraView(models.Model):
    camera_view_id = models.AutoField(verbose_name='id', primary_key=True, help_text='auto increment PK')
    site = models.ForeignKey(Site, models.DO_NOTHING, db_column='site_id', help_text='사이트 번호')
    date = models.DateTimeField(blank=True, null=True, help_text='날짜', auto_now=True)
    latitude = models.CharField(max_length=100,blank=True, null=True, help_text='위도')
    longitude = models.CharField(max_length=100,blank=True, null=True, help_text='경도')
    cardinal_direction = models.CharField(max_length=100, blank=True, null=True, help_text='방위')

    class Meta:
        managed = False
        db_table = 'camera_view'