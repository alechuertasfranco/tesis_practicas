# Generated by Django 3.1.7 on 2021-09-08 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionTesis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juradotesis',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='plantesis',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]