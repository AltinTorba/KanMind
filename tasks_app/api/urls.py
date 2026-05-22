from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CommentListCreateView

router = DefaultRouter()
router.register(r"", TaskViewSet, basename="task") # Duhet basename, sepse route është bosh ("")

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += [
    path(
        "<int:task_id>/comments/",
        CommentListCreateView.as_view(),
        name="task-comments"
    ),
        path(
        "<int:task_id>/comments/<int:comment_id>/",
        CommentListCreateView.as_view(),
        name="task-comment-delete"
    ),
]