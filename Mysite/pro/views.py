from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.safestring import mark_safe

from .forms import Loginform, RowProduitsForm, RowClientsForm, \
    OrderForm, Visite_testForm, BcForm
from .models import Clients, Produit, Wilaya, Order, Visite_test, Bc, Localité, Distributeur
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .filter import PumalFilter, ClientsFilter, NumberFilter, Visite_testFilter, NumberFilter2, \
    Number_Filter3
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum, F
from django.views.generic import TemplateView, CreateView
from django.db.models.functions import TruncMonth, ExtractMonth, Coalesce
import json

from django.views import generic
from datetime import datetime, timedelta, date
import calendar
from django.urls import reverse
from django.forms import inlineformset_factory, modelformset_factory


@login_required(login_url='Login')
def index2(request):
    AllProduits_list = Order.objects.all().order_by('-id')

    myFilter = PumalFilter(request.GET, queryset=Order.objects.all())
    AllProduits_list = myFilter.qs

    paginator = Paginator(AllProduits_list, 30)  # Show 5 clients per page

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'AllProduits': AllProduits_list,
               'myFilter': myFilter,
               'page_object': page_object}
    return render(request, "home3.html", context)


@login_required(login_url='Login')
def index3(request, page=1):
    AllClients_list = Clients.objects.all().order_by('-id')
    my_filter = ClientsFilter(request.GET, queryset=Clients.objects.all())
    AllClients_list = my_filter.qs

    paginator = Paginator(AllClients_list, 30)  # Show 2 clients per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'AllClients': AllClients_list,
               'myFilter': my_filter,
               'page_obj': page_obj,

               }
    return render(request, "home4.html", context)


def pagelogin(request):
    uservalue = ''
    passwordvalue = ''

    log_form = Loginform()
    if request.method == "POST":
        log_form = Loginform(request.POST or None)
        if log_form.is_valid():

            uservalue = log_form.cleaned_data.get("username")
            passwordvalue = log_form.cleaned_data.get("password")

            user = authenticate(username=uservalue, password=passwordvalue)
            if user is not None:
                login(request, user)
                context = {'form': log_form,
                           'error': 'The login has been successful'}

                return redirect('Liste_Des_Clients')

            else:
                context = {'form': log_form,
                           'error': 'The username and password combination is incorrect'}

                return render(request, 'login.html', context)

    else:
        context = {'form': log_form}
        return render(request, 'login.html', context)


def pagelogout(request):
    if request.method == "POST":
        logout(request)

        return redirect('Login')


@login_required(login_url='Login')
def clients(request):
    c_form = RowClientsForm()
    if request.method == "POST":
        c_form = RowClientsForm(request.POST or None)
    if c_form.is_valid():
        print(c_form.cleaned_data)
        Clients.objects.create(**c_form.cleaned_data)
        return redirect('Liste_Des_Clients')

    context = {
        'form': c_form
    }

    return render(request, "client.html", context)


@login_required(login_url='Login')
def count_client(request):
    count_all = Clients.objects.all().count()
    count_ouest = Clients.objects.all().filter(région="1").count()
    count_centre = Clients.objects.all().filter(région="2").count()
    count_est = Clients.objects.all().filter(région="3").count()

    produit_nom = Produit.objects.all()

    mynumberFilter = NumberFilter(request.GET, queryset=Order.objects.all())
    AllProduits_list = mynumberFilter.qs

    mynumberFilter = NumberFilter(request.GET, queryset=Bc.objects.all())
    Allbc_list = mynumberFilter.qs

    count_bc_ouest = Allbc_list.all().filter(client__région="1").count()
    count_bc_centre = Allbc_list.all().filter(client__région="2").count()
    count_bc_est = Allbc_list.all().filter(client__région="3").count()

    mynumberFilter2 = NumberFilter2(request.GET, queryset=Visite_test.objects.all())
    Allvisite_list = mynumberFilter2.qs

    count_visite_ouest = Allvisite_list.all().filter(région="1", status="Cloturée").count()
    count_visite_centre = Allvisite_list.all().filter(région="2",status="Cloturée").count()
    count_visite_est = Allvisite_list.all().filter(région="3",status="Cloturée").count()

    produit_count = AllProduits_list.values('designation__nom').annotate(
        ouest_commande=Coalesce(Sum('commande', filter=Q(bc__client__région="1")), 0),
        centre_commande=Coalesce(Sum('commande', filter=Q(bc__client__région="2")), 0),
        est_commande=Coalesce(Sum('commande', filter=Q(bc__client__région="3")), 0)).order_by("-designation__nom")

    produit_count2 = AllProduits_list.values('designation__nom').annotate(
        ouest_commande=Coalesce(Sum('commande', filter=Q(bc__client__région="1")), 0),
        centre_commande=Coalesce(Sum('commande', filter=Q(bc__client__région="2")), 0),
        est_commande=Coalesce(Sum('commande', filter=Q(bc__client__région="3")), 0),
        month=TruncMonth('date')).order_by("-designation__nom")

    context = {

        'count_all': count_all,
        'count_centre': count_centre,
        'count_ouest': count_ouest,
        'count_est': count_est,

        'Allbc_list': Allbc_list,

        'count_bc_ouest': count_bc_ouest,
        'count_bc_centre': count_bc_centre,
        'count_bc_est': count_bc_est,

        'count_visite_ouest': count_visite_ouest,
        'count_visite_centre': count_visite_centre,
        'count_visite_est': count_visite_est,

        'produit_nom': produit_nom,

        'mynumberFilter2': mynumberFilter2,
        'mynumberFilter': mynumberFilter,
        'AllProduits_list': AllProduits_list,
        'produit_count': produit_count,
        'produit_count2': produit_count2,

    }

    return render(request, 'number.html', context)


