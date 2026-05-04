from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from projects.models import Project, ProjectMember
from tasks.models import Task


@login_required
def dashboard(request):
    user = request.user
    now = timezone.now()

    if user.is_admin:
        projects = Project.objects.all().select_related('created_by')
        all_tasks = Task.objects.all().select_related('project', 'assigned_to')
    else:
        member_project_ids = ProjectMember.objects.filter(user=user).values_list('project_id', flat=True)
        projects = Project.objects.filter(id__in=member_project_ids)
        all_tasks = Task.objects.filter(assigned_to=user)

    total_tasks = all_tasks.count()
    todo_tasks = all_tasks.filter(status='todo').count()
    in_progress_tasks = all_tasks.filter(status='in_progress').count()
    done_tasks = all_tasks.filter(status='done').count()
    overdue_tasks = all_tasks.filter(due_date__lt=now, status__in=['todo', 'in_progress'])

    recent_tasks = all_tasks.order_by('-created_at')[:5]
    recent_projects = projects.order_by('-created_at')[:4]

    context = {
        'projects': projects,
        'total_tasks': total_tasks,
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
        'overdue_tasks': overdue_tasks,
        'overdue_count': overdue_tasks.count(),
        'recent_tasks': recent_tasks,
        'recent_projects': recent_projects,
        'completion_rate': round((done_tasks / total_tasks * 100) if total_tasks else 0),
    }
    return render(request, 'dashboard.html', context)
