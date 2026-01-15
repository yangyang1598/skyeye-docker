from django.db import models

# Create your models here.
class Helikite(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=100, help_text='헬리카이트 일련번호')
    cubic = models.IntegerField(blank=True, null=True, help_text='큐빅')
    type = models.CharField(max_length=100, blank=True, null=True, help_text='형태')
    weight = models.FloatField(blank=True, null=True, help_text='무게')
    payload = models.FloatField(blank=True, null=True, help_text='페이로드')
    production_year = models.TextField(blank=True, null=True, help_text='제작 년도(1901-2155)')
    image_file_path = models.CharField(max_length=100, blank=True, null=True, help_text='헬리카이트 이미지 파일 경로')

    class Meta:
        managed = False
        db_table = 'helikite'
