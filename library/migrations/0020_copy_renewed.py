# Generated by Django 2.0.3 on 2018-04-04 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0019_auto_20180404_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='copy',
            name='renewed',
            field=models.BooleanField(default=False),
        ),
    ]