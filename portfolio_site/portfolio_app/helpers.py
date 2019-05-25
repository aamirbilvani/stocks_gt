from .models import StockPick, Stock

class StockPick_Set:
    def __init__(self, stockpick):
        self.stock = stockpick.stock
        self._set = [stockpick]

    def add(self, stockpick):
        if stockpick.stock.symbol == self.stock.symbol:
            self._set.append(stockpick)

    def is_stockpick_valid(self, stockpick):
        return stockpick.stock.symbol == self.stock.symbol

    def current_value(self):
        current_value = 0.0
        for stockpick in self._set:
            current_value += stockpick.current_value()
        return current_value

    def original_value(self):
        original_value = 0.0
        for stockpick in self._set:
            original_value += stockpick.original_value()
        return original_value

    def quantity(self):
        quantity = 0
        for stockpick in self._set:
            quantity += stockpick.quantity
        return quantity

    def value_per_share(self):
        return self.original_value() / self.quantity()

    def day_begin_value(self):
        day_begin_value = 0
        for stockpick in self._set:
            day_begin_value += stockpick.day_begin_value()
        return day_begin_value

    def daily_pl(self):
        daily_pl = 0
        for stockpick in self._set:
            daily_pl += stockpick.daily_pl()
        return daily_pl

    def total_pl(self):
        total_pl = 0
        for stockpick in self._set:
            total_pl += stockpick.total_pl()
        return total_pl

    def year_begin_value(self):
        year_begin_value = 0
        for stockpick in self._set:
            year_begin_value += stockpick.year_begin_value()
        return year_begin_value

    def ytd_pl(self):
        ytd_pl = 0
        for stockpick in self._set:
            ytd_pl += stockpick.ytd_pl()
        return ytd_pl

    def daily_pl_percent(self):
        return self.daily_pl() / self.day_begin_value() * 100

    def total_pl_percent(self):
        return self.total_pl() / self.original_value() * 100

    def ytd_pl_percent(self):
        return self.ytd_pl() / self.year_begin_value() * 100

    def annualized_return(self):
        annualized_return_total = 0.0
        for stockpick in self._set:
            annualized_return_total += stockpick.annualized_return() / 100 * stockpick.original_value()
        return annualized_return_total / self.original_value() * 100
