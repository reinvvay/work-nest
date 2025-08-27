from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.http import HttpRequest, HttpResponse

from accounts.forms import WorkerAuthenticationForm, WorkerCreationForm, WorkerUpdateForm
from tasks.models import Worker


class LoginView(generic.FormView):
    template_name = "accounts/login.html"
    form_class = WorkerAuthenticationForm
    success_url = reverse_lazy("tasks:task_list")

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form: WorkerAuthenticationForm) -> HttpResponse:
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class SignupView(generic.FormView):
    template_name = "accounts/signup.html"
    form_class = WorkerCreationForm
    success_url = reverse_lazy("accounts:signup_success")

    def form_valid(self, form: WorkerCreationForm) -> HttpResponse:
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class SignupSuccessView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/signup_success.html"


class LogoutView(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        logout(request)
        return redirect("tasks:index")


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("tasks:task_list")

    def get_object(self):
        return self.request.user
