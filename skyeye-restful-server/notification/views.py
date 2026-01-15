from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from rest_framework.response import Response
from skyeye.models import Site
from accounts.models import NotificationUser
from django.views.decorators.csrf import csrf_exempt
from notification.send import change_notification_state
import json
from rest_framework import status

# Create your views here.

def add_notification_site(request):
    items = Site.objects.all().order_by('site_id')
    
    # 컨텍스트 딕셔너리를 만들어 템플릿에 전달할 데이터를 저장합니다
    context = {
        'items': items,
    }
      
    return render(request, 'notification/add_notification_site.html',context)

def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        site_ids = request.POST.getlist('site_item')  # 모든 선택된 site_item 값을 리스트로 가져옵니다.
        
        print(name, site_ids)  # 디버깅용으로 출력해봅니다.
        
        # 선택된 site_id 값이 있다면 User 모델에 저장합니다.
        for site_id in site_ids:
            site = Site.objects.get(pk=site_id)  # site_id로 Site 객체를 조회합니다.
        
            # User 모델에 데이터가 없다면 새로 생성합니다.
            if not NotificationUser.objects.filter(phone_number=phone_number, site_id=site).exists():
                NotificationUser.objects.create(name=name, phone_number=phone_number, site_id=site)

    return redirect('add_notification_site')  # 적절한 리다이렉션을 설정하세요.


def notification_state(request):
    context = {
        'items': Site.objects.all().order_by('site_id'),
    }

    return render(request, 'notification/change_notification_state.html', context)

@csrf_exempt
def toggle_alert(request, site_id):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            new_state = data.get('state') == 'ON'
            print(f"new_state: {new_state}")
            site = get_object_or_404(Site, site_id=site_id)
            if site.alarm != new_state:
                change_notification_state(site_id, site.name, new_state)
                site.alarm = new_state
                site.save()
                return JsonResponse({'status': 'success'}, status=status.HTTP_201_CREATED)
            return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'fail'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_site_data(request):
    sites = Site.objects.all()
    data = [
        {
            'site_id': site.site_id,
            'name': site.name,  # Assuming SiteSettingsConfig has a related Site object
            'alarm': site.alarm
        }
        for site in sites
    ]
    return JsonResponse(data, safe=False)
