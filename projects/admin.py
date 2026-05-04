from django.contrib import admin
from .models import Project, ProjectMember


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1
    autocomplete_fields = ['user']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'priority', 'created_by', 'task_count', 'member_count', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('name', 'description')
    inlines = [ProjectMemberInline]
    raw_id_fields = ('created_by',)


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'joined_at')
    list_filter = ('role',)
    search_fields = ('user__email', 'project__name')
