from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score
import numpy as np

class RandomForestAnomalyDetector(BaseEstimator, ClassifierMixin):
    def __init__(self, max_depth=20, random_state=0, outlier_fraction=0.4, class_weight=None, sample_weights=None, threshold=None):
        self.outlier_fraction = outlier_fraction
        self.class_weight = class_weight
        self.sample_weights = sample_weights
        self.threshold = threshold
        self.model = RandomForestClassifier(max_depth=max_depth, random_state=random_state, class_weight=class_weight, n_jobs=-1)

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict_proba(self, X_test):
        temp = self.model.predict_proba(X_test)
        self.proba = temp[:,1]
        return temp


    def predict(self, X_test):
        self.predict_proba(X_test)
        if self.threshold is None:
            threshold = np.percentile(self.proba, 100 - (self.outlier_fraction * 100))
        else:
            threshold = self.threshold
        return (self.proba > threshold).astype(int)

    def evaluate(self, X_test, y_test):
        self.y_pred = self.predict(X_test)

    def get_params(self, deep=True):
        return {"outlier_fraction": self.outlier_fraction}

    def set_params(self, **params):
        for parameter, value in params.items():
            setattr(self, parameter, value)
        return self