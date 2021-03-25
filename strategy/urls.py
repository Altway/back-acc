from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from. import views

from .views import (
    HierarchicalViewSet, RecordHypothesisViewSet, UserViewSet, HistoricalValueViewSet, 
    risk, returns, coins_list, goals
)

hypothesis_data = RecordHypothesisViewSet.as_view({
    'get': 'hypothesis_data',
})
""" FOR THE RECORD
from rest_framework import renderers
hropt = HierarchicalViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
hropt_detail = HierarchicalViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
hropt_highlight = HierarchicalViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
"""
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)

hropt_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
hropt_router.register(r'hropt', HierarchicalViewSet)

historical_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
historical_router.register(r'historical', HistoricalValueViewSet)

hypothesis_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
hypothesis_router.register(r'hypothesis', RecordHypothesisViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(hropt_router.urls)),
    path('', include(historical_router.urls)),
    path('', include(hypothesis_router.urls)),
    path('hypothesis_data', hypothesis_data, name='hypothesis-data'),
    path('risk', risk, name='risk'),
    path('returns', returns, name='returns'),
    path('coins_list', coins_list, name='coins_list'),
    path('goals', goals, name='goals'),
]
"""
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])
urlpatterns = [
    path('risk', views.risk, name='risk'),
    path('returns', views.returns, name='returns'),
    #path('hrpopt', views.HRPOpt_method, name='hrpopt'),
    path('historical', views.historical_method, name='historical'),
    path('coins_list', views.coins_list, name='coins_list'),
    path('goals', views.goals, name='goals'),
    path('queue', views.queue, name='queue'),
    path('preferred_hypothesis', views.preferred_hypothesis, name='preferred_hypothesis'),
    path('hypothesis_data', views.hypothesis_data, name='hypothesis_data'),

    path('snippets/', views.HierarchicalRiskParityList.as_view()),
    path('snippets/<int:pk>', views.HierarchicalRiskParityDetail.as_view()),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
]
"""