from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class AzureOpenAIConfig(BaseModel):
    """Azure OpenAI configuration"""
    endpoint: str = Field("", description="Azure OpenAI endpoint URL")
    api_version: str = Field("2023-05-15", description="Azure OpenAI API version")
    deployment: str = Field("gpt4o", description="Azure OpenAI deployment name")
    temperature: float = Field(0.0, description="Temperature for LLM generation (0.0-1.0)")
    max_tokens: int = Field(1000, description="Maximum tokens for LLM responses")

class GoogleSearchConfig(BaseModel):
    """Google Search API configuration"""
    api_key: str = Field("", description="Google API key")
    cx: str = Field("", description="Google Programmable Search Engine ID")
    max_results: int = Field(10, description="Maximum number of results per query")

class SearchConfig(BaseModel):
    """Configuration for the search engine"""
    # Azure OpenAI
    azure_openai: AzureOpenAIConfig = Field(default_factory=AzureOpenAIConfig)
    
    # Search query generation
    max_search_queries: int = Field(3, description="Maximum number of search queries to generate")
    query_enhancement: bool = Field(True, description="Whether to enhance queries with LLM")
    
    # Search execution
    search_api: str = Field("google", description="Search API to use (google, bing, etc.)")
    google_search: GoogleSearchConfig = Field(default_factory=GoogleSearchConfig)
    max_results_per_query: int = Field(5, description="Maximum number of results per query")
    
    # Content processing
    max_sources: int = Field(10, description="Maximum number of sources to process")
    
    # Content moderation
    enable_moderation: bool = Field(True, description="Whether to enable content moderation")
    moderation_threshold: float = Field(0.8, description="Threshold for content moderation (0.0-1.0)")
    
    # Response generation
    response_template: Optional[str] = Field(None, description="Template for response generation")
    
    # Performance
    max_concurrency: int = Field(5, description="Maximum number of concurrent requests")
    use_streaming: bool = Field(True, description="Whether to use streaming for responses")
    timeout: int = Field(30, description="Timeout for external API calls in seconds")
    
    # Caching
    enable_caching: bool = Field(True, description="Whether to enable caching")
    cache_ttl: int = Field(3600, description="Time-to-live for cache entries in seconds")
    
    # Retry configuration
    max_retries: int = Field(3, description="Maximum number of retries for failed requests")
    retry_delay: int = Field(1, description="Delay between retries in seconds")
    
    # Spelling correction
    handle_spelling_corrections: bool = Field(True, description="Whether to handle spelling corrections from search results")
    
    def get_runnable_config(self) -> Dict[str, Any]:
        """
        Get configuration for LangGraph runnables
        
        Returns:
            Dictionary with configuration for LangGraph runnables
        """
        return {
            "configurable": {
                "max_search_queries": self.max_search_queries,
                "max_results_per_query": self.max_results_per_query,
                "max_sources": self.max_sources,
                "max_concurrency": self.max_concurrency,
                "azure_openai": self.azure_openai.dict(),
                "google_search": self.google_search.dict() if self.search_api == "google" else {},
                "enable_moderation": self.enable_moderation,
                "handle_spelling_corrections": self.handle_spelling_corrections
            }
        }
