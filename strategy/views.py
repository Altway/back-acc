from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from .misc.portefolio import ici, historical_value, hrpopt

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
        "SAMPLECOV": "sample covariance",
        "SEMICOV": "semi covariance",
        "EXPCOV": "exponential covariance",
        "MINDETCOV": "minimum determinant covariance",
        "COVSHRINKAGE": "covariance Shrinkage",
        "LEDOITWOLF": "ledoit-Wolf method",
        "ORACLEAPPROX": "oracle Approximation",
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
def HRPOpt_method(request):
    print(json.loads(request.body))
    data = json.loads(request.body)
    _ = {
        'risk_choice': data["risk_choice"], 
        'returns_choice': data["returns_choice"], 
        'risk_percentage': data["risk_percentage"], 
        'expected_return': data["expected_return"], 
        'coins_selected': data["coins_selected"], 
        'short_selling': data["short_selling"],
        'risk_free_rate': float(data["risk_free_rate"]),
        'capital': int(data["capital"]),
        'gamma':data["gamma"],
        "short_ratio": 0.3,
        "objectif": None,
        "period": "1y",
    }

    result = hrpopt(_)
    #allocation, weights = historical_value(_)
    #allocation = json.dumps(allocation, cls=NpEncoder)
    #weights = json.dumps(weights, cls=NpEncoder)
    return HttpResponse(json.dumps(result["allocation"], cls=NpEncoder))
    #return HttpResponse(json.dumps({"maisoui": 40, "bonjour": 15, "trcu": 25, "this": 20}))


@csrf_exempt
def historical_method(request):
    print(json.loads(request.body))
    data = json.loads(request.body)
    _ = {
        'risk_choice': data["risk_choice"], 
        'returns_choice': data["returns_choice"], 
        'risk_percentage': data["risk_percentage"], 
        'expected_return': data["expected_return"], 
        'coins_selected': data["coins_selected"], 
        'short_selling': data["short_selling"],
        'risk_free_rate': float(data["risk_free_rate"]),
        'capital': int(data["capital"]),
        'gamma':data["gamma"],
        "short_ratio": 0.3,
        "objectif": None,
        "period": "1y",
    }

    result = historical_value(_)
    #allocation, weights = historical_value(_)
    #allocation = json.dumps(allocation, cls=NpEncoder)
    #weights = json.dumps(weights, cls=NpEncoder)
    return HttpResponse(json.dumps(result["allocation"], cls=NpEncoder))
    #return HttpResponse(json.dumps({"maisoui": 40, "bonjour": 15, "trcu": 25, "this": 20}))


def coins_list(request):
    url = "https://api.coingecko.com/api/v3/coins/list"
    r = requests.get(url)

    #a = json.dumps(r.json()[30:50])
    #print(a)
    a = [
        {"id": 1,"symbol": "ABNB"}, 
        {"id": 2,"symbol": "AMD"}, 
        {"id": 3,"symbol": "V"}, 
        {"id": 4,"symbol": "CSCO"}, 
        {"id": 5,"symbol": "HNI"}, 
        {"id": 6,"symbol": "ORI"}, 
        {"id": 7,"symbol": "SPR"}, 
        {"id": 8,"symbol": "XOM"}, 
        {"id": 9,"symbol": "CB"}, 
        {"id": 10,"symbol": "LOW"}, 
        {"id": 11,"symbol": "MDLZ"}, 
        {"id": 12,"symbol": "GRWG"}, 
        {"id": 13,"symbol": "BIIB"}, 
        {"id": 14,"symbol": "ADBE"}, 
        {"id": 15,"symbol": "CRSR"}, 
        {"id": 16,"symbol": "INTC"}, 
        {"id": 17,"symbol": "JNJ"}, 
        {"id": 18,"symbol": "JPM"}, 
        {"id": 19,"symbol": "LAZ"}, 
        {"id": 20,"symbol": "NVDA"}, 
    ]
    #a = [
    #    {"id": "0-5x-long-shitcoin-index-token", "symbol": "halfshit", "name": "0.5X Long Shitcoin Index Token"}, 
    #    {"id": "0-5x-long-swipe-token", "symbol": "sxphalf", "name": "0.5X Long Swipe Token"}, 
    #    {"id": "0-5x-long-tether-gold-token", "symbol": "xauthalf", "name": "0.5X Long Tether Gold Token"}, {"id": "0-5x-long-tether-token", "symbol": "usdthalf", "name": "0.5X Long Tether Token"}, {"id": "0-5x-long-tezos-token", "symbol": "xtzhalf", "name": "0.5X Long Tezos Token"}, {"id": "0-5x-long-theta-network-token", "symbol": "thetahalf", "name": "0.5X Long Theta Network Token"}, {"id": "0-5x-long-tomochain-token", "symbol": "tomohalf", "name": "0.5X Long TomoChain Token"}, {"id": "0-5x-long-trx-token", "symbol": "trxhalf", "name": "0.5X Long TRX Token"}, {"id": "0-5x-long-xrp-token", "symbol": "xrphalf", "name": "0.5X Long XRP Token"}, {"id": "0cash", "symbol": "zch", "name": "0cash"}, {"id": "0chain", "symbol": "zcn", "name": "0chain"}, {"id": "0x", "symbol": "zrx", "name": "0x"}, {"id": "0xcert", "symbol": "zxc", "name": "0xcert"}, {"id": "0xmonero", "symbol": "0xmr", "name": "0xMonero"}, {"id": "100-waves-eth-btc-set", "symbol": "100wratio", "name": "100 Waves ETH/BTC Set"}, {"id": "100-waves-eth-usd-yield-set", "symbol": "100w", "name": "100 Waves ETH/USD Yield Set"}, {"id": "12ships", "symbol": "TSHP", "name": "12Ships"}, {"id": "1337", "symbol": "1337", "name": "Elite"}]
        
    """    
        "V", "AMD", "CSCO", "HNI", "ORI", 
        "SPR", "XOM", "CB", "LOW", "MDLZ", "GRWG", 
        "BIIB", "ADBE", "CRSR", "INTC", "JNJ", 
        "JPM", "LAZ", "NVDA"
    """
    return HttpResponse(json.dumps(a))

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