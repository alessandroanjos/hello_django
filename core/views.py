from django.shortcuts import render, redirect, HttpResponse
from core.models import Evento


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


def lista_eventos(request):
    usuario = request.user
    eventos = Evento.objects.filter(usuario=usuario)
    data = {'eventos' : eventos}
    return render(request, 'agenda.html', data)
