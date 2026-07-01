from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest
from django.db.models import Count, Prefetch, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from kombu.asynchronous.aws.sqs import message

from devboard.forms import TaskForm, ProjectForm
from devboard.models import Project, Task, Comment
from devboard.mixins import OwnerQuerysetMixin

from django.utils.translation import gettext_lazy as _


# funkcja indeksowa ktora zwraca w przegladarce odpowiedz (indeksowa jest tylko zaslepka na szybko
# bo generalnie w html bedziemy pozniej to pisac)
# def index(request):
#     return HttpResponse("<h1>DevBoard - etap 1: scaffold!</h1>")

# # funkcja renderowa
# def index(request):
#     return render(request, 'index.html')




class ProjectListView(OwnerQuerysetMixin, ListView):    #MEEEGA wazna kolejnosc by Mixiny byly pierwsze
    #tu bedzie lista projektow - poki co jeden
    model = Project     #bedzie listował Project
    template_name = 'devboard/project_list.html'    # Ścieżka do szablonu
    context_object_name = 'projects'    # Domyślnie w HTML byłoby 'object_list'

    #dynamiczne filtrowanie wg nas:
    def get_queryset(self):
        #ustawimy tak aby widziec tylko swoje projekty, a nie kazdego tzn nie wszystkie
        return (
            # Project.objects.filter(owner=self.request.user)
            super().get_queryset()
            .annotate(task_count=Count('tasks'))     #annotate() dopisuje pola, komentarz etc
            .order_by('-created_at')
        )

class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    model = Project
    template_name = 'devboard/project_detail.html'
    context_object_name = 'project'

    # def get_queryset(self):
    #     return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tasks'] = (
            self.object.tasks
            .select_related('assignee')  # Pobierz dane o przypisanym użytkowniku
            .order_by('-priority', 'due_date')
        )
        ctx['tasks_count'] = self.object.tasks.count()
        return ctx

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "devboard/project_create.html"
    form_class = ProjectForm
    success_url = reverse_lazy("devboard:lista-project")

    # def get_success_url(self):
    #     return reverse_lazy("devboard:project-detail", args=[self.object.id])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Projekt '{form.instance.name}' został utworzony.")
        return super().form_valid(form)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'devboard/task_create.html'
    form_class = TaskForm       #to musi byc zdefiniowane w forms.py, bo inaczej nie bedzie wiedzialo jak wyglada formularz
    # success_url = reverse_lazy("devboard:lista-project")  #przekierowanie po dodaniu zadania na liste projektow

    def get_success_url(self):
        # return reverse_lazy("devboard:project-detail", args=[self.object.project.id])
        return self.object.project.get_absolute_url()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['project'].queryset = Project.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, f"Zadanie '{form.instance.title}' zostało dodane!")
        return super().form_valid(form)

# class TaskDetailView(LoginRequiredMixin, DetailView):
#     model = Task
#     template_name = 'devboard/task_detail.html'
#     context_object_name = 'task'
#
#     def get_queryset(self):
#         # Pokazujemy tylko zadania należące do projektów użytkownika
#         return Task.objects.filter(project__owner=self.request.user).select_related('project', 'assignee')
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         # Pobierz komentarze razem z autorem, aby uniknąć dodatkowych zapytań
#         ctx['comments'] = self.object.comments.select_related('author').all()
#         return ctx

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'devboard/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context

class TaskUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Task
    template_name = "devboard/task_create.html"
    form_class = TaskForm
    owner_field = "project__owner"  # Ustawiamy owner_field na pole powiązane z projektem

    def get_success_url(self):
        # return reverse_lazy("devboard:project-detail", args=[self.object.project.id])
        return self.object.project.get_absolute_url()

class TaskDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Task
    template_name = "devboard/task_confirm_delete.html"
    owner_field = "project__owner"  # Ustawiamy owner_field na pole powiązane z projektem
    # success_url = reverse_lazy("devboard:list-projects")  # przekierowanie po dodaniu zadania na liste projektow

    def get_success_url(self):
        # return reverse_lazy("devboard:project-detail", args=[self.object.project.id])
        return self.object.project.get_absolute_url()    #przekierowanie po usunieciu zadania na strone projektureturn self.object.project.get_absolute_url()

class TaskStatusUpdateView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        # qs = ...    #  pk taska: self.kwargs["pk"]
        q_owner = Q(project__owner=self.request.user)
        q_assignee = Q(assignee=self.request.user)
        qs = Task.objects.filter(q_owner | q_assignee).filter(pk=self.kwargs["pk"])
        task = get_object_or_404(qs)
        new_status = request.POST.get('status')

        #zweryfikowac new_status
        if not new_status or new_status not in Task.Status.values:
            raise BadRequest("Brak statusu w żądaniu POST lub niepoprawny ststus.")
            return HttpResponseBadRequest("Brak lub niepoprawny ststus.")

        task.status = new_status
        task.save()
        messages.success(request, f"Status zadania '{task.title}' został zaktualizowany.")
        # return redirect("devboard:task-detail", pk=task.pk)
        # return redirect("devboard:project-detail", pk=task.project.pk)
        return redirect(task.project.get_absolute_url())



