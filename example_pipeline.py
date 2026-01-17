from src.crew.aetherflow_crew import AetherFlowCrew
import pandas as pd
import os

# Create sample data
os.makedirs('./data', exist_ok=True)
df = pd.DataFrame({
    'id': range(1, 101),
    'name': [f'Product_{i}' for i in range(1, 101)],
    'price': [10.5 + i * 0.5 for i in range(100)],
    'category': ['Electronics', 'Clothing', 'Food'] * 33 + ['Electronics']
})
df.to_csv('./data/sample_sales.csv', index=False)

# Run pipeline
crew = AetherFlowCrew()
result = crew.run({
    'dataset_name': 'sample_sales',
    'source_path': './data/sample_sales.csv',
    'target_format': 'csv'
})

print("\n=== PIPELINE RESULT ===")
print(result)
