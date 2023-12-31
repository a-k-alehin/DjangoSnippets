from django.http import Http404, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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


def snippets_page_(request, my):
    pagename='Просмотр сниппетов'
    if my:
        snippets=Snippet.objects.filter(user=request.user)
        pagename='Просмотр моих сниппетов'
    elif request.user.is_authenticated:
        snippets=Snippet.objects.filter(Q(is_public=True) | Q(user=request.user))
    else:
        snippets=Snippet.objects.filter(is_public=True)
    lang=request.GET.get("lang")
    if lang:
        snippets=snippets.filter(language__shortname=lang)
    snippets=snippets.order_by("name")
    context = {"snippets": snippets, 'pagename': pagename, 'count': snippets.count(), "lang": lang}
    return render(request, 'pages/view_snippets.html', context)


def snippets_page(request):
    return snippets_page_(request, False)


@login_required
def snippets_my_page(request):
    return snippets_page_(request, True)


def snippet_detail_page(request, id):
    if request.method == "GET":
        try:
            snippet = Snippet.objects.get(id=id)
            #comments = Comment.objects.filter(snippet=snippet).order_by('creation_date')
            comments = snippet.comments.all()
        except ObjectDoesNotExist:
            return HttpResponseNotFound(f'Сниппет с id={id} не найден')
        context = {
            "snippet": snippet,
            "comments": comments,
            "comment_form": CommentForm,
            "can_edit": False}
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
            snippet.language=request.POST.get('language',snippet.language)
            snippet.code=request.POST.get('code',snippet.code)
            snippet.is_public=request.POST.get('is_public', False)  #(request.POST.get('is_public',"") == 'on')
            snippet.save()
            messages.add_message(request, messages.SUCCESS, 'Сохранено')
            #messages.success(request, 'Сохранено')
            return redirect('snippet_detail', id)
        messages.error(request, 'Надо исправить')
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


@login_required
def comment_add(request):
    if request.method == "POST":
        try:
            snippet_id = request.POST.get('snippet_id')
        except ObjectDoesNotExist:
            raise Http404
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippet_id)
            comment.save()
        #return redirect('snippet_detail', snippet_id)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    raise Http404