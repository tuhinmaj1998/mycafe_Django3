# Generated by Django 3.0.8 on 2020-08-15 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20200815_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='useWallet',
            field=models.BooleanField(),
        ),
    ]
