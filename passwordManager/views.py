from django.shortcuts import render
from django.http import JsonResponse
from .models import Account


# Create your views here.

def fetch_platform_with_existing_accounts(request):
    user_id = request.GET.get('user_id')
    accounts = Account.objects.all().filter(user=user_id)
    platform_data = {int(account.platform.pk): account.platform.platform_name for account in accounts}
    data = {"platforms": platform_data}
    return JsonResponse(data)