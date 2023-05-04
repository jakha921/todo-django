from django.urls import path, include
from rest_framework import routers

from .views import TaskViewSet, TaskAttachmentUploadView
from .drf_yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('tasks/<int:pk>/attachment/', TaskAttachmentUploadView.as_view(), name='task-attachment'),
]

urlpatterns += doc_urls
