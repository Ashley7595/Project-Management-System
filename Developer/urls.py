from django.urls import path
from app1 import views as app1_views
from . import views

urlpatterns = [
    path('', app1_views.login_view, name='login'),
    path('login/', app1_views.login_view, name='login'),
    path('developer/', views.developer_view, name='developer'),
    path('tasks/', views.all_tasks, name='all_tasks'),
    path('update_task_status/', views.update_task_status, name='update_task_status'),
    path('view_all_bugs/', views.view_all_bugs, name='view_all_bugs'),
    path('mark-bug-fixed/<int:bug_id>/', views.mark_bug_fixed, name='mark_bug_fixed'),
]
