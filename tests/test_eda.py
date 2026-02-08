"""
Unit tests for the Automated EDA Tool.
"""
import pytest
import pandas as pd
import numpy as np
from src.eda_engine import EDAEngine


class TestEDAEngine:
    """Tests for the EDA Engine."""

    @pytest.fixture
    def sample_data(self, tmp_path):
        """Create a sample CSV file for testing."""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['x', 'y', 'x', 'z', 'x'],
            'C': [1.1, 2.2, np.nan, 4.4, 5.5],
            'D': [10, 100, 10, 10, 10]  # outlier at 100
        })
        file_path = tmp_path / "test_data.csv"
        df.to_csv(file_path, index=False)
        return str(file_path)

    def test_initialization(self, sample_data):
        """Test engine initialization."""
        engine = EDAEngine(sample_data)
        assert isinstance(engine.df, pd.DataFrame)
        assert len(engine.df) == 5

    def test_basic_stats(self, sample_data):
        """Test descriptive statistics generation."""
        engine = EDAEngine(sample_data)
        stats = engine.get_basic_stats()
        
        assert 'A' in stats
        assert 'C' in stats
        assert 'D' in stats
        # 'B' is categorical, so describe() behavior depends on pandas version/include arg
        # By default describe() on mixed dataframe only handles numerics
        
        assert stats['A']['mean'] == 3.0
        assert stats['A']['max'] == 5.0

    def test_missing_values(self, sample_data):
        """Test missing value detection."""
        engine = EDAEngine(sample_data)
        missing = engine.analyze_missing_values()
        
        assert 'C' in missing
        assert missing['C'] == 1
        assert 'A' not in missing

    def test_categorical_summary(self, sample_data):
        """Test categorical data summary."""
        engine = EDAEngine(sample_data)
        summary = engine.get_categorical_summary()
        
        assert 'B' in summary
        assert summary['B']['unique_count'] == 3
        # 'x' appears 3 times
        assert summary['B']['top_freq']['x'] == 3

    def test_correlations(self, sample_data):
        """Test correlation matrix calculation."""
        engine = EDAEngine(sample_data)
        corr = engine.get_correlations()
        
        assert 'A' in corr
        assert 'C' in corr
        assert corr['A']['A'] == 1.0

    def test_outlier_detection(self, sample_data):
        """Test outlier detection using IQR."""
        engine = EDAEngine(sample_data)
        outliers = engine.detect_outliers_iqr()
        
        # Column D has one outlier (100) compared to others (10)
        assert 'D' in outliers
        assert outliers['D'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
