from django.db import models
#from django.contrib.postgres.fields import ArrayField, JSONField
from .utils.strategy import StrategyTypes, MethodTypes

from django.utils.timezone import now

STRATEGY_NAME = (
    ("EF", "Efficient Frontier"),
    ("HRP", "Hierarchical Risk Parity"),
    ("CLA", "Critical Line Algorithm"),
)


EXPECTED_RETURN = (
    ("MEAN", "Mean historical return"),
    ("EMA", "Exponential historical return"),
    ("CAPM", "Capital asset pricing model"),
)

RISK_MODEL = (
    ("SAMPLECOV", "Sample covariance"),
    ("SEMICOV", "Semi covariance"),
    ("EXPCOV", "Exponential covariance"),
    ("MINDETCOV", "Minimum determinant covariance"),
    ("COVSHRINKAGE", "Covariance Shrinkage"),
    ("LEDOITWOLF", "Ledoit-Wolf method"),
    ("ORACLEAPPROX", "Oracle Approximation"),
)

class RecordHypothethis(models.Model):
    name = models.CharField(max_length=200)
    capital = models.IntegerField(null=True)
    risk_free_rate = models.IntegerField(null=True)
    broker_fees = models.IntegerField(null=True)
    gamma = models.IntegerField(null=True)
    short_selling = models.BooleanField(null=True)
    #allocation = JSONField(null=True)
    allocation = models.CharField(max_length=200)
    #tickers_selected = ArrayField(base_field=models.CharField, null=True)
    tickers_selected = models.CharField(max_length=200)
    method = models.CharField(max_length=200)
    strategy = models.CharField(max_length=200)
    #strategy = models.IntegerField(choices=StrategyTypes.choices(), default=StrategyTypes.PROSPECT)
    #method = models.IntegerField(choices=MethodTypes.choices(), default=MethodTypes.PROSPECT)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=True)

    def get_strategy_type_label(self):
        return StrategyTypes(self.type).name.title()

    def get_method_type_label(self):
        return MethodTypes(self.type).name.title()

class Strategy(models.Model):
    name = models.CharField(max_length=200, choices=STRATEGY_NAME)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=True)

class ExpectedReturn(models.Model):
    name = models.CharField(max_length=200, choices=EXPECTED_RETURN)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=True)

class RiskModel(models.Model):
    name = models.CharField(max_length=200, choices=RISK_MODEL)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=True)

class EfficientFrontier(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    expected_return = models.ForeignKey(ExpectedReturn, on_delete=models.CASCADE)
    risk_model = models.ForeignKey(RiskModel, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=True)

class HierarchicalRiskParity(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    risk_model = models.ForeignKey(RiskModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=True)

class CriticalLineAlgorithm(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    expected_return = models.ForeignKey(ExpectedReturn, on_delete=models.CASCADE)
    risk_model = models.ForeignKey(RiskModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=True)

class BlackLitterman(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    risk_model = models.ForeignKey(RiskModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=True)