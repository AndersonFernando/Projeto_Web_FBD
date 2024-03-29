from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Filme, Serie, Anime, Agenda


class HomePageView(TemplateView):
    template_name = "listagem.html"

@login_required
def listagem(request):
    context = {}
    context['filmes'] = Filme.objects.all()
    context['series'] = Serie.objects.all()
    context['animes'] = Anime.objects.all()

    return render(request, 'core/listagem.html', context)

@login_required
def listagem_agenda(request):
    context = {}
    context['filmes'] = Agenda.objects.filter(user=request.user, serie__isnull=True, anime__isnull=True)
    context['series'] = Agenda.objects.filter(user=request.user, filme__isnull=True, anime__isnull=True)
    context['animes'] = Agenda.objects.filter(user=request.user, serie__isnull=True, filme__isnull=True)
    for agenda in Agenda.objects.filter(user=request.user, serie__isnull=True, anime__isnull=True):
        print(agenda)

    return render(request, 'core/listagem_agenda.html', context)


def inicio(request):
    return render(request, 'core/inicio.html')


def mudar_status_agenda(request, pk):
    novo_status = request.GET.get("novo_status", None)
    if pk != None and novo_status != None:
        Agenda.objects.filter(pk=pk).update(status=novo_status)
    return redirect("core:listagem_agenda")


def agendar(request, pk):
    status = request.GET.get("status", None)
    if Filme.objects.filter(pk=pk).exists():
        filme = Filme.objects.get(pk=pk)
        Agenda.objects.create(filme=filme, user=request.user, status=status)

    elif Serie.objects.filter(pk=pk).exists():
        serie = Serie.objects.get(pk=pk)
        Agenda.objects.create(serie=serie, user=request.user, status=status)

    elif Anime.objects.filter(pk=pk).exists():
        anime = Anime.objects.get(pk=pk)
        Agenda.objects.create(anime=anime, user=request.user, status=status)

    return redirect("listagem")



#tipo = filme ou anime
#numero_ep_ou_temporada = numero referente ao ep ou a temporada (que foi alterado)
#tipo_ep_ou_temporada = se é ep ou a temporada que está sendo alterado


def alterar_episodio(request):
    print("ENTROU AQUI")
    # if tipo == "anime":
    #     if tipo_ep_ou_temporada == 'ep':
    #         Anime.objects.filter(id=id).update(ep_atual = numero_ep_ou_temporada)
    #     elif tipo_ep_ou_temporada == 'temp':
    #         Anime.objects.filter(id=id).update(temp_atual=numero_ep_ou_temporada)

    return {"status": "Erro"}