# Generated by Django 3.1.6 on 2021-02-10 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0008_auto_20210205_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordhypothesis',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]