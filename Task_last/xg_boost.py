import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_preprocess():
    columns = [
        "age", "workclass", "fnlwgt", "education", "education_num", "marital_status",
        "occupation", "relationship", "race", "sex", "capital_gain", "capital_loss",
        "hours_per_week", "native_country", "income"
    ]

    train = pd.read_csv(
        "adult/adult.data",
        header=None, names=columns,
        na_values=" ?", skipinitialspace=True
    )
    test = pd.read_csv(
        "adult/adult.test",
        header=None, names=columns,
        na_values=" ?", skipinitialspace=True, skiprows=1
    )

    # 数据治理
    train.dropna(inplace=True)
    test.dropna(inplace=True)
    test["income"] = test["income"].str.replace(".", "", regex=False)

    # 类别编码
    categorical_cols = train.select_dtypes(include="object").columns.drop("income")
    for col in categorical_cols:
        le = LabelEncoder()
        train[col] = le.fit_transform(train[col])
        test[col] = le.transform(test[col])

    X_train = train.drop("income", axis=1)
    y_train = (train["income"] == ">50K").astype(int)
    X_test = test.drop("income", axis=1)
    y_test = (test["income"] == ">50K").astype(int)

    # 标准化
    scaler = StandardScaler()
    X_train[X_train.columns] = scaler.fit_transform(X_train)
    X_test[X_test.columns] = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = load_and_preprocess()


clf = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss"   # 保留这个即可
)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("XGBoost Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 创建输出路径
output_dir = "./utils"
os.makedirs(output_dir, exist_ok=True)

# 混淆矩阵
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
            xticklabels=["<=50K", ">50K"],
            yticklabels=["<=50K", ">50K"])
plt.title("XGBoost Confusion Matrix")
confusion_matrix_path = os.path.join(output_dir, "xg_boost_confusion_matrix.png")
plt.savefig(confusion_matrix_path)
plt.close()
print(f"Confusion matrix saved to {confusion_matrix_path}")

# 特征重要性
importances = pd.Series(clf.feature_importances_, index=X_train.columns)
plt.figure(figsize=(8, 6))
importances.sort_values(ascending=False)[:10].plot(kind="barh", title="XGBoost Top Features")
feature_importance_path = os.path.join(output_dir, "xg_boost_top_features.png")
plt.tight_layout()
plt.savefig(feature_importance_path)
plt.close()
print(f"Feature importance plot saved to {feature_importance_path}")
