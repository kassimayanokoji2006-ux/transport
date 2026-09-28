from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Etudiant, Bus, Trans
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):
    etu_count = Etudiant.objects.count()
    bus_count = Bus.objects.count()
    trans_count = Trans.objects.count()
    return render(request, "layout/dashboard.html", {
        'etu_count': etu_count,
        'bus_count': bus_count,
        'trans_count': trans_count,
    })


# ----------------- Etudiant CRUD -----------------
def etudiant_list(request):
    q = (request.GET.get('q') or '').strip()
    items = Etudiant.objects.all()
    if q:
        items = items.filter(
            Q(matrE__icontains=q) |
            Q(nomE__icontains=q) |
            Q(prenomE__icontains=q) |
            Q(adresse__icontains=q) |
            Q(telParent__icontains=q)
        )
    items = items.order_by('nomE', 'prenomE')
    paginator = Paginator(items, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'etudiant/list.html', { 'items': page_obj.object_list, 'page_obj': page_obj, 'q': q })


def etudiant_create(request):
    if request.method == 'POST':
        Etudiant.objects.create(
            matrE=request.POST.get('matrE'),
            nomE=request.POST.get('nomE'),
            prenomE=request.POST.get('prenomE'),
            dateN=request.POST.get('dateN'),
            adresse=request.POST.get('adresse'),
            telParent=request.POST.get('telParent'),
        )
        return redirect('etudiant_list')
    return render(request, 'etudiant/form.html')


def etudiant_update(request, pk: str):
    item = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        item.nomE = request.POST.get('nomE')
        item.prenomE = request.POST.get('prenomE')
        item.dateN = request.POST.get('dateN')
        item.adresse = request.POST.get('adresse')
        item.telParent = request.POST.get('telParent')
        item.save()
        return redirect('etudiant_list')
    return render(request, 'etudiant/form.html', { 'item': item })


def etudiant_delete(request, pk: str):
    item = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('etudiant_list')
    return render(request, 'etudiant/confirm_delete.html', { 'item': item })


# ----------------- Bus CRUD -----------------
def bus_list(request):
    q = (request.GET.get('q') or '').strip()
    items = Bus.objects.all()
    if q:
        items = items.filter(
            Q(idBus__icontains=q) |
            Q(matrV__icontains=q) |
            Q(marque__icontains=q)
        )
    items = items.order_by('idBus')
    paginator = Paginator(items, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bus/list.html', { 'items': page_obj.object_list, 'page_obj': page_obj, 'q': q })


def bus_create(request):
    if request.method == 'POST':
        Bus.objects.create(
            idBus=request.POST.get('idBus'),
            matrV=request.POST.get('matrV'),
            marque=request.POST.get('marque'),
            capacite=request.POST.get('capacite') or 0,
        )
        return redirect('bus_list')
    return render(request, 'bus/form.html')


def bus_update(request, pk: str):
    item = get_object_or_404(Bus, pk=pk)
    if request.method == 'POST':
        item.matrV = request.POST.get('matrV')
        item.marque = request.POST.get('marque')
        item.capacite = request.POST.get('capacite') or 0
        item.save()
        return redirect('bus_list')
    return render(request, 'bus/form.html', { 'item': item })


def bus_delete(request, pk: str):
    item = get_object_or_404(Bus, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('bus_list')
    return render(request, 'bus/confirm_delete.html', { 'item': item })


# ----------------- Trans CRUD -----------------
def trans_list(request):
    q = (request.GET.get('q') or '').strip()
    items = Trans.objects.select_related('matrE', 'idBus').all()
    if q:
        items = items.filter(
            Q(refT__icontains=q) |
            Q(dateTrans__icontains=q) |
            Q(matrE__matrE__icontains=q) |
            Q(matrE__nomE__icontains=q) |
            Q(idBus__idBus__icontains=q) |
            Q(idBus__marque__icontains=q)
        )
    items = items.order_by('dateTrans')
    paginator = Paginator(items, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'transports/list.html', { 'items': page_obj.object_list, 'page_obj': page_obj, 'q': q })


def trans_create(request):
    if request.method == 'POST':
        Trans.objects.create(
            refT=request.POST.get('refT'),
            dateTrans=request.POST.get('dateTrans'),
            matrE=get_object_or_404(Etudiant, pk=request.POST.get('matrE')),
            idBus=get_object_or_404(Bus, pk=request.POST.get('idBus')),
        )
        return redirect('trans_list')
    return render(request, 'transports/form.html', {
        'etudiants': Etudiant.objects.all(),
        'buses': Bus.objects.all(),
    })


def trans_update(request, pk: str):
    item = get_object_or_404(Trans, pk=pk)
    if request.method == 'POST':
        item.dateTrans = request.POST.get('dateTrans')
        item.matrE = get_object_or_404(Etudiant, pk=request.POST.get('matrE'))
        item.idBus = get_object_or_404(Bus, pk=request.POST.get('idBus'))
        item.save()
        return redirect('trans_list')
    return render(request, 'transports/form.html', {
        'item': item,
        'etudiants': Etudiant.objects.all(),
        'buses': Bus.objects.all(),
    })


def trans_delete(request, pk: str):
    item = get_object_or_404(Trans, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('trans_list')
    return render(request, 'transports/confirm_delete.html', { 'item': item })
