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

def change_status(request):
    account_id = int(request.GET.get('account_id'))
    old_status = request.GET.get('current_status')
    account = Account.objects.get(pk=account_id)

    if old_status == "True":
        account.status = False
        new_status = "False"
    else:
        account.status = True
        new_status = "True"

    account.save()

    data = {"new_status": new_status}
    return JsonResponse(data)

def get_users_accounts(request):
    pass