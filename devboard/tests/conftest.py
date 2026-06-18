import pytest
from django.contrib.auth.models import User

from devboard.models import Project, Task


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def project(user):
    return Project.objects.create(name='Test Project', owner=user)

@pytest.fixture
def task(project):
    return Task.objects.create(title='Test Task',
                               project=project,
                               status=Task.Status.TODO,
                               priority=Task.Priority.MEDIUM)

@pytest.fixture
def logged_user():
    return User.objects.create_user(username='loggeduser', password='testpass123')