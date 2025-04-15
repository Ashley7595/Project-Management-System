from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from PM.models import Task
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from Tester.models import Bugs


def is_developer(user):
    return hasattr(user, 'employee_roles') and user.employee_roles.all_roles == 'Web Developer'


@login_required(login_url='login')
@user_passes_test(is_developer, login_url='login')
def developer_view(request):
    query = request.GET.get('q', '')
    tasks = Task.objects.filter(task_assigned_to=request.user, task_assigned_to__is_superuser=False).order_by('-task_start_date')[:5]

    if query:
        tasks = tasks.filter(
            models.Q(task_title__icontains=query) |
            models.Q(task_description__icontains=query) |
            models.Q(task_status__icontains=query) |
            models.Q(task_priority__icontains=query)
        )

    return render(request, 'developer.html', {'tasks': tasks, 'query': query})



@login_required(login_url='login') 
@user_passes_test(is_developer, login_url='login')
def all_tasks(request):
    tasks = Task.objects.filter(task_assigned_to=request.user)
    return render(request, 'view_tasks.html', {'tasks': tasks})


@csrf_exempt
def update_task_status(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        task_id = data.get('task_id')
        new_status = data.get('status')

        try:
            task = Task.objects.get(id=task_id)
            task.task_status = new_status
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required(login_url='login')
def view_all_bugs(request):
    bugs = Bugs.objects.filter(is_fixed=False)
    return render(request, 'view_all_bugs.html', {'bugs': bugs})


@login_required
def mark_bug_fixed(request, bug_id):
    bug = get_object_or_404(Bugs, bug_id=bug_id)
    bug.is_fixed = True
    bug.save()
    return redirect('all_tasks') 
