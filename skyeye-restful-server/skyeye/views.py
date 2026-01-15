from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from rest_framework.response import Response
import logging

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

class PoiViewSet(viewsets.ModelViewSet):
    queryset = Poi.objects.all()
    serializer_class = PoiSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not Poi.objects.filter(poi_id=request.data['poi_id'], site=request.data['site']).exists():
                serializer.save()
                print("POI 로그 데이터", serializer.data)
                return Response(serializer.data['poi_id'], status=status.HTTP_201_CREATED)
        db_logger.exception(status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            site_id = request.GET['name']
            data = Poi.objects.filter(site_id=site_id)
            if data != None:
                serializer = PoiSerializer(data, many=True)
                # print("POI 데이터 GCS 전송", serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                db_logger.exception(status.HTTP_404_NOT_FOUND)
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            data = Poi.objects.get(poi_id=request.data['poi_id'], site=request.data['site'])
            data.delete()

            return Response(request.data['poi_id'], status=status.HTTP_200_OK)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            partial = kwargs.pop('partial', False)
            _data = JSONParser().parse(request)
            instance = Poi.objects.get(poi_id=_data['c_poi_id'], site=_data['site'])
            instance.save()

            del _data['site'], _data['c_poi_id']
            serializer = self.get_serializer(instance, data=_data, partial=partial)

            if serializer.is_valid(): 
                serializer.update(instance, _data)
                return Response(serializer.data['poi_id'], status=status.HTTP_200_OK)
            else:
                db_logger.exception(status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            db_logger.exception(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
       