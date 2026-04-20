import time
from django_eventstream import send_event
from django.contrib.auth import get_user_model


def heartbeat_loop():
    while True:
        try:
            User = get_user_model()
            user = User.objects.first()  # 아무 유저 하나
            send_event("global", "heartbeat", {"type": "heartbeat"}, user)
            print("🔥 heartbeat send", flush=True)
        except Exception as e:
            print(f"[heartbeat error] {e}",flush=True)

        time.sleep(10)