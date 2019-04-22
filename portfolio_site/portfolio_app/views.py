# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404
# from django.template import loader
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import transaction
from .models import Portfolio
from .forms import *


class PortfolioListView(ListView):
    template_name = 'portfolio_app/index.html'
    model = Portfolio
    context_object_name = 'portfolio_list'

class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = 'portfolio_app/portfolio_details.html'
    context_object_name = 'portfolio'

class PortfolioCreateView(CreateView):
    model = Portfolio
    fields = '__all__'
    template_name = 'portfolio_app/portfolio_form.html'

    def get_success_url(self):
        portfolio = self.object
        return '/portfolio/' + str(portfolio.id)

    def get_context_data(self, **kwargs):
        data = super(PortfolioCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['stockpicks'] = StockPickFormSet(self.request.POST)
        else:
            data['stockpicks'] = StockPickFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        stockpicks = context['stockpicks']
        with transaction.atomic():
            self.object = form.save()

            if stockpicks.is_valid():
                stockpicks.instance = self.object
                stockpicks.save()
                return super(PortfolioCreateView, self).form_valid(form)
            else:
                context.update({
                    'stockpicks': stockpicks
                })
                return self.render_to_response(context)

class PortfolioEditView(UpdateView):
    model = Portfolio
    fields = '__all__'
    template_name = 'portfolio_app/portfolio_form.html'

    def get_success_url(self):
        portfolio = self.object
        return '/portfolio/' + str(portfolio.id)

    def get_context_data(self, **kwargs):
        context = super(PortfolioEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['stockpicks'] = StockPickFormSet(self.request.POST, instance=self.object)
            context['stockpicks'].full_clean()
        else:
            context['stockpicks'] = StockPickFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        stockpicks = context['stockpicks']
        
        if stockpicks.is_valid():
            response = super().get_context_data(form=form)
            stockpicks.instance = self.object
            stockpicks.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)