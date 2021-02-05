# Generated by Django 3.1.6 on 2021-02-05 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('strategy', '0005_auto_20210128_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordhypothesis',
            name='broker_fees',
        ),
        migrations.RemoveField(
            model_name='recordhypothesis',
            name='gamma',
        ),
        migrations.RemoveField(
            model_name='recordhypothesis',
            name='short_selling',
        ),
        migrations.AddField(
            model_name='recordhypothesis',
            name='user_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
