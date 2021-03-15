from django.db import models
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django.urls import reverse
from mapbox_location_field.models import LocationField
from django.contrib.auth.models import User




class Clients (models.Model):
    région = models.ForeignKey('Location', on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=255, null=True,help_text='Syntaxe : Prénom Nom')
    type = (

        ('Ceramiste', 'Ceramiste'),
        ('Materiaux de Construction', 'Materiaux De Construction'),
        ('Quincaillerie', 'Quincaillerie'),
    )

    type = models.CharField(choices=type,max_length=255, null=True)
    wilaya = models.ForeignKey('Wilaya', on_delete=models.SET_NULL, null=True)
    localité = models.ForeignKey('Localité', on_delete=models.SET_NULL, null=True,blank=True)
    nom_gérant = models.CharField(max_length=255,null=True,blank=True,help_text='Syntaxe : Prénom Nom')
    adresse = models.CharField(max_length=255,null=True,blank=True, help_text='Adresse de Registre de Commerce')
    téléphone = models.CharField(max_length=255,null=True,blank=True)
    potentiel = (

        ('Fort', 'Fort'),
        ('Moyen', 'Moyen'),
        ('Faible', 'Faible'),
    )

    potentiel = models.CharField(choices=potentiel,max_length=255,null=True,blank=True)
    distributeur = models.ForeignKey('Distributeur', on_delete=models.SET_NULL, null=True,blank=True)



    def __str__(self):
        return self.nom
    class Meta:
        ordering = ["id"]


class Distributeur (models.Model):
    nom = models.CharField(max_length=255)
    région = models.ForeignKey('Location', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nom
    class Meta:
        ordering = ["-id"]

class Location (models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom



class Produit (models.Model):
    nom = models.CharField(max_length=255)
    prix =models.FloatField(null=True, default=True)

    def __str__(self):
        return self.nom

    ordering = ["-id"]

class Wilaya (models.Model) :
    région = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Localité (models.Model) :
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name



class Bc (models.Model):
    client = models.ForeignKey('Clients', null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "#BC_"+ str(self.id)
    @property
    def get_bc_total(self):
        bcitems = self.order_set.all()
        total = sum([item.get_total for item in bcitems])
        return total

    class Meta:
        ordering = ["-id"]


class Order (models.Model):
    bc = models.ForeignKey('Bc', null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey('Clients', null=True, on_delete=models.SET_NULL)
    designation = models.ForeignKey('Produit',null=True, on_delete=models.SET_NULL)
    quantité_disponible = models.IntegerField()
    commande = models.IntegerField()
    description = models.CharField(max_length=255, blank=True)
    disponibilité_concurrent = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True, null=True)
    créer_par = CurrentUserField()

    @property
    def get_total(self):
        total = self.designation.prix * self.commande
        return total



    class Meta:
        ordering = ["-date"]





class Visite_test (models.Model):

    Titre = models.CharField(max_length=255)
    région = models.ForeignKey(Location, on_delete=models.CASCADE)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True)
    localité = models.ForeignKey(Localité, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    localisation = LocationField(null=True, blank=True)
    date = models.DateField(null=True)
    modifiée_par = models.ForeignKey(User,on_delete=models.CASCADE, default=True)

    status_choice = (
        ('Planifiée', 'Planifiée'),
        ('Annulée', 'Annulée'),

        ('Changée', 'Changée'),
        ('Cloturée', 'Cloturée'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    class Meta:
        ordering = ["-date"]



