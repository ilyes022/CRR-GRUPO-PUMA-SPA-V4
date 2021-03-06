# Generated by Django 3.0.8 on 2021-03-14 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import mapbox_location_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Syntaxe : NOM Prénom', max_length=255, null=True)),
                ('type', models.CharField(choices=[('Ceramiste', 'Ceramiste'), ('Materiaux de construction', 'Materiaux De Construction'), ('Quincaillerie', 'Quincaillerie')], max_length=255, null=True)),
                ('nom_gérant', models.CharField(blank=True, help_text='Syntaxe : NOM Prénom', max_length=255, null=True)),
                ('adresse', models.CharField(blank=True, help_text='Adresse de Registre de Commerce', max_length=255, null=True)),
                ('téléphone', models.CharField(blank=True, max_length=255, null=True)),
                ('potentiel', models.CharField(blank=True, choices=[('Fort', 'Fort'), ('Moyen', 'Moyen'), ('Faible', 'Faible')], max_length=255, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Localité',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('prix', models.FloatField(default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wilaya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('région', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Visite_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titre', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('localisation', mapbox_location_field.models.LocationField(blank=True, map_attrs={}, null=True)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('Planifiée', 'Planifiée'), ('Annulée', 'Annulée'), ('Changée', 'Changée'), ('Cloturée', 'Cloturée')], max_length=10)),
                ('localité', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Localité')),
                ('modifiée_par', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('région', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro.Location')),
                ('wilaya', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Wilaya')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantité_disponible', models.IntegerField()),
                ('commande', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=255)),
                ('disponibilité_concurrent', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('bc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Bc')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Clients')),
                ('créer_par', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('designation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Produit')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='localité',
            name='wilaya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro.Wilaya'),
        ),
        migrations.CreateModel(
            name='Distributeur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('région', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.Location')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='clients',
            name='distributeur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Distributeur'),
        ),
        migrations.AddField(
            model_name='clients',
            name='localité',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Localité'),
        ),
        migrations.AddField(
            model_name='clients',
            name='région',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.Location'),
        ),
        migrations.AddField(
            model_name='clients',
            name='wilaya',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Wilaya'),
        ),
        migrations.AddField(
            model_name='bc',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pro.Clients'),
        ),
    ]
