from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from kombu.asynchronous.aws.sqs import message

from devboard.forms import TaskForm
from devboard.models import Project, Task

from django.utils.translation import gettext_lazy as _


# funkcja indeksowa ktora zwraca w przegladarce odpowiedz (indeksowa jest tylko zaslepka na szybko
# bo generalnie w html bedziemy pozniej to pisac)
# def index(request):
#     return HttpResponse("<h1>DevBoard - etap 1: scaffold!</h1>")

# # funkcja renderowa
# def index(request):
#     return render(request, 'index.html')

class ProjectListView(LoginRequiredMixin, ListView):    #MEEEGA wazna kolejnosc by Mixiny byly pierwsze
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

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'devboard/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tasks'] = (
            self.object.tasks
            .select_related('assignee')  # Pobierz dane o przypisanym użytkowniku
            .order_by('-priority', 'due_date')
        )
        ctx['tasks_count'] = self.object.tasks.count()
        return ctx

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'devboard/task_create.html'
    form_class = TaskForm       #to musi byc zdefiniowane w forms.py, bo inaczej nie bedzie wiedzialo jak wyglada formularz
    # success_url = reverse_lazy("devboard:task_list")
    success_url = reverse_lazy("devboard:lista-projects")  #przekierowanie po dodaniu zadania na liste projektow

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['project'].queryset = Project.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, f"Zadanie '{form.instance.title}' zostało dodane!")
        return super().form_valid(form)
