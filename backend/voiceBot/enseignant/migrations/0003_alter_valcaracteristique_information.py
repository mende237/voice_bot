# Generated by Django 3.2.9 on 2022-04-14 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enseignant', '0002_valcaracteristique_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valcaracteristique',
            name='information',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enseignant.information'),
        ),
    ]