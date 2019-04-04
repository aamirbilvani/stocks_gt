from django.db import models
import csv
from datetime import datetime, timedelta
import os

class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField('Date Added')

    def __str__(self):
        return self.name + ", CurrentValue: Rs." + str('{:.2f}'.format(self.current_value()))

    def current_value(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        sum = 0.0
        for stockpick in stockpicks:
            sum += (stockpick.stock.current_value() * stockpick.quantity)
        return sum
        

class Stock(models.Model):
    name = models.CharField('Company Name', max_length=255)
    url = models.CharField('URL', max_length=255)
    symbol = models.CharField('Symbol', max_length=10)
    
    def __str__(self):
        return self.name + ", CurrentValue: Rs." + str('{:.2f}'.format(self.current_value()))

    def current_value(self):
        current_date = datetime.today()
        new_date = current_date

        for _ in range(7):
            path = '../data/{:04d}_{:02d}_{:02d}.csv'.format(new_date.year, new_date.month, new_date.day)
            if os.path.isfile(path):
                break
            else:
                new_date = new_date - timedelta(days=1)

        with open(path, 'r') as data_file:
            data_list = list(csv.reader(data_file))
            header_row = data_list[0]

            for i in range(len(header_row)):
                col_symbol = str(header_row[i]).strip()
                if col_symbol == self.symbol:
                    value = data_list[-1][i].strip()
                    if not value:
                        value = data_list[-2][i].strip()
                    current_value = float(value)
                    return current_value


class StockPick(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    quantity = models.IntegerField('Quantity')
    value_per_share = models.FloatField('Value per share')
    date_added = models.DateTimeField('Date Added')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stockpicks')

    def __str__(self):
        return self.stock.name + ", Quantity: " + str(self.quantity) + ", Quantity: " + str(self.quantity)
    
    def current_value(self):
        return self.stock.current_value() * self.quantity
