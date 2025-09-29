import numpy as np
import pandas as pd
import random

# 设置随机种子确保可复现结果
np.random.seed(42)
random.seed(42)

def generate_height_data(n_samples=30):
    """
    生成身高预测数据集
    包含遗传因素、营养因素和锻炼习惯
    """
    data = []
    
    for i in range(n_samples):
        # 1. 遗传因素 (单位：cm)
        # 祖辈身高在合理范围内生成
        grandfather_height = np.random.normal(170, 7)
        grandmother_height = np.random.normal(158, 6)
        maternal_grandfather = np.random.normal(168, 7)
        maternal_grandmother = np.random.normal(156, 6)
        
        # 父母身高基于祖辈身高计算（考虑遗传因素）
        father_height = (grandfather_height + grandmother_height) / 2 + np.random.normal(5, 3)
        mother_height = (maternal_grandfather + maternal_grandmother) / 2 + np.random.normal(4, 2)
        
        # 2. 营养因素 (1-5分，1=很少，5=很多)
        nutrition_1_3 = random.randint(1, 5)
        nutrition_4_6 = random.randint(1, 5)
        nutrition_7_10 = random.randint(1, 5)
        nutrition_11_14 = random.randint(1, 5)
        nutrition_15_18 = random.randint(1, 5)
        nutrition_total = sum([nutrition_1_3, nutrition_4_6, nutrition_7_10, nutrition_11_14, nutrition_15_18])
        
        # 3. 锻炼因素 (1-5分，1=很少，5=很多)
        exercise_1_3 = random.randint(1, 5)
        exercise_4_6 = random.randint(1, 5)
        exercise_7_10 = random.randint(1, 5)
        exercise_11_14 = random.randint(1, 5)
        exercise_15_18 = random.randint(1, 5)
        exercise_total = sum([exercise_1_3, exercise_4_6, exercise_7_10, exercise_11_14, exercise_15_18])
        
        # 4. 预测身高计算（基于遗传公式和环境因素）
        # 遗传基础（使用改进的中国公式）[7,8](@ref)
        genetic_base = (father_height * 1.11 + mother_height) / 2 if random.random() > 0.5 else (father_height + mother_height * 0.95) / 2
        
        # 环境因素影响（营养和锻炼占总影响的25%）[8](@ref)
        environment_factor = (nutrition_total / 25 * 0.15 + exercise_total / 25 * 0.10) * 15
        
        # 最终预测身高（加入合理随机波动）
        predicted_height = genetic_base + environment_factor + np.random.normal(0, 2)
        predicted_height = max(150, min(195, predicted_height))  # 限制在合理身高范围
        
        # 身高类别（高于170cm为1，否则为0）
        height_category = 1 if predicted_height > 170 else 0
        
        # 添加数据记录
        record = {
            'ID': i + 1,
            'Father_Height': round(father_height, 1),
            'Grandfather_Height': round(grandfather_height, 1),
            'Grandmother_Height': round(grandmother_height, 1),
            'Mother_Height': round(mother_height, 1),
            'Maternal_Grandfather_Height': round(maternal_grandfather, 1),
            'Maternal_Grandmother_Height': round(maternal_grandmother, 1),
            'Nutrition_1_3': nutrition_1_3,
            'Nutrition_4_6': nutrition_4_6,
            'Nutrition_7_10': nutrition_7_10,
            'Nutrition_11_14': nutrition_11_14,
            'Nutrition_15_18': nutrition_15_18,
            'Exercise_1_3': exercise_1_3,
            'Exercise_4_6': exercise_4_6,
            'Exercise_7_10': exercise_7_10,
            'Exercise_11_14': exercise_11_14,
            'Exercise_15_18': exercise_15_18,
            'Predicted_Height': round(predicted_height, 1),
            'Height_Category': height_category
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

# 生成数据
df = generate_height_data(30)

# 保存数据到CSV文件
df.to_csv('height_prediction_data.csv', index=False)

# 显示数据统计信息
print("数据统计信息：")
print(f"总样本数: {len(df)}")
print(f"身高高于170cm的样本数: {sum(df['Height_Category'])}")
print(f"身高低于170cm的样本数: {len(df) - sum(df['Height_Category'])}")

# 显示前5条数据
print("\n生成的数据样本：")
print(df.head().to_string(index=False))