from django.http import HttpResponse
from django.shortcuts import render

# from django.views.generic import ListView,DetailView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Task

from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = "login.html"
    # use this template
    fields = '__all__'
    # get all fields
    redirect_authenticated_user = True

    # redirect user when logged in

    def get_success_url(self):
        # login in user to task page
        return reverse_lazy('tasks')


class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm

    success_url = reverse_lazy('tasks')
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            # if user was successfully created
            login(self.request, user)
            # user login function
        return super(Register, self).form_valid(form)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        # each user to access his/own data
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input
            )
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = "task_detail.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_create.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task-update.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task-delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
