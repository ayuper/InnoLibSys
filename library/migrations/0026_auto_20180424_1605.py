# Generated by Django 2.0.3 on 2018-04-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0025_auto_20180412_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='priv1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='priv2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='priv3',
            field=models.BooleanField(default=False),
        ),
    ]