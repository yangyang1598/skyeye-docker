from accounts.models import NotificationUser
from datetime import datetime, timedelta
from skyeye.models import Site
from mission_device.models import MissiondeviceDataLog
from winch.models import WinchDataLog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import requests
import hmac
import base64
import hashlib
from django.db import connection, close_old_connections
from django.utils import timezone

# 네이버 클라우드 플랫폼에서 발급받은 정보를 입력합니다.
access_key = 'TdNIgfIWRQ0vmEk71A80'
secret_key = '4bIYVnU8JLsfGBBX2ElgNkyncBQb0rRuFRtJwaPd'
msg_service_id = 'ncp:sms:kr:337423977376:skyeye_manage_sms'  # SENS 프로젝트 ID
talk_service_id = 'ncp:kkobizmsg:kr:337423976556:skyeye_manage_service'  # SENS 프로젝트 ID
plus_friend_id = '@스카이아이관리서비스'  # 플러스친구 ID
sender_number = '01083487560'  # 발신자 번호
scheduler = BackgroundScheduler(timezone='Asia/Seoul')
scheduler_warning = BackgroundScheduler(timezone='Asia/Seoul')

# 긴급 알림
def warning_notification(site_id, name, altitude, altitude_low, winch_tether_angle, tether_angle_high, tether_angle_low):
    
    users = NotificationUser.objects.filter(site_id=site_id)
    if users.exists():
        recipient_number = [user.phone_number for user in users]
        # print(recipient_number)
        content = ''
        now = datetime.now()
        if altitude_low != None and altitude < altitude_low:
            content = f"""
            [추락위험 - 고도하한]
 ■ 시간 : {now.strftime('%Y/%m/%d %H:%M:%S')}

 ■ 위치 :{name}
   • 현재 고도:{altitude}m
     - 위험 고도:{str(altitude_low)+"m 미만"}"""
            send_warning("alt_warntalk", recipient_number, now, content)
            return True
        
        if tether_angle_high != None and tether_angle_high <= winch_tether_angle:
            
            content = f"""
            [추락위험 - {"각도 상한"}]
 ■ 시간 : {now.strftime('%Y/%m/%d %H:%M:%S')}

 ■ 위치 :{name}
   • 현재 각도:{winch_tether_angle}º
     - 위험 각도:{str(tether_angle_high)+"° 이상"}"""
            send_warning("Tether_warntalk", recipient_number, now, content)
            return True
        
        if tether_angle_low != None and winch_tether_angle < tether_angle_low:
            content = f"""
            [추락위험 - {"각도 하한"}]
 ■ 시간 : {now.strftime('%Y/%m/%d %H:%M:%S')}

 ■ 위치 :{name}
   • 현재 각도:{winch_tether_angle}º
     - 위험 각도:{str(tether_angle_low)+"° 미만"}"""
        
        
            
            send_warning("Tether_warntalk", recipient_number, now, content)
            return True
    return False

def send_warning(mode, phone_number, now, content):
    if mode=="Tether_warntalk":
        template_code = "TetherwarningNotification" 
        messages = [
            {
                "to": number,
                "content": content,
                 "buttons": [
                    {
                        "type": "WL",
                        "name": "알림 설정 활성화",
                        "linkMobile": "http://skyeyeserver.duckdns.org:8001/notification/change_notification_state/",
                        "linkPc": "http://skyeyeserver.duckdns.org:8001/notification/change_notification_state/"
                    }]
            } for number in phone_number
        ]
        data = {
            "plusFriendId": plus_friend_id,
            "templateCode": template_code,
            "messages": messages
        }
        send_alimtalk(data)
    elif mode=="alt_warntalk":
        service_id = talk_service_id
        template_code = "AltwarningNotification" 
        messages = [
            {
                "to": number,
                "content": content,
                 "buttons": [
                    {
                        "type": "WL",
                        "name": "알림 설정 활성화",
                        "linkMobile": "http://skyeyeserver.duckdns.org:8001/notification/change_notification_state/",
                        "linkPc": "http://skyeyeserver.duckdns.org:8001/notification/change_notification_state/"
                    }]
            } for number in phone_number
        ]
        data = {
            "plusFriendId": plus_friend_id,
            "templateCode": template_code,
            "messages": messages
        }
        

        send_alimtalk(data)

