# Generated by Django 3.1.7 on 2021-08-30 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionSeguridad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]