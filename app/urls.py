from django.urls import path
from .views import home_view, register_view, login_view, logout_view, budget_view, expenses_view, transaction_history_view, financial_analysis_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('budget/', budget_view, name='budget'),
    path('expenses/', expenses_view, name='expenses'),
    path('transactions/', transaction_history_view, name='transactions'),
    path('analysis/', financial_analysis_view, name='analysis'),
]
