from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
@api_view(['GET'])
def all_tasks(request):
    tasks = Task.objects.all()
    if not tasks.exists():
        return Response({"message": "There is no task", "error": "Not Found"}, status=404)
    serializer = TaskSerializer(tasks, many=True)
    return Response({"data": serializer.data})

@api_view(['GET'])
def get_task(request, id):
    if not str(id).isdigit():
        return Response({"message": "Invalid ID", "error": "Bad Request"}, status=400)
    try:
        task = Task.objects.get(pk=id)
        serializer = TaskSerializer(task)
        return Response({"data": serializer.data})
    except Task.DoesNotExist:
        return Response({"message": "Task not found", "error": "Not Found"}, status=404)

@api_view(['POST'])
def add_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Successfully added"})
    return Response({"message": "Invalid data", "error": serializer.errors}, status=400)

@api_view(['PATCH'])
def update_task(request):
    if 'id' not in request.data:
        return Response({"message": "Missing ID", "error": "Bad Request"}, status=400)
    try:
        task = Task.objects.get(pk=request.data['id'])
    except Task.DoesNotExist:
        return Response({"message": "Task not found", "error": "Not Found"}, status=404)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Successfully updated"})
    return Response({"message": "Invalid data", "error": serializer.errors}, status=400)

@api_view(['DELETE'])
def delete_task(request, id):
    if not str(id).isdigit():
        return Response({"message": "Invalid ID", "error": "Bad Request"}, status=400)
    try:
        task = Task.objects.get(pk=id)
        task.delete()
        return Response({"message": "Successfully deleted"})
    except Task.DoesNotExist:
        return Response({"message": "Task not found", "error": "Not Found"}, status=404)

def index(request):
    return render(request, 'index.html')

def redirect_to_task(request):
    path = request.GET.get('path', '')
    return redirect(f'/{path}')
