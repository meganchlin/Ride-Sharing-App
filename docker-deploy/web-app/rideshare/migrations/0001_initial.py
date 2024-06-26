# Generated by Django 4.2.9 on 2024-02-02 03:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vehicle_type', models.CharField(choices=[('small', 'SMALL'), ('medium', 'MEDIUM'), ('large', 'LARGE')], default='small', max_length=20)),
                ('capacity', models.IntegerField()),
                ('license_plate_number', models.CharField(max_length=20)),
                ('special_vehicle_info', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False)),
                ('destination_address', models.CharField(max_length=255)),
                ('required_arrival_time', models.DateTimeField()),
                ('vehicle_type', models.CharField(choices=[('small', 'SMALL'), ('medium', 'MEDIUM'), ('large', 'LARGE')], default='small', max_length=20)),
                ('num_passengers', models.IntegerField()),
                ('shared', models.BooleanField()),
                ('special_requests', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Open', 'OPEN'), ('Confirmed', 'CONFIRMED'), ('Complete', 'COMPLETE')], default='Open', max_length=20)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides_as_driver', to='rideshare.driver')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides_as_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sharer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('earliest_arrival_time', models.DateTimeField()),
                ('latest_arrival_time', models.DateTimeField()),
                ('num_passengers', models.IntegerField()),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rideshare.ride')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
