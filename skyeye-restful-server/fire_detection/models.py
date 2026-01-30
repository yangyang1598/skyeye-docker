from django.db import models
from django.conf import settings

# Create your models here.
class Detection(models.Model):
    id = models.AutoField(verbose_name='id', primary_key=True, help_text='auto increment PK')
    site_id=models.IntegerField(max_length=11, null=True)
    date = models.DateTimeField(blank=True, null=True, auto_now=True)
    # image = models.ImageField(upload_to="%Y/%m/%d", null=True)
    # detection_rate = models.CharField(max_length=100, null=True)
    class_name = models.CharField(max_length=100, null=True)
    ai_model = models.CharField(max_length=20, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    # image = models.ImageField(upload_to="image")
