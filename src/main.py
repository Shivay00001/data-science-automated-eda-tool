import argparse
import json
import numpy as np
from src.eda_engine import EDAEngine

# Custom encoder for numpy types
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def main():
    parser = argparse.ArgumentParser(description="Automated EDA Tool")
    parser.add_argument("--file", required=True, help="Path to CSV dataset")
    parser.add_argument("--output", default="eda_report.json", help="Output report file")
    
    args = parser.parse_args()
    
    try:
        print(f"Analyzing {args.file}...")
        engine = EDAEngine(args.file)
        
        report = {
            "dataset": args.file,
            "shape": engine.df.shape,
            "missing_values": engine.analyze_missing_values(),
            "numerical_stats": engine.get_basic_stats(),
            "categorical_summary": engine.get_categorical_summary(),
            "outliers_detected": engine.detect_outliers_iqr(),
            "correlations": engine.get_correlations()
        }
        
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2, cls=NpEncoder)
            
        print(f"EDA Report saved to {args.output}")
        
        # summary to console
        print("\n--- Quick Summary ---")
        print(f"Rows: {report['shape'][0]}, Columns: {report['shape'][1]}")
        print(f"Missing Values: {sum(report['missing_values'].values())}")
        print(f"Outliers Detected: {sum(report['outliers_detected'].values())}")
        
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
