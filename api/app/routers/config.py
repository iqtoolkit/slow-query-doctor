from fastapi import APIRouter, HTTPException, Depends
from app.core.config import settings
from app.core.config_manager import config_manager
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/config", tags=["configuration"])

@router.get("/")
async def get_config() -> Dict[str, Any]:
    """Get current configuration"""
    try:
        return {
            "api": {
                "host": settings.api_host,
                "port": settings.api_port,
                "workers": settings.api_workers,
                "allowed_origins": settings.allowed_origins
            },
            "llm": {
                "provider": config_manager.get("llm.provider"),
                "ollama": {
                    "base_url": settings.ollama_base_url,
                    "model": settings.ollama_model,
                    "timeout": settings.ollama_timeout
                }
            },
            "analysis": {
                "max_log_size_mb": settings.max_log_size_mb,
                "max_queries_per_request": settings.max_queries_per_request,
                "min_duration_ms": settings.min_duration_ms,
                "top_n_queries": settings.top_n_queries,
                "supported_formats": settings.supported_formats
            },
            "reports": {
                "formats": settings.report_formats,
                "syntax_highlighting": settings.syntax_highlighting,
                "include_execution_plan": settings.include_execution_plan,
                "max_queries_per_report": settings.max_queries_per_report
            }
        }
    except Exception as e:
        logger.error(f"Error retrieving config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{section}/{key}")
async def update_config(section: str, key: str, value: Any):
    """Update configuration value"""
    try:
        config_key = f"{section}.{key}"
        config_manager.set(config_key, value)
        config_manager.save()
        settings.reload()
        return {"message": f"Updated {config_key} to {value}"}
    except Exception as e:
        logger.error(f"Error updating config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reload")
async def reload_config():
    """Reload configuration from file"""
    try:
        settings.reload()
        return {"message": "Configuration reloaded successfully"}
    except Exception as e:
        logger.error(f"Error reloading config: {e}")
        raise HTTPException(status_code=500, detail=str(e))