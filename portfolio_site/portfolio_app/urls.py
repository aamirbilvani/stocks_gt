from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('portfolio/<int:portfolio_id>', views.portfolio, name='portfolio')
]