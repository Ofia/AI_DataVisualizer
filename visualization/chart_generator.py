import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from .templates import get_template_config

class ChartGenerator:
    """Generate charts using Plotly"""
    
    def __init__(self, template_name):
        self.template = get_template_config(template_name)
        self.colors = self.template['colors']
    
    def create_bar_chart(self, data, x_column, y_column, title, description):
        """Create a bar chart"""
        try:
            df = pd.DataFrame(data)
            
            # Handle multiple y columns (comma-separated)
            if ',' in y_column:
                y_columns = [col.strip() for col in y_column.split(',')]
                
                # Create grouped bar chart
                fig = go.Figure()
                for i, col in enumerate(y_columns):
                    if col in df.columns:
                        fig.add_trace(go.Bar(
                            name=col,
                            x=df[x_column],
                            y=df[col],
                            marker_color=self.colors[i % len(self.colors)],
                            text=df[col],
                            textposition='auto',
                        ))
                
                fig.update_layout(barmode='group')
                yaxis_title = ' / '.join(y_columns)
            else:
                # Single column bar chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=df[x_column],
                        y=df[y_column],
                        marker_color=self.colors[0],
                        text=df[y_column],
                        textposition='auto',
                    )
                ])
                yaxis_title = y_column
            
            fig.update_layout(
                title=title,
                xaxis_title=x_column,
                yaxis_title=yaxis_title,
                plot_bgcolor=self.template['chart_style']['plot_bgcolor'],
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                xaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                yaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                height=400
            )
            
            return {
                'type': 'bar',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    
    def create_line_chart(self, data, x_column, y_column, title, description):
        """Create a line chart"""
        try:
            df = pd.DataFrame(data)
            
            # Handle multiple y columns (comma-separated)
            if ',' in y_column:
                y_columns = [col.strip() for col in y_column.split(',')]
                
                # Create multi-line chart
                fig = go.Figure()
                for i, col in enumerate(y_columns):
                    if col in df.columns:
                        fig.add_trace(go.Scatter(
                            name=col,
                            x=df[x_column],
                            y=df[col],
                            mode='lines+markers',
                            line=dict(color=self.colors[i % len(self.colors)], width=3),
                            marker=dict(size=8)
                        ))
                
                yaxis_title = ' / '.join(y_columns)
            else:
                # Single line chart
                fig = go.Figure(data=[
                    go.Scatter(
                        x=df[x_column],
                        y=df[y_column],
                        mode='lines+markers',
                        line=dict(color=self.colors[0], width=3),
                        marker=dict(size=8, color=self.colors[1])
                    )
                ])
                yaxis_title = y_column
            
            fig.update_layout(
                title=title,
                xaxis_title=x_column,
                yaxis_title=yaxis_title,
                plot_bgcolor=self.template['chart_style']['plot_bgcolor'],
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                xaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                yaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                height=400
            )
            
            return {
                'type': 'line',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_pie_chart(self, data, labels_column, values_column, title, description):
        """Create a pie chart"""
        try:
            df = pd.DataFrame(data)
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=df[labels_column],
                    values=df[values_column],
                    marker=dict(colors=self.colors),
                    textinfo='label+percent',
                    hoverinfo='label+value+percent'
                )
            ])
            
            fig.update_layout(
                title=title,
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                height=400
            )
            
            return {
                'type': 'pie',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_scatter_chart(self, data, x_column, y_column, title, description):
        """Create a scatter plot"""
        try:
            df = pd.DataFrame(data)
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=df[x_column],
                    y=df[y_column],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color=self.colors[0],
                        opacity=0.7,
                        line=dict(width=1, color=self.colors[1])
                    )
                )
            ])
            
            fig.update_layout(
                title=title,
                xaxis_title=x_column,
                yaxis_title=y_column,
                plot_bgcolor=self.template['chart_style']['plot_bgcolor'],
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                xaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                yaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                height=400
            )
            
            return {
                'type': 'scatter',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_heatmap(self, data, title, description):
        """Create a heatmap"""
        try:
            df = pd.DataFrame(data)
            # Select only numeric columns
            numeric_df = df.select_dtypes(include=['number'])
            
            fig = go.Figure(data=go.Heatmap(
                z=numeric_df.values,
                x=numeric_df.columns,
                y=list(range(len(numeric_df))),
                colorscale=[[0, self.colors[0]], [1, self.colors[1]]],
                hoverongaps=False
            ))
            
            fig.update_layout(
                title=title,
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                height=400
            )
            
            return {
                'type': 'heatmap',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def _error_chart(self, error_message):
        """Return an error placeholder"""
        return {
            'type': 'error',
            'html': f'<div class="chart-error">Chart generation error: {error_message}</div>',
            'description': 'Unable to generate chart'
        }
