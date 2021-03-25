from django.urls import path, include
from rest_framework_nested import routers

from .views import (
    HierarchicalViewSet, RecordHypothesisViewSet, UserViewSet, HistoricalValueViewSet, 
    risk, returns, coins_list, goals
)

hypothesis_data = RecordHypothesisViewSet.as_view({
    'get': 'hypothesis_data',
})


router = routers.DefaultRouter()

router.register(r'users', UserViewSet)

hierarchical_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
hierarchical_router.register(r'hierarchical', HierarchicalViewSet)

historical_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
historical_router.register(r'historical', HistoricalValueViewSet)

hypothesis_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
hypothesis_router.register(r'hypothesis', RecordHypothesisViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(hierarchical_router.urls)),
    path('', include(historical_router.urls)),
    path('', include(hypothesis_router.urls)),
    path('hypothesis_data', hypothesis_data, name='hypothesis-data'),
    path('risk', risk, name='risk'),
    path('returns', returns, name='returns'),
    path('coins_list', coins_list, name='coins_list'),
    path('goals', goals, name='goals'),
]