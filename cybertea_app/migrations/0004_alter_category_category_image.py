# Generated by Django 5.0.7 on 2024-09-07 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cybertea_app', '0003_alter_category_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.ImageField(upload_to='imgs/'),
        ),
    ]