# Generated by Django 2.2.5 on 2019-09-26 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terreno', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lote',
            old_name='Medida',
            new_name='medidas',
        ),
        migrations.RenameField(
            model_name='lote',
            old_name='ubicacion',
            new_name='ubicaciones',
        ),
    ]
