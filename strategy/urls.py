from django.urls import path

from . import views
from .views import HierarchicalViewSet, UserViewSet
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = routers.DefaultRouter()
 #router.register(r'hropt', views.HierarchicalRiskParitySet)

snippet_list = HierarchicalViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = HierarchicalViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = HierarchicalViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
user_hypothesis = UserViewSet.as_view({
    'get': 'bip'
})

router = DefaultRouter()
router.register(r'snippets', views.HierarchicalViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'hypothesis', views.RecordHypothesisViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('risk', views.risk, name='risk'),
    path('returns', views.returns, name='returns'),
    path('coins_list', views.coins_list, name='coins_list'),
    path('goals', views.goals, name='goals'),
    path('preferred_hypothesis', views.preferred_hypothesis, name='preferred_hypothesis'),
    path('hypothesis_data', views.hypothesis_data, name='hypothesis_data'),
    path('users/<int:pk>/hypothesis', user_hypothesis, name='user-hypothesis'),
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