from django.forms import ModelForm, inlineformset_factory
from portfolio_app.models import Portfolio, StockPick
from .widgets import FengyuanChenDatePickerInput

class StockPickForm(ModelForm):
    class Meta:
        model = StockPick
        fields = '__all__'
        widgets = {
            'date_added':FengyuanChenDatePickerInput(
                attrs={
                    'class': 'date-picker-input form-control'
                }
            )
        }

StockPickFormSet = inlineformset_factory(Portfolio, StockPick, form=StockPickForm, exclude=[], extra=1, can_delete=True)
