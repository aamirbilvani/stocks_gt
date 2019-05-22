from django.forms import DateInput

class FengyuanChenDatePickerInput(DateInput):
    template_name = 'portfolio_app/fengyuanchen_datepicker.html'
