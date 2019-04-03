from django.contrib import admin
from .models import Portfolio, Stock, StockPick

class StockPickInline(admin.StackedInline):
    model = StockPick
    extra = 3


class PortfolioAdmin(admin.ModelAdmin):    
    inlines = [StockPickInline]

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Stock)