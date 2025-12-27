#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pandas numpy scikit-learn imbalanced-learn xgboost fastapi uvicorn joblib


# In[3]:


import pandas as pd

df = pd.read_csv("transactions.csv")

# Convert rule logic into features
df["amount_ratio"] = df["amount"] / df["avg_user_amount"]

features = [
    "amount_ratio",
    "txn_count_5min",
    "location_changed",
    "is_night",
    "new_device",
    "merchant_risk"
]

X = df[features]
y = df["label"]


# In[7]:


from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)


# In[9]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

y_pred = log_model.predict(X_test)
y_prob = log_model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))


# In[11]:


from xgboost import XGBClassifier

xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42
)

xgb_model.fit(X_train, y_train)

y_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]

print("XGBoost ROC-AUC:", roc_auc_score(y_test, y_prob_xgb))


# In[13]:


import joblib

joblib.dump(log_model, "logistic_fraud_model.pkl")
joblib.dump(xgb_model, "xgb_fraud_model.pkl")

