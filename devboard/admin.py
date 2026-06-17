from asyncio import tasks

from django.contrib import admin
from django.utils.html import format_html

from .models import Project, Task, Comment

# z modelu wrzucamy do paznelu zarzadzania w panelu administrarttowa
# admin.site.register(Project)
# admin.site.register(Task)
admin.site.register(Comment)
# Register your models here.

#funkcja inline - mozliwosc edycji bez opuszczania projektu glownego
class TaskInline(admin.TabularInline):
    """Zadania wyświetlane wewnątrz projektu."""
    model = Task
    fields = ("title", "status", "priority", "assignee", "due_date")
    extra = 1       # ilosc pustych pol w folmularzu do dodania
    show_change_link = True     #przy kazdym zadnaiu jest link do folmularza /olowek/

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (    #co wyswietlamy
        'id',
        'name',
        'owner',
        'created_at',
        'task_count'
    )
    search_fields = ('name','description')  #moze wyszukiwac po name i description
    list_filter = ('name', 'created_at',)   #poczym filtrujemy

    inlines = [TaskInline]  # musi byc aby zadzialala klas TaskInline

    # #nasza wlasna kolumna zliczajaccca zadania:
    @admin.display(description="Zadań")
    def task_count(self, obj):
        return obj.tasks.count()



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title", "project", "priority",
        "assignee", "due_date", "status_badge"
    )
    list_filter = ("status", "priority", "project", "assignee")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"           #funkcja adminowa, daje nam kolumne datetime na poczatku
    readonly_fields = ("created_at", "updated_at")  #te pola mozna tylko ogladac, czyli np te ktore tworza sie same
    # fieldsety daja w formularzu mozliowsc ustawiania belek, w sensie jak beda podzielone
    fieldsets = (
        (None, {"fields": ("title", "description", "project")}),
        ("Przypisanie", {"fields": ("assignee", "due_date")}),
        ("Status", {"fields": ("status", "priority")}),
        ("Metadane", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),   #collapse to zwijanie/rozwijanie
    )

    # teraz robimy aby sie ststusy wyswietlały kolorami- to do, in progress, etc
    # do list_display wpisujemy ststus_badge i na poczatki importujemy html
    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {
            "TODO": "#6c757d",
            "IN_PROGRESS": "#0d6efd",
            "DONE": "#198754",
        }
        color = colors.get(obj.status, "#000")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px">{}</span>',
            color, obj.get_status_display(),
        )

admin.site.site_header = "DevBoard - Panel Administracyjny"
admin.site.site_title = "DevBoard Admin"
admin.site.index_title = "Zarządzanie projektem"