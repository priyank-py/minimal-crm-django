# Generated by Django 2.2.8 on 2020-01-11 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Client Email'),
        ),
    ]
