# Generated by Django 3.0.8 on 2020-07-24 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_orderproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='paytm_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MID', models.CharField(blank=True, max_length=20)),
                ('INDUSTRY_TYPE_ID', models.CharField(blank=True, max_length=20)),
                ('WEBSITE', models.CharField(blank=True, max_length=20)),
                ('CHANNEL_ID', models.CharField(blank=True, max_length=20)),
                ('CALLBACK_URL', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
