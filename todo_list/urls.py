from django.urls import path
from todo_list import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, Register
from django.contrib.auth.views import LogoutView

# app_name = 'todo_list'

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('register', Register.as_view(), name='register'),

    path('', TaskList.as_view(template_name='task_list.html'), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
]
