from django.http import JsonResponse
from .models import Account


# Create your views here.

def fetch_platform_with_existing_accounts(request):
    """
        :param request: The HTTP request object.

        This function takes a user_id as input and retrieves the platforms on which the user with this ID has accounts.
    """
    user_id = request.GET.get('user_id')
    accounts = Account.objects.all().filter(user=user_id)
    platform_data = {int(account.platform.pk): account.platform.platform_name for account in accounts}
    data = {"platforms": platform_data}
    return JsonResponse(data)

def change_status(request):
    """
        :param request: The HTTP request object.

        This function is triggered when the status toggle in the account list display is clicked. 
        It takes the old status and updates it in the database while simultaneously 
        performing the appropriate action of either activating or deactivating the account 
        using defined methods in the account model.
    """
    account_id = int(request.GET.get('account_id'))
    old_status = request.GET.get('current_status')
    account = Account.objects.get(pk=account_id)
    platform = account.platform
    user = account.user
    new_status = old_status
    

    if old_status == "True":
        if Account.deactivate_account(account=account, platform=platform, user=user) is not False:
            account.status = False
            new_status = "False"
    else:
        if Account.activate_account(account=account, platform=platform, user=user) is not False:
            account.status = True
            new_status = "True"
    
    account.save()

    data = {"new_status": new_status}
    return JsonResponse(data)
