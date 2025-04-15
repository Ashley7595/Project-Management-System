from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from .models import EmployeeUser, Project, PasswordResetToken
from app1.forms import AddEmployeeForm, EditEmployeeForm , AddProjectForm, EditProjectForm
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.utils.http import urlencode


#LOGIN, LOGOUT

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('user_field')
        password = request.POST.get('pass_field')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff and user.is_superuser:  
                return redirect('admin_dashboard') 
            elif hasattr(user, 'employee_roles') and user.employee_roles.all_roles == "Project Manager":
                return redirect('project_manager')
            elif hasattr(user, 'employee_roles') and user.employee_roles.all_roles == "Web Developer":
                return redirect('developer')
            elif hasattr(user, 'employee_roles') and user.employee_roles.all_roles == "Tester":
                return redirect('tester')
            else:
                messages.error(request, "Unauthorized access. Contact the admin.")
                logout(request)  
                return redirect('login')  
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')  

    return render(request, 'login.html')  



def logout_view(request):
    logout(request)
    request.session.flush() 
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


#ADMIN

def is_admin(user):
    return user.is_staff 



@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    query = request.GET.get('q', '')

    # Employee search/filtering

    # Project search/filtering
    today = timezone.now().date()
    upcoming_deadline = today + timedelta(days=30)

    projects = Project.objects.filter(
        project_end_date__range=[today, upcoming_deadline]
    ).order_by('project_end_date')  # Sort by soonest deadline

    if query:
        projects = projects.filter(
        Q(project_name__icontains=query) |
        Q(project_priority__icontains=query) |
        Q(project_description__icontains=query)
    )

    projects = projects[:5]  # Limit to top 5 upcoming


    # Dashboard cards
    card_data = [
        {"title": "Active Employees", "value": EmployeeUser.objects.filter(is_active="True").count()},
        {"title": "Total Projects", "value": Project.objects.count()},
        {"title": "Active Projects", "value": Project.objects.filter(is_active="True").count()},
    ]

    # Total employees: All (active + inactive) excluding superusers
    total_employees = EmployeeUser.objects.filter(is_superuser=False).count()

    # Active roles: Only active users with specific roles
    project_managers = EmployeeUser.objects.filter(
        is_superuser=False, is_active=True, employee_roles__all_roles='Project Manager'
    ).count()

    developers = EmployeeUser.objects.filter(
        is_superuser=False, is_active=True, employee_roles__all_roles='Web Developer'
    ).count()

    testers = EmployeeUser.objects.filter(
        is_superuser=False, is_active=True, employee_roles__all_roles='Tester'
    ).count()

    # Chart Data
    pie_chart_labels = ['Total Employees', 'Project Managers', 'Developers', 'Testers']
    pie_chart_values = [total_employees, project_managers, developers, testers]


    context = {
    'Add_Projects': projects,
    'query': query,
    'card_data': card_data,
    'pie_chart_labels': pie_chart_labels,
    'pie_chart_values': pie_chart_values
}


    return render(request, 'admin_dashboard.html', context)




@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def add_employees(request):
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            messages.success(request, "Employee added successfully.")
            return redirect('view_employees')
        else:
            messages.error(request, 'There was an issue with your submission.')
    else:
        form = AddEmployeeForm()
    
    return render(request, 'add_employees.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def check_username(request):
    username = request.GET.get('username', None)
    exists = EmployeeUser.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})
    



@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def view_employees(request):
    query = request.GET.get('q', '')
    employees = EmployeeUser.objects.filter(is_superuser=False)

    if query:
        employees = employees.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(employee_roles__icontains=query)
        )

    paginator = Paginator(employees, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'view_employees.html', {
        'page_obj': page_obj,
        'query': query
    })



User = get_user_model()
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def initiate_password_reset(request, employee_id):
    employee = get_object_or_404(User, pk=employee_id)

    token = PasswordResetToken.objects.create(user=employee)

    reset_link = request.build_absolute_uri(reverse('reset_password_confirm', args=[str(token.token)]))
    print(f"Reset Link: {reset_link}")

    subject = "Password Reset Request"
    message = f"Please click the following link to reset your password: {reset_link}"
    if settings.EMAIL_HOST_USER:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [employee.email])
        messages.success(request, "Password reset link sent to user's email")
    else:
        messages.warning(request, "Email not configured, Password reset link created, but not emailed")
    return redirect('view_employees')



def reset_password_confirm(request, token):
    reset_token = get_object_or_404(PasswordResetToken, token=token)

    if not reset_token.is_valid():
        messages.error(request, "Password reset link has expired.")
        return redirect('login')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            reset_token.delete()
            messages.success(request, "Password reset successful.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'reset_password_form.html', {'token': token})



@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def toggle_employee_active(request, employee_id):
    employee = get_object_or_404(EmployeeUser, pk=employee_id)
    employee.is_active = not employee.is_active
    employee.save()

    # Get current pagination + search context
    page = request.GET.get('page', '')
    query = request.GET.get('q', '')

    # Build redirect URL with preserved params
    base_url = reverse('view_employees')
    query_string = urlencode({'page': page, 'q': query})
    return redirect(f'{base_url}?{query_string}')



@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def edit_employees(request, employee_id):
    employee = get_object_or_404(EmployeeUser, pk=employee_id)

    if request.method == 'POST':
        form = EditEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('view_employees')
    else:
        form = EditEmployeeForm(instance=employee)

    return render(request, 'edit_employees.html', {'form': form, 'employee': employee})



@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def update_employee(request, employee_id=None):
    if employee_id:
        updateEmployee = EmployeeUser.objects.filter(employee_id=employee_id).first()
    else:
        updateEmployee = None

    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, instance=updateEmployee)
        if form.is_valid():
            form.save()
        return redirect('dashboard')


class EntryDeleteView(DeleteView):
    model = EmployeeUser
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('view_employees')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def add_projects(request):
    if request.method == 'POST':
        project_form = AddProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False) 
            selected_employee_ids = request.POST.getlist('project_manager')
            if selected_employee_ids:
                employee = EmployeeUser.objects.get(pk=selected_employee_ids[0])  
                project.project_manager = employee  
            project.save()  

            return redirect('view_projects')
    else:
        projectform = AddProjectForm()

    return render(request, 'add_projects.html', {'form': projectform})



@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def view_projects(request):
    all_projects = Project.objects.all() 
    projects_data = []

    for project in all_projects:
        projects_data.append({
            'project_name': project.project_name,
            'project_priority': project.project_priority,
            'project_description': project.project_description,
            'project_start_date': project.project_start_date,
            'project_end_date': project.project_end_date,
            'project_id': project.project_id,
            'project_managers': [project.project_manager.get_full_name()] if project.project_manager else [], 
        })

    paginator = Paginator(projects_data, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'view_projects.html', context)



@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save() 
            return redirect('view_projects')
    else:
        form = EditProjectForm(instance=project) 

    return render(request, 'edit_project.html', {'form': form, 'project': project}) 



class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'view_projects.html' 
    success_url = reverse_lazy('view_projects') 