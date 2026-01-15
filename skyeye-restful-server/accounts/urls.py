from django.urls import path, include
from .views import *
from django.urls import path
from .views import all_logs_view


urlpatterns = [
    path('signup', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    #path('admin/all-logs/', all_logs_view, name='all_logs'),
]