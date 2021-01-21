from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Coin
import json
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
#from .models import auth

#@login_required
def index(request):
    a = Coin.objects.all()
    output = json.dumps(list(a.values())[:20])
    print(output)
    return HttpResponse(output)


def home(request):
    return render(request, "login.html")

@csrf_exempt
def user(request, id):
    a = User.objects.get(pk=id)
    print(dir(a))
    output= {
        "email": a.email,
        "firstname": a.first_name,
        "lastname": a.last_name,
    }
    print(output)
    return HttpResponse(json.dumps(output))