from django.forms import ModelForm, inlineformset_factory
from portfolio_app.models import Portfolio, StockPick
    
StockPickFormSet = inlineformset_factory(Portfolio, StockPick, exclude=[], extra=1, can_delete=True)
