# Generated by Django 2.0.3 on 2018-04-10 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0022_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='notifications',
            name='new_copy',
            field=models.BooleanField(default=False),
        ),
    ]