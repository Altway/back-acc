# Generated by Django 3.1.3 on 2020-11-23 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpectedReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('MEAN', 'Mean historical return'), ('EMA', 'Exponential historical return'), ('CAPM', 'Capital asset pricing model')], max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RiskModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('SAMPLECOV', 'Sample covariance'), ('SEMICOV', 'Semi covariance'), ('EXPCOV', 'Exponential covariance'), ('MINDETCOV', 'Minimum determinant covariance'), ('COVSHRINKAGE', 'Covariance Shrinkage'), ('LEDOITWOLF', 'Ledoit-Wolf method'), ('ORACLEAPPROX', 'Oracle Approximation')], max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('EF', 'Efficient Frontier'), ('HRP', 'Hierarchical Risk Parity'), ('CLA', 'Critical Line Algorithm')], max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HierarchicalRiskParity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('risk_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.riskmodel')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.strategy')),
            ],
        ),
        migrations.CreateModel(
            name='EfficientFrontier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expected_return', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.expectedreturn')),
                ('risk_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.riskmodel')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.strategy')),
            ],
        ),
        migrations.CreateModel(
            name='CriticalLineAlgorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expected_return', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.expectedreturn')),
                ('risk_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.riskmodel')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.strategy')),
            ],
        ),
        migrations.CreateModel(
            name='BlackLitterman',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('risk_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.riskmodel')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.strategy')),
            ],
        ),
    ]