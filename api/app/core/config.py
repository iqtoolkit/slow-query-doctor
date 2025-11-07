from pydantic_settings import BaseSettings
from typing import Optional, List
from .config_manager import config_manager

class Settings(BaseSettings):
    # Load from config manager with environment variable override
    
    # Ollama
    ollama_base_url: str = config_manager.get("llm.ollama.base_url", "http://localhost:11434")
    ollama_model: str = config_manager.get("llm.ollama.model", "llama2:13b")
    ollama_timeout: int = config_manager.get("llm.ollama.timeout", 300)
    
    # API
    api_host: str = config_manager.get("api.host", "0.0.0.0")
    api_port: int = config_manager.get("api.port", 8000)
    api_workers: int = config_manager.get("api.workers", 4)
    allowed_origins: List[str] = config_manager.get("api.allowed_origins", ["http://localhost:8000"])
    
    # Security
    api_key_enabled: bool = config_manager.get("security.api_key_enabled", False)
    api_key: Optional[str] = config_manager.get("security.api_key", None)
    cors_enabled: bool = config_manager.get("security.cors_enabled", True)
    
    # Analysis
    max_log_size_mb: int = config_manager.get("analysis.max_log_size_mb", 50)
    max_queries_per_request: int = config_manager.get("analysis.max_queries_per_request", 100)
    min_duration_ms: int = config_manager.get("analysis.min_duration_ms", 1000)
    top_n_queries: int = config_manager.get("analysis.top_n_queries", 10)
    supported_formats: List[str] = config_manager.get("analysis.formats", ["plain", "csv", "json"])
    
    # Reports
    report_formats: List[str] = config_manager.get("reports.formats", ["markdown", "html"])
    syntax_highlighting: bool = config_manager.get("reports.syntax_highlighting", True)
    include_execution_plan: bool = config_manager.get("reports.include_execution_plan", True)
    max_queries_per_report: int = config_manager.get("reports.max_queries_per_report", 50)
    
    class Config:
        env_file = ".env"

    def reload(self):
        """Reload configuration from file and environment"""
        config_manager.reload()
        self.__init__()

settings = Settings()