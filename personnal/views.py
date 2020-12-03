from django.shortcuts import render
from django.http import HttpResponse
from .models import Coin
import json

def index(request):
    a = Coin.objects.all()
    output = json.dumps(list(a.values())[:20])
    print(output)
    return HttpResponse(output)