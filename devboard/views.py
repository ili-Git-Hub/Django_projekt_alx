from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from devboard.models import Project


# funkcja indeksowa ktora zwraca w przegladarce odpowiedz (indeksowa jest tylko zaslepka na szybko
# bo generalnie w html bedziemy pozniej to pisac)
# def index(request):
#     return HttpResponse("<h1>DevBoard - etap 1: scaffold!</h1>")

# # funkcja renderowa
# def index(request):
#     return render(request, 'index.html')

class ProjectListView(ListView, LoginRequiredMixin):
    #tu bedzie lista projektow - poki co jeden
    model = Project     #bedzie listował Project
    template_name = 'devboard/project_list.html'    # Ścieżka do szablonu
    context_object_name = 'projects'    # Domyślnie w HTML byłoby 'object_list'

    #dynamiczne filtrowanie wg nas:
    def get_queryset(self):
        #ustawimy tak aby widziec tylko swoje projekty, a nie kazdego tzn nie wszystkie
        return (
            Project.objects.filter(owner=self.request.user)
            .annotate(task_count=Count('tasks'))     #annotate() dopisuje pola, komentarz etc
            .order_by('-created_at')
        )
