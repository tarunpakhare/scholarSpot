# Generated by Django 4.2 on 2023-04-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='location',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='college',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
