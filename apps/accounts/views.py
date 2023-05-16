import environ

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


import sweetify

from users.decorators import authAccessDecorator
from users.models import CustomUser, Referals
from users.forms import SignupForm
# Create your views here.

env = environ.Env()

@authAccessDecorator
def CustomLoginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    sweetify.success(request,'Login Successful',  text="Welcome Home Admin!!!")
                else:
                    sweetify.success(request,'Login Successful',  text="You are now logged in")
                return HttpResponseRedirect(reverse_lazy("dashboard"))
        elif form.is_valid() == False:
            User = get_user_model()
            try:
                username = form.cleaned_data.get("username")
                user = User.objects.get(email=username)
                from_email = config('EMAIL_HOST_USER')
                sweetify.success(request,"Success", text="Click Activation mail sent to your mail to verify")
            except User.DoesNotExist:
                sweetify.error(request,"Error", text="Invalids username or password.")
        else:
            sweetify.error(request,"Error", text="Invalid username or password.")
            
            
    else:
        form = AuthenticationForm()
    return render(request, "Registration/login.html", {"form": form})

@authAccessDecorator
def SignupView(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            rf = form.instance.referral_code
  

            mail = form.cleaned_data.get("email")
            name = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            recipient_list = [mail]
            from_email = settings.EMAIL_HOST_USER
            
            domain = request.META['HTTP_HOST']
            subject = "Registration Successful"
            message = f"""
            Dear {name}, 
            You have successfully created an account at {domain}.

            Thank You
            """

            send_mail(subject, message, from_email, recipient_list)
            form.save(request)

            if rf != '':
                try:
                    CustomUser.objects.get(referral_code=rf)
                except CustomUser.DoesNotExist:
                    sweetify.error(request, 'Error', text='Invalid Refferal Code')

                rf_user = CustomUser.objects.get(referral_code=rf)

                try:
                    Referals.objects.get(user=rf_user)
                except Referals.DoesNotExist:
                    Referals.objects.create(user=rf_user)
                    
                rfm = Referals.objects.get(user=rf_user)
                rfm.referred_user = f"{form.instance.first_name} {form.instance.last_name}"
                rfm.referred_email = form.instance.email
                rfm.save()

            
            return redirect("logins")
        else:
            # print(form.errors)
            print("Form is not valid")
    else:
        form = SignupForm()
    return render(request, "Registration/register.html", {"form": form})
