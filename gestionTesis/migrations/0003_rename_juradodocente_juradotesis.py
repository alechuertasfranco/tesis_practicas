# Generated by Django 3.2.4 on 2021-08-31 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionSeguridad', '0001_initial'),
        ('gestionTesis', '0002_juradodocente'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JuradoDocente',
            new_name='JuradoTesis',
        ),
    ]
