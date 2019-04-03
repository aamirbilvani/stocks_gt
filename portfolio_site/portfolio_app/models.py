from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    date_added = models.DateField('Date Added')

    def __str__(self):
        return "Portfolio: " + self.name

class Stock(models.Model):
    name = models.CharField('Company Name', max_length=255)
    url = models.CharField('URL', max_length=255)
    symbol = models.CharField('Symbol', max_length=10)
    
    def __str__(self):
        return "Stock: " + self.name

class StockPick(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    quantity = models.IntegerField('Quantity')
    value_per_share = models.FloatField('Value per share')
    date_added = models.DateField('Date Added')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return "StockPick: " + self.stock.name + ", Quantity: " + str(self.quantity)
