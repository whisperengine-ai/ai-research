"""
OpenRouter LLM Integration
Provides interface to OpenRouter API for various LLM models
"""

import os
import requests
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenRouterLLM:
    """
    Interface to OpenRouter API
    Supports multiple LLM providers through a single API
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 model: Optional[str] = None,
                 site_name: Optional[str] = None,
                 site_url: Optional[str] = None):
        """
        Initialize OpenRouter client
        
        Args:
            api_key: OpenRouter API key (or set OPENROUTER_API_KEY env var)
            model: Model to use (or set OPENROUTER_MODEL env var)
            site_name: Your site name for tracking
            site_url: Your site URL for tracking
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.model = model or os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-chat-v3.1')
        self.site_name = site_name or os.getenv('OPENROUTER_SITE_NAME', 'consciousness-simulator')
        self.site_url = site_url or os.getenv('OPENROUTER_SITE_URL', 'http://localhost')
        
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key not found. Set OPENROUTER_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        print(f"✓ OpenRouter initialized with model: {self.model}")
    
    def generate(self, 
                prompt: str,
                max_tokens: int = 150,
                temperature: float = 0.7,
                conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Generate text using OpenRouter API with context window management
        
        Args:
            prompt: The prompt to generate from
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-2.0)
            conversation_history: Previous conversation turns
            
        Returns:
            Generated text response
        """
        # Build messages array
        messages = []
        
        # Add conversation history with token budget management
        if conversation_history:
            # Approximate token budget (most models support 8k+ context)
            # Reserve: ~500 for system prompt, max_tokens for response, 200 buffer
            max_history_tokens = 8000 - 500 - max_tokens - 200  # ~7000 tokens for history
            estimated_tokens = 0
            
            # Start from most recent and work backward (reverse iteration)
            history_to_add = []
            for turn in reversed(conversation_history[-20:]):  # Consider last 20 turns max
                # Rough token estimation: ~4 chars per token
                turn_tokens = (len(turn['user']) + len(turn['ai'])) // 4
                
                # Check if adding this turn would exceed budget
                if estimated_tokens + turn_tokens > max_history_tokens:
                    break  # Stop adding older turns
                
                # Add to front of list (since we're iterating backward)
                history_to_add.insert(0, turn)
                estimated_tokens += turn_tokens
            
            # Add the selected history to messages
            for turn in history_to_add:
                messages.append({"role": "user", "content": turn['user']})
                messages.append({"role": "assistant", "content": turn['ai']})
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Prepare request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            return generated_text.strip()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"OpenRouter API error: {str(e)}"
            if hasattr(e.response, 'text'):
                error_msg += f"\nResponse: {e.response.text}"
            print(f"⚠️ {error_msg}")
            return f"[API Error: {str(e)}]"
        except Exception as e:
            print(f"⚠️ Unexpected error: {str(e)}")
            return f"[Error: {str(e)}]"
    
    def generate_short(self, prompt: str, max_tokens: int = 50, temperature: float = 0.6) -> str:
        """Generate short response (for meta-cognitive reflections)"""
        return self.generate(prompt, max_tokens=max_tokens, temperature=temperature)
    
    @staticmethod
    def list_available_models() -> List[str]:
        """
        List popular models available through OpenRouter
        """
        return [
            # OpenAI
            "openai/gpt-4-turbo-preview",
            "openai/gpt-4",
            "openai/gpt-3.5-turbo",
            
            # Anthropic
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-opus",
            "anthropic/claude-3-sonnet",
            "anthropic/claude-3-haiku",
            
            # Meta
            "meta-llama/llama-3-70b-instruct",
            "meta-llama/llama-3-8b-instruct",
            
            # Google
            "google/gemini-pro",
            "google/palm-2-chat-bison",
            
            # Mistral
            "mistralai/mistral-large",
            "mistralai/mistral-medium",
            "mistralai/mistral-small",
            
            # Others
            "cohere/command-r-plus",
            "perplexity/llama-3-sonar-large-32k-online",
        ]


def get_llm_from_config() -> OpenRouterLLM:
    """
    Create OpenRouter LLM instance from environment configuration
    """
    return OpenRouterLLM()


if __name__ == "__main__":
    # Test the OpenRouter integration
    print("Testing OpenRouter integration...\n")
    
    try:
        llm = OpenRouterLLM()
        
        print(f"Model: {llm.model}")
        print(f"Site: {llm.site_name}\n")
        
        # Test generation
        response = llm.generate("Say hello in a friendly way.", max_tokens=50)
        print(f"Test response: {response}\n")
        
        print("✓ OpenRouter integration working!")
        
    except ValueError as e:
        print(f"⚠️ Configuration error: {e}")
        print("\nPlease set your OPENROUTER_API_KEY in .env file")
        print("See .env.example for template")