#알림 전송 기능 상태 변경
def change_notification_state(site_id, name, notification_state):
    users = NotificationUser.objects.filter(site_id=site_id)
    if users.exists():
        recipient_number = [user.phone_number for user in users]
        now = datetime.now()
        # content = {
        #     "현재시간": now.strftime('%Y/%m/%d %H:%M:%S'),
        #     "위치": name
        # }
        hour = int(now.strftime("%H"))
       
        if notification_state:
            content =f"""[알림 전송 기능 활성화]

 ■ 시간:{now.strftime('%Y/%m/%d %H:%M:%S')}

 ■ 위치:{name}"""
            send_change_notification_state("alimtalk1", recipient_number, now, content)
        else:
            content =f"""[알림 전송 기능 비활성화]

 ■ 시간:{now.strftime('%Y/%m/%d %H:%M:%S')}

 ■ 위치:{name}"""
            send_change_notification_state("alimtalk0", recipient_number, now, content)

def send_change_notification_state(mode, phone_number, now, content):
    

    if mode == "alimtalk0" or mode == "alimtalk1":
        template_code = "OnNotification" if mode == "alimtalk1" else "OffNotification"
        messages = [
            {
                "to": number,
                "content": content,
                "buttons": [
                    {
                        "type": "WL",
                        "name": "알림 설정 활성화",
                        "linkMobile": "http://skyeyeserver.duckdns.org:8001/notification/change_notification_state/",
                        "linkPc": "http://skyeyeserver.duckdns.org:8001/notification/change_notification_state/"
                    }]
            } for number in phone_number
        ]
        data = {
            "plusFriendId": plus_friend_id,
            "templateCode": template_code,
            "messages": messages
        }
        
        send_alimtalk(data)
# site_winch_temperature  = {}
def job_daily_notification():
    # global site_winch_temperature
    try:
        close_old_connections() #기존 DB 연결 제거(타임아웃 유발 connection)
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")  # 이때 Django가 자동으로 새로운 DB 연결을 생성
        
        sites = Site.objects.all()
        
        date_range_end = datetime.now()
        date_range_start = date_range_end - timedelta(minutes=30)
        
        for site in sites:
            #site_winch_temperature[site.name] = None
            missiondevice_serial_number = site.missiondevice_serial_number
            winch_serial_number = site.winch_serial_number
            
            missiondevice_state = False
            altitude = None
            if missiondevice_serial_number != None:
                missiondevice_data = MissiondeviceDataLog.objects.filter(
                    missiondevice_serial_number = missiondevice_serial_number, 
                    date__range = [date_range_start, date_range_end]).last()
                if missiondevice_data != None:
                    missiondevice_state = True
                    altitude = missiondevice_data.altitude

            winch_state = False
            if winch_serial_number != None:
                winch_data = WinchDataLog.objects.filter(
                    winch_serial_number = winch_serial_number,
                    date__range = [date_range_start, date_range_end]).last()
                
                # site_winch_temperature[site.name] = winch_data.temperature

                if winch_data != None:
                    winch_state = True
                
            daily_notification(site.site_id, site.name, winch_serial_number, winch_state, missiondevice_serial_number, missiondevice_state, altitude, site.alarm)
    except Exception as e:
        print(f"Error occurred: {e}")
        job_daily_notification()

def daily_notification(site_id, name, winch_serial_number, winch_state, missiondevice_serial_number, missiondevice_state, altitude, notification_state):

    try:
        users = NotificationUser.objects.filter(site_id=site_id)

        if users.exists():
            recipient_number = [user.phone_number for user in users]
            now = datetime.now()
            
            content = f"""[스카이아이 정기 알림]
■ 시간 : {now.strftime('%Y/%m/%d %H:%M:%S')}

■ 위치 : {name}
    • 윈치
        - 시리얼번호 : {'-' if winch_serial_number == None else winch_serial_number.serial_number}
        - 데이터 : {'정상 수신' if winch_state else '미수신'}

    • 임무장비
        - 시리얼번호 : {'-' if missiondevice_serial_number == None else missiondevice_serial_number.serial_number}
        - 데이터 : {'정상 수신' if missiondevice_state else '미수신'}
        - 고도 : {'-' if altitude == None else altitude}

■ 긴급상황 알림 : {'비활성화' if notification_state == 0 else '활성화'}

* 정기 알림의 경우 긴급상황 알림 서비스 상태와 상관없이 전송됩니다.
"""
            # print(content)
            
            send_daily_notification(recipient_number, now, content)
    except Exception as e:
        print(e)
        job_daily_notification()

