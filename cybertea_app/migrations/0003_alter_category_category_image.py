# Generated by Django 5.0.7 on 2024-09-07 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cybertea_app', '0002_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.ImageField(upload_to='cybertea_app/imgs/'),
        ),
    ]