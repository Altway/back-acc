import json
import requests

from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
#from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.http import require_http_methods, require_GET, require_POST

from rest_framework import viewsets, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from acc.encoders import NpEncoder 
from acc.serializers import UserSerializer, HierarchicalRiskParitySerializer, RecordHypothesisSerializer, HistoricalValueSerializer
from acc.permissions import IsOwner, IsOwnerOrReadOnly, Open

from .models import RecordHypothesis, HierarchicalRiskParity, HistoricalValue
from .misc.portefolio import historical_value_analyze, hrpopt_analyze, get_portfolio_performance


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


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsOwner]
    permission_classes = [Open]

class HierarchicalViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = HierarchicalRiskParity.objects.all()
    serializer_class = HierarchicalRiskParitySerializer
    permission_classes = [Open]  #[IsOwner] [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, user_pk=None):
        queryset = HierarchicalRiskParity.objects.filter(user_id=user_pk).order_by('-id').all()
        serializer = HierarchicalRiskParitySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        queryset = HierarchicalRiskParity.objects.filter()
        obj = get_object_or_404(queryset, pk=user_pk)
        serializer = HierarchicalRiskParitySerializer(obj)
        return Response(serializer.data)

    def create(self, request):
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
    permission_classes = [Open]  #[IsOwner] [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def list(self, request, user_pk=None):
        queryset = HistoricalValue.objects.filter(user_id=user_pk).order_by('-id').all()
        serializer = HistoricalValueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        queryset = HistoricalValue.objects.filter()
        obj = get_object_or_404(queryset, pk=user_pk)
        serializer = HistoricalValueSerializer(obj)
        return Response(serializer.data)

    def create(self, request):
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
    permission_classes = [Open]  #[IsOwner] [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def list(self, request, user_pk=None):
        queryset = RecordHypothesis.objects.filter(user_id=user_pk).order_by('-id').all()
        serializer = RecordHypothesisSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        queryset = RecordHypothesis.objects.filter(id=pk, user_id=user_pk)
        obj = get_object_or_404(queryset, pk=pk)
        serializer = RecordHypothesisSerializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def hypothesis_data(self, request, pk=None, user_pk=None, *args, **kwargs):
        queryset = RecordHypothesis.objects.filter(id=pk, user_id=user_pk)
        obj = get_object_or_404(queryset, pk=pk)
        serializer = RecordHypothesisSerializer(obj)
        portfolio_performance = get_portfolio_performance(obj)
        cumsum_portfolio_performance = portfolio_performance.fillna(0).cumsum()
        pct_change_portfolio_performance = portfolio_performance.pct_change().fillna(0) * 100

        bigChartData = {
            "simple": portfolio_performance.fillna(0).tolist(),
            "cumsum": cumsum_portfolio_performance.tolist(),
            "pct": pct_change_portfolio_performance.tolist(),
        }
        bigChartLabels = [
            "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", 
            "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"]
        output = json.dumps({
            "info": serializer.data,
            "bigChartData": bigChartData, 
            "bigChartLabels": bigChartLabels,
        })
        return HttpResponse(output)