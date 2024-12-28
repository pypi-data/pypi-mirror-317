# src/explorytics/visualizations/plots.py
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, List, Union
from ..utils.helpers import validate_dataframe

class DataVisualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = validate_dataframe(df)
        self._numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self._categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        self.default_width = 800
        self.default_height = 800

    def _set_figure_size(self, fig: go.Figure) -> go.Figure:
        """Set consistent figure size for all plots"""
        fig.update_layout(
            width=self.default_width,
            height=self.default_height,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12)
        )
        return fig

    def plot_distribution(self, column: str, 
                         bins: Optional[int] = None, 
                         kde: bool = True) -> go.Figure:
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
            
        if column in self._numeric_cols:
            if bins is None:
                bins = int(np.ceil(np.log2(len(self.df))) + 1)
            
            fig = px.histogram(self.df, x=column, 
                             nbins=bins,
                             title=f'Distribution of {column}')
            
            if kde:
                kde_vals = self._compute_kde(self.df[column])
                fig.add_trace(go.Scatter(x=kde_vals['x'], 
                                       y=kde_vals['y'],
                                       name='KDE',
                                       line={'color': 'red'}))
        else:
            value_counts = self.df[column].value_counts()
            fig = px.bar(x=value_counts.index, 
                        y=value_counts.values,
                        title=f'Distribution of {column}')
            
        fig.update_layout(
            showlegend=kde,
            xaxis_title=column,
            yaxis_title="Count"
        )
        return self._set_figure_size(fig)

    def plot_correlation_matrix(self) -> go.Figure:
        corr_matrix = self.df[self._numeric_cols].corr()
        
        fig = px.imshow(corr_matrix,
                       labels=dict(color="Correlation"),
                       title='Correlation Matrix')
        fig.update_layout(
            xaxis_title="Features",
            yaxis_title="Features"
        )
        return self._set_figure_size(fig)

    def plot_missing_values(self) -> go.Figure:
        missing = (self.df.isnull().sum() / len(self.df) * 100).sort_values(ascending=True)
        
        fig = px.bar(x=missing.values,
                    y=missing.index,
                    orientation='h',
                    title='Missing Values (%)',
                    labels={'x': 'Missing Values (%)', 'y': 'Features'})
        return self._set_figure_size(fig)

    def plot_scatter(self, x: str, y: str, 
                    color: Optional[str] = None,
                    size: Optional[str] = None) -> go.Figure:
        if x not in self._numeric_cols or y not in self._numeric_cols:
            raise ValueError("Both x and y must be numeric columns")
            
        fig = px.scatter(self.df, x=x, y=y, 
                        color=color, size=size,
                        title=f'Scatter Plot: {x} vs {y}')
        return self._set_figure_size(fig)

    def plot_boxplot(self, numeric_col: str, 
                    group_by: Optional[str] = None) -> go.Figure:
        if numeric_col not in self._numeric_cols:
            raise ValueError(f"Column '{numeric_col}' must be numeric")
            
        fig = px.box(self.df, y=numeric_col, x=group_by,
                    title=f'Box Plot: {numeric_col}')
        return self._set_figure_size(fig)

    def _compute_kde(self, data: pd.Series) -> dict:
        from scipy.stats import gaussian_kde
        
        data_cleaned = data.dropna()
        kde = gaussian_kde(data_cleaned)
        x_range = np.linspace(data_cleaned.min(), data_cleaned.max(), 100)
        y = kde.evaluate(x_range)
        hist_values, _ = np.histogram(data_cleaned, bins='auto')
        scaling_factor = max(hist_values) / max(y)
        y = y * scaling_factor
        
        return {'x': x_range, 'y': y}