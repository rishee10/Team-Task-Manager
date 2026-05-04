from django.contrib import admin
from .models import Task, TaskComment


class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'priority', 'due_date', 'is_overdue', 'created_at')
    list_filter = ('status', 'priority', 'project')
    search_fields = ('title', 'description', 'assigned_to__email')
    raw_id_fields = ('assigned_to', 'created_by', 'project')
    inlines = [TaskCommentInline]
    list_editable = ('status', 'priority')


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('task__title', 'author__email', 'content')
