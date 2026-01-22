import pandas as pd

# Load expanded scenarios
df = pd.read_excel(
    r"C:\Users\HUSSAIN\Desktop\Policy_Compliance_Project\Data\compliance_scenarios_expanded.xlsx"
)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

print(df.head())
print(df["label"].value_counts())

#encoding--------------------------------------------------

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df["label_encoded"] = le.fit_transform(df["label"])

# Compliant → 0
# Violation → 1

# TF-IDF Vectorization------------------------------------

from sklearn.feature_extraction.text import TfidfVectorizer

X = df["scenario"]
y = df["label_encoded"]

tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=3000,
    ngram_range=(1, 2)
)

X_tfidf = tfidf.fit_transform(X)

# TRAIN - TEST SPLIT ------------------------------------

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# MODEL 1 - LOGISTIC REGRESSION ( BASELINE MODEL) ----

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

y_pred_lr = lr.predict(X_test)

print("Logistic Regression Results")
print(confusion_matrix(y_test, y_pred_lr))
print(classification_report(y_test, y_pred_lr))

# MODEL 2 - RANDOM FOREST -----------------------------

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)

print("Random Forest Results")
print(confusion_matrix(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# SAVING THE MODELS -----------------------

import joblib

# Save TF-IDF
joblib.dump(tfidf, r"C:\Users\HUSSAIN\Desktop\Policy_Compliance_Project\Models\tfidf_vectorizer.pkl")

# Save models
joblib.dump(lr, r"C:\Users\HUSSAIN\Desktop\Policy_Compliance_Project\Models\logistic_regression_model.pkl")
joblib.dump(rf, r"C:\Users\HUSSAIN\Desktop\Policy_Compliance_Project\Models\random_forest_model.pkl")

print("Models saved successfully")