@login_required(login_url='Login')
def count_produits(request):
    orders = Order.objects.all()
    total_orders = orders.filter(client__région='2').count()

    count_bc_ouest = Bc.objects.all().filter(client__région="3").count()

    return render(request, 'count.html',
                  {'orders': orders, 'total_orders': total_orders, 'count_bc_ouest': count_bc_ouest, })


@login_required(login_url='Login')
def load_wilaya(request):
    région_id = request.GET.get('région_id')
    cities = Wilaya.objects.filter(région_id=région_id).order_by('name')
    return render(request, 'dropdown_list.html', {'cities': cities})
    # print(list(wilaya.values('id','name')))
    # return JsonResponse (list(wilaya.values('id','name')),safe=False)


def load_distributeur(request):
    région_id = request.GET.get('région_id')
    cities = Distributeur.objects.filter(région_id=région_id).order_by('nom')
    return render(request, 'dropdown_list_dist.html', {'cities': cities})
    # print(list(wilaya.values('id','name')))
    # return JsonResponse (list(wilaya.values('id','name')),safe=False)


@login_required(login_url='Login')
def load_localite(request):
    wilaya_id = request.GET.get('wilaya_id')
    commune = Localité.objects.filter(wilaya_id=wilaya_id).order_by('name')
    return render(request, 'dropdown_list_loc.html', {'commune': commune})


@login_required(login_url='Login')
def customer(request, pk_test):
    customer = Clients.objects.get(id=pk_test)

    bc_form = BcForm()

    if request.method == "POST":
        bc_form = BcForm(request.POST or None)

    if bc_form.is_valid():
        print(bc_form.cleaned_data)
        Bc.objects.create(**bc_form.cleaned_data)
        return redirect('customer', pk_test=customer.id)

    bc = customer.bc_set.all()
    bc_count = bc.count()

    paginator = Paginator(bc, 30)  # Show 2 bc per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'customer': customer, 'bc': bc, 'page_obj': page_obj, 'bc_form': bc_form, 'bc_count':bc_count}

    return render(request, 'customer2.html', context)


@login_required(login_url='Login')
def bc(request, pk_test, bc_id):
    customer = Clients.objects.get(id=pk_test)

    bc = Bc.objects.get(id=bc_id)

    orders = bc.order_set.all()

    paginator = Paginator(orders, 10)  # Show 10 orders per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'bc': bc, 'customer': customer, 'orders': orders, 'page_obj': page_obj}

    return render(request, 'customer.html', context)


@login_required(login_url='Login')
def createOrder(request, pk_test, bc_id):
    customer = Clients.objects.get(id=pk_test)

    bc = Bc.objects.get(id=bc_id)

    OrderFormset = inlineformset_factory(Bc, Order, fields=(
        'designation', 'quantité_disponible', 'commande', 'description', 'disponibilité_concurrent'), extra=5)

    formset = OrderFormset(queryset=Order.objects.none(), instance=bc)

    # form = OrderForm(initial={'client':customer})
    if request.method == 'POST':

        formset = OrderFormset(request.POST, instance=bc)
        if formset.is_valid():
            formset.save()

            return redirect('customer', pk_test=customer.id)
    context = {'formset': formset, 'customer': customer, 'bc': bc}
    return render(request, 'order_form.html', context)


@login_required(login_url='Login')
def creer_visite_test(request):
    mon_form = Visite_testForm()

    if request.method == "POST":
        mon_form = Visite_testForm(request.POST or None)

    if mon_form.is_valid():

        print(mon_form.cleaned_data)
        Visite_test.objects.create(**mon_form.cleaned_data)

        #mon_form.save()
        return redirect('visite_list')

    context = {
        'mon_form': mon_form}

    return render(request, "visite.html", context)


@login_required(login_url='Login')
def visite_list(request):
    AllVisite_list = Visite_test.objects.all().order_by('-id')

    visite_Filter = Visite_testFilter(request.GET, queryset=Visite_test.objects.all())
    AllVisite_list = visite_Filter.qs

    paginator = Paginator(AllVisite_list, 30)  # Show 10 visite per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'AllVisite': AllVisite_list,
               'myvisiteFilter': visite_Filter,
               'AllVisite_list': AllVisite_list,
               'page_obj': page_obj,

               }
    return render(request, "visite_list.html", context)


@login_required(login_url='Login')
def updateViste(request, pk):
    visite = Visite_test.objects.get(id=pk)

    mon_form = Visite_testForm(instance=visite)

    if request.method == "POST":
        mon_form = Visite_testForm(request.POST, instance=visite)
    if mon_form.is_valid():
        mon_form.modifiée_par = request.user

        mon_form.save()

        return redirect('visite_list')
    context = {
        'mon_form': mon_form,
        # 'visite':visite,
    }
    return render(request, "visite.html", context)


@login_required(login_url='Login')
def updateClient(request, pk):
    client = Clients.objects.get(id=pk)


    c_form = RowClientsForm(instance=client)


    if request.method == "POST":
        c_form = RowClientsForm(request.POST,instance=client)
    if c_form.is_valid():
        c_form.modifiée_par = request.user

        c_form.save()

        return redirect('Liste_Des_Clients')
    context = {
        'form': c_form,

    }
    return render(request, "client.html", context)