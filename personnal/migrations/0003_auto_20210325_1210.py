# Generated by Django 3.1.7 on 2021-03-25 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('strategy', '0010_historicalvalue'),
        ('personnal', '0002_usermeta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermeta',
            name='preferred_hypothesis',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='userpreferredhypothesis', to='strategy.recordhypothesis'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermeta',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='usermeta', to='auth.user'),
            preserve_default=False,
        ),
    ]
