# Generated by Django 3.2.12 on 2022-03-09 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20220309_1139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='time',
            new_name='m_time',
        ),
    ]
