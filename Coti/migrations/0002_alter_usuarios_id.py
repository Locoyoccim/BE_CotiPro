# Generated by Django 5.0.3 on 2024-10-22 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coti', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
