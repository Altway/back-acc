import json
import requests

from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
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
    permission_classes = [Open] # [IsOwner]
    
    @action(detail=True, methods=["get"])
    def calculate_repartition(self, request, *args, **kwargs):
        queryset = HierarchicalRiskParity.objects.filter()
        obj = get_object_or_404(queryset, pk=kwargs.get("user_pk", None))
        serializer = HierarchicalRiskParitySerializer(obj)
        request.data.update({
            'short_ratio': 0.3,
            'objectif': None,
            'period': '1y',
        })
        result = historical_value_analyze(request.data)
        hypothesis = RecordHypothesis(
            name=request.data["name"],
            user_id=request.data["user_id"],
            capital=request.data["capital"],
            risk_free_rate=request.data["risk_free_rate"],
            method=request.data["method_choice"],
            strategy=request.data["risk_choice"],
            tickers_selected=request.data["tickers_selected"],
            allocation=json.dumps(result["allocation"], cls=NpEncoder),
        )
        hypothesis.save()
        resp = serializer.data
        resp.update({"hypothesis_id": hypothesis.id})
        

        return Response(resp, status=status.HTTP_201_CREATED, headers=headers)

class HierarchicalViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = HierarchicalRiskParity.objects.all()
    serializer_class = HierarchicalRiskParitySerializer
    permission_classes = [Open]  #[IsOwner] [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


    def list(self, request, user_pk=None):
        queryset = HierarchicalRiskParity.objects.filter(user_id=user_pk).order_by('-id').all()
        serializer = HierarchicalRiskParitySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        queryset = HierarchicalRiskParity.objects.filter()
        obj = get_object_or_404(queryset, pk=user_pk)
        serializer = HierarchicalRiskParitySerializer(obj)
        return Response(serializer.data)

    def create(self, request, user_pk=None, *args, **kwargs):
        request.data.update({"user": user_pk, "user_id": int(user_pk)})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        request.data.update({
            'short_ratio': 0.3,
            'objectif': None,
            'period': '1y',
        })
        result = hrpopt_analyze(request.data)
        hypothesis = RecordHypothesis(
            name=request.data["name"],
            user_id=request.data["user_id"],
            capital=request.data["capital"],
            risk_free_rate=request.data["risk_free_rate"],
            method=request.data["method_choice"],
            strategy=request.data["risk_choice"],
            tickers_selected=request.data["tickers_selected"],
            allocation=json.dumps(result["allocation"], cls=NpEncoder),
        )
        hypothesis.save()
        resp = serializer.data
        resp.update({"hypothesis_id": hypothesis.id})
        queryset = User.objects.filter()
        obj = get_object_or_404(queryset, pk=user_pk)
        obj.usermeta.preferred_hypothesis_id = hypothesis.id
        obj.save()

        return Response(resp, status=status.HTTP_201_CREATED, headers=headers)

class HistoricalValueViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = HistoricalValue.objects.all()
    serializer_class = HistoricalValueSerializer
    permission_classes = [Open]  #[IsOwner] [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    """
    def list(self, request, user_pk=None):
        queryset = HistoricalValue.objects.filter(user_id=user_pk).order_by('-id').all()
        serializer = HistoricalValueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = HistoricalValue.objects.filter()
        obj = get_object_or_404(queryset, pk=kwargs.get("pk", None))
        serializer = HistoricalValueSerializer(obj)
        return Response(serializer.data)
    """
    def create(self, request, user_pk=None, *args, **kwargs):
        request.data.update({"user": user_pk, "user_id": int(user_pk)})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Create the associated hypothesis
        request.data.update({
            'short_ratio': 0.3,
            'objectif': None,
            'period': '1y',
        })
        result = historical_value_analyze(request.data)
        hypothesis = RecordHypothesis(
            name=request.data["name"],
            user_id=request.data["user_id"],
            capital=request.data["capital"],
            risk_free_rate=request.data["risk_free_rate"],
            method=request.data["method_choice"],
            strategy=request.data["risk_choice"],
            tickers_selected=request.data["tickers_selected"],
            allocation=json.dumps(result["allocation"], cls=NpEncoder),
        )
        hypothesis.save()
        resp = serializer.data
        resp.update({"hypothesis_id": hypothesis.id})
        

        return Response(resp, status=status.HTTP_201_CREATED, headers=headers)
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
        print(queryset)
        if queryset:
            obj = get_object_or_404(queryset, pk=pk)
            serializer = RecordHypothesisSerializer(obj)
        else:
            queryset = RecordHypothesis.objects.filter(user_id=user_pk).order_by('-id').first()
            serializer = RecordHypothesisSerializer(queryset)

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