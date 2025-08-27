from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from tasks.models import Task, TaskType, Worker, Position


class TasksTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.user = Worker.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="ComplexPass123!",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Feature")
        self.task = Task.objects.create(
            name="Test Task",
            description="Task description",
            deadline=timezone.now(),
            priority="Medium Priority",
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)

    def test_task_list_view(self) -> None:
        self.client.login(username="testuser", password="ComplexPass123!")
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertTemplateUsed(response, "tasks/task_list.html")

    def test_task_detail_view(self) -> None:
        self.client.login(username="testuser", password="ComplexPass123!")
        response = self.client.get(
            reverse("tasks:task_detail", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.description)
        self.assertContains(response, self.user.username)
        self.assertTemplateUsed(response, "tasks/task_detail.html")

    def test_task_create_view(self) -> None:
        self.client.login(username="testuser", password="ComplexPass123!")
        response = self.client.post(
            reverse("tasks:create_task"),
            {
                "name": "New Task",
                "description": "New description",
                "deadline": timezone.now().strftime("%Y-%m-%dT%H:%M"),
                "priority": "High Priority",
                "task_type": self.task_type.id,
                "assignees": [self.user.id],
            },
        )
        self.assertEqual(Task.objects.filter(name="New Task").count(), 1)
        self.assertRedirects(response, reverse("tasks:task_list"))

    def test_task_toggle_view(self) -> None:
        self.client.login(username="testuser", password="ComplexPass123!")
        old_status = self.task.is_completed
        response = self.client.post(
            reverse("tasks:toggle", args=[self.task.pk])
        )
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.is_completed, old_status)
        self.assertRedirects(response, reverse("tasks:task_list"))

    def test_task_delete_view(self) -> None:
        self.client.login(username="testuser", password="ComplexPass123!")
        response = self.client.post(
            reverse("tasks:delete", args=[self.task.pk])
        )
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertRedirects(response, reverse("tasks:task_list"))
