import json

from django.contrib.auth.models import User 
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Coin, UserMeta
from strategy.models import RecordHypothesis
from acc.serializers import UserMetaSerializer
from acc.permissions import IsOwner, IsOwnerOrReadOnly, Open


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


class UserMetaViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = UserMeta.objects.all()
    serializer_class = UserMetaSerializer
    permission_classes = [Open]  #[IsOwner] [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def list(self, request, user_pk=None):
        queryset = UserMeta.objects.filter(user_id=user_pk).first()
        serializer = UserMetaSerializer(queryset, many=False)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        queryset = UserMeta.objects.filter()
        obj = get_object_or_404(queryset, pk=user_pk)
        serializer = UserMetaSerializer(obj)
        return Response(serializer.data)