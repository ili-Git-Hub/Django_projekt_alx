from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# ta klasa dziedziczy z modelu
class Project(models.Model):
    #teraz pola ponizej - symbolizuja pola bazodanowe
    name = models.CharField(max_length=200, verbose_name="Nazwa")
    description = models.TextField(blank=True, verbose_name="Opis")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,   #co sie wydarzy jak usuniemy usera Kowalskiego
        related_name="projects",    #jak zrobimy user.projects to on bedzie wiedział jakie sa relacje user-projekty
        verbose_name="Właściciel",  #nazwa w bazie, zeby admin wiedzial co mial na mysli tworca
    )
    created_at = models.DateTimeField(auto_now_add=True)    #gdy tworzymy projekt to automat data sie wpisze
    updated_at = models.DateTimeField(auto_now=True)

    #tajemnicza klasa Meta to metadane czyli podstawowe opcje ktore mozna uzyc
    class Meta:
        ordering = ["-created_at"]  #segregowanie, sortowanie wpisow
        verbose_name = "Projekt"
        verbose_name_plural = "Projekty"    #wersja mnoga, wyswietlanie, gadzet

    # magic function, inaczej dunder - ten akurat ustawia ze nasza klasa Projekt autometycznie wyswietla pole name
    def __str__(self) -> str:
        return self.name

    # funkcja obliczajaca/zliczajaca zadnia
    def task_count(self) -> int:
        return self.tasks.count()

#klasa zadan
class Task(models.Model):
    """Zadanie przypisane do projektu."""

    #lista mozliwosci w statusie
    class Status(models.TextChoices):
        TODO = "TODO", _("Do zrobienia")
        IN_PROGRESS = "IN_PROGRESS", _("W trakcie")
        DONE = "DONE", _("Ukończone")

    class Priority(models.IntegerChoices):
        LOW = 1, _("Niski")
        MEDIUM = 2, _("Średni")
        HIGH = 3, _("Wysoki")

    title = models.CharField(max_length=300, verbose_name=_("Tytuł"))
    description = models.TextField(blank=True, verbose_name="Opis")
    #zadania beda korespondowaly z projektem:
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Projekt",
    )
    #osoba odpowedzialna za projekt
    assignee = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  #tutaj nie kasujemy projektu jak usuniemy usera, tylko zostawiamy puste pole
        related_name="assigned_tasks",
        verbose_name="Przypisany do",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
        verbose_name="Status",
    )
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="Priorytet",
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Termin")   #data tylko
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-priority", "due_date"]    #malejaco i rosnaco 2gie
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"

    def __str__(self) -> str:
        return f"[{self.get_priority_display()}] {self.title}"

    # to odlicza czas do wykonania zadania: - daje sie wywolac bez nawiastow, bo jest @property
    @property
    def is_overdue(self) -> bool:
        if self.due_date and self.status != self.Status.DONE:
            return self.due_date < timezone.now().date()
        return False

# klasa komentarzy - do zadania
class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Zadanie",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Autor",
    )
    body = models.TextField(verbose_name="Treść")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"

    def __str__(self) -> str:
        return f"{self.author.username} @ {self.task.title[:40]}"   #geeeneruje tytul obciety do 40 znakow


class Status:
    pass