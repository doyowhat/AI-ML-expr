# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# 1. 数据加载与探索
df = pd.read_csv("fitness_test_data.csv")
print("First 5 rows:\n", df.head())
print("\nDescriptive statistics:\n", df.describe())

# 2. 数据预处理
# 提取特征（排除ID和BodyType）
features = df.columns[1:-1]  
X = df[features].values

# 标准化数据（K-means对特征尺度敏感）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("\nStandardized data sample:\n", X_scaled[:2])

# 3. 确定最佳K值（肘部法则 & 轮廓系数）
inertias = []  # 存储不同K值下的簇内平方和
sil_scores = []  # 存储不同K值下的轮廓系数
K_range = range(2, 8)  # 测试K=2到7

for k in K_range:
    # 创建K-means模型，设置n_init=10确保兼容性
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)  # 记录簇内平方和
    sil_scores.append(silhouette_score(X_scaled, kmeans.labels_))  # 计算轮廓系数

# 可视化评估指标
plt.figure(figsize=(12, 5))
plt.subplot(121)
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('K value', fontsize=12)
plt.ylabel('Inertia', fontsize=12)
plt.title('Elbow Method', fontsize=14)

plt.subplot(122)
plt.plot(K_range, sil_scores, 'go-')
plt.xlabel('K value', fontsize=12)
plt.ylabel('Silhouette Score', fontsize=12)
plt.title('Silhouette Score Evaluation', fontsize=14)
plt.tight_layout()
plt.savefig('k_selection.png')
plt.show()

# 4. 选择K=3训练模型（根据业务需求与指标）
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
df['Cluster'] = clusters  # 保存聚类结果

# 5. 结果分析
# 计算轮廓系数
sil_score = silhouette_score(X_scaled, clusters)
print(f"\nSilhouette Score (K={optimal_k}): {sil_score:.3f}")

# 查看聚类中心（反标准化解释特征）
centers_scaled = kmeans.cluster_centers_
centers_original = scaler.inverse_transform(centers_scaled)
centers_df = pd.DataFrame(centers_original, columns=features)
print("\nCluster center feature values:\n", centers_df)

# 6. 可视化（使用PCA降维至2D）
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    X_pca[:, 0], X_pca[:, 1], 
    c=clusters, cmap='viridis', alpha=0.8
)
plt.scatter(
    pca.transform(centers_scaled)[:, 0], 
    pca.transform(centers_scaled)[:, 1],
    marker='X', s=200, c='red', label='Cluster Centers'
)
plt.xlabel('Principal Component 1', fontsize=12)
plt.ylabel('Principal Component 2', fontsize=12)
plt.title('K-means Clustering Results (PCA Reduced)', fontsize=14)
plt.legend(*scatter.legend_elements(), title='Clusters')
plt.grid(alpha=0.2)
plt.savefig('clusters_pca.png')
plt.show()

# 7. 保存结果
df.to_csv("clustered_fitness_data.csv", index=False)
print("\nClustering results saved to clustered_fitness_data.csv")