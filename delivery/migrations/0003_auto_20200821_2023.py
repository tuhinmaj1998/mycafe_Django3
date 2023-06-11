# Generated by Django 3.0.8 on 2020-08-21 14:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_auto_20200821_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliverymanagement',
            options={'ordering': ['-deliveryStatus']},
        ),
        migrations.AddField(
            model_name='deliverymanagement',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]