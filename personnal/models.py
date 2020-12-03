from django.db import models

class Exchange(models.Model):
    name = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

class Coin(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    ticker = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    sector = models.IntegerField(null=True)
    industry = models.IntegerField(null=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

class DataVendor(models.Model):
    name = models.CharField(max_length=200)
    website_url = models.CharField(max_length=200)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)


class DailyPrice(models.Model):
    data_vendor = models.ForeignKey(DataVendor, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Coin, on_delete=models.CASCADE)

    open_price = models.IntegerField(null=True)
    high_price = models.IntegerField(null=True)
    low_price = models.IntegerField(null=True)
    close_price = models.IntegerField(null=True)
    adj_close_price = models.IntegerField(null=True)
    volume = models.IntegerField(null=True)
    
    price_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)