import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('height_data.csv')

# 显示数据基本信息
print("数据集基本信息：")
print(df.info())
print("\n数据前5行：")
print(df.head())

# 数据预处理
print("\n=== 数据预处理 ===")

# 1. 检查缺失值
print("缺失值检查：")
print(df.isnull().sum())

# 2. 检查异常值
print("\n数据描述性统计：")
print(df.describe())

# 3. 特征工程 - 创建新特征
# 遗传因素组合特征
df['Parent_Avg_Height'] = (df['Father_Height'] + df['Mother_Height']) / 2
df['Grandparent_Avg_Height'] = (df['Grandfather_Height'] + df['Grandmother_Height'] + 
                               df['Maternal_Grandfather_Height'] + df['Maternal_Grandmother_Height']) / 4
df['Genetic_Diff'] = df['Parent_Avg_Height'] - df['Grandparent_Avg_Height']

# 营养和锻炼总分
df['Total_Nutrition'] = (df['Nutrition_1_3'] + df['Nutrition_4_6'] + df['Nutrition_7_10'] + 
                        df['Nutrition_11_14'] + df['Nutrition_15_18'])
df['Total_Exercise'] = (df['Exercise_1_3'] + df['Exercise_4_6'] + df['Exercise_7_10'] + 
                       df['Exercise_11_14'] + df['Exercise_15_18'])

# 营养和锻炼在关键发育期的得分
df['Critical_Nutrition'] = df['Nutrition_11_14'] + df['Nutrition_15_18']  # 青春期营养
df['Critical_Exercise'] = df['Exercise_11_14'] + df['Exercise_15_18']    # 青春期锻炼

# 4. 定义特征和目标变量
feature_columns = [
    'Father_Height', 'Mother_Height', 'Grandfather_Height', 'Grandmother_Height',
    'Maternal_Grandfather_Height', 'Maternal_Grandmother_Height',
    'Nutrition_1_3', 'Nutrition_4_6', 'Nutrition_7_10', 'Nutrition_11_14', 'Nutrition_15_18',
    'Exercise_1_3', 'Exercise_4_6', 'Exercise_7_10', 'Exercise_11_14', 'Exercise_15_18',
    'Parent_Avg_Height', 'Grandparent_Avg_Height', 'Genetic_Diff',
    'Total_Nutrition', 'Total_Exercise', 'Critical_Nutrition', 'Critical_Exercise'
]

X = df[feature_columns]
y = df['Height_Category']

print(f"\n特征数量: {X.shape[1]}")
print(f"样本数量: {X.shape[0]}")
print(f"类别分布: {dict(pd.Series(y).value_counts())}")

# 5. 数据分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# 6. 特征标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n=== 模型训练与评估 ===")

# 7. 训练多个模型
models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
}

results = {}

for name, model in models.items():
    print(f"\n{name} 模型:")
    
    # 对于树模型使用原始特征，对于线性模型使用标准化特征
    if name == 'Random Forest':
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    else:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    
    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = accuracy
    
    print(f"准确率: {accuracy:.4f}")
    print("分类报告:")
    print(classification_report(y_test, y_pred, target_names=['<=170cm', '>170cm']))

# 8. 选择最佳模型进行详细分析
best_model_name = max(results, key=results.get)
print(f"\n最佳模型: {best_model_name} (准确率: {results[best_model_name]:.4f})")

# 使用最佳模型进行预测
if best_model_name == 'Random Forest':
    best_model = RandomForestClassifier(n_estimators=100, random_state=42)
    best_model.fit(X_train, y_train)
    y_pred_best = best_model.predict(X_test)
    feature_importance = best_model.feature_importances_
else:
    best_model = LogisticRegression(random_state=42, max_iter=1000)
    best_model.fit(X_train_scaled, y_train)
    y_pred_best = best_model.predict(X_test_scaled)
    feature_importance = abs(best_model.coef_[0])

# 9. 混淆矩阵可视化
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred_best)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['<=170cm', '>170cm'], 
            yticklabels=['<=170cm', '>170cm'])
plt.title(f'{best_model_name} 混淆矩阵')
plt.ylabel('真实标签')
plt.xlabel('预测标签')
plt.tight_layout()
plt.savefig('confusion_matrix.png')
print("混淆矩阵已保存为 confusion_matrix.png")

# 10. 特征重要性可视化
plt.figure(figsize=(12, 8))
feature_importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': feature_importance
}).sort_values('Importance', ascending=False)

plt.barh(range(len(feature_importance_df)), feature_importance_df['Importance'])
plt.yticks(range(len(feature_importance_df)), feature_importance_df['Feature'])
plt.xlabel('重要性')
plt.title(f'{best_model_name} 特征重要性')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance.png')
print("特征重要性图已保存为 feature_importance.png")

# 11. 输出特征重要性排名
print("\n特征重要性排名:")
for i, row in feature_importance_df.head(10).iterrows():
    print(f"{row['Feature']}: {row['Importance']:.4f}")

# 12. 保存模型结果
results_df = pd.DataFrame({
    'Model': list(results.keys()),
    'Accuracy': list(results.values())
})
results_df.to_csv('model_results.csv', index=False)
print("\n模型结果已保存为 model_results.csv")

# 13. 保存预测结果
predictions_df = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred_best
})
predictions_df.to_csv('predictions.csv', index=False)
print("预测结果已保存为 predictions.csv")

print("\n=== 脚本执行完成 ===")
print("生成的文件:")
print("1. confusion_matrix.png - 混淆矩阵图")
print("2. feature_importance.png - 特征重要性图")
print("3. model_results.csv - 模型结果")
print("4. predictions.csv - 预测结果")