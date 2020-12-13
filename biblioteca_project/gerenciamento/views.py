from django.shortcuts import render, redirect
from .models import Book
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
import datetime
from datetime import timedelta
from .models import *
from .forms import *

def home(request):
	return render(request, 'gerenciamento/home.html')


#Lista de todos os livros
def BookListView(request):
    book_list = Book.objects.all()
    return render(request, 'catalogo/book_list.html', locals())


@login_required
def BookCreate(request):
	if not request.user.is_superuser:
		messages.warning(request, f'É necessário logar como administrador para fazer isso.')
		return redirect('gerenciamento-home')
	form = BookForm()
	if request.method == 'POST':
		form = BookForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, f'Livro adicionado com sucesso!')
			return redirect('gerenciamento-home')
	return render(request, 'catalogo/form.html', locals())



def BookDetailView(request, pk):
	book = get_object_or_404(Book, id=pk)

	try:
		stu = User.objects.get(roll_no=request.user)
		
	except:
		pass
		return render(request, 'catalogo/book_detail.html', locals())



@login_required
def user_request_issue(request, pk):

	obj = Book.objects.get(id=pk)
	s = request.user
	if obj.quantity > 0:
		message = "Empréstimo de 14 dias iniciado. Você pode coletar o livro!"
		a = Borrower()
		a.usuario = s
		a.livro = obj
		a.data_emprestimo = datetime.datetime.now()
		a.data_retorno = datetime.datetime.now()+timedelta(days=14)
		obj.quantity = obj.quantity - 1
		obj.save()
		a.save()
	else:
		message = "Não existem cópias disoníveis atualmente"

	return render(request, 'catalogo/result.html', locals())


@login_required
def BookDelete(request, *args, **kwargs):
    if not request.user.is_superuser:
    	return redirect('gerenciamento-home')
    pk = kwargs.get('pk')
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    messages.success(request, f'Livro excluído com sucesso.')
    return redirect('gerenciamento-home')



@login_required
def BookUpdate(request, pk):
	if not request.user.is_superuser:
		return redirect('gerenciamento-home')
	obj = Book.objects.get(id=pk)
	form = BookForm(instance=obj)
	if request.method == 'POST':
		form = BookForm(data=request.POST, files=request.FILES, instance=obj)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			messages.success(request, f'Informações do livro atualizadas com sucesso!')
			return redirect('gerenciamento-home')
	return render(request, 'catalogo/form.html', locals())



@login_required
def return_book(request, pk):
    if not request.user.is_superuser:
        return redirect('gerenciamento-home')
    obj = Borrower.objects.get(id=pk)
    book_pk = obj.livro.id
    book = Book.objects.get(id=book_pk)
    book.quantity = book.quantity + 1
    book.save()
    obj.delete()
    return redirect('gerenciamento-home')




import re
from django.db.models import Q


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    
    query = None 
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None 
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'description','author'])

        book_list= Book.objects.filter(entry_query)

    return render(request,'catalogo/book_list.html',locals())

