from rest_framework import viewsets, permissions

from devboard.models import Comment, Task
from devboard.serializers import CommentSerializer, TaskSerializer


# class CommentViewSet(viewsets.ReadOnlyModelViewSet):
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).select_related("author","task")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            project__owner=self.request.user
        ).select_related("project", "assignee")