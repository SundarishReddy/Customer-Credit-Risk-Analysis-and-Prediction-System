"""
Training script for credit risk model. Reads the Excel dataset used in the original notebook,
preprocesses features, trains an XGBoost classifier inside a sklearn Pipeline (preprocessor + clf),
and saves the pipeline to disk.

Usage:
    python train.py --data data/default_of_credit_card_clients.xls --out backend/model.joblib

"""
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import joblib


def load_data(path):
    # The original file has a header row at index 1 (header=1)
    df = pd.read_excel(path, header=1)
    return df


def build_and_train(df):
    # drop ID and rename target
    if 'ID' in df.columns:
        df = df.drop(columns=['ID'])
    if 'default payment next month' in df.columns:
        df = df.rename(columns={'default payment next month': 'target'})
    else:
        df = df.rename(columns={df.columns[-1]: 'target'})

    # categorical columns from notebook
    cat_cols = ['SEX','EDUCATION','MARRIAGE','PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6']
    num_cols = [c for c in df.columns if c not in cat_cols + ['target']]

    # ensure types
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype(str)

    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse=False), [c for c in cat_cols if c in X.columns]),
        ('num', MinMaxScaler(), num_cols)
    ], remainder='drop')

    clf = XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=100, random_state=42)

    pipe = Pipeline(steps=[('preprocessor', preprocessor), ('clf', clf)])

    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)
    proba = pipe.predict_proba(X_test)[:,1]

    metrics = {
        'accuracy': float(accuracy_score(y_test, preds)),
        'f1': float(f1_score(y_test, preds)),
        'roc_auc': float(roc_auc_score(y_test, proba))
    }

    return pipe, metrics


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='Path to Excel dataset (header=1)')
    parser.add_argument('--out', default='backend/model.joblib', help='Output path for saved pipeline')
    args = parser.parse_args()

    df = load_data(args.data)
    print('Loaded', df.shape)
    pipe, metrics = build_and_train(df)
    joblib.dump(pipe, args.out)
    print('Saved pipeline to', args.out)
    print('Metrics:', metrics)
