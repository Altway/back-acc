from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from .misc.portefolio import ici



import json
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)



def risk(request):
    RISK_MODEL = {
        "SAMPLECOV": "Sample covariance",
        "SEMICOV": "Semi covariance",
        "EXPCOV": "Exponential covariance",
        "MINDETCOV": "Minimum determinant covariance",
        "COVSHRINKAGE": "Covariance Shrinkage",
        "LEDOITWOLF": "Ledoit-Wolf method",
        "ORACLEAPPROX": "Oracle Approximation",
    }
    output = json.dumps(RISK_MODEL)
    return HttpResponse(output)

def returns(request):
    EXPECTED_RETURNS = {
        "MEANHISTORICAL": "Mean historical",
        "EMAHISTORICAL": "Exponential mean historical",
        "CAPMRETURN": "Capital asset pricing model",
    }
    output = json.dumps(EXPECTED_RETURNS)
    return HttpResponse(output)

@csrf_exempt
def input(request):
    print(json.loads(request.body))
    allocation, weights = ici()
    output = json.dumps(allocation, cls=NpEncoder)
    output = json.dumps(weights, cls=NpEncoder)
    #return HttpResponse(output)
    return HttpResponse(json.dumps({"maisoui": 40, "bonjour": 15, "trcu": 25, "this": 20}))


def coins_list(request):
    url = "https://api.coingecko.com/api/v3/coins/list"
    r = requests.get(url)

    a = json.dumps(r.json()[:10])
    return HttpResponse(a)

def goals(request):
    a = ["max_sharpe", "min_volatility", "max_performance", "quadratic_utility", "efficient_risk", "efficient_volatily"]
    output = json.dumps(a)
    return HttpResponse(output)

def queue(request):

    #from .tasks import random_task
    #from django.contrib import messages
    #a = random_task.delay(15)
    #messages.success(request, "We are doing stuff")
    output = json.dumps(["alala"])
    return HttpResponse(output)