# src/pyeda/visualizations/plots.py
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, List, Union
from ..utils.helpers import validate_dataframe

class DataVisualizer:
    """Class for creating interactive visualizations"""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with a pandas DataFrame"""
        self.df = validate_dataframe(df)
        self._numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self._categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        
        # Define color scheme
        self.colors = {
            'primary': '#636EFA',    # Main color for plots
            'secondary': '#EF553B',  # Secondary color (e.g., for KDE curves)
            'background': '#F9F9F9', # Plot background
            'grid': '#E5E5E5',       # Grid lines
            'text': '#2F2F2F'        # Text color
        }
        
        # Define common layout settings
        self.layout_template = {
            'plot_bgcolor': self.colors['background'],
            'paper_bgcolor': 'white',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': self.colors['text']
            },
            'title': {
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            'xaxis': {
                'gridcolor': self.colors['grid'],
                'zeroline': False
            },
            'yaxis': {
                'gridcolor': self.colors['grid'],
                'zeroline': False
            }
        }

    def _apply_common_layout(self, fig: go.Figure, title: str) -> go.Figure:
        """Apply common layout settings to figure"""
        
        layout_settings = {**self.layout_template, 'title': title}
        
        fig.update_layout(
            **layout_settings,
            margin=dict(t=50, l=50, r=20, b=50),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#E5E5E5',
                borderwidth=1
            )
        )
        
        return fig


    def plot_distribution(self, column: str, 
                         bins: Optional[int] = None, 
                         kde: bool = True) -> go.Figure:
        """Create distribution plot for a numeric column"""
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
            
        if column in self._numeric_cols:
            # Calculate number of bins using Sturges' rule if not specified
            if bins is None:
                bins = int(np.ceil(np.log2(len(self.df))) + 1)
            
            fig = go.Figure()
            
            # Add histogram
            fig.add_trace(go.Histogram(
                x=self.df[column],
                nbinsx=bins,
                name='Distribution',
                marker_color=self.colors['primary'],
                opacity=0.7
            ))
            
            if kde:
                # Add KDE plot
                kde_vals = self._compute_kde(self.df[column])
                fig.add_trace(go.Scatter(
                    x=kde_vals['x'],
                    y=kde_vals['y'],
                    name='Density',
                    line={'color': self.colors['secondary'], 'width': 2},
                    mode='lines'
                ))

            title = f'Distribution of {column}'
            fig = self._apply_common_layout(fig, title)
            fig.update_layout(
                xaxis_title=column,
                yaxis_title="Count",
                bargap=0.1
            )
            
        else:
            # For categorical columns
            value_counts = self.df[column].value_counts()
            fig = go.Figure([go.Bar(
                x=value_counts.index,
                y=value_counts.values,
                marker_color=self.colors['primary'],
                name='Count'
            )])
            
            title = f'Distribution of {column}'
            fig = self._apply_common_layout(fig, title)
            fig.update_layout(
                xaxis_title=column,
                yaxis_title="Count",
                bargap=0.2
            )
            
        return fig

    def plot_correlation_matrix(self) -> go.Figure:
        """Create correlation matrix heatmap"""
        corr_matrix = self.df[self._numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            zmin=-1,
            zmax=1,
            colorscale='RdBu',
            colorbar=dict(title='Correlation')
        ))
        
        title = 'Correlation Matrix'
        fig = self._apply_common_layout(fig, title)
        fig.update_layout(
            xaxis={'side': 'bottom'},
            yaxis={'autorange': 'reversed'}
        )
        
        return fig

    def plot_missing_values(self) -> go.Figure:
        """Create missing values visualization"""
        missing = (self.df.isnull().sum() / len(self.df) * 100).sort_values(ascending=True)
        
        fig = go.Figure([go.Bar(
            x=missing.values,
            y=missing.index,
            orientation='h',
            marker_color=self.colors['primary'],
            name='Missing Values'
        )])
        
        title = 'Missing Values Analysis'
        fig = self._apply_common_layout(fig, title)
        fig.update_layout(
            xaxis_title='Missing Values (%)',
            yaxis_title='Features',
            showlegend=False,
            yaxis={'automargin': True}
        )
        
        return fig

    def plot_scatter(self, x: str, y: str, 
                    color: Optional[str] = None,
                    size: Optional[str] = None) -> go.Figure:
        """Create scatter plot between two numerical variables"""
        if x not in self._numeric_cols or y not in self._numeric_cols:
            raise ValueError("Both x and y must be numeric columns")
            
        fig = px.scatter(
            self.df, 
            x=x, 
            y=y,
            color=color,
            size=size,
            title=f'Scatter Plot: {x} vs {y}',
            template='simple_white'
        )
        
        fig = self._apply_common_layout(fig, f'Relationship between {x} and {y}')
        fig.update_traces(
            marker=dict(
                line=dict(width=1, color='white')
            )
        )
        
        return fig

    def plot_boxplot(self, numeric_col: str, 
                    group_by: Optional[str] = None) -> go.Figure:
        """Create box plot for numerical variable"""
        if numeric_col not in self._numeric_cols:
            raise ValueError(f"Column '{numeric_col}' must be numeric")
            
        fig = go.Figure()
        
        if group_by:
            for group in self.df[group_by].unique():
                fig.add_trace(go.Box(
                    y=self.df[self.df[group_by] == group][numeric_col],
                    name=str(group),
                    marker_color=self.colors['primary']
                ))
        else:
            fig.add_trace(go.Box(
                y=self.df[numeric_col],
                name=numeric_col,
                marker_color=self.colors['primary']
            ))
        
        title = f'Distribution of {numeric_col}'
        if group_by:
            title += f' by {group_by}'
            
        fig = self._apply_common_layout(fig, title)
        fig.update_layout(
            yaxis_title=numeric_col,
            showlegend=bool(group_by)
        )
        
        return fig

    def _compute_kde(self, data: pd.Series) -> dict:
        """Compute Kernel Density Estimation"""
        from scipy.stats import gaussian_kde
        
        data_cleaned = data.dropna()
        kde = gaussian_kde(data_cleaned)
        
        # Generate points for the KDE curve
        x_range = np.linspace(data_cleaned.min(), data_cleaned.max(), 200)
        y = kde.evaluate(x_range)
        
        # Scale the KDE curve to match histogram height
        hist_values, _ = np.histogram(data_cleaned, bins='auto')
        scaling_factor = max(hist_values) / max(y)
        y = y * scaling_factor
        
        return {'x': x_range, 'y': y}