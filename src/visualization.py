"""
Visualization Module for Automated EDA.

Provides functions to generate standard EDA plots using matplotlib and seaborn.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional
import io
import base64


class Visualizer:
    """
    Generates visualizations for Exploratory Data Analysis.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a pandas DataFrame.
        """
        self.df = df
        # Set standardized style
        plt.style.use('ggplot')
        sns.set_theme(style="whitegrid")

    def plot_histograms(self, columns: Optional[List[str]] = None, figsize=(10, 6)):
        """
        Plot histograms for numerical columns.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        num_cols = len(columns)
        if num_cols == 0:
            return None
            
        fig, axes = plt.subplots(num_cols, 1, figsize=(figsize[0], figsize[1] * num_cols))
        if num_cols == 1:
            axes = [axes]
            
        for ax, col in zip(axes, columns):
            sns.histplot(self.df[col], kde=True, ax=ax)
            ax.set_title(f"Distribution of {col}")
            
        plt.tight_layout()
        return fig

    def plot_correlation_heatmap(self, figsize=(10, 8)):
        """
        Plot correlation heatmap for numerical columns.
        """
        corr = self.df.select_dtypes(include=[np.number]).corr()
        if corr.empty:
            return None
            
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
        plt.title("Correlation Matrix")
        plt.tight_layout()
        return fig

    def plot_categorical_counts(self, columns: Optional[List[str]] = None, figsize=(10, 6)):
        """
        Plot bar charts for categorical columns.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
            
        num_cols = len(columns)
        if num_cols == 0:
            return None
            
        fig, axes = plt.subplots(num_cols, 1, figsize=(figsize[0], figsize[1] * num_cols))
        if num_cols == 1:
            axes = [axes]
            
        for ax, col in zip(axes, columns):
            # Limit to top 20 categories to avoid clutter
            top_cats = self.df[col].value_counts().head(20).index
            data = self.df[self.df[col].isin(top_cats)]
            
            sns.countplot(y=col, data=data, order=top_cats, ax=ax)
            ax.set_title(f"Count of {col} (Top 20)")
            
        plt.tight_layout()
        return fig

    def plot_pairplot(self, columns: Optional[List[str]] = None, hue: Optional[str] = None):
        """
        Generate pairplot for numerical columns.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
            
        if hue and hue in self.df.columns:
            # Drop rows where hue is NaN for plotting
            data = self.df.dropna(subset=[hue])
        else:
            data = self.df
            
        if len(columns) < 2:
            return None
            
        # Limit columns to prevent huge plots
        if len(columns) > 5:
            columns = columns[:5]
            
        fig = sns.pairplot(data[columns + ([hue] if hue else [])], hue=hue)
        return fig

    @staticmethod
    def fig_to_base64(fig) -> str:
        """
        Convert matplotlib figure to base64 string for HTML embedding.
        """
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return img_str
