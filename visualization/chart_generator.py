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
    
    def create_bubble_chart(self, data, x_column, y_column, size_column, title, description, color_column=None):
        """Create a bubble chart with size dimension"""
        try:
            df = pd.DataFrame(data)
            
            # Prepare scatter data with size
            scatter_data = go.Scatter(
                x=df[x_column],
                y=df[y_column],
                mode='markers',
                marker=dict(
                    size=df[size_column],
                    sizemode='diameter',
                    sizeref=2.*max(df[size_column])/(40.**2),
                    sizemin=4,
                    color=df[color_column] if color_column and color_column in df.columns else self.colors[0],
                    colorscale='Viridis' if color_column and color_column in df.columns else None,
                    showscale=bool(color_column and color_column in df.columns),
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                text=df[size_column].astype(str),
                hovertemplate=f'<b>{x_column}</b>: %{{x}}<br><b>{y_column}</b>: %{{y}}<br><b>{size_column}</b>: %{{text}}<extra></extra>'
            )
            
            fig = go.Figure(data=[scatter_data])
            
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
                'type': 'bubble',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_histogram(self, data, x_column, title, description):
        """Create a histogram for distribution analysis"""
        try:
            df = pd.DataFrame(data)
            
            fig = go.Figure(data=[
                go.Histogram(
                    x=df[x_column],
                    marker_color=self.colors[0],
                    opacity=0.8,
                    nbinsx=20
                )
            ])
            
            fig.update_layout(
                title=title,
                xaxis_title=x_column,
                yaxis_title='Frequency',
                plot_bgcolor=self.template['chart_style']['plot_bgcolor'],
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                xaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                yaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                height=400
            )
            
            return {
                'type': 'histogram',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_box_plot(self, data, y_column, title, description, x_column=None):
        """Create a box plot for statistical distribution"""
        try:
            df = pd.DataFrame(data)
            
            if x_column and x_column in df.columns:
                # Grouped box plot
                fig = go.Figure()
                for category in df[x_column].unique():
                    category_data = df[df[x_column] == category][y_column]
                    fig.add_trace(go.Box(
                        y=category_data,
                        name=str(category),
                        marker_color=self.colors[len(fig.data) % len(self.colors)]
                    ))
            else:
                # Single box plot
                fig = go.Figure(data=[
                    go.Box(
                        y=df[y_column],
                        marker_color=self.colors[0],
                        name=y_column
                    )
                ])
            
            fig.update_layout(
                title=title,
                yaxis_title=y_column,
                xaxis_title=x_column if x_column else '',
                plot_bgcolor=self.template['chart_style']['plot_bgcolor'],
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                xaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                yaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                height=400
            )
            
            return {
                'type': 'box',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_sunburst(self, data, labels_column, values_column, title, description, parents_column=None):
        """Create a sunburst chart for hierarchical data"""
        try:
            df = pd.DataFrame(data)
            
            # If no parents column, create a simple sunburst
            if not parents_column or parents_column not in df.columns:
                # Add a root parent for all items
                labels = ['Total'] + df[labels_column].tolist()
                parents = [''] + ['Total'] * len(df)
                values = [df[values_column].sum()] + df[values_column].tolist()
            else:
                labels = df[labels_column].tolist()
                parents = df[parents_column].tolist()
                values = df[values_column].tolist()
            
            fig = go.Figure(go.Sunburst(
                labels=labels,
                parents=parents,
                values=values,
                marker=dict(colors=self.colors),
                hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
            ))
            
            fig.update_layout(
                title=title,
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                height=400
            )
            
            return {
                'type': 'sunburst',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_funnel(self, data, x_column, y_column, title, description):
        """Create a funnel chart for conversion/pipeline visualization"""
        try:
            df = pd.DataFrame(data)
            
            fig = go.Figure(go.Funnel(
                y=df[x_column],
                x=df[y_column],
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(color=self.colors),
                connector=dict(line=dict(color="royalblue", width=2))
            ))
            
            fig.update_layout(
                title=title,
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                height=400
            )
            
            return {
                'type': 'funnel',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_waterfall(self, data, x_column, y_column, title, description):
        """Create a waterfall chart for cumulative effect visualization"""
        try:
            df = pd.DataFrame(data)
            
            fig = go.Figure(go.Waterfall(
                name="",
                orientation="v",
                x=df[x_column],
                y=df[y_column],
                connector=dict(line=dict(color="rgb(63, 63, 63)")),
                increasing=dict(marker=dict(color=self.colors[0] if len(self.colors) > 0 else "green")),
                decreasing=dict(marker=dict(color=self.colors[1] if len(self.colors) > 1 else "red")),
                totals=dict(marker=dict(color=self.colors[2] if len(self.colors) > 2 else "blue"))
            ))
            
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
                'type': 'waterfall',
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(str(e))
    
    def create_chart_from_json(self, chart_json):
        """
        Create a chart directly from Plotly JSON specification
        
        Args:
            chart_json: Dictionary containing 'figure' key with 'data' and 'layout'
        """
        try:
            figure_data = chart_json.get('figure', {})
            data = figure_data.get('data', [])
            layout = figure_data.get('layout', {})
            
            # Create figure
            fig = go.Figure(data=data, layout=layout)
            
            # Apply template styling overrides to ensure consistency
            # But respect specific layout choices from AI
            fig.update_layout(
                plot_bgcolor=self.template['chart_style']['plot_bgcolor'],
                paper_bgcolor=self.template['chart_style']['paper_bgcolor'],
                font=dict(family=self.template['font_family'], color=self.template['text_color']),
                xaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                yaxis=dict(gridcolor=self.template['chart_style']['gridcolor']),
                height=450  # Slightly taller for complex charts
            )
            
            title = chart_json.get('title', 'Chart')
            description = chart_json.get('description', '')
            chart_type = chart_json.get('chart_type', 'custom')
            
            return {
                'type': chart_type,
                'html': fig.to_html(full_html=False, include_plotlyjs=False, div_id=f"chart_{hash(title)}"),
                'description': description
            }
        except Exception as e:
            return self._error_chart(f"Error rendering AI chart: {str(e)}")

    def _error_chart(self, error_message):
        """Return an error placeholder"""
        return {
            'type': 'error',
            'html': f'<div class="chart-error">Chart generation error: {error_message}</div>',
            'description': 'Unable to generate chart'
        }
