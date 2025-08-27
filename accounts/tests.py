from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="ComplexPass123!"
        )

    def test_signup_creates_user_and_logs_in(self) -> None:
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertRedirects(response, reverse("accounts:signup_success"))
        user_id = self.client.session.get("_auth_user_id")
        self.assertIsNotNone(user_id)
        self.assertEqual(int(user_id), User.objects.get(username="newuser").pk)

    def test_signup_with_existing_email_fails(self) -> None:
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "anotheruser",
                "email": self.user.email,
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("A user with that email already exists.", form.errors["email"])
        self.assertEqual(User.objects.filter(username="anotheruser").count(), 0)

    def test_login_authenticates_user(self) -> None:
        response = self.client.post(
            reverse("accounts:login"),
            {"username": self.user.username, "password": "ComplexPass123!"},
        )
        self.assertRedirects(response, reverse("tasks:task_list"))
        user_id = self.client.session.get("_auth_user_id")
        self.assertEqual(int(user_id), self.user.pk)

    def test_login_invalid_credentials(self) -> None:
        response = self.client.post(
            reverse("accounts:login"),
            {"username": self.user.username, "password": "WrongPassword"},
        )
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("__all__", form.errors)
        self.assertIn(
            "Please enter a correct username and password. Note that both fields may be case-sensitive.",
            form.errors["__all__"],
        )
        self.assertIn(
            "Please enter a correct username and password. Note that both fields may be case-sensitive.",
            form.errors["__all__"],
        )
        self.assertIsNone(self.client.session.get("_auth_user_id"))

    def test_logout(self) -> None:
        self.client.login(username=self.user.username, password="ComplexPass123!")
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("tasks:index"))
        self.assertIsNone(self.client.session.get("_auth_user_id"))

    def test_signup_success_requires_login(self) -> None:
        response = self.client.get(reverse("accounts:signup_success"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:signup_success')}",
        )
        self.client.login(username=self.user.username, password="ComplexPass123!")
        response = self.client.get(reverse("accounts:signup_success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup_success.html")
