# Generated by Django 3.0.8 on 2020-08-07 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_comment_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply',
        ),
    ]
