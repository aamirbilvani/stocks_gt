from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.PortfolioListView.as_view())),
    path('portfolio/<int:pk>', login_required(views.PortfolioDetailView.as_view())),
    path('new', login_required(views.PortfolioCreateView.as_view())),
    path('portfolio/<int:pk>/edit', login_required(views.PortfolioEditView.as_view())),
    # path('new', views.portfolio_create, name='portfolio_create'),
    # path('portfolio/<int:portfolio_id>/edit', views.portfolio_create, name='portfolio_create'),
]