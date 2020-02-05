from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import Http404, JsonResponse


# Create your views here.


def index(request):
    return redirect('/agenda')


def hello(request, nome, idade):
    return HttpResponse('Hello {} de anos {}'.format(nome, idade))


def soma(request, valor1, valor2):
    soma = int(valor1) + int(valor2)
    return HttpResponse('Soma  de {} + {} é: {}'.format(valor1, valor2, soma))


def identidade(request, nome, rg, cpf):
    pass


def eventos(request, titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse('Nome do Evento:  <b>{} </b> , Data : {} '.format(evento.titulo, evento.data_evento))


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    eventos = Evento.objects.filter(usuario=usuario)
    data = {'eventos': eventos}
    return render(request, 'agenda.html', data)


@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    eventos = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(eventos), safe=False)


@login_required(login_url='/login/')
def json_lista_evento_by_user(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    eventos = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(eventos), safe=False)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data, descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo, data_evento=data, descricao=descricao, usuario=usuario)

    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user

    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()

    if evento.usuario == usuario:
        evento.delete()
    else:
        raise Http404()

    #Evento.objects.filter(id=id_evento).delete()
    return redirect('/')


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
        return redirect('/')
