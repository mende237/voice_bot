# Generated by Django 3.2.7 on 2022-04-09 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_alter_noeud_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noeud',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.noeud'),
        ),
    ]