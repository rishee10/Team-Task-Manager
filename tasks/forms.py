from django import forms
from .models import Task, TaskComment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'assigned_to', 'status', 'priority', 'due_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            self.fields['assigned_to'].queryset = project.members.all()
        self.fields['assigned_to'].empty_label = '— Unassigned —'


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('status',)
        widgets = {'status': forms.Select(attrs={'class': 'form-select form-select-sm'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a comment...'})}
