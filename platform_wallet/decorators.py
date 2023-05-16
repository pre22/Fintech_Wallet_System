from django.shortcuts import redirect
from django.urls import reverse_lazy

# Permission Decorator
# Restricts logged in users from accessing the Authentication pages


def auth_access_decorator(view_func):
    '''Restricts page access from logged in users'''
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated is True:
            return redirect(reverse_lazy("dashboard"))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def admin_access_only(view_func):
    '''Restricts page to admin only'''
    def wrapper_func(request, *args, **kwargs):
        users = request.user
        if users.is_authenticated is True:
            if users.is_superuser is True:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(reverse_lazy("dashboard"))
        else:
            return redirect(reverse_lazy("login"))

    return wrapper_func
