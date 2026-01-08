from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def analyze_data(self, extracted_data, template_name='professional'):
        """
        Analyze the extracted data and return insights, visualization recommendations
        
        Args:
            extracted_data: Dictionary containing the extracted data and metadata
            
        Returns:
            Dictionary with analysis results including:
            - insights: List of key insights about the data
            - chart_recommendations: List of recommended chart types
            - descriptions: Descriptions for each visualization
            - color_scheme: Recommended colors for the template
        """
        pass
    
    @abstractmethod
    def is_available(self):
        """Check if the provider is properly configured and available"""
        pass
