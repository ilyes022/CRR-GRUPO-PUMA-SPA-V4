import django_filters
from .models import  Clients, Order, Visite_test, Bc, Location
from django_filters import DateFilter, CharFilter, ModelChoiceFilter


class PumalFilter(django_filters.FilterSet):


    client = ModelChoiceFilter(field_name='bc__client', label='client', queryset=Clients.objects.all())

    région = ModelChoiceFilter(field_name='bc__client__région', label='région', queryset=Location.objects.all())

    date_début = DateFilter(field_name='date', lookup_expr='gte', label='Date début')

    date_fin = DateFilter(field_name='date', lookup_expr='lte', label='Date Fin')

    class Meta:
        model = Order
        fields = [ 'designation']



class ClientsFilter(django_filters.FilterSet):
    nom= CharFilter(field_name='nom', lookup_expr='icontains', label='Nom')
    type= CharFilter(field_name='type', lookup_expr='icontains', label='Type')
    class Meta :
        model = Clients
        fields = ['région','wilaya']

class NumberFilter(django_filters.FilterSet):

    class Meta:
        model = Order

        fields = {
           'date': ['month'],
       }


class NumberFilter2(django_filters.FilterSet):
    class Meta:
        model = Visite_test

        fields = {
            'date': ['month'],
        }


class Number_Filter3(django_filters.FilterSet):
    class Meta:
        model = Bc

        fields = {
            'date': ['month'],
        }




class Visite_testFilter(django_filters.FilterSet):
    class Meta :
        model = Visite_test
        fields = ['région','wilaya','date','status']
