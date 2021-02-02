from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.core import serializers



from .models import RecordHypothesis, HierarchicalRiskParity
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

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, RecordHypothesis):
            return str(obj)
        return super().default(obj)

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
        'method_choice': data["method_choice"], 
        'risk_percentage': data["risk_percentage"], 
        'expected_return': data["expected_return"], 
        'coins_selected': data["coins_selected"], 
        'short_selling': data["short_selling"],
        'risk_free_rate': float(data["risk_free_rate"]),
        'broker_fees': float(data["broker_fees"]),
        'capital': int(data["capital"]),
        'gamma':data["gamma"],
        "short_ratio": 0.3,
        "objectif": None,
        "period": "1y",
        "name": data["name"],
    }

    result = hrpopt(_)
    #allocation, weights = historical_value(_)
    #allocation = json.dumps(allocation, cls=NpEncoder)
    #weights = json.dumps(weights, cls=NpEncoder)

    # Save in database user try

    hypothesis = RecordHypothesis(
        name=_["name"],
        capital=_["capital"],
        risk_free_rate=_["risk_free_rate"],
        broker_fees=_["broker_fees"],
        gamma=_["gamma"],
        short_selling=_["short_selling"],
        method=_["method_choice"],
        strategy=_["risk_choice"],
        tickers_selected=_["coins_selected"],
        allocation=json.dumps(result["allocation"], cls=NpEncoder),
    )
    hypothesis.save()

    return HttpResponse(json.dumps(result["allocation"], cls=NpEncoder))
    #return HttpResponse(json.dumps({"maisoui": 40, "bonjour": 15, "trcu": 25, "this": 20}))


@csrf_exempt
def historical_method(request):
    print(json.loads(request.body))
    data = json.loads(request.body)
    _ = {
        'risk_choice': data["risk_choice"], 
        'returns_choice': data["returns_choice"], 
        'method_choice': data["method_choice"], 
        'risk_percentage': data["risk_percentage"], 
        'expected_return': data["expected_return"], 
        'coins_selected': data["coins_selected"], 
        'short_selling': data["short_selling"],
        'risk_free_rate': float(data["risk_free_rate"]),
        'broker_fees': float(data["broker_fees"]),
        'capital': int(data["capital"]),
        'gamma':data["gamma"],
        "short_ratio": 0.3,
        "objectif": None,
        "period": "1y",
        "name": data["name"],
    }
    result = historical_value(_)
    #allocation, weights = historical_value(_)
    #allocation = json.dumps(allocation, cls=NpEncoder)
    #weights = json.dumps(weights, cls=NpEncoder)

    hypothesis = RecordHypothesis(
        name=_["name"],
        capital=_["capital"],
        risk_free_rate=_["risk_free_rate"],
        broker_fees=_["broker_fees"],
        gamma=_["gamma"],
        short_selling=_["short_selling"],
        method=_["method_choice"],
        strategy=_["risk_choice"],
        tickers_selected=_["coins_selected"],
        allocation=json.dumps(result["allocation"], cls=NpEncoder),
    )
    hypothesis.save()
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


@csrf_exempt
def hypothesis_data(request):
    #data = json.loads(request.body)
    #print(json.loads(request.body))
    #_ = {
    #    "id": data["id"],
    #}

    bigChartData = {
        "Test": [40,30,10,10,50,45,85,80,100,45,55,45],
        "Truc": [80,10,20,60,54,75,5,40,0,12,58,12],
        "Mich": [30,10,100,40,41,78,98,100,100,130,45,20],
    }
    bigChartLabels = [
        "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", 
        "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    output = json.dumps({
        "bigChartData": bigChartData, 
        "bigChartLabels": bigChartLabels,
    })

    return HttpResponse(output)


from django.contrib.auth.models import User, Group
from acc.serializers import UserSerializer, GroupSerializer, HierarchicalRiskParitySerializer
from .models import RecordHypothesis, HierarchicalRiskParity
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import routers, serializers, viewsets
from rest_framework import permissions
from rest_framework import generics


from .permissions import IsOwner, IsOwnerOrReadOnly

from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework import renderers

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
@csrf_exempt
def preferred_hypothesis(request):
    data = json.loads(request.body)
    data = {}
    data["id"] = 1
    print(json.loads(request.body))
    _ = {
        "id": data["id"],
    }
    a = RecordHypothesis.objects.filter(id=_["id"]).order_by('-id').first()
    #print(a)
    if a:
        response = serializers.serialize('python', [a], ensure_ascii=False)
    else:
        return HttpResponse(status=404)

    a = response[0]["fields"]
    a.pop("created_at", None)
    a.pop("updated_at", None)
    a.pop("short_selling", None)
    print(a)
    #output = json.dumps(list(a))
    #print(output)
    print(type(a))
    return HttpResponse(json.dumps([a]))


class HierarchicalViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = HierarchicalRiskParity.objects.all()
    serializer_class = HierarchicalRiskParitySerializer
    permission_classes = [IsOwner]
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
   #                       IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):
        print("TES COUILLE FRERE")
        print(request.body)
        print(request.headers)
        return Response({"meh": 123})

    def create(self, request):
        print(json.loads(request.body))
        data = json.loads(request.body)
        _ = {
            'risk_choice': data["risk_choice"], 
            'returns_choice': data["returns_choice"], 
            'method_choice': data["method_choice"], 
            'risk_percentage': data["risk_percentage"], 
            'expected_return': data["expected_return"], 
            'coins_selected': data["coins_selected"], 
            'short_selling': data["short_selling"],
            'risk_free_rate': float(data["risk_free_rate"]),
            'broker_fees': float(data["broker_fees"]),
            'capital': int(data["capital"]),
            'gamma':data["gamma"],
            "short_ratio": 0.3,
            "objectif": None,
            "period": "1y",
            "name": data["name"],
        }

        result = hrpopt(_)
        #allocation, weights = historical_value(_)
        #allocation = json.dumps(allocation, cls=NpEncoder)
        #weights = json.dumps(weights, cls=NpEncoder)

        # Save in database user try

        hypothesis = RecordHypothesis(
            name=_["name"],
            capital=_["capital"],
            risk_free_rate=_["risk_free_rate"],
            broker_fees=_["broker_fees"],
            gamma=_["gamma"],
            short_selling=_["short_selling"],
            method=_["method_choice"],
            strategy=_["risk_choice"],
            tickers_selected=_["coins_selected"],
            allocation=json.dumps(result["allocation"], cls=NpEncoder),
        )
        hypothesis.save()

        return HttpResponse(json.dumps(result["allocation"], cls=NpEncoder))
        #return HttpResponse(json.dumps({"maisoui": 40, "bonjour": 15, "trcu": 25, "this": 20}))