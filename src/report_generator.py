"""
Report Generator Module.

Generates comprehensive HTML reports from EDA results and visualizations.
"""
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from .eda_engine import EDAEngine
from .visualization import Visualizer


class ReportGenerator:
    """
    Generates HTML reports for Automated EDA.
    """
    
    def __init__(self, df: pd.DataFrame, title: str = "Automated EDA Report"):
        self.df = df
        self.title = title
        self.engine = EDAEngine(df)
        self.viz = Visualizer(df)
        
    def generate_report(self) -> str:
        """
        Generate full HTML report.
        """
        # Gather data
        stats = self.engine.get_basic_stats()
        missing = self.engine.get_missing_values()
        categorical = self.engine.get_categorical_summary()
        outliers = self.engine.get_outliers()
        
        # Generate Plots
        hist_fig = self.viz.plot_histograms()
        corr_fig = self.viz.plot_correlation_heatmap()
        cat_fig = self.viz.plot_categorical_counts()
        
        hist_img = self.viz.fig_to_base64(hist_fig) if hist_fig else ""
        corr_img = self.viz.fig_to_base64(corr_fig) if corr_fig else ""
        cat_img = self.viz.fig_to_base64(cat_fig) if cat_fig else ""
        
        # Build HTML
        html = [
            f"""<!DOCTYPE html>
            <html>
            <head>
                <title>{self.title}</title>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max_width: 1200px; margin: 0 auto; padding: 20px; }}
                    h1, h2, h3 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                    .section {{ margin-bottom: 40px; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                    .stats-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                    .stats-table th, .stats-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                    .stats-table th {{ background-color: #f8f9fa; font-weight: 600; }}
                    img {{ max_width: 100%; height: auto; border-radius: 4px; margin: 15px 0; }}
                    .metric-card {{ background: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 10px; }}
                    .timestamp {{ color: #666; font-size: 0.9em; margin-bottom: 30px; }}
                </style>
            </head>
            <body>
                <h1>{self.title}</h1>
                <p class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <div class="section">
                    <h2>Dataset Overview</h2>
                    <div class="metric-card">
                        <strong>Rows:</strong> {len(self.df)} | 
                        <strong>Columns:</strong> {len(self.df.columns)} | 
                        <strong>Memory Usage:</strong> {self.df.memory_usage(deep=True).sum() / 1024:.2f} KB
                    </div>
                </div>
            """
        ]
        
        # Descriptive Statistics
        html.append("""
            <div class="section">
                <h2>Descriptive Statistics</h2>
                <div style="overflow-x: auto;">
        """)
        html.append(pd.DataFrame(stats).to_html(classes="stats-table", float_format=lambda x: f"{x:.2f}"))
        html.append("</div></div>")
        
        # Missing Values
        if missing:
            html.append("""
                <div class="section">
                    <h2>Missing Values Analysis</h2>
                    <table class="stats-table">
                        <thead><tr><th>Column</th><th>Missing Count</th><th>Percentage</th></tr></thead>
                        <tbody>
            """)
            for col, count in missing.items():
                pct = (count / len(self.df)) * 100
                html.append(f"<tr><td>{col}</td><td>{count}</td><td>{pct:.1f}%</td></tr>")
            html.append("</tbody></table></div>")
            
        # Outliers
        if outliers:
            html.append("""
                <div class="section">
                    <h2>Outlier Detection (IQR Method)</h2>
                    <table class="stats-table">
                        <thead><tr><th>Column</th><th>Outlier Count</th></tr></thead>
                        <tbody>
            """)
            for col, count in outliers.items():
                html.append(f"<tr><td>{col}</td><td>{count}</td></tr>")
            html.append("</tbody></table></div>")
            
        # Visualizations
        html.append('<div class="section"><h2>Visualizations</h2>')
        
        if corr_img:
            html.append(f'<h3>Correlation Matrix</h3><img src="data:image/png;base64,{corr_img}" alt="Correlation Matrix">')
            
        if hist_img:
            html.append(f'<h3>Numerical Distributions</h3><img src="data:image/png;base64,{hist_img}" alt="Histograms">')
            
        if cat_img:
            html.append(f'<h3>Categorical Distributions</h3><img src="data:image/png;base64,{cat_img}" alt="Categorical Counts">')
            
        html.append("</div></body></html>")
        
        return "\n".join(html)

    def save_report(self, filepath: str):
        """Save report to file."""
        report_html = self.generate_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_html)
