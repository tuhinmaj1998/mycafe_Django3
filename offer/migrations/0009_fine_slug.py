# Generated by Django 3.0.8 on 2020-08-09 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0008_fine'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
