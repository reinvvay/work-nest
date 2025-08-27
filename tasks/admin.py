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
    list_display = ["name", "deadline", "priority", "task_type", "is_completed", "assignee_list"]
    search_fields = ["name"]
    list_filter = ["deadline", "priority", "task_type", "is_completed", "assignees"]

    def assignee_list(self, obj: Task) -> str:
        return ", ".join([user.username for user in obj.assignees.all()])
    assignee_list.short_description = "Assignees"


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]


admin.site.unregister(Group)
