"""
Metrics collection for prompt usage and performance tracking.
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from pathlib import Path


@dataclass
class PromptMetric:
    """Single prompt usage metric"""
    prompt_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    token_count: int = 0
    success: bool = True
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class MetricsCollector:
    """Collector for prompt usage metrics"""
    
    def __init__(self, metrics_dir: Optional[str] = None):
        """Initialize metrics collector
        
        Args:
            metrics_dir: Optional custom metrics directory path
        """
        self.metrics_dir = metrics_dir or str(Path(__file__).parent / "metrics")
        self.metrics: List[PromptMetric] = []
        self.logger = logging.getLogger(__name__)
        
        # Ensure metrics directory exists
        Path(self.metrics_dir).mkdir(parents=True, exist_ok=True)
        
    def record_prompt_usage(
        self,
        prompt_name: str,
        token_count: int,
        success: bool = True,
        error: Optional[str] = None,
        **metadata
    ) -> None:
        """Record a prompt usage
        
        Args:
            prompt_name: Name of the prompt used
            token_count: Number of tokens used
            success: Whether the prompt was successful
            error: Optional error message
            **metadata: Additional metadata to record
        """
        metric = PromptMetric(
            prompt_name=prompt_name,
            token_count=token_count,
            success=success,
            error=error,
            metadata=metadata
        )
        self.metrics.append(metric)
        self._write_metric(metric)
        
    def _write_metric(self, metric: PromptMetric) -> None:
        """Write a metric to storage
        
        Args:
            metric: Metric to write
        """
        try:
            metric_file = Path(self.metrics_dir) / f"{metric.timestamp.strftime('%Y%m%d')}.jsonl"
            with open(metric_file, 'a') as f:
                f.write(json.dumps({
                    "prompt_name": metric.prompt_name,
                    "timestamp": metric.timestamp.isoformat(),
                    "duration_ms": metric.duration_ms,
                    "token_count": metric.token_count,
                    "success": metric.success,
                    "error": metric.error,
                    "metadata": metric.metadata
                }) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write metric: {str(e)}")
            
    def get_metrics(
        self,
        prompt_name: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[PromptMetric]:
        """Get filtered metrics
        
        Args:
            prompt_name: Optional prompt name to filter by
            start_time: Optional start time to filter by
            end_time: Optional end time to filter by
            
        Returns:
            List of matching metrics
        """
        filtered = self.metrics
        
        if prompt_name:
            filtered = [m for m in filtered if m.prompt_name == prompt_name]
            
        if start_time:
            filtered = [m for m in filtered if m.timestamp >= start_time]
            
        if end_time:
            filtered = [m for m in filtered if m.timestamp <= end_time]
            
        return filtered
        
    def get_summary(self, prompt_name: Optional[str] = None) -> Dict[str, Any]:
        """Get usage summary statistics
        
        Args:
            prompt_name: Optional prompt name to filter by
            
        Returns:
            Summary statistics
        """
        metrics = self.get_metrics(prompt_name=prompt_name)
        
        if not metrics:
            return {}
            
        return {
            "total_usage": len(metrics),
            "total_tokens": sum(m.token_count for m in metrics),
            "success_rate": sum(1 for m in metrics if m.success) / len(metrics),
            "avg_duration_ms": sum(m.duration_ms for m in metrics) / len(metrics),
            "error_count": sum(1 for m in metrics if not m.success)
        }


class MetricsDecorator:
    """Decorator for automatic metrics collection"""
    
    def __init__(self, collector: MetricsCollector):
        """Initialize metrics decorator
        
        Args:
            collector: Metrics collector to use
        """
        self.collector = collector
        
    def __call__(self, func):
        """Decorate a function with metrics collection
        
        Args:
            func: Function to decorate
            
        Returns:
            Decorated function
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            prompt_name = kwargs.get("prompt_name", func.__name__)
            
            try:
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                
                self.collector.record_prompt_usage(
                    prompt_name=prompt_name,
                    token_count=getattr(result, "token_count", 0),
                    duration_ms=duration,
                    success=True
                )
                
                return result
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                
                self.collector.record_prompt_usage(
                    prompt_name=prompt_name,
                    token_count=0,
                    duration_ms=duration,
                    success=False,
                    error=str(e)
                )
                
                raise
                
        return wrapper 