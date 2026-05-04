from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.my_tasks, name='my_tasks'),
    path('create/<int:project_id>/', views.task_create, name='task_create'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/status/', views.task_update_status, name='task_status'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]