def send_daily_notification(phone_number, now, content):
    try:
        template_code = "daliynotification"
        messages = [
            {
                "to": number,
                "content": content
            } for number in phone_number
        ]

        data = {
            "plusFriendId": plus_friend_id,
            "templateCode": template_code,
            "messages":messages
        }

        send_alimtalk(data)
    except Exception as e:
        print(e)
        job_daily_notification()

def job_warning_notification():
    try:
        close_old_connections() #기존 DB 연결 제거(타임아웃 유발 connection)
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")  # 이때 Django가 자동으로 새로운 DB 연결을 생성
        
        sites = Site.objects.all()
        
        date_range_end = datetime.now()
        date_range_start = date_range_end - timedelta(minutes=5)

        for site in sites:
            missiondevice_serial_number = site.missiondevice_serial_number
            if missiondevice_serial_number != None:
                missiondevice_data = MissiondeviceDataLog.objects.filter(
                    missiondevice_serial_number = missiondevice_serial_number, 
                    date__range = [date_range_start, date_range_end]).exists()
                if not missiondevice_data and site.state == 0:
                    print('!!!!')
                    data = MissiondeviceDataLog.objects.filter(missiondevice_serial_number = missiondevice_serial_number).values('date').order_by('-date').first()
                    if data !=None:
                        date = timezone.localtime(data['date']).replace(tzinfo=None)
                    else:
                        date = '-'
                    no_data_warning_notification(site.site_id, site.name, missiondevice_serial_number, date,site.alarm)
                    site.state = 1
                    site.save()

                elif missiondevice_data and site.state == 1:
                    site.state = 0
                    site.save()
                
    except Exception as e:
        print(f"Error occurred: {e}")

def no_data_warning_notification(site_id, name, missiondevice_serial_number, last_data_time,notification_state):
    users = NotificationUser.objects.filter(site_id=site_id)
    if users.exists() and notification_state == 1:
        recipient_number = [user.phone_number for user in users]
        now = datetime.now()
        content = f"""
        [추락 위험 - 데이터 미수신]
 ■ 시간 : {now.strftime('%Y/%m/%d %H:%M:%S')}

 ■ 위치 :{name}
   ▲ 임무장비
     - 시리얼번호 : { missiondevice_serial_number.serial_number}
     - 마지막 데이터 수신 : {last_data_time}
※ 윈치 내 임무장치 전원 공급부 재시작 필요
"""
        send_warning_notification(recipient_number, now, content)

       

def send_warning_notification(phone_number, now, content):
    try:

        template_code = "DataWarningNotification"
        service_id = talk_service_id
        messages = [
            {
                "to":number,
                "content": content
            } for number in phone_number
        ]
        data = {
            "plusFriendId": plus_friend_id,
            "messages":messages,
            "templateCode": template_code,
        }
        url = f"https://sens.apigw.ntruss.com/alimtalk/v2/services/{service_id}/messages"
        uri = f"/alimtalk/v2/services/{service_id}/messages"
        timestamp = str(int(now.timestamp() * 1000))
        signature = make_signature(f"POST {uri}\n{timestamp}\n{access_key}", secret_key)
            
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signature,
        }
        response = requests.post(url, headers=headers, json=data)
        print(response.json(),"response.status_code)") 
    except Exception as e:
        print(e)

def make_signature(string_to_sign, secret_key):
    secret_key_bytes = bytes(secret_key, 'UTF-8')
    string_to_sign_bytes = bytes(string_to_sign, 'UTF-8')
    string_to_sign_hmac = hmac.new(secret_key_bytes, string_to_sign_bytes, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(string_to_sign_hmac).decode('UTF-8')
    return signature

def send_alimtalk(data):
    now = datetime.now()
    url = f"https://sens.apigw.ntruss.com/alimtalk/v2/services/{talk_service_id}/messages"
    uri = f"/alimtalk/v2/services/{talk_service_id}/messages"
    timestamp = str(int(now.timestamp() * 1000))
    signature = make_signature(f"POST {uri}\n{timestamp}\n{access_key}", secret_key)
        
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": signature,
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json(),response.status_code) 
    
def start():
    scheduler.add_job(
        job_daily_notification, 
        trigger=CronTrigger(hour=9,minute=0), 
        id='job_daily',
        misfire_grace_time=300,
      replace_existing=True,)
    scheduler.start()

    scheduler_warning.add_job(
        job_warning_notification, 
        trigger=IntervalTrigger(minutes=5),
        id='job_warning',
        misfire_grace_time=300,
      replace_existing=True,)
    scheduler_warning.start()
