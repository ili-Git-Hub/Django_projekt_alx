from django.urls import path

from devboard import views
from devboard.views import ProjectDetailView, TaskDetailView

app_name = "devboard"

urlpatterns = [

    path("", views.ProjectListView.as_view(), name="lista-project"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("zadania/nowe", views.TaskCreateView.as_view(), name="task-create"),
    path("zadania/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),  # nowy URL
    path("projekty/nowy/", views.ProjectCreateView.as_view(), name="project-create"),
    path("zadania/<int:pk>/edytuj/", views.TaskUpdateView.as_view(), name="task-update"),
    path("zadania/<int:pk>/usun/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("zadania/<int:pk>/status", views.TaskStatusUpdateView.as_view(), name="task-status"),
]
