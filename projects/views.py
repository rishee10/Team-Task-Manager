from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project, ProjectMember
from .forms import ProjectForm, AddMemberForm
from tasks.models import Task
from accounts.models import User


def get_user_project(request, project_id, require_admin=False):
    """Helper: get project if user has access, else raise 403-like redirect."""
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if user.is_admin:
        return project
    membership = ProjectMember.objects.filter(project=project, user=user).first()
    if not membership:
        messages.error(request, 'You are not a member of this project.')
        return None
    if require_admin and membership.role != 'admin':
        messages.error(request, 'You need admin role in this project.')
        return None
    return project


@login_required
def project_list(request):
    user = request.user
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')

    if user.is_admin:
        projects = Project.objects.all().select_related('created_by')
    else:
        member_ids = ProjectMember.objects.filter(user=user).values_list('project_id', flat=True)
        projects = Project.objects.filter(id__in=member_ids).select_related('created_by')

    if q:
        projects = projects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if status:
        projects = projects.filter(status=status)

    return render(request, 'projects/list.html', {'projects': projects, 'q': q, 'status_filter': status})


@login_required
def project_create(request):
    if not request.user.is_admin:
        messages.error(request, 'Only admins can create projects.')
        return redirect('project_list')
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            ProjectMember.objects.create(project=project, user=request.user, role='admin')
            messages.success(request, f'Project "{project.name}" created!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/form.html', {'form': form, 'action': 'Create'})


@login_required
def project_detail(request, pk):
    project = get_user_project(request, pk)
    if not project:
        return redirect('project_list')

    tasks = project.tasks.select_related('assigned_to').order_by('-created_at')
    members = project.project_members.select_related('user').all()
    add_member_form = AddMemberForm()

    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    context = {
        'project': project,
        'tasks': tasks,
        'members': members,
        'add_member_form': add_member_form,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'is_project_admin': request.user.is_admin or members.filter(user=request.user, role='admin').exists(),
    }
    return render(request, 'projects/detail.html', context)


@login_required
def project_edit(request, pk):
    project = get_user_project(request, pk, require_admin=True)
    if not project:
        return redirect('project_list')
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/form.html', {'form': form, 'project': project, 'action': 'Edit'})


@login_required
def project_delete(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Only admins can delete projects.')
        return redirect('project_list')
    project = get_object_or_404(Project, id=pk)
    if request.method == 'POST':
        name = project.name
        project.delete()
        messages.success(request, f'Project "{name}" deleted.')
        return redirect('project_list')
    return render(request, 'projects/confirm_delete.html', {'project': project})


@login_required
def add_member(request, pk):
    project = get_user_project(request, pk, require_admin=True)
    if not project:
        return redirect('project_list')
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['email']
            role = form.cleaned_data['role']
            obj, created = ProjectMember.objects.get_or_create(project=project, user=user, defaults={'role': role})
            if created:
                messages.success(request, f'{user.full_name} added to project.')
            else:
                obj.role = role
                obj.save()
                messages.info(request, f'{user.full_name} role updated.')
    return redirect('project_detail', pk=pk)


@login_required
def remove_member(request, pk, user_id):
    project = get_user_project(request, pk, require_admin=True)
    if not project:
        return redirect('project_list')
    member = get_object_or_404(ProjectMember, project=project, user_id=user_id)
    if member.user == request.user:
        messages.error(request, 'You cannot remove yourself.')
    else:
        name = member.user.full_name
        member.delete()
        messages.success(request, f'{name} removed from project.')
    return redirect('project_detail', pk=pk)
