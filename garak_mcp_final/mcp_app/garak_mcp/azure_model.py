

import os
import requests
import logging
from typing import Optional, Dict, Any
from functools import lru_cache
import time

logger = logging.getLogger(__name__)

class AzureOpenAIClient:
    """
    Enhanced Azure OpenAI client with configuration management and error handling
    """
    
    def __init__(self, 
                 endpoint: Optional[str] = None,
                 api_key: Optional[str] = None,
                 model: Optional[str] = None,
                 api_version: str = "2024-06-01"):
        
        # Get configuration from environment or parameters
        self.endpoint = endpoint or os.getenv("AZURE_ENDPOINT", "https://opeanai-eastus.openai.azure.com/")
        self.api_key = api_key or os.getenv("AZURE_API_KEY")
        self.model = model or os.getenv("AZURE_MODEL_NAME", "gpt4o")
        self.api_version = api_version
        
        # Ensure endpoint ends with /
        if not self.endpoint.endswith('/'):
            self.endpoint += '/'
        
        # Validate required configuration
        if not self.api_key:
            raise ValueError("Azure API key is required. Set AZURE_API_KEY environment variable or pass api_key parameter.")
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # Minimum 100ms between requests
        
        logger.info(f"Initialized Azure OpenAI client for model: {self.model}")
    
    def _make_request(self, prompt: str, **kwargs) -> str:
        """
        Make a request to Azure OpenAI API with enhanced error handling
        """
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        url = f"{self.endpoint}openai/deployments/{self.model}/chat/completions?api-version={self.api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        
        # Default parameters
        default_params = {
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        
        # Merge with provided parameters
        params = {**default_params, **kwargs}
        
        data = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            **params
        }
        
        try:
            logger.debug(f"Making request to Azure OpenAI: {url}")
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            self.last_request_time = time.time()
            
            result = response.json()
            
            # Extract the response content
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                # Log token usage if available
                if "usage" in result:
                    usage = result["usage"]
                    logger.info(f"Token usage - Prompt: {usage.get('prompt_tokens', 0)}, "
                              f"Completion: {usage.get('completion_tokens', 0)}, "
                              f"Total: {usage.get('total_tokens', 0)}")
                
                return content
            else:
                logger.error(f"Unexpected response format: {result}")
                return "Error: Unexpected response format from Azure OpenAI"
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error from Azure OpenAI: {e}")
            if e.response.status_code == 429:
                return "Error: Rate limit exceeded. Please try again later."
            elif e.response.status_code == 401:
                return "Error: Authentication failed. Please check your API key."
            elif e.response.status_code == 400:
                return "Error: Bad request. Please check your input."
            else:
                return f"Error: HTTP {e.response.status_code} - {e.response.text}"
        
        except requests.exceptions.Timeout:
            logger.error("Request timeout to Azure OpenAI")
            return "Error: Request timed out. Please try again."
        
        except requests.exceptions.ConnectionError:
            logger.error("Connection error to Azure OpenAI")
            return "Error: Could not connect to Azure OpenAI. Please check your internet connection."
        
        except Exception as e:
            logger.error(f"Unexpected error in Azure OpenAI request: {e}")
            return f"Error: Unexpected error occurred - {str(e)}"
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Azure OpenAI"""
        return self._make_request(prompt, **kwargs)
    
    def generate_with_system_prompt(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate text with separate system and user prompts"""
        url = f"{self.endpoint}openai/deployments/{self.model}/chat/completions?api-version={self.api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        
        default_params = {
            "max_tokens": 1000,
            "temperature": 0.7,
        }
        
        params = {**default_params, **kwargs}
        
        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            **params
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error in generate_with_system_prompt: {e}")
            return f"Error: {str(e)}"

# Global client instance
_azure_client = None

def get_azure_client() -> AzureOpenAIClient:
    """Get or create the global Azure OpenAI client"""
    global _azure_client
    if _azure_client is None:
        _azure_client = AzureOpenAIClient()
    return _azure_client

def azure_model(prompt: str, **kwargs) -> str:
    """
    Legacy function for backwards compatibility
    Simple interface to Azure OpenAI
    """
    client = get_azure_client()
    return client.generate_text(prompt, **kwargs)

def azure_model_with_config(prompt: str, 
                          max_tokens: int = 1000,
                          temperature: float = 0.7,
                          **kwargs) -> str:
    """
    Enhanced Azure model function with explicit configuration
    """
    client = get_azure_client()
    return client.generate_text(
        prompt, 
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )

# Configuration validation
def validate_azure_config() -> Dict[str, Any]:
    """Validate Azure OpenAI configuration"""
    config = {
        "endpoint": os.getenv("AZURE_ENDPOINT"),
        "api_key": "***" if os.getenv("AZURE_API_KEY") else None,
        "model": os.getenv("AZURE_MODEL_NAME"),
        "status": "unknown"
    }
    
    try:
        client = get_azure_client()
        # Try a simple test request
        test_response = client.generate_text("Hello", max_tokens=5)
        if not test_response.startswith("Error:"):
            config["status"] = "connected"
        else:
            config["status"] = "error"
            config["error"] = test_response
    except Exception as e:
        config["status"] = "error"
        config["error"] = str(e)
    
    return config