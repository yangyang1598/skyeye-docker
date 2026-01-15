import logging
from .serializers import *
from .models import *
from django.http import HttpResponse
from rest_framework import viewsets

logger = logging.getLogger('db')


class StatusLogViewSet(viewsets.ModelViewSet):
    queryset = StatusLog.objects.all()
    serializer_class = StatusLogSerializer


def __gen_500_errors(request):
    try:
        1 / 0
    except Exception as e:
        logger.exception(e)

    return HttpResponse('Hello 500!')
