# Generated by Django 3.0.8 on 2020-08-10 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20200810_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriber',
            old_name='user_ends',
            new_name='userEnds',
        ),
    ]
