from django.db import models
from django.conf import settings

# Create your models here.
class Detection(models.Model):
    id = models.AutoField(verbose_name='id', primary_key=True, help_text='auto increment PK')
    site_id=models.IntegerField(max_length=11, null=True)
    date = models.DateTimeField(blank=True, null=True, auto_now=True)
    class_name = models.CharField(max_length=100, null=True)
    location=models.CharField(max_length=100,null=True)
  
    class Meta:
        managed = True
        db_table = 'fire_detection'
