from django.forms import ModelForm, inlineformset_factory
from portfolio_app.models import Portfolio, StockPick

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        exclude = ()

class StockPickForm(ModelForm):
    class Meta:
        model = StockPick
        exclude = ()
    
StockPickFormSet = inlineformset_factory(Portfolio, StockPick, StockPickForm, extra=1)
