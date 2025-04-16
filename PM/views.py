from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app1.models import Project, EmployeeUser, EmployeeRoles
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm, EditTaskForm
from django.http import JsonResponse, HttpResponse
from django.views.generic import DeleteView
from django.db import models
from Tester.models import Bugs 
from django.core.paginator import Paginator


def is_project_manager(user):
    return hasattr(user, 'employee_roles') and user.employee_roles.all_roles == 'Project Manager'


@login_required(login_url='login')
@user_passes_test(is_project_manager, login_url='login')
def project_manager(request):
    query = request.GET.get('q', '')

    tasks = Task.objects.filter(task_assigned_to__is_superuser=False).order_by('-task_start_date')[:5]

    if query:
        tasks = tasks.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(email__icontains=query) |
            models.Q(employee_roles__icontains=query)
        )
    
    tasks = tasks[:5]

    # Dashboard cards
    card_data = [
        {"title": "Total Projects", "value": Project.objects.count()},
        {"title": "Active Developers", "value": EmployeeUser.objects.filter(
            is_superuser=False, is_active=True, employee_roles__all_roles='Web Developer').count()},
        {"title": "Active Testers", "value": EmployeeUser.objects.filter(
            is_superuser=False, is_active=True, employee_roles__all_roles='Tester').count()},
    ]

    # Count total number of tasks
    total_tasks = Task.objects.count()

    # Count tasks with status 'Pending'
    progress_tasks = Task.objects.filter(task_status='In Progress').count()

    # Count tasks with status 'Pending'
    pending_tasks = Task.objects.filter(task_status='Pending').count()

    # Count tasks with status 'Completed'
    completed_tasks = Task.objects.filter(task_status='Completed').count()

     # Chart Data
    pie_chart_labels = ['Total','In Progress','Pending', 'Completed']
    pie_chart_values = [total_tasks, progress_tasks, pending_tasks, completed_tasks]

    context = {
    'Tasks': tasks,
    'query': query,
    'card_data': card_data,
    'pie_chart_labels': pie_chart_labels,
    'pie_chart_values': pie_chart_values,
    }

    return render(request, 'project_manager.html', context)



@login_required(login_url='login')
@user_passes_test(is_project_manager, login_url='login')
def all_projects(request):
    projects = Project.objects.filter(project_manager=request.user)
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'projects.html', {'page_obj': page_obj})
    
    

@login_required(login_url='login')
@user_passes_test(is_project_manager, login_url='login')
def toggle_project_active(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    project.is_active = not project.is_active
    project.save()

    print(f"Project {project.project_name} is now {'Active' if project.is_active else 'Inactive'}")
    return redirect('all_projects')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project.html' 
    success_url = reverse_lazy('project') 









@login_required(login_url='login')
@user_passes_test(is_project_manager, login_url='login')
def tasks(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)  
        if form.is_valid():
            task = form.save(commit=False)  
            task.task_assigned_by = request.user  
            task.save()
            form.save_m2m()
            role = form.cleaned_data['task_roles'] 
            return redirect('tasks')  
    else:
        form = TaskForm(user=request.user)  

    return render(request, 'assign_tasks.html', {'form': form})
    


def get_employees(request):
    role_id = request.GET.get('role_id')
    try:
        role = EmployeeRoles.objects.get(id=role_id)  # ✅ use role_id here
        employees = EmployeeUser.objects.filter(employee_roles=role)  # ✅ filter based on the role

        employee_data = [
            {
                "id": employee.id,
                "name": employee.get_full_name().strip() if employee.get_full_name().strip() else employee.username
            }
            for employee in employees
        ]
        return JsonResponse({"employees": employee_data})

    except EmployeeRoles.DoesNotExist:
        return JsonResponse({"employees": []})
    

def get_completed_tasks(request, project_id):
    completed_tasks = Task.objects.filter(task_project_id=project_id, task_status='Completed')
    data = [{"id": t.id, "title": t.task_title} for t in completed_tasks]
    return JsonResponse({"tasks": data})













@login_required(login_url='login')
@user_passes_test(is_project_manager, login_url='login')
def task_status(request):
    all_tasks = Task.objects.all() 
    tasks_data = []

    for task_details in all_tasks:

        roles = task_details.task_roles.all()  
        print(f"Task ID: {task_details.id}, Task Title: {task_details.task_title}") 

        tasks_data.append({
            'id': task_details.id,
            'task_project': task_details.task_project,
            'task_title': task_details.task_title,
            'task_description': task_details.task_description,
            'task_roles': ", ".join([role.all_roles for role in task_details.task_roles.all()]), 
            'task_assigned_to': task_details.task_assigned_to,
            'task_priority': task_details.task_priority,
            'task_status' : task_details.task_status,
            'task_due_date': task_details.task_due_date,
        })

        paginator = Paginator(all_tasks, 6) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


    context = {'page_obj': page_obj,'task_details': tasks_data}
    return render(request, 'task_status.html', context)





@login_required(login_url='login')
@user_passes_test(is_project_manager, login_url='login')
def view_details(request,id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'view_details.html', {'task' : task})
    


@login_required(login_url='login')
@user_passes_test(is_project_manager, login_url='login')
def edit_task(request, id):
    task = get_object_or_404(Task, pk=id)
    
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save() 
            return redirect('task_status')
    else:
        form = EditTaskForm(instance = task) 

    return render(request, 'edit_task.html', {'form': form, 'task': task}) 


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_status.html' 
    success_url = reverse_lazy('task_status') 


 
@login_required(login_url='login')
def view_all_bugs(request):
    bugs = Bugs.objects.filter(is_approved=False)
    return render(request, 'view_bugs.html', {'bugs': bugs})
