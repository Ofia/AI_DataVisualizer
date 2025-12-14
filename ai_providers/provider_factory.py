from .anthropic_provider import AnthropicProvider
from .huggingface_provider import HuggingFaceProvider
from config import config

class ProviderFactory:
    """Factory class to get the appropriate AI provider"""
    
    @staticmethod
    def get_provider(provider_name=None):
        """
        Get an AI provider instance
        
        Args:
            provider_name: Name of the provider ('anthropic', 'openai', 'gemini', 'llama')
                          If None, uses default from config
        
        Returns:
            Instance of the requested provider
        
        Raises:
            ValueError: If provider is not available or not supported
        """
        if provider_name is None:
            provider_name = config.DEFAULT_AI_PROVIDER
        
        provider_name = provider_name.lower()
        
        # Check if provider is enabled
        if provider_name not in config.AI_PROVIDERS:
            raise ValueError(f"Unknown AI provider: {provider_name}")
        
        if not config.AI_PROVIDERS[provider_name]['enabled']:
            raise ValueError(f"AI provider '{provider_name}' is not currently enabled")
        
        # Return the appropriate provider
        if provider_name == 'anthropic':
            provider = AnthropicProvider()
            if not provider.is_available():
                raise ValueError("Anthropic API key not configured")
            return provider
        elif provider_name == 'huggingface':
            provider = HuggingFaceProvider()
            if not provider.is_available():
                raise ValueError("Hugging Face API key not configured")
            return provider
        elif provider_name == 'openai':
            # TODO: Implement OpenAI provider
            raise ValueError("OpenAI provider not yet implemented")
        elif provider_name == 'gemini':
            # TODO: Implement Gemini provider
            raise ValueError("Gemini provider not yet implemented")
        elif provider_name == 'llama':
            # TODO: Implement Llama provider
            raise ValueError("Local Llama provider not yet implemented")
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")
    
    @staticmethod
    def get_available_providers():
        """Get a list of all available (enabled) providers"""
        return [
            name for name, info in config.AI_PROVIDERS.items() 
            if info['enabled']
        ]
