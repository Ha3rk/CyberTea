# Generated by Django 5.0.7 on 2024-09-07 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cybertea_app', '0004_alter_category_category_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_image',
            new_name='image',
        ),
    ]