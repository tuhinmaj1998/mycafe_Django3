# Generated by Django 3.0.8 on 2020-08-15 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='cashBackTotal',
            field=models.IntegerField(default=0),
        ),
    ]
