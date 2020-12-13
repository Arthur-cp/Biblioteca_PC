# Project urls
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from usuarios import views as usuarios_views
from gerenciamento import views as gerenciamento_views


urlpatterns = [
	path('', gerenciamento_views.BookListView),
	path('home/', include('gerenciamento.urls')),
    path('admin/', admin.site.urls),
    path('register/', usuarios_views.register, name='registro'),
    path('profile/', usuarios_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
    path('gerenciamento/', include('gerenciamento.urls')),
    path('bookslist/', gerenciamento_views.BookListView, name='lista_livros' ),
    path('book/create/', gerenciamento_views.BookCreate, name='criar_livro'),
    path('book/<int:pk>/delete/', gerenciamento_views.BookDelete, name='excluir_livro'),
    path('book/<int:pk>/borrow/', gerenciamento_views.user_request_issue, name='emprestimo'),
    path('book/<int:pk>', gerenciamento_views.BookDetailView, name='detalhes_livro'),
    path('book/<int:pk>/update', gerenciamento_views.BookUpdate, name='atualizar_livro'),


url(r'^search_b/', gerenciamento_views.search_book, name="search_b")
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
