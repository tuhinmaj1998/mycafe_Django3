# Generated by Django 3.0.8 on 2020-08-07 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0019_remove_comment_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.CharField(blank=True, max_length=250)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('status', models.CharField(choices=[('New', 'New'), ('True', 'True'), ('False', 'False')], default='True', max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('parentComment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]