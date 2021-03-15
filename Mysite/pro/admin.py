from django.contrib import admin
from .models import   Clients, Location, Produit, Wilaya, Order, Localité, Visite_test, Bc


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')









class ClientsAdmin(admin.ModelAdmin):
    list_display = ('nom','type','wilaya','distributeur','téléphone')

admin.site.register(Clients, ClientsAdmin)




admin.site.register(Location)


admin.site.register(Produit)

admin.site.register(Wilaya)



admin.site.register(Bc)


admin.site.register(Localité)


class Visite_testAdmin(admin.ModelAdmin):
    list_display = ('Titre','région','wilaya','localité','description','localisation','date','status','modifiée_par')
admin.site.register(Visite_test, Visite_testAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('bc','designation', 'quantité_disponible', 'commande', 'disponibilité_concurrent')

admin.site.register(Order, OrderAdmin)



