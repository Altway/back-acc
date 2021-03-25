# Generated by Django 3.1.7 on 2021-03-12 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('strategy', '0009_auto_20210210_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('capital', models.FloatField(blank=True, default=None, null=True)),
                ('risk_free_rate', models.FloatField(blank=True, default=None, null=True)),
                ('broker_fees', models.FloatField(blank=True, default=None, null=True)),
                ('gamma', models.FloatField(blank=True, default=None, null=True)),
                ('tickers_selected', models.CharField(max_length=200)),
                ('short_selling', models.BooleanField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expected_return', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.expectedreturn')),
                ('risk_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.riskmodel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historicalvalue', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]