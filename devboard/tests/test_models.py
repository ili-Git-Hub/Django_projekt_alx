import pytest

from devboard.models import Task

@pytest.mark.django_db
class TestTaskModel:
    def test_default_status_is_todo(self, task):
        assert task.status == Task.Status.TODO

    def test_str_contains_title(self, task):
        assert 'Test Task' in str(task)

