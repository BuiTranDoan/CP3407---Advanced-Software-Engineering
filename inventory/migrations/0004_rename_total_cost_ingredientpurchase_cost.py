# Generated by Django 5.1.9 on 2025-07-23 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_remove_ingredient_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientpurchase',
            old_name='total_cost',
            new_name='cost',
        ),
    ]
