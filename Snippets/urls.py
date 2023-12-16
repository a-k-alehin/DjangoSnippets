from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page),
    path('snippets/add', views.add_snippet_page, name='snippets_add'),
    path('snippets/list', views.snippets_page, name='snippets_list'),
    path('snippet/<int:id>', views.snippet_detail_page, name='snippet_detail'),
    #path('snippet/create', views.snippet_create, name='snippet_create'),
    path('snippet/delete', views.snippet_delete, name='snippet_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
