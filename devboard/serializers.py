from rest_framework import serializers

from devboard.models import Comment, Task


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True, source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'task', 'author_name', 'body', 'created')
        read_only_fields = ('id', 'author_name', 'created')

class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(source='assignee.username',
                                          read_only=True,
                                          default=None)
    project_name = serializers.CharField(source='project.name',
                                         read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'title',
            'description', 'status', 'priority',
            'assignee_name', 'project_name',
        )
        read_only_fields = ('id', 'created_at')
