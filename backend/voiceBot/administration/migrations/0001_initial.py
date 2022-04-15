# Generated by Django 3.2.7 on 2022-03-31 12:09

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('image', models.ImageField(blank=True, upload_to='uploads/user/admin/')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Noeud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='administration.noeud')),
            ],
        ),
        migrations.CreateModel(
            name='Feuille',
            fields=[
                ('noeud_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administration.noeud')),
                ('description', models.TextField(blank=True, max_length=500)),
            ],
            bases=('administration.noeud',),
        ),
        migrations.CreateModel(
            name='Caracteristique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('1', 'Date'), ('2', 'Entier'), ('3', 'Reel'), ('4', 'ChaineDeCaractere')], max_length=2)),
                ('feuille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.feuille')),
            ],
        ),
    ]