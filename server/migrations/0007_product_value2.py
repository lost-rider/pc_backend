# Generated by Django 5.1 on 2024-09-02 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_product_value1_alter_product_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='value2',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]