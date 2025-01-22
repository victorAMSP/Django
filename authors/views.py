from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })

@require_POST
def register_create(request):
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Criptografa a senha
        user.save()
        messages.success(request, 'Your user is created, please log in.')
        del request.session['register_form_data']  # Remove os dados da sessão
        return redirect('authors:register')  # Redireciona somente após o sucesso

    # Renderiza novamente a página com os erros de validação
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })

def login_view(request):

    form = LoginForm()

    return render(request, 'authors/pages/login.html', {
        'form': form,
        'action_form': reverse('authors:login_create')
    })

def login_create(request):
    return render(request, '')