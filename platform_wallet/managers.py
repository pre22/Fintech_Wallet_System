from django.shortcuts import redirect
from django.urls import reverse_lazy

# Permission Decorator
# Restricts logged in users from accessing the Authentication pages
def authAccessDecorator(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated == True:
            return redirect(reverse_lazy("dashboard"))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def admin_access_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        users = request.user
        if users.is_authenticated == True:
            if users.is_superuser == True:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(reverse_lazy("dashboard"))
        else:
            return redirect(reverse_lazy("login"))

    return wrapper_func