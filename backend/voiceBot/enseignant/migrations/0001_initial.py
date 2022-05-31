# Generated by Django 3.1.5 on 2022-05-06 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0005_merge_20220429_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delai', models.DateField(verbose_name='date limite de validite')),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enseignant.enseignant')),
            ],
        ),
        migrations.CreateModel(
            name='ValCaracteristique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=30)),
                ('caracteristique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.caracteristique')),
                ('information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enseignant.information')),
            ],
        ),
    ]
