from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Coin
import json

#@login_required
def index(request):
    a = Coin.objects.all()
    output = json.dumps(list(a.values())[:20])
    print(output)
    return HttpResponse(output)


def home(request):
    return render(request, "login.html")