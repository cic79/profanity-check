import pandas as pd
from joblib import dump
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

data = pd.read_csv("clean_data_en.csv")
texts = data["text"].astype(str)
y = data["is_offensive"]

vectorizer = TfidfVectorizer(stop_words="english", min_df=0.0001)
X = vectorizer.fit_transform(texts)

model = LinearSVC(class_weight="balanced", dual=False, tol=1e-2, max_iter=1e5)
cclf = CalibratedClassifierCV(base_estimator=model)
cclf.fit(X, y)

dump(vectorizer, "vectorizer_en.joblib")
dump(cclf, "model_en.joblib")

data = pd.read_csv("clean_data_it.csv")
texts = data["text"].astype(str)
y = data["is_offensive"]

vectorizer = TfidfVectorizer(stop_words="italian", min_df=0.0001)
X = vectorizer.fit_transform(texts)

model = LinearSVC(class_weight="balanced", dual=False, tol=1e-2, max_iter=1e5)
cclf = CalibratedClassifierCV(base_estimator=model)
cclf.fit(X, y)

dump(vectorizer, "vectorizer_it.joblib")
dump(cclf, "model_it.joblib")
