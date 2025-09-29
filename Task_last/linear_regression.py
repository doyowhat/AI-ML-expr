# 步骤: 界定问题边界 -> 数据集 -> 数据治理 -> 特征提取 -> 模型 -> 训练预测 -> 量化分析 -> 可视化
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. 确定数据集
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

# 2. 数据治理
train.dropna(inplace=True)
test.dropna(inplace=True)
# 修正测试集标签（去掉多余的点号）
test["income"] = test["income"].str.replace(".", "", regex=False)

# 3. 特征提取与编码
categorical_cols = train.select_dtypes(include="object").columns.drop("income")
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    train[col] = le.fit_transform(train[col])
    test[col] = le.transform(test[col])
    label_encoders[col] = le

X_train = train.drop("income", axis=1)
y_train = (train["income"] == ">50K").astype(int)

X_test = test.drop("income", axis=1)
y_test = (test["income"] == ">50K").astype(int)

# 标准化（数值特征）
scaler = StandardScaler()
X_train[X_train.columns] = scaler.fit_transform(X_train)
X_test[X_test.columns] = scaler.transform(X_test)

# 4. 模型训练
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# 5. 预测
y_pred = clf.predict(X_test)

# 6. 量化分析
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 7. 可视化展示
# 混淆矩阵

# 创建输出路径
output_dir = "./utils"
os.makedirs(output_dir, exist_ok=True)

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["<=50K", ">50K"],
            yticklabels=["<=50K", ">50K"])
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
confusion_matrix_path = os.path.join(output_dir, "linear_regression_confusion_matrix.png")
plt.savefig(confusion_matrix_path)
plt.close()
print(f"Confusion matrix saved to {confusion_matrix_path}")

# 简单特征重要性可视化（逻辑回归系数）
importance = pd.Series(clf.coef_[0], index=X_train.columns)
plt.figure(figsize=(6,8))
importance.sort_values(ascending=False)[:10].plot(kind="barh", title="Top Features")
feature_importance_path = os.path.join(output_dir, "linear_regression_top_features.png")
plt.tight_layout()
plt.savefig(feature_importance_path)
plt.close()
print(f"Feature importance plot saved to {feature_importance_path}")
