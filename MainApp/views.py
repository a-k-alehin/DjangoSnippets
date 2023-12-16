from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    context = {"snippets": Snippet.objects.all(), 'pagename': 'Просмотр сниппетов'}
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail_page(request, id):
    try:
        snippet = Snippet.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Сниппет с id={id} не найден')
    context = {"snippet": snippet}
    return render(request, "pages/detail_snippet.html", context)  