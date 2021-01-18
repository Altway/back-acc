from django.urls import path

from . import views

urlpatterns = [
    path('risk', views.risk, name='risk'),
    path('returns', views.returns, name='returns'),
    path('hrpopt', views.HRPOpt_method, name='hrpopt'),
    path('historical', views.historical_method, name='historical'),
    path('coins_list', views.coins_list, name='coins_list'),
    path('goals', views.goals, name='goals'),
    path('queue', views.queue, name='queue'),
    path('preferred_hypothesis', views.preferred_hypothesis, name='preferred_hypothesis'),
    path('hypothesis_data', views.hypothesis_data, name='hypothesis_data'),
]