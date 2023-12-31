# Generated by Django 4.2.1 on 2023-08-17 10:31

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('verification_code', models.CharField(max_length=4, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('invite_code', models.CharField(blank=True, max_length=6, null=True)),
                ('activated_invite_code', models.CharField(blank=True, max_length=6, null=True)),
            ],
        ),
    ]
