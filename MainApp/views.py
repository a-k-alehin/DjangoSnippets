from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
                'form': form,
                'pagename': 'Добавление нового сниппета'}
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
       form = SnippetForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect("snippets_list")
    return render(request,'pages/add_snippet.html',{'form': form, 'pagename': 'Надо исправить'})


def snippet_delete(request, id):
    try:
        snippet = Snippet.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Сниппет с id={id} не найден')
    if request.method =="POST":
        snippet.delete()
        return redirect('snippets_list')
    context = {"snippet": snippet}
    return render(request, "pages/detail_snippet.html", context)