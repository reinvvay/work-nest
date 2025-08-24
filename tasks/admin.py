from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from tasks.models import Task, TaskType, Position

User = get_user_model()


@admin.register(User)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "position__name"]
    search_fields = ["username", "first_name", "last_name", "position__name"]
    list_filter = ["position"]
    exclude = ["groups"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "deadline", "priority", "task_type", "is_completed"]
    search_fields = ["name"]
    list_filter = ["deadline", "priority", "task_type", "is_completed", "assignees"]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["name"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["name"]


admin.site.unregister(Group)
