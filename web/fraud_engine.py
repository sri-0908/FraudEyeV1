
from django.utils import timezone
from datetime import timedelta
from .models import Transaction
import statistics


def analyze_transaction(user, amount, country, customer_id):
    risk = 0
    reasons = []

    now = timezone.now()
    txns = Transaction.objects.filter(user=user)

    # 1️⃣ Large amount anomaly
    amounts = list(txns.values_list("amount", flat=True))
    if amounts:
        avg = statistics.mean(amounts)
        if amount > avg * 3:
            risk += 30
            reasons.append("Unusually large amount compared to user history")

    # 2️⃣ Rapid transactions (last 5 minutes)
    recent = txns.filter(created_at__gte=now - timedelta(minutes=5)).count()
    if recent >= 3:
        risk += 25
        reasons.append("Multiple rapid transactions detected")

    # 3️⃣ High frequency today
    today_count = txns.filter(created_at__date=now.date()).count()
    if today_count >= 10:
        risk += 20
        reasons.append("High transaction frequency today")

    # 4️⃣ SPAM: same customer + same amount rapidly
    spam_txns = txns.filter(
        customer_id=customer_id,
        amount=amount,
        created_at__gte=now - timedelta(minutes=3)
    ).count()

    if spam_txns >= 2:
        risk += 30
        reasons.append("Repeated spam transactions from same customer")

    # 5️⃣ Foreign country
    if country != "IN":
        risk += 10
        reasons.append("Transaction from foreign country")

    risk = min(risk, 100)

    if risk >= 70:
        label = "Mostly Fraud"
        flag = True
    elif risk >= 40:
        label = "Medium Risk"
        flag = True
    else:
        label = "Safe"
        flag = False

    return {
        "risk_score": risk,
        "fraud_flag": flag,
        "label": label,
        "explanation": reasons
    }

