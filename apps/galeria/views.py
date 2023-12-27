from django.shortcuts import render, get_object_or_404, redirect
from apps.galeria.forms import FotografiaForms
from apps.galeria.models import Fotografia
from django.contrib import messages
from apps.utils.utils import check_authentication

@check_authentication
def index(request):    
    fotografias = Fotografia.objects.order_by(
        "data_fotografia").filter(publicada=True)
    return render(request, 'galeria/index.html', {"cards": fotografias})

@check_authentication
def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

@check_authentication
def buscar(request):    
    fotografias = Fotografia.objects.order_by(
        "data_fotografia").filter(publicada=True)
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)
            
    return render(request, "galeria/index.html", {"cards": fotografias})

@check_authentication
def nova_imagem(request):    
    form = FotografiaForms()
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        form['foto']
        if form.is_valid():
            form.save()
            messages.success(request, 'Fotografia cadastrada com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao cadastrar fotografia')
            
    return render(request, 'galeria/nova_imagem.html', {"form": form})

@check_authentication
def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    form = FotografiaForms(instance=fotografia)
    
    if request.method == 'POST':
        form = FotografiaForms(
            request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fotografia editada com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao editar fotografia')
    return render(request, 'galeria/editar_imagem.html', {"form": form, 'foto_id': foto_id})

@check_authentication
def deletar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    fotografia.delete()
    messages.success(request, 'Fotografia deletada com sucesso!')
    return redirect('index')

@check_authentication
def filtro(request, categoria):    
    fotografias = Fotografia.objects.order_by('data_fotografia').filter(publicada=True, categoria=categoria)
    return render(request, 'galeria/index.html', {"cards": fotografias})