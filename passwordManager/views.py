from django.shortcuts import render
from models import AccountForm
from django.views.generic.edit import FormView


# Create your views here.

class AccountFormView(FormView):
    #template_name = "contact.html"
    form_class = AccountForm
    #success_url = "/thanks/"

    def form_valid(self, form):
        if self.request.method == 'GET':
            user = self.request.GET.get("user")
            if user:

                print("heello")
                
                
            else :
                print("no")
        return super().form_valid(form)