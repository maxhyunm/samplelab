# Generated by Django 3.2.4 on 2021-06-05 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_alter_data_detailfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='fixedfile',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='fixednumfile',
            field=models.JSONField(null=True),
        ),
    ]