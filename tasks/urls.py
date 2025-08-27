from django.urls import path

from tasks.views import index, TaskListView, TaskCreateView, TaskToggleView, TaskDeleteView, TaskDetailView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("create/", TaskCreateView.as_view(), name="create_task"),
    path("toggle/<int:pk>/", TaskToggleView.as_view(), name="toggle"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="delete"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
]

app_name = "tasks"
