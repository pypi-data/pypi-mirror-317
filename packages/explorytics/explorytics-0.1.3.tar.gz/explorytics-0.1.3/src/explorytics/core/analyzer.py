# src/explorytics/core/analyzer.py
from typing import Optional, Dict, List, Union
import pandas as pd
import numpy as np
from dataclasses import dataclass
from ..visualizations.plots import DataVisualizer
from ..utils.helpers import validate_dataframe

@dataclass
class AnalysisResult:
    """Container for analysis results"""
    basic_stats: Dict
    missing_values: Dict
    correlations: Optional[pd.DataFrame] = None
    outliers: Optional[Dict] = None

class DataAnalyzer:
    """Main class for performing exploratory data analysis"""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with a pandas DataFrame"""
        self.df = validate_dataframe(df)
        self.visualizer = DataVisualizer(self.df)
        self._analysis_results = None

    def analyze(self, include_correlations: bool = True, detect_outliers: bool = True) -> AnalysisResult:
        """Perform comprehensive analysis of the dataset"""
        results = {}
        
        # Basic statistics
        results['basic_stats'] = self._compute_basic_stats()
        
        # Missing values analysis
        results['missing_values'] = self._analyze_missing_values()
        
        # Correlation analysis
        if include_correlations:
            results['correlations'] = self._compute_correlations()
            
        # Outlier detection
        if detect_outliers:
            results['outliers'] = self._detect_outliers()
            
        self._analysis_results = AnalysisResult(**results)
        return self._analysis_results

    def _compute_basic_stats(self) -> Dict:
        """Compute basic statistics for numerical columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        stats = {
            'numeric_summary': self.df[numeric_cols].describe().to_dict(),
            'dtypes': self.df.dtypes.value_counts().to_dict(),
            'shape': self.df.shape
        }
        return stats

    def _analyze_missing_values(self) -> Dict:
        """Analyze missing values in the dataset"""
        missing = {
            'total_missing': self.df.isnull().sum().to_dict(),
            'percent_missing': (self.df.isnull().sum() / len(self.df) * 100).to_dict()
        }
        return missing

    def _compute_correlations(self) -> pd.DataFrame:
        """Compute correlation matrix for numerical columns"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        return numeric_df.corr()

    def _detect_outliers(self, method: str = 'iqr') -> Dict:
        """Detect outliers in numerical columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_cols:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers[col] = {
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound,
                    'count': len(self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)])
                }
        return outliers