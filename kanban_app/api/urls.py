from rest_framework.routers import DefaultRouter

from .views import BoardViewSet


router = DefaultRouter()

router.register("boards", BoardViewSet)

urlpatterns = router.urls