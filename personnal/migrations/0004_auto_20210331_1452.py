# Generated by Django 3.1.7 on 2021-03-31 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personnal', '0003_auto_20210325_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermeta',
            name='id',
        ),
        migrations.AlterField(
            model_name='usermeta',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='usermeta', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]