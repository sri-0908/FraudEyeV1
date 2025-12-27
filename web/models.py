from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=20)
    customer_id = models.CharField(max_length=20)
    amount = models.FloatField()
    country = models.CharField(max_length=5)
    risk_score = models.IntegerField()
    fraud_flag = models.BooleanField()
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
