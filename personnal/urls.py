from django.urls import path, include
from rest_framework_nested import routers

from .views import (
    UserMetaViewSet
)
from strategy.views import UserViewSet as strategy_userviewset

router = routers.DefaultRouter()
# The name UserViewSet and view.UserMEtaViewSet are not from the same view !!!! (WARNING naming uscks here)
router.register(r'users', strategy_userviewset)

usermeta_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
usermeta_router.register(r'usermeta', UserMetaViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(usermeta_router.urls)),
]