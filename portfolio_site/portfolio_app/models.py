from django.db import models
import csv
from datetime import datetime, timedelta
import os
from django.conf import settings

class Portfolio(models.Model):
    name = models.CharField('Portfolio Name', max_length=50)
    date_added = models.DateTimeField('Date Added', auto_now_add=True)

    def __str__(self):
        return self.name

    def current_value(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        portfolio_value = 0.0
        for stockpick in stockpicks:
            portfolio_value += (stockpick.stock.current_value() * stockpick.quantity)
        return portfolio_value

    def daily_pl(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        day_begin_value = 0.0
        for stockpick in stockpicks:
            day_begin_value += stockpick.day_begin_value()
        return self.current_value() - day_begin_value
    
    def daily_pl_percent(self):
        return self.daily_pl() / self.current_value() * 100

    def total_pl(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        total_value = 0.0
        for stockpick in stockpicks:
            total_value += stockpick.quantity * stockpick.value_per_share
        return self.current_value() - total_value

    def total_pl_percent(self):
        return self.total_pl() / self.current_value() * 100


class Stock(models.Model):
    name = models.CharField('Company Name', max_length=255)
    url = models.CharField('URL', max_length=255)
    symbol = models.CharField('Symbol', max_length=10, db_index=True)
    
    def __str__(self):
        return self.symbol + " - " + self.name

    def current_value(self):
        current_date = datetime.today()
        new_date = current_date

        for _ in range(7):
            path = os.path.join(settings.BASE_DIR, '../data/{:04d}_{:02d}_{:02d}.csv'.format(new_date.year, new_date.month, new_date.day))
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

    class Meta:
        ordering = ['symbol']


class StockPick(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    quantity = models.IntegerField('Quantity')
    value_per_share = models.FloatField('Value per share')
    date_added = models.DateTimeField('Date Added', auto_now_add=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stockpicks')

    def __str__(self):
        return self.stock.name + ", Quantity: " + str(self.quantity)
    
    def current_value(self):
        return self.stock.current_value() * self.quantity

    def day_begin_value(self):
        current_date = datetime.today()
        new_date = current_date
        today = True

        for _ in range(7):
            path = os.path.join(settings.BASE_DIR, '../data/{:04d}_{:02d}_{:02d}.csv'.format(new_date.year, new_date.month, new_date.day))
            if os.path.isfile(path):
                break
            else:
                new_date = new_date - timedelta(days=1)
                today = False

        with open(path, 'r') as data_file:
            data_list = list(csv.reader(data_file))
            header_row = data_list[0]

            for i in range(len(header_row)):
                col_symbol = str(header_row[i]).strip()
                if col_symbol == self.stock.symbol:
                    if today:
                        day_begin_value = data_list[1][i].strip()
                    else:
                        day_begin_value = data_list[-1][i].strip()
                    
                    day_begin_value = float(day_begin_value)
                    return day_begin_value * self.quantity

    def daily_pl(self):        
        return self.current_value() - self.day_begin_value()      
    
    def daily_pl_percent(self):
        return self.daily_pl() / self.current_value() * 100

    def total_pl(self):
        original_value = self.quantity * self.value_per_share
        return self.current_value() - original_value

    def total_pl_percent(self):
        return self.total_pl() / self.current_value() * 100
