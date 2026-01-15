from django.urls import path
from . import views

urlpatterns = [
    path('add_notification_site/', views.add_notification_site, name='add_notification_site'),  # 사용자 추가 OAuth
    path('register_user/', views.register_user, name='register_user'),
    path('toggle_alert/<int:site_id>/', views.toggle_alert, name='toggle_alert'),
    path('change_notification_state/', views.notification_state, name='change_notification_state'),  # 사용자 추가 OAuth
    path('your-data-endpoint/', views.get_site_data, name='get_site_data'),
]
