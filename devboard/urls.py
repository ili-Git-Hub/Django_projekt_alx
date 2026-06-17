from django.urls import path

from devboard import views
from devboard.views import ProjectDetailView

app_name = "devboard"

urlpatterns = [

    path("", views.ProjectListView.as_view(), name="lista-project"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project-detail")
]