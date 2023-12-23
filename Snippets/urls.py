from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='snippets_add'),
    path('snippets/list', views.snippets_page, name='snippets_list'),
    path('snippets/list/my', views.snippets_my_page, name='snippets_list_my'),
    path('snippet/<int:id>', views.snippet_detail_page, name='snippet_detail'),
    path('snippet/edit/<int:id>', views.snippet_edit_page, name='snippet_edit'),
    path('snippet/delete/<int:id>', views.snippet_delete, name='snippet_delete'),
    path('accounts/register', views.accounts_register, name='accounts_register'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
