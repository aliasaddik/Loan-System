# Generated by Django 4.2.2 on 2023-07-03 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='installments',
            old_name='Loan',
            new_name='loan',
        ),
    ]
