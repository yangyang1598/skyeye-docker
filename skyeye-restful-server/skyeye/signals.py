from django.db.models.signals import post_save, post_delete,post_migrate
from django.dispatch import receiver
from .models import Site  # "site" 앱의 대상 모델 import
from mission_device.views import check_site
# 데이터가 추가될 때 실행
@receiver(post_save, sender=Site)
def log_addition(sender, instance, created, **kwargs):
    if created:  # 새로 추가된 경우
        print(f"[ADD] '{instance}'이(가) 추가되었습니다.")
        check_site(instance)
    else:
        print(f"[UPDATE] {instance}이(가) 수정되었습니다.")
        check_site(instance)
        
# 데이터가 삭제될 때 실행
@receiver(post_delete, sender=Site)
def log_deletion(sender, instance, **kwargs):
    print(f"[DELETE] '{instance}'이(가) 삭제되었습니다.")
    check_site(instance)


