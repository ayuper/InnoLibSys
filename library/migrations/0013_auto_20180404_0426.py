# Generated by Django 2.0.3 on 2018-04-04 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_document_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='patron_type',
            field=models.IntegerField(choices=[(0, 'Instructor (Faculty)'), (1, 'Student'), (2, 'Visiting Professor'), (3, 'TA (Faculty)'), (4, 'Professor (Faculty)')], default=0),
        ),
    ]
