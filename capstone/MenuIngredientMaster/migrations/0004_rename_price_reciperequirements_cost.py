# Generated by Django 5.1.4 on 2025-06-10 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MenuIngredientMaster', '0003_rename_reciperequirement_reciperequirements'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reciperequirements',
            old_name='price',
            new_name='cost',
        ),
    ]
