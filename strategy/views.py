from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

    print("MEHEHEHE")
    print(json.loads(request.body))
    output = {"truc": 123}
    return HttpResponse(output)