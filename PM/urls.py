from django.urls import path
from app1 import views as app1_views
from . import views
from .views import TaskDeleteView, ProjectDeleteView

urlpatterns = [
    path('', app1_views.login_view, name='login'),
    path('login/', app1_views.login_view, name='login'),
    path('project_manager/', views.project_manager, name='project_manager'),
    path('projects/', views.all_projects, name='all_projects'),
    path('toggle_project_active/<int:project_id>/', views.toggle_project_active, name='toggle_project_active'),
    path('delete_project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete_project'),
    path('assign_tasks/', views.tasks, name='tasks'), 
    path('task_status/', views.task_status, name='task_status'),
    path('view_details/<int:id>/', views.view_details, name='view_details'),
    path('edit_task/<int:id>/', views.edit_task, name='edit_task'), 
    path('delete_task/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),

    path('get-completed-tasks/<int:project_id>/', views.get_completed_tasks, name='get_completed_tasks'),
    path('get-employees/<int:role_id>/', views.get_employees, name='get_employees'),
    
    path('view_bugs/', views.view_all_bugs, name='view_bugs'),
]
