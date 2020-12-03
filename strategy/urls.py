from django.urls import path

from . import views

urlpatterns = [
    path('risk', views.risk, name='risk'),
    path('returns', views.returns, name='returns'),
    path('input', views.input, name='input'),
]