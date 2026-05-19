from rest_framework.routers import DefaultRouter

from .views import BoardViewSet


# router = DefaultRouter()

# router.register("boards", BoardViewSet)

router = DefaultRouter()
router.register(r"", BoardViewSet, basename="task") # Duhet basename, sepse route është bosh ("")

urlpatterns = router.urls