from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db import transaction
from django.db.models import F
import logging
from django.db import connection
db_logger = logging.getLogger('db')


# Create your views here.
class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            if request.GET.get('site_id') is not None:
                site_id = request.GET.get('site_id')
                data = Site.objects.filter(site_id=site_id).last()
            elif  request.GET.get('winch_serial_number') is not None:
                winch_serial_number = request.GET.get('winch_serial_number')
                data = Site.objects.filter(winch_serial_number=winch_serial_number).last()
            elif request.GET.get('missiondevice_serial_number') is not None:
                missiondevice_serial_number = request.GET.get('missiondevice_serial_number')
                # print(missiondevice_serial_number)
                data = Site.objects.filter(missiondevice_serial_number=missiondevice_serial_number).last()
            elif request.GET.get('gcs_serial_number') is not None:
                gcs_serial_number = request.GET.get('gcs_serial_number')
                data = Site.objects.filter(gcs_serial_number=gcs_serial_number).last()
            else:
                data = Site.objects.all()
                serializer = SiteSerializer(data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            if data != None:
                serializer = SiteSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                db_logger.exception(status.HTTP_404_NOT_FOUND)
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get", "put"])
    def scan360(self, request, pk=None):
        site = self.get_object()

        if request.method == "GET":
            try:
                config = site.scan360
            except Scan360Config.DoesNotExist:
                return Response(
                    {"detail": "Config not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = Scan360ConfigSerializer(config)
            return Response(serializer.data)

        if request.method == "PUT":
            config, created = Scan360Config.objects.update_or_create(
                site=site,
                defaults={
                    "step_angle": request.data.get("step_angle"),
                    "pitch": request.data.get("pitch"),
                    "zoom_level": request.data.get("zoom_level"),
                    "dwell_seconds": request.data.get("dwell_seconds"),
                }
            )

            serializer = Scan360ConfigSerializer(config)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED
            )

class PoiViewSet(viewsets.ModelViewSet):
    queryset = Poi.objects.all()
    serializer_class = PoiSerializer
    
    def list(self, request, *args, **kwargs):
        try:
            site_id = request.GET['site']

            if not site_id:
                return Response({"error": "site required"}, status=status.HTTP_400_BAD_REQUEST)
            
            queryset = Poi.objects.filter(site_id=site_id).order_by('order')
            serializer = PoiSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        db_logger.exception(status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        poi = self.get_object()
        deleted_order = poi.order
        site_id = poi.site_id

        poi.delete()


        Poi.objects.filter(
            site_id=site_id,
            order__gt=deleted_order
        ).update(order=F('order') - 1)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'])
    @transaction.atomic  
    def reorder(self, request):
        try:
            site_id = request.data.get('site')
            items = request.data.get('items', [])

            if not site_id or not isinstance(items, list):
                return Response({"error": "Invalid payload"},status=status.HTTP_400_BAD_REQUEST)

            for item in items:
                Poi.objects.filter(
                    id=item['id'],
                    site_id=site_id
                ).update(order=-item['order'])

            for item in items:
                Poi.objects.filter(
                    id=item['id'],
                    site_id=site_id
                ).update(order=item['order'])

            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)