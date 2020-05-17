# Generated by Django 3.0.5 on 2020-05-12 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200506_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='apartmentNumber',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='street',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='streetNumber',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='zipcode',
            field=models.CharField(max_length=30, null=True),
        ),
    ]