from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
from rest_framework.test import APIRequestFactory
from .views import CameraViewSet
scheduler = BackgroundScheduler(timezone='Asia/Seoul')

def start():
    scheduler.add_job(
        delete_cameraview, 
        trigger=CronTrigger(hour=17,minute=0), 
        id='delete_daily',
        misfire_grace_time=300,
      replace_existing=True,)
    scheduler.start()
    
def delete_cameraview():
    
    factory = APIRequestFactory()

    # 예제 요청 데이터

    # DELETE 요청 생성
    request = factory.delete('/camera_view', format='json')
    request.META['HTTP_AUTHORIZATION'] = f'Token {"9cc677a95a7e30226f05ce4d4926af33d2338bb2"}' 
    # View 인스턴스 생성
    view = CameraViewSet.as_view({'delete': 'delete'})

    # View 호출
    response = view(request)

    # 응답 확인
    print(response.status_code)  # 예: 200 또는 204
    print(response.data)         # 응답 데이터 (없을 수 있음)