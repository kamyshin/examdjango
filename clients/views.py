from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Client
from .forms import ClientForm


def health_check(request):
    """Эндпоинт для проверки работоспособности"""
    return JsonResponse({'status': 'ok'})


def client_list(request):
    """Список всех клиентов"""
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'clients/client_list.html', {'clients': clients})


def client_create(request):
    """Создание нового клиента"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form, 'client': None})


def client_update(request, pk):
    """Редактирование клиента"""
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form, 'client': client})


def client_delete(request, pk):
    """Удаление клиента"""
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})
