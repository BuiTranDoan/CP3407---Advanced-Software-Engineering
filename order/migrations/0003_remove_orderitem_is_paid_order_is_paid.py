# Generated by Django 5.1.9 on 2025-07-14 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_orderitem_created_at_orderitem_is_paid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
