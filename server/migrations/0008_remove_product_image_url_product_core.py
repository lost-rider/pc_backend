# Generated by Django 5.1 on 2024-09-13 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_product_value2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
        migrations.AddField(
            model_name='product',
            name='core',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
