from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Task, TaskComment
from .forms import TaskForm, CommentForm
from projects.models import Project, ProjectMember


def can_access_task(user, task):
    if user.is_admin:
        return True
    return ProjectMember.objects.filter(project=task.project, user=user).exists()


def can_edit_task(user, task):
    if user.is_admin:
        return True
    membership = ProjectMember.objects.filter(project=task.project, user=user).first()
    if not membership:
        return False
    return membership.role in ('admin', 'member') or task.assigned_to == user or task.created_by == user


@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if not request.user.is_admin:
        membership = ProjectMember.objects.filter(project=project, user=request.user).first()
        if not membership or membership.role == 'viewer':
            messages.error(request, 'Viewers cannot create tasks.')
            return redirect('project_detail', pk=project_id)

    if request.method == 'POST':
        form = TaskForm(project, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created!')
            return redirect('project_detail', pk=project_id)
    else:
        form = TaskForm(project)
    return render(request, 'tasks/form.html', {'form': form, 'project': project, 'action': 'Create'})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)
    if not can_access_task(request.user, task):
        messages.error(request, 'Access denied.')
        return redirect('project_list')

    comments = task.comments.select_related('author').all()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.task = task
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comment added.')
                return redirect('task_detail', pk=pk)

    context = {
        'task': task,
        'comments': comments,
        'comment_form': comment_form,
        'can_edit': can_edit_task(request.user, task),
    }
    return render(request, 'tasks/detail.html', context)


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, id=pk)
    if not can_edit_task(request.user, task):
        messages.error(request, 'You cannot edit this task.')
        return redirect('task_detail', pk=pk)

    if request.method == 'POST':
        form = TaskForm(task.project, request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('task_detail', pk=pk)
    else:
        form = TaskForm(task.project, instance=task)
    return render(request, 'tasks/form.html', {'form': form, 'task': task, 'project': task.project, 'action': 'Edit'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk)
    if not can_edit_task(request.user, task):
        messages.error(request, 'You cannot delete this task.')
        return redirect('task_detail', pk=pk)
    project_id = task.project_id
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted.')
        return redirect('project_detail', pk=project_id)
    return render(request, 'tasks/confirm_delete.html', {'task': task})


@login_required
def task_update_status(request, pk):
    """AJAX endpoint for quick status update."""
    task = get_object_or_404(Task, id=pk)
    if not can_edit_task(request.user, task):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Task.STATUS_CHOICES):
            task.status = status
            task.save()
            return JsonResponse({'success': True, 'status': task.get_status_display()})
    return JsonResponse({'error': 'Invalid'}, status=400)


@login_required
def my_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user).select_related('project').order_by('due_date')
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    return render(request, 'tasks/my_tasks.html', {'tasks': tasks, 'status_filter': status_filter})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(TaskComment, id=pk)
    if comment.author != request.user and not request.user.is_admin:
        messages.error(request, 'Cannot delete this comment.')
        return redirect('task_detail', pk=comment.task_id)
    task_id = comment.task_id
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('task_detail', pk=task_id)
