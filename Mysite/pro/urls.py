from django.urls import path, re_path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.index2, name='Home'),

    path('login', views.pagelogin, name='Login'),
    path('logout', views.pagelogout, name='Logout'),

    path('Disponibilté', views.index2, name="Disponibilté"),
    path('Nouveau_Client', views.clients, name='Nouveau_Client'),
    path('Liste_Des_Clients', views.index3, name='Liste_Des_Clients'),

    path('number', views.count_client, name='number'),

    path('count', views.count_produits, name= 'count'),
    path('load-wilaya', views.load_wilaya, name='load-wilaya'),
    path('load-localite', views.load_localite, name='load-localite'),
    path('load-distributeur', views.load_distributeur, name='load-distributeur'),

    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('customer/<str:pk_test>/bc/<str:bc_id>/', views.bc, name="bc"),

    path('create_order/customer/<str:pk_test>/bc/<str:bc_id>/', views.createOrder, name="create_order"),
    path('creer_visite_test', views.creer_visite_test, name='creer_visite_test'),
    path('visite_list', views.visite_list, name="visite_list"),

    path('update_visite/<str:pk>/', views.updateViste, name='update_visite'),

    path('update_client/<str:pk>/', views.updateClient, name='update_client'),








]