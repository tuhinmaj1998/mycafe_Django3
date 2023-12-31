# Generated by Django 3.0.8 on 2020-08-15 07:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offer', '0024_auto_20200812_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashBackCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
                ('cashBackLimit', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000)])),
                ('cashBackexpiryDate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('cashBackPercent', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('cashBackstatus', models.CharField(choices=[('Active', 'Active'), ('Paused', 'Paused')], default='Active', max_length=10)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
