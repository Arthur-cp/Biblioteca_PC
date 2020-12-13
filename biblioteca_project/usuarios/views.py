# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Sua conta foi criada! Agora você pode fazer login.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'usuarios/register.html', {'form': form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Sua conta foi atualizada!')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'usuarios/profile.html', context)

















'''
logger = logging.getLogger(_name_)

class Auntenticacao(View):
    #Class Based View para autenticação de usuários

    def get(self, request):
        contexto = {
            'usuario': '',
            'mensagem': 'Teste 012345',
            'senha': ''
        }
        return render(request, 'autenticacao.html', contexto)

    def post(self, request):
        #Armazena valores recebidos
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)

        #Apresenta no log(terminal) os valores recebidos
        logger.info('Usuário: {}'.format(usuario))
        logger.info('senha: {}'.format(senha))

        #Verifica as credenciais de autenticação fornecidas
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            #Verifica se o usuario ainda está ativo no sistema
            if user.is_active:
                login(request, user)
                return HttpResponse ('Usuário autenticado com sucesso')

            return render(request, 'autenticacao.html',{'mensagem': 'Usuário inativo'})

        return render(request, 'autenticacao.html', {'mensagem': 'Usuário ou senha incorretos'})'''

