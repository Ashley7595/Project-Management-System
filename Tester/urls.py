from django.urls import path
from app1 import views as app1_views
from . import views

urlpatterns = [
    path('', app1_views.login_view, name='login'),
    path('login/', app1_views.login_view, name='login'),
    path('tester/', views.tester_view, name='tester'),
    path('done_tasks/', views.done_tasks, name='done_tasks'),
    path('add-bugs/<int:task_id>/', views.add_bugs, name='add_bugs'),
    path('verify_bugs/', views.verify_bugs, name='verify_bugs'),
    path('approve-bug-fix/<int:bug_id>/', views.approve_bug_fix, name='approve_bug_fix'),
    path('reject-bug-fix/<int:bug_id>/', views.reject_bug_fix, name='reject_bug_fix'),
]