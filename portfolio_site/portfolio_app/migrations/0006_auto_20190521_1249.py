# Generated by Django 2.2 on 2019-05-21 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0005_auto_20190419_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockpick',
            name='date_added',
            field=models.DateField(verbose_name='Date Added'),
        ),
    ]
