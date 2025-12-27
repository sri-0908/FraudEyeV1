from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Transaction
from .fraud_engine import analyze_transaction
import random, string


# Home
def home(request):
    return render(request, "web/home.html")


# Register
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "web/register.html", {"error": "Username exists"})

        User.objects.create_user(username=username, password=password)
        return redirect("login")

    return render(request, "web/register.html")


# Login
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("dashboard")

        return render(request, "web/login.html", {"error": "Invalid credentials"})

    return render(request, "web/login.html")


# Logout
def logout_view(request):
    logout(request)
    return redirect("home")


# Dashboard (DJANGO ONLY)
@login_required
def dashboard(request):
    if request.method == "POST":

        transaction_id = "TXN" + "".join(random.choices(string.digits, k=6))
        customer_id = random.choice(["CUST1001", "CUST1002", "CUST1003"])

        amount = round(random.uniform(100, 80000), 2)
        country = random.choice(["IN", "US", "AE"])

        result = analyze_transaction(
            user=request.user,
            amount=amount,
            country=country,
            customer_id=customer_id
        )

        Transaction.objects.create(
            user=request.user,
            transaction_id=transaction_id,
            customer_id=customer_id,
            amount=amount,
            country=country,
            risk_score=result["risk_score"],
            fraud_flag=result["fraud_flag"],
            explanation=", ".join(result["explanation"])
        )

    transactions = Transaction.objects.filter(user=request.user).order_by("-created_at")
    avg_risk = round(sum(t.risk_score for t in transactions) / len(transactions), 2) if transactions else 0

    return render(request, "web/dashboard.html", {
        "transactions": transactions,
        "avg_risk": avg_risk
    })
