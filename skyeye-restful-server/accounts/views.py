from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
# from accounts.forms import RegistrationForm, AccountAuthForm
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.admin.models import LogEntry
from django.shortcuts import render
from django.utils.timezone import now


def all_logs_view(request):
    logs = LogEntry.objects.all().order_by('-action_time')
    return render(request, 'admin/all_logs.html', {'logs': logs})


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response(token.key, status=status.HTTP_200_OK)
