# Generated by Django 3.2.16 on 2024-03-31 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motobikes', '0002_delete_owners'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='motobike',
            options={'ordering': ('manufacturer', 'model'), 'verbose_name': 'мотоцикл', 'verbose_name_plural': 'Мотоциклы'},
        ),
    ]