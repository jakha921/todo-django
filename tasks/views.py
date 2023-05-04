from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import TasksSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only the tasks created by the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new task associated with the authenticated user"""
        serializer.save(user=self.request.user)


class TaskAttachmentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        file = requests.FILES.get('file')
        if file:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(file.name, file)
            task.attachment = fs.url(filename)
            task.save()
            return Response({'status': 'success'})
        return Response({'status': 'failed'})
