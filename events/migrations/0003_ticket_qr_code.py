# Generated by Django 5.1.7 on 2025-04-20 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]
