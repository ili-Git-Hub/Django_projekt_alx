import pytest
from django.test import Client
from django.urls import reverse

from devboard.models import Task


@pytest.mark.django_db(transaction=True)
class TestTaskCreateView:
    # def test_create_task(self, logged_user, project):
    def test_create_task(self, user, project):
        # Log in the user
        # logged_user.set_password('testpass123')
        # logged_user.save()
        user.set_password('testpass123')
        user.save()
        client = Client()
        # client.login(username='testuser', password='testpass123')
        client.login(username=user.username, password='testpass123')

        # Prepare data for creating a task
        data = {
            'title': 'New Task',
            'description': 'Task description',
            'status': Task.Status.TODO,
            'priority': Task.Priority.MEDIUM,
            'project': project.id
        }

        # Send POST request to create a task
        response = client.post(reverse('devboard:task-create'), data)

        # Check if the task was created successfully
        assert response.status_code == 302  # Redirect after successful creation
        assert response.url == reverse('devboard:lista-project')
        assert Task.objects.count() == 1