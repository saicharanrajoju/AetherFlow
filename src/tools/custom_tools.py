from crewai_tools import tool
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict
import json

@tool("Schema Checker")
def schema_checker(file_path: str) -> str:
    """Validate CSV schema and data types"""
    try:
        df = pd.read_csv(file_path)
        
        schema_info = {
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "row_count": len(df),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": int(df.duplicated().sum())
        }
        
        return json.dumps(schema_info, indent=2)
    except Exception as e:
        return f"Schema check failed: {str(e)}"

@tool("Anomaly Detector")
def anomaly_detector(file_path: str) -> str:
    """Detect statistical anomalies using Z-score"""
    try:
        df = pd.read_csv(file_path)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        anomalies = {}
        for col in numeric_cols:
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            outliers = df[z_scores > 3][col].tolist()
            if outliers:
                anomalies[col] = {
                    "count": len(outliers),
                    "sample_values": outliers[:5]
                }
        
        return json.dumps(anomalies, indent=2) if anomalies else "No anomalies detected"
    except Exception as e:
        return f"Anomaly detection failed: {str(e)}"

@tool("Stats Calculator")
def stats_calculator(file_path: str) -> str:
    """Calculate statistical summary"""
    try:
        df = pd.read_csv(file_path)
        return df.describe().to_json()
    except Exception as e:
        return f"Stats calculation failed: {str(e)}"

@tool("Pandas Tool")
def pandas_tool(file_path: str, operation: str) -> str:
    """Execute pandas operations: dropna, fillna_mean, remove_duplicates"""
    try:
        df = pd.read_csv(file_path)
        
        if operation == "dropna":
            df = df.dropna()
            result = f"Removed rows with missing values. New shape: {df.shape}"
        elif operation == "fillna_mean":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            result = f"Filled missing numeric values with mean"
        elif operation == "remove_duplicates":
            original_len = len(df)
            df = df.drop_duplicates()
            result = f"Removed {original_len - len(df)} duplicate rows"
        else:
            result = f"Unknown operation: {operation}"
        
        # Save cleaned file
        output_path = file_path.replace('.csv', '_cleaned.csv')
        df.to_csv(output_path, index=False)
        
        return f"{result}. Saved to {output_path}"
    except Exception as e:
        return f"Pandas operation failed: {str(e)}"

@tool("Regex Cleaner")
def regex_cleaner(file_path: str, column: str, pattern: str, replacement: str) -> str:
    """Clean text columns using regex"""
    try:
        df = pd.read_csv(file_path)
        df[column] = df[column].astype(str).str.replace(pattern, replacement, regex=True)
        
        output_path = file_path.replace('.csv', '_cleaned.csv')
        df.to_csv(output_path, index=False)
        
        return f"Cleaned column '{column}' using pattern '{pattern}'. Saved to {output_path}"
    except Exception as e:
        return f"Regex cleaning failed: {str(e)}"
