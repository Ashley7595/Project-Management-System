from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from PM.models import Task
from .models import Bugs
from django.db import models
from .forms import AddBugsForm
from django.contrib import messages
from django.utils import timezone


def is_tester(user):
    return hasattr(user, 'employee_roles') and user.employee_roles.all_roles == 'Tester'

@login_required(login_url='login')
@user_passes_test(is_tester, login_url='login')
def tester_view(request):

    query = request.GET.get('q', '')

    tasks = Task.objects.filter(task_assigned_to=request.user, task_assigned_to__is_superuser=False).order_by('-task_start_date')[:5]

    if query:
        tasks = tasks.filter(
            models.Q(task_title__icontains=query) |
            models.Q(task_description__icontains=query) |
            models.Q(task_status__icontains=query) |
            models.Q(task_priority__icontains=query)
        )

    return render(request, 'tester.html', {'tasks': tasks, 'query': query})




@login_required(login_url='login')
@user_passes_test(is_tester, login_url='login')
def done_tasks(request):
    tasks = Task.objects.filter(task_assigned_to=request.user)
    return render(request, 'done_tasks.html', {'tasks': tasks})




@login_required(login_url='login')
@user_passes_test(lambda u: u.employee_roles.all_roles == 'Tester', login_url='login')
def add_bugs(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = AddBugsForm(request.POST, request.FILES)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.related_task = task
            bug.save()
            messages.success(request, "Bug added successfully!")
            return redirect('done_tasks') 
    else:
        form = AddBugsForm()

    return render(request, 'add_bugs.html', {'form': form, 'task': task})


@login_required
def approve_bug_fix(request, bug_id):
    bug = get_object_or_404(Bugs, bug_id=bug_id)
    bug.is_approved = True
    bug.save()
    return redirect('verify_bugs')


@login_required
def reject_bug_fix(request, bug_id):
    bug = get_object_or_404(Bugs, bug_id=bug_id)
    bug.is_fixed = False  
    bug.save()
    return redirect('verify_bugs')


@login_required
@user_passes_test(is_tester, login_url='login')
def verify_bugs(request):
    bugs = Bugs.objects.filter(is_fixed=True, is_approved=False, is_rejected=False)
    return render(request, 'verify_bugs.html', {'bugs': bugs})