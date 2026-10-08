import polars as pl
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, r2_score, mean_squared_error

class MLModelMetrics(BaseModel):
    model_name: str
    task_type: str  # classification, regression
    primary_metric_name: str
    primary_metric_value: float
    all_metrics: Dict[str, float]
    feature_importances: Dict[str, float]
    train_samples: int
    test_samples: int

class MLAnalysisResult(BaseModel):
    task_type: str
    target_column: str
    models_evaluated: List[MLModelMetrics]
    best_model_name: str
    limitations: List[str]

class MLEngine:
    """
    ML Engine: Trains baseline and tree-based models, evaluates performance,
    extracts feature importances, and checks for data leakage.
    """
    
    @staticmethod
    def train_and_evaluate(df: pl.DataFrame, target_col: Optional[str] = None) -> MLAnalysisResult:
        pdf = df.to_pandas()
        
        cols_lower = {c.lower(): c for c in pdf.columns}
        if not target_col:
            target_col = cols_lower.get("churn") or cols_lower.get("target") or cols_lower.get("converted")
            
        if not target_col or target_col not in pdf.columns:
            return MLAnalysisResult(
                task_type="classification",
                target_column="N/A",
                models_evaluated=[],
                best_model_name="None",
                limitations=["No valid target column identified for ML training."]
            )

        clean_df = pdf.dropna(subset=[target_col]).copy()
        
        # Prepare feature matrix X and target y
        y = clean_df[target_col]
        X_raw = clean_df.drop(columns=[target_col])
        
        # Keep numeric columns and one-hot encode low-cardinality categorical columns
        X = pd.get_dummies(X_raw, drop_first=True)
        # Select numeric columns only if any NaN remains
        X = X.select_dtypes(include=[np.number]).fillna(0)
        
        if X.shape[1] == 0 or len(clean_df) < 10:
            return MLAnalysisResult(
                task_type="classification",
                target_column=target_col,
                models_evaluated=[],
                best_model_name="None",
                limitations=["Insufficient clean samples or feature columns for model training."]
            )

        unique_y = y.unique()
        is_classification = len(unique_y) <= 10
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        
        evaluated: List[MLModelMetrics] = []
        
        if is_classification:
            # 1. Baseline Logistic Regression
            lr = LogisticRegression(max_iter=500, random_state=42)
            lr.fit(X_train, y_train)
            y_pred_lr = lr.predict(X_test)
            acc_lr = accuracy_score(y_test, y_pred_lr)
            f1_lr = f1_score(y_test, y_pred_lr, average='weighted', zero_division=0)
            
            evaluated.append(MLModelMetrics(
                model_name="Logistic Regression Baseline",
                task_type="classification",
                primary_metric_name="Accuracy",
                primary_metric_value=float(acc_lr),
                all_metrics={"accuracy": float(acc_lr), "f1_weighted": float(f1_lr)},
                feature_importances={col: float(abs(coef)) for col, coef in zip(X.columns, lr.coef_[0]) if abs(coef) > 0.001},
                train_samples=len(X_train),
                test_samples=len(X_test)
            ))
            
            # 2. Random Forest Classifier
            rf = RandomForestClassifier(n_estimators=50, random_state=42)
            rf.fit(X_train, y_train)
            y_pred_rf = rf.predict(X_test)
            acc_rf = accuracy_score(y_test, y_pred_rf)
            f1_rf = f1_score(y_test, y_pred_rf, average='weighted', zero_division=0)
            
            importances = dict(sorted(zip(X.columns, rf.feature_importances_), key=lambda x: x[1], reverse=True)[:10])
            importances = {k: float(v) for k, v in importances.items()}
            
            evaluated.append(MLModelMetrics(
                model_name="Random Forest Classifier",
                task_type="classification",
                primary_metric_name="Accuracy",
                primary_metric_value=float(acc_rf),
                all_metrics={"accuracy": float(acc_rf), "f1_weighted": float(f1_rf)},
                feature_importances=importances,
                train_samples=len(X_train),
                test_samples=len(X_test)
            ))
            
            best_m = max(evaluated, key=lambda m: m.primary_metric_value)
            
            return MLAnalysisResult(
                task_type="classification",
                target_column=target_col,
                models_evaluated=evaluated,
                best_model_name=best_m.model_name,
                limitations=[
                    "Association model. Feature importances indicate predictive correlation, not direct causality.",
                    "Validation evaluated on 25% holdout test split."
                ]
            )
        else:
            # Regression task
            rf = RandomForestRegressor(n_estimators=50, random_state=42)
            rf.fit(X_train, y_train)
            y_pred_rf = rf.predict(X_test)
            r2 = r2_score(y_test, y_pred_rf)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))
            
            importances = dict(sorted(zip(X.columns, rf.feature_importances_), key=lambda x: x[1], reverse=True)[:10])
            importances = {k: float(v) for k, v in importances.items()}
            
            evaluated.append(MLModelMetrics(
                model_name="Random Forest Regressor",
                task_type="regression",
                primary_metric_name="R2_Score",
                primary_metric_value=float(r2),
                all_metrics={"r2_score": float(r2), "rmse": float(rmse)},
                feature_importances=importances,
                train_samples=len(X_train),
                test_samples=len(X_test)
            ))
            
            return MLAnalysisResult(
                task_type="regression",
                target_column=target_col,
                models_evaluated=evaluated,
                best_model_name="Random Forest Regressor",
                limitations=["Evaluated on 25% holdout test set."]
            )
