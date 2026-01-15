from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
import logging

db_logger = logging.getLogger('db')


# Create your views here.
class WinchViewSet(viewsets.ModelViewSet):
    queryset = Winch.objects.all()
    serializer_class = WinchSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WinchDataLogViewSet(viewsets.ModelViewSet):
    queryset = WinchDataLog.objects.all()
    serializer_class = WinchDataLogSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            name = request.GET['name']
            data = WinchDataLog.objects.filter(winch_serial_number=name).last()
            if data != None:
                serializer = WinchDataLogSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                db_logger.exception(status.HTTP_404_NOT_FOUND)
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
