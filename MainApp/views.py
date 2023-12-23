from django.http import Http404, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def accounts_register(request):
    if request.method == "GET":
        context = {
            'form': UserRegistrationForm(),
            'pagename': 'Добавление нового пользователя'}
        return render(request, "pages/user_register.html", context)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect("home")
        context = {
            'form': form,
            'pagename': 'Добавление нового пользователя - ошибка'}
        return render(request, "pages/user_register.html", context)


def login(request):
    if request.method == 'GET':
        return render(request, 'pages/login.html', {})
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'pagename': 'PythonBin',
                'errors': ["wrong username or password"]}
            return render(request, 'pages/index.html', context)
            #pass
    to = request.META.get('HTTP_REFERER', '/')
    print(f'{to=}')
    if not '/login' in to:
        return redirect(to)
    else:
        return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')


def index_page(request):
    # print(f'vars(request) = ')
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def snippets_page(request):
    context = {"snippets": Snippet.objects.filter(is_public=True), 'pagename': 'Просмотр сниппетов'}
    return render(request, 'pages/view_snippets.html', context)


@login_required
def snippets_my_page(request):
    context = {"snippets": Snippet.objects.filter(user=request.user), 'pagename': 'Просмотр моих сниппетов'}
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail_page(request, id):
    if request.method == "GET":
        try:
            snippet = Snippet.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound(f'Сниппет с id={id} не найден')
        context = {"snippet": snippet, "can_edit": False}
        return render(request, "pages/detail_snippet.html", context)
    return HttpResponseNotAllowed(('GET',))


@login_required
def snippet_edit_page(request, id):
    try:
        snippet = Snippet.objects.get(id=id)
    except ObjectDoesNotExist:
        #raise Http404
        return HttpResponseNotFound(f'Сниппет с id={id} не найден')
    context = {"snippet": snippet, "can_edit": True}
    if request.method == "GET":
        return render(request, "pages/detail_snippet.html", context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet.name=request.POST.get('name',snippet.name)
            snippet.lang=request.POST.get('lang',snippet.lang)
            snippet.code=request.POST.get('code',snippet.code)
            snippet.is_public=request.POST.get('is_public', False)  #(request.POST.get('is_public',"") == 'on')
            snippet.save()
            return redirect("snippets_list_my")
        context['pagename'] = 'Надо исправить'
        return render(request, 'pages/detail_snippet.html', context)
    return HttpResponseNotAllowed(('GET','POST'))


@login_required
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
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets_list_my")
        return render(request,'pages/add_snippet.html',{'form': form, 'pagename': 'Надо исправить'})
    return HttpResponseNotAllowed(('GET','POST'))


@login_required
def snippet_delete(request, id):
    try:
        #id=request.POST.get('id','')
        snippet = Snippet.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Сниппет с id={id} не найден')
    if request.method != "POST":
        return render(request, 'pages/del_snippet.html', {'snippet': snippet})
    snippet.delete()
    return redirect('snippets_list_my')


