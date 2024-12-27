from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect


def switch_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("/")
    else:
        return HttpResponse("something not working")
