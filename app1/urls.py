from django.urls import path
from . import views
from .views import ProjectDeleteView 


urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('check-username/', views.check_username, name='check_username'),
    path('add_employees/',views.add_employees,name='add_employees'),
    path('view_employees/',views.view_employees,name='view_employees'),
    path('edit_employees/<int:employee_id>/', views.edit_employees, name='edit_employees'),
    path('employee/updateEmployee/<int:employee_id>/', views.update_employee, name='employee_update'),
    path('employees/toggle-active/<int:employee_id>/', views.toggle_employee_active, name='toggle_employee_active'),
    path('employees/reset-password/<int:employee_id>/', views.initiate_password_reset, name='initiate_password_reset'),
    path('reset-password/<uuid:token>/', views.reset_password_confirm, name='reset_password_confirm'),  
    path('add_projects/',views.add_projects,name='add_projects'),
    path('view_projects/',views.view_projects,name='view_projects'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),  
    path('delete_project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete_project'),
]