# app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Budget, Expense
from django.contrib.auth.models import User

# Home page view
def home_view(request):
    return render(request, 'home.html')

# User registration view
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')

# User login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

# User logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

# Budget management view
@login_required
def budget_view(request):
    if request.method == 'POST':
        amount = request.POST.get('budget')
        if amount:
            budget = Budget(user=request.user, amount=amount)
            budget.save()
            messages.success(request, "Budget set successfully.")
            return redirect('budget')

    budget = Budget.objects.filter(user=request.user).first()
    return render(request, 'budget.html', {'budget': budget})

# Expense tracking view
@login_required
def expenses_view(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        category = request.POST.get('category')
        amount = request.POST.get('amount')

        if description and category and amount:
            expense = Expense(
                user=request.user,
                description=description,
                category=category,
                amount=amount
            )
            expense.save()
            messages.success(request, "Expense added successfully.")
            return redirect('expenses')

    expenses = Expense.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'expenses.html', {'expenses': expenses})

# Transaction history view
@login_required
def transaction_history_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'transaction_history.html', {'expenses': expenses})

# Financial analysis view
@login_required
def financial_analysis_view(request):
    budget = Budget.objects.filter(user=request.user).first()
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    remaining_budget = budget.amount - total_expenses if budget else 0
    return render(request, 'financial_analysis.html', {
        'budget': budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
    })
