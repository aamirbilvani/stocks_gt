# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404
# from django.template import loader
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Portfolio
from .forms import StockPickFormSet


class PortfolioListView(ListView):
    template_name = 'portfolio_app/index.html'
    model = Portfolio
    context_object_name = 'portfolio_list'

    def get_context_data(self, **kwargs):
        context = super(PortfolioListView, self).get_context_data(**kwargs)
        context['back_url'] = "/"
        return context

class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = 'portfolio_app/portfolio_details.html'
    context_object_name = 'portfolio'

    def get_context_data(self, **kwargs):
        context = super(PortfolioDetailView, self).get_context_data(**kwargs)
        context['back_url'] = "/"
        return context

class PortfolioCreateView(CreateView):
    model = Portfolio
    fields = '__all__'
    template_name = 'portfolio_app/portfolio_form.html'

    def get_success_url(self):
        portfolio = self.object
        return '/portfolio/' + str(portfolio.id)

    def get_context_data(self, **kwargs):
        context = super(PortfolioCreateView, self).get_context_data(**kwargs)
        context['cancel_url'] = "/"
        context['back_url'] = "/"
        if self.request.POST:
            context['stockpicks'] = StockPickFormSet(self.request.POST)
        else:
            context['stockpicks'] = StockPickFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['stockpicks']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class PortfolioEditView(UpdateView):
    model = Portfolio
    fields = '__all__'
    template_name = 'portfolio_app/portfolio_form.html'

    def get_success_url(self):
        portfolio = self.object
        return '/portfolio/' + str(portfolio.id)

    def get_context_data(self, **kwargs):
        context = super(PortfolioEditView, self).get_context_data(**kwargs)
        context['cancel_url'] = self.get_success_url()
        context['back_url'] = self.get_success_url()

        if self.request.POST:
            context['stockpicks'] = StockPickFormSet(self.request.POST, instance=self.object)
            context['stockpicks'].full_clean()
        else:
            context['stockpicks'] = StockPickFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['stockpicks']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)