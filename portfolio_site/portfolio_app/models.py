import csv
from datetime import datetime, timedelta, date
import os
from django.conf import settings
from django.db import models
from django.core.cache import cache

class Portfolio(models.Model):
    name = models.CharField('Portfolio Name', max_length=50)
    date_added = models.DateTimeField('Date Added', auto_now_add=True)

    def __str__(self):
        return self.name

    def current_value(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        portfolio_value = 0.0
        for stockpick in stockpicks:
            portfolio_value += (stockpick.current_value())
        return portfolio_value

    def original_value(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        portfolio_original_value = 0.0
        for stockpick in stockpicks:
            portfolio_original_value += (stockpick.original_value())
        return portfolio_original_value

    def day_begin_value(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        day_begin_value = 0.0
        for stockpick in stockpicks:
            day_begin_value += stockpick.day_begin_value()
        return day_begin_value

    def daily_pl(self):
        return self.current_value() - self.day_begin_value()
    
    def daily_pl_percent(self):
        return self.daily_pl() / self.day_begin_value() * 100

    def total_value(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        total_value = 0.0
        for stockpick in stockpicks:
            total_value += stockpick.quantity * stockpick.value_per_share
        return total_value

    def total_pl(self):
        return self.current_value() - self.total_value()

    def total_pl_percent(self):
        return self.total_pl() / self.total_value() * 100

    def year_begin_value(self):
        stockpicks = StockPick.objects.filter(portfolio_id=self.id)
        year_begin_value = 0.0
        for stockpick in stockpicks:
            year_begin_value += stockpick.year_begin_value()
        return year_begin_value

    def ytd_pl(self):
        return self.current_value() - self.year_begin_value()
    
    def ytd_pl_percent(self):
        return self.ytd_pl() / self.year_begin_value() * 100

class Stock(models.Model):
    name = models.CharField('Company Name', max_length=255)
    url = models.CharField('URL', max_length=255)
    symbol = models.CharField('Symbol', max_length=10, db_index=True)
    
    def __str__(self):
        return self.symbol + " - " + self.name

    def current_value(self):
        cache_key = self.symbol + "_CURR"
        cached_current_value = cache.get(cache_key)
        if cached_current_value is not None:
            return cached_current_value

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

                    cache.set(cache_key, current_value)
                    return current_value

    class Meta:
        ordering = ['symbol']


class StockPick(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    quantity = models.IntegerField('Quantity')
    value_per_share = models.FloatField('Value per share')
    date_added = models.DateField('Date Added')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stockpicks')

    def __str__(self):
        return self.stock.name + ", Quantity: " + str(self.quantity)
    
    def current_value(self):
        return self.stock.current_value() * self.quantity

    def original_value(self):
        return self.quantity * self.value_per_share

    def day_begin_value(self):
        cache_key = self.stock.symbol + "_DAY_BEGIN"
        cached_day_begin_value = cache.get(cache_key)
        if cached_day_begin_value is not None:
            return cached_day_begin_value * self.quantity

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
                    cache.set(cache_key, day_begin_value)
                    return day_begin_value * self.quantity

    def daily_pl(self):        
        return self.current_value() - self.day_begin_value()      
    
    def daily_pl_percent(self):
        return self.daily_pl() / self.day_begin_value() * 100

    def total_pl(self):
        return self.current_value() - self.original_value()

    def total_pl_percent(self):
        return self.total_pl() / self.original_value() * 100

    def year_begin_value(self):
        cache_key = self.stock.symbol + "_YEAR_BEGIN"
        cached_year_begin_value = cache.get(cache_key)
        if cached_year_begin_value is not None:
            return cached_year_begin_value * self.quantity

        current_date = datetime.today()
        year = current_date.year - 1
        
        value = ''
        col_index = -1
        while year > 2013 and value == '':
            year_file_path = os.path.join(settings.BASE_DIR, '../data/historical/{:04d}.csv'.format(year))
            with open(year_file_path) as year_file:
                year_list = list(csv.reader(year_file))
                header_row = year_list[0]

                for i in range(len(header_row)):
                    col_symbol = str(header_row[i]).strip()
                    if col_symbol == self.stock.symbol:
                        col_index = i
                
                for i in range(len(year_list) - 1, 0, -1):
                    if year_list[i][col_index]:
                        value = year_list[i][col_index].strip()
                        break

            year -= 1
        
        year_begin_value = float(value)
        cache.set(cache_key, year_begin_value)
        return year_begin_value * self.quantity
    
    def ytd_pl(self):
        return self.current_value() - self.year_begin_value()

    def ytd_pl_percent(self):
        return self.ytd_pl() / self.year_begin_value() * 100

    def annualized_return(self):
        today = date.today()
        time_period = today - self.date_added
        time_period_years = time_period.days / 365
        annualized_return = ((1 + self.total_pl_percent() / 100) ** (1 / time_period_years)) - 1
        return annualized_return * 100
