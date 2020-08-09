from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cupom
from .forms import CupomForm
from datetime import date


def index(request):
    filter = request.GET.get('filter')
    datainicio = request.GET.get('dataInicio')
    datafim = request.GET.get('dataFim')

    if filter:
        cupons = Cupom.objects.filter(situacao=filter).order_by('-created_at')
    elif datainicio and datafim:
        if datainicio >= datafim:
            messages.warning(request, 'A data de início deve ser menor que a data final!')
            return redirect('/cupom')
        cupons = Cupom.objects.filter(dataExpiracao__gte=datainicio).exclude(dataExpiracao__gte=datafim).order_by('-created_at')
    else:
        cupons = Cupom.objects.all().order_by('-created_at')
    return render(request, 'cupons/index.html', {'cupons': cupons})


def detalhe(request, codigo):
    cupom = get_object_or_404(Cupom, pk=codigo)
    return render(request, 'cupons/detalhe.html', {'cupom': cupom})


def adicionar(request):
    if request.method == 'POST':
        form = CupomForm(request.POST)
        if form.is_valid():
            cupom = form.save(commit=False)
            if cupom.codigo.isnumeric():
                messages.warning(request, 'O código precisa ter pelo menos uma letra!')
                return render(request, 'cupons/adicionar.html', {'form': form})
            cupom.situacao = 'Ativo'
            cupom.save()
            messages.success(request, 'Cupom adicionado com sucesso!')
            return redirect('/cupom')
        else:
            messages.warning(request, 'Um ou mais campos foram preenchidos incorretamente!')
            return render(request, 'cupons/adicionar.html', {'form': form})
    else:
        form = CupomForm()
        return render(request, 'cupons/adicionar.html', {'form': form})


def editar(request, codigo):
    cupom = get_object_or_404(Cupom, pk=codigo)
    if cupom.situacao == 'Expirado':
        messages.warning(request, 'Cupons expirados não podem ser editados!')
        return redirect('/cupom')
    form = CupomForm(instance=cupom)
    if request.method == 'POST':
        form = CupomForm(request.POST, instance=cupom)
        if form.is_valid():
            cupom = form.save(commit=False)
            if cupom.codigo.isnumeric():
                messages.warning(request, 'O código precisa ter pelo menos uma letra!')
                return render(request, 'cupons/editar.html', {'form': form, 'cupom': cupom})
            cupom.save()
            messages.success(request, 'Cupom atualizado com sucesso!')
            return redirect('/cupom')
        else:
            messages.warning(request, 'Um ou mais campos foram preenchidos incorretamente!')
            return render(request, 'cupons/editar.html', {'form': form, 'cupom': cupom})
    else:
        return render(request, 'cupons/editar.html', {'form': form, 'cupom': cupom})


def deletar(request, codigo):
    cupom = get_object_or_404(Cupom, pk=codigo)
    cupom.delete()
    messages.success(request, 'Cupom deletado com sucesso!')
    return redirect('/cupom')


def usar(request, codigo):
    cupom = get_object_or_404(Cupom, pk=codigo)
    if cupom.situacao == 'Ativo':
        cupom.situacao = 'Utilizado'
        cupom.dataUso = date.today()
    else:
        cupom.situacao = 'Ativo'
        cupom.dataUso = None
    cupom.save()
    return redirect('/cupom')


def expirar(request, codigo):
    cupom = get_object_or_404(Cupom, pk=codigo)
    cupom.situacao = 'Expirado'
    cupom.save()
    return redirect('/cupom')
