# Generated by Django 3.2.9 on 2021-12-20 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chronos', '0009_automaticplan'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subject',
            name='unique_name_per_site',
        ),
    ]
