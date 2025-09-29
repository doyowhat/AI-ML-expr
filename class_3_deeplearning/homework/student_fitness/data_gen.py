import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Define profiles for three body types
type_profiles = {
    "Endurance": {
        "height": (175, 5),        # Mean height (cm), std dev
        "weight": (65, 5),         # Mean weight (kg), std dev
        "lung_capacity": (4800, 300),  # Lung capacity (ml)
        "run_50m": (8.5, 0.5),     # 50m sprint (seconds)
        "long_jump": (220, 15),    # Standing long jump (cm)
        "run_1000m": (220, 15),    # 1000m run (seconds)
        "run_3000m": (780, 45),    # 3000m run (seconds)
        "sit_reach": (15, 3)       # Sit-and-reach flexibility (cm)
    },
    "Power": {
        "height": (178, 4),
        "weight": (75, 6),
        "lung_capacity": (4500, 400),
        "run_50m": (7.2, 0.4),
        "long_jump": (260, 12),
        "run_1000m": (260, 20),
        "run_3000m": (900, 60),
        "sit_reach": (10, 4)
    },
    "Flexibility": {
        "height": (172, 5),
        "weight": (60, 5),
        "lung_capacity": (4200, 300),
        "run_50m": (9.0, 0.6),
        "long_jump": (200, 15),
        "run_1000m": (280, 25),
        "run_3000m": (960, 50),
        "sit_reach": (25, 4)
    }
}

# Generate 30 records (10 per body type)
data = []
for i in range(30):
    body_type = "Endurance" if i < 10 else ("Power" if i < 20 else "Flexibility")
    profile = type_profiles[body_type]
    
    record = {
        "ID": i + 1,
        "Height_cm": round(np.random.normal(profile["height"][0], profile["height"][1]), 1),
        "Weight_kg": round(np.random.normal(profile["weight"][0], profile["weight"][1]), 1),
        "LungCapacity_ml": int(np.random.normal(profile["lung_capacity"][0], profile["lung_capacity"][1])),
        "Run50m_sec": round(np.random.normal(profile["run_50m"][0], profile["run_50m"][1]), 1),
        "LongJump_cm": int(np.random.normal(profile["long_jump"][0], profile["long_jump"][1])),
        "Run1000m_sec": int(np.random.normal(profile["run_1000m"][0], profile["run_1000m"][1])),
        "Run3000m_sec": int(np.random.normal(profile["run_3000m"][0], profile["run_3000m"][1])),
        "SitReach_cm": round(np.random.normal(profile["sit_reach"][0], profile["sit_reach"][1]), 1),
        "BodyType": body_type
    }
    data.append(record)

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("fitness_test_data.csv", index=False, encoding="utf-8")

# Output confirmation
print("Generated 30 fitness test records:")
print(f"- Body Type Distribution:")
print(f"  Endurance: {sum(df['BodyType'] == 'Endurance')} records")
print(f"  Power: {sum(df['BodyType'] == 'Power')} records")
print(f"  Flexibility: {sum(df['BodyType'] == 'Flexibility')} records")
print("\nSample Data (First 3 records):")
print(df.head(3).to_string(index=False))
print("\nFile saved: fitness_test_data.csv (UTF-8 encoded)")