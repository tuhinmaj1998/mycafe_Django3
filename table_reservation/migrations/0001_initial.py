# Generated by Django 3.0.8 on 2020-08-31 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('seat', models.PositiveSmallIntegerField(verbose_name='No. of Seats')),
                ('total', models.IntegerField(verbose_name='Total no. of tables')),
            ],
        ),
        migrations.CreateModel(
            name='time_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('hour_selection', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15)], unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='table_reserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_from', models.PositiveSmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)], unique=True)),
                ('on_date', models.DateField()),
                ('table', models.ForeignKey(default='Unknown Table Name', on_delete=django.db.models.deletion.SET_DEFAULT, to='table_reservation.table')),
                ('time_table', models.ForeignKey(default='Unknown Table Name', on_delete=django.db.models.deletion.SET_DEFAULT, to='table_reservation.time_table')),
            ],
        ),
    ]
