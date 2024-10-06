from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
from django.http import JsonResponse

def home(request):
    todos = Todo.objects.all()
    form = TodoForm()
    return render(request, 'myprj/home.html', {'form': form, 'todos': todos})

def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            return JsonResponse({'id': todo.id, 'title': todo.title, 'description': todo.description,
                                 'deadline': todo.deadline.strftime('%Y-%m-%d %H:%M:%S'),
                                 'completed': todo.completed})
    return JsonResponse({'error': 'Invalid form submission'}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Todo
import json

@csrf_exempt  # Only if you're not using CSRF tokens for this view
def delete_todo(request, todo_id):
    if request.method == 'POST':
        try:
            todo = get_object_or_404(Todo, id=todo_id)
            todo.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
