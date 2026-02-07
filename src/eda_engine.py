import pandas as pd
import numpy as np

class EDAEngine:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)

    def get_basic_stats(self) -> dict:
        """Returns descriptive statistics."""
        desc = self.df.describe().to_dict()
        return desc

    def analyze_missing_values(self) -> dict:
        """Returns missing value counts."""
        missing = self.df.isnull().sum()
        return missing[missing > 0].to_dict()

    def get_categorical_summary(self) -> dict:
        """Returns unique counts for categorical columns."""
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns
        summary = {}
        for col in cat_cols:
            summary[col] = {
                "unique_count": self.df[col].nunique(),
                "top_freq": self.df[col].value_counts().head(3).to_dict()
            }
        return summary

    def get_correlations(self) -> dict:
        """Computes correlation matrix for numerical columns."""
        nums = self.df.select_dtypes(include=[np.number])
        if nums.empty:
            return {}
        return nums.corr().to_dict()

    def detect_outliers_iqr(self) -> dict:
        """Detects outliers using IQR method for numerical columns."""
        nums = self.df.select_dtypes(include=[np.number])
        outliers = {}
        
        for col in nums.columns:
            Q1 = nums[col].quantile(0.25)
            Q3 = nums[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            count = ((nums[col] < lower_bound) | (nums[col] > upper_bound)).sum()
            if count > 0:
                outliers[col] = int(count)
                
        return outliers
