# Generated by Django 3.2.6 on 2021-09-06 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionSeguridad', '0002_auto_20210905_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escuela',
            name='descripcion',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='facultad',
            name='descripcion',
            field=models.CharField(max_length=70),
        ),
    ]
