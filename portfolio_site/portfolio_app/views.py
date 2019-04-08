from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Portfolio, Stock, StockPick


def index(request):
    if request.user.is_authenticated:
        portfolio_list = Portfolio.objects.all()
        context = {
            'portfolio_list': portfolio_list,
        }
        return render(request, 'portfolio_app/index.html', context)
    else:
        return HttpResponseRedirect('/portfolio_app/login')    
    
    # portfolio_list = Portfolio.objects.all()
    # context = {
    #     'portfolio_list': portfolio_list,
    # }
    # return render(request, 'portfolio_app/index.html', context)


def portfolio(request, portfolio_id):
    p = get_object_or_404(Portfolio, pk=portfolio_id)
    context = {
        'portfolio': p,
    }
    return render(request, 'portfolio_app/portfolio.html', context)

# def portfolio(request, portfolio_id):
#     return HttpResponse()