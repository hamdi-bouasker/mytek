# Generated by Django 3.2.7 on 2021-09-26 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_terms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='terms',
        ),
    ]