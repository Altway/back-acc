import json
from pypfopt.base_optimizer import portfolio_performance
import requests

from django.shortcuts import get_object_or_404

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .models import RecordHypothesis, HierarchicalRiskParity
from acc.encoders import NpEncoder 

from .misc.portefolio import historical_value_analyze, hrpopt_analyze, get_portfolio_performance

from django.contrib.auth.models import User 
from acc.serializers import UserSerializer, HierarchicalRiskParitySerializer, RecordHypothesisSerializer, HistoricalValueSerializer
from .models import RecordHypothesis, HierarchicalRiskParity, HistoricalValue
from rest_framework.renderers import JSONRenderer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import routers, serializers, viewsets
from rest_framework import permissions
from rest_framework import generics


from .permissions import IsOwner, IsOwnerOrReadOnly, Open

from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework import renderers


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


def coins_list(request):
    url = "https://api.coingecko.com/api/v3/coins/list"
    r = requests.get(url)

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
@require_POST
def hypothesis_data(request):
    data = json.loads(request.body)
    _ = {
        "user_id": data["user_id"],
        "hypothesis_name": data["hypothesis_name"],
    }

    if _["hypothesis_name"]:
        a = RecordHypothesis.objects.filter(user_id=_["user_id"], name=_["hypothesis_name"]).order_by('-id').first()
    else:
        a = RecordHypothesis.objects.filter(user_id=_["user_id"]).order_by('-id').first()
    b = get_portfolio_performance(a)

    print(f" DATA TOUT COURT {b}")
    d = b.fillna(0).cumsum()
    print(f"CUMSUM {d}")
    e = b.pct_change().fillna(0) * 100
    print(f"PCT CHANGE {e}")
    bigChartData = {
        "simple": b.fillna(0).tolist(),
        "cumsum": d.tolist(),
        "pct": e.tolist(),
    }
    bigChartLabels = [
        "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", 
        "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
    output = json.dumps({
        "bigChartData": bigChartData, 
        "bigChartLabels": bigChartLabels,
    })

    return HttpResponse(output)

    
@csrf_exempt
@require_POST
def preferred_hypothesis(request):
    if not request:
        data = {}
    data = json.loads(request.body)
    print(json.loads(request.body))
    _ = {
        "user_id": data["user_id"],
        "hypothesis_name": data["hypothesis_name"],
    }
    if _["hypothesis_name"]:
        a = RecordHypothesis.objects.filter(user_id=_["user_id"], name=_["hypothesis_name"]).order_by('-id').first()
    else:
        a = RecordHypothesis.objects.filter(user_id=_["user_id"]).order_by('-id').first()
    b = get_portfolio_performance(a)
    if a:
        #response = serializers.serialize('python', [a], ensure_ascii=False)
        response = JSONRenderer().render(RecordHypothesisSerializer(a).data)
        #response = a
    else:
        return HttpResponse(status=404)

    return HttpResponse(response)

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsOwner]
    permission_classes = [Open]

    def get_user_hypothesis_data(self, request, *args, **kwargs):
        user = self.get_object()
        print(dir(user))
        _ = {}

        if _["hypothesis_name"]:
            hypothesis = RecordHypothesis.objects.filter(user_id=user.id, name=_["hypothesis_name"]).order_by('-id').first()
        else:
            hypothesis = RecordHypothesis.objects.filter(user_id=user.id).order_by('-id').first()
        portfolio_performance = get_portfolio_performance(hypothesis)

        print(f" DATA TOUT COURT {portfolio_performance}")
        cumsum_portfolio = portfolio_performance.fillna(0).cumsum()
        print(f"CUMSUM {cumsum_portfolio}")
        pct_chg_portfolio = portfolio_performance.pct_change().fillna(0) * 100
        print(f"PCT CHANGE {pct_chg_portfolio}")
        bigChartData = {
            "simple": portfolio_performance.fillna(0).tolist(),
            "cumsum": cumsum_portfolio.tolist(),
            "pct": pct_chg_portfolio.tolist(),
        }
        bigChartLabels = [
            "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", 
            "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
        output = json.dumps({
            "bigChartData": bigChartData, 
            "bigChartLabels": bigChartLabels,
        })

        if portfolio_performance:
            #response = serializers.serialize('python', [a], ensure_ascii=False)
            response = JSONRenderer().render(RecordHypothesisSerializer(portfolio_performance).data)
            response.update(output)
            response = RecordHypothesisSerializer(portfolio_performance, many=True).data
            response.update(output)
            #response = a
        else:
            return HttpResponse(status=404)

        #a = [i.created_at for i in a]
        return Response(response)

class HierarchicalViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = HierarchicalRiskParity.objects.all()
    serializer_class = HierarchicalRiskParitySerializer
    #permission_classes = [IsOwner]
    permission_classes = [Open]
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
   #                       IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, user_pk=None):
        queryset = HierarchicalRiskParity.objects.filter(user_id=user_pk)
        serializer = HierarchicalRiskParitySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        queryset = HierarchicalRiskParity.objects.filter()
        hropt = get_object_or_404(queryset, pk=user_pk)
        serializer = HierarchicalRiskParitySerializer(hropt)
        return Response(serializer.data)

    def create(self, request):
        print(json.loads(request.body))
        data = json.loads(request.body)
        _ = {
            'name': data["name"],
            'risk_choice': data["risk_choice"], 
            'user_id': data["user_id"],
            'broker_fees': float(data["broker_fees"]),
            'capital': int(data["capital"]),
            'expected_return': data["expected_return"], 
            'expected_returns_id': data["expected_returns_id"], 
            'gamma':data["gamma"],
            'risk_free_rate': float(data["risk_free_rate"]),
            'short_selling': data["short_selling"],
            'coins_selected': data["coins_selected"], 

            'risk_model_id': data["risk_model_id"], 
            'returns_choice': data["returns_choice"], 
            'method_choice': data["method_choice"], 
            'risk_percentage': data["risk_percentage"], 
            'short_ratio': 0.3,
            'objectif': None,
            'period': '1y',
        }
        print(f"LE MEGA PAYLOAD: {_}")

        result = hrpopt_analyze(_)

        hropt = HierarchicalRiskParity(
            name=_["name"],
            risk_model_id=_["risk_model_id"],
            user_id=_["user_id"],
            broker_fees=_["broker_fees"],
            capital=_["capital"],
            expected_return_id=int(_["expected_returns_id"]), 
            gamma=_["gamma"],
            risk_free_rate=_["risk_free_rate"],
            short_selling=_["short_selling"],
            tickers_selected=_["coins_selected"],
        )
        hropt.save()

        # Save user try in database
        hypothesis = RecordHypothesis(
            name=_["name"],
            user_id=_["user_id"],
            capital=_["capital"],
            risk_free_rate=_["risk_free_rate"],
            method=_["method_choice"],
            strategy=_["risk_choice"],
            tickers_selected=_["coins_selected"],
            allocation=json.dumps(result["allocation"], cls=NpEncoder),
        )
        hypothesis.save()

        return HttpResponse(json.dumps(result["allocation"], cls=NpEncoder))

class HistoricalValueViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = HistoricalValue.objects.all()
    serializer_class = HistoricalValueSerializer
    permission_classes = [IsOwner]
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
   #                       IsOwnerOrReadOnly]

    def list(self, request):
        print("TES COUILLE FRERE")
        print(request.body)
        print(request.headers)
        return Response({"meh": 123})

    def create(self, request):
        print(json.loads(request.body))
        data = json.loads(request.body)
        _ = {
            'name': data["name"],
            'risk_choice': data["risk_choice"], 
            'user_id': data["user_id"],
            'broker_fees': float(data["broker_fees"]),
            'capital': int(data["capital"]),
            'expected_return': data["expected_return"], 
            'expected_returns_id': data["expected_returns_id"], 
            'gamma':data["gamma"],
            'risk_free_rate': float(data["risk_free_rate"]),
            'short_selling': data["short_selling"],
            'coins_selected': data["coins_selected"], 

            'risk_model_id': data["risk_model_id"], 
            'returns_choice': data["returns_choice"], 
            'method_choice': data["method_choice"], 
            'risk_percentage': data["risk_percentage"], 
            'short_ratio': 0.3,
            'objectif': None,
            'period': '1y',
        }
        print(f"LE MEGA PAYLOAD: {_}")

        result = historical_value_analyze(_)

        hv = HistoricalValue(
            name=_["name"],
            risk_model_id=_["risk_model_id"],
            user_id=_["user_id"],
            broker_fees=_["broker_fees"],
            capital=_["capital"],
            expected_return_id=int(_["expected_returns_id"]), 
            gamma=_["gamma"],
            risk_free_rate=_["risk_free_rate"],
            short_selling=_["short_selling"],
            tickers_selected=_["coins_selected"],
        )
        hv.save()

        # Save user try in database
        hypothesis = RecordHypothesis(
            name=_["name"],
            user_id=_["user_id"],
            capital=_["capital"],
            risk_free_rate=_["risk_free_rate"],
            method=_["method_choice"],
            strategy=_["risk_choice"],
            tickers_selected=_["coins_selected"],
            allocation=json.dumps(result["allocation"], cls=NpEncoder),
        )
        hypothesis.save()

        return HttpResponse(json.dumps(result["allocation"], cls=NpEncoder))



class RecordHypothesisViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = RecordHypothesis.objects.all()
    serializer_class = RecordHypothesisSerializer
    permission_classes = [IsOwner]
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
   #                       IsOwnerOrReadOnly]
    def list(self, request):
        data = json.loads(request.body)
        print(json.loads(request.body))
        _ = {
            "user_id": data["user_id"],
        }
        a = RecordHypothesis.objects.filter(user_id=_["user_id"]).order_by('-id').all()
        print("LES COUCOUILLES")
        print(request.body)
        print(request.headers)
        response = JSONRenderer().render(RecordHypothesisSerializer(a).data)
        print(response)
        return Response(response)