# Generated by Django 3.0.8 on 2020-08-24 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_useraddress_color'),
        ('order', '0022_auto_20200821_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='userAddress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.UserAddress'),
        ),
    ]
