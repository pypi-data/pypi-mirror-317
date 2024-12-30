"""
A/B testing functionality for prompts.
"""

import random
from typing import Dict, Any, List, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
import logging
from .metrics import MetricsCollector

T = TypeVar('T')


@dataclass
class Variant(Generic[T]):
    """Prompt variant configuration"""
    name: str
    config: T
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExperimentResult:
    """Result of an experiment run"""
    variant_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class Experiment(Generic[T]):
    """A/B testing experiment"""
    
    def __init__(
        self,
        name: str,
        variants: List[Variant[T]],
        metrics_collector: Optional[MetricsCollector] = None
    ):
        """Initialize experiment
        
        Args:
            name: Experiment name
            variants: List of variants to test
            metrics_collector: Optional metrics collector
        """
        self.name = name
        self.variants = variants
        self.metrics_collector = metrics_collector
        self.results: List[ExperimentResult] = []
        self.logger = logging.getLogger(__name__)
        
        # Normalize weights
        total_weight = sum(v.weight for v in variants)
        for variant in variants:
            variant.weight /= total_weight
            
    def get_variant(self) -> Variant[T]:
        """Get a random variant based on weights
        
        Returns:
            Selected variant
        """
        r = random.random()
        cumsum = 0
        for variant in self.variants:
            cumsum += variant.weight
            if r <= cumsum:
                return variant
        return self.variants[-1]
        
    def record_result(
        self,
        variant_name: str,
        metrics: Dict[str, float],
        **metadata
    ) -> None:
        """Record an experiment result
        
        Args:
            variant_name: Name of the variant used
            metrics: Metrics from the run
            **metadata: Additional result metadata
        """
        result = ExperimentResult(
            variant_name=variant_name,
            metrics=metrics,
            metadata=metadata
        )
        self.results.append(result)
        
        if self.metrics_collector:
            self.metrics_collector.record_prompt_usage(
                prompt_name=f"{self.name}_{variant_name}",
                token_count=metadata.get("token_count", 0),
                success=metadata.get("success", True),
                error=metadata.get("error"),
                experiment=self.name,
                variant=variant_name,
                **metrics
            )


class ExperimentManager:
    """Manager for A/B testing experiments"""
    
    def __init__(
        self,
        experiments_dir: Optional[str] = None,
        metrics_collector: Optional[MetricsCollector] = None
    ):
        """Initialize experiment manager
        
        Args:
            experiments_dir: Optional custom experiments directory path
            metrics_collector: Optional metrics collector
        """
        self.experiments_dir = experiments_dir or str(Path(__file__).parent / "experiments")
        self.metrics_collector = metrics_collector
        self.experiments: Dict[str, Experiment] = {}
        self.logger = logging.getLogger(__name__)
        
        # Ensure experiments directory exists
        Path(self.experiments_dir).mkdir(parents=True, exist_ok=True)
        
    def add_experiment(self, experiment: Experiment) -> None:
        """Add an experiment
        
        Args:
            experiment: Experiment to add
        """
        self.experiments[experiment.name] = experiment
        
    def get_experiment(self, name: str) -> Optional[Experiment]:
        """Get an experiment by name
        
        Args:
            name: Experiment name
            
        Returns:
            Experiment if found
        """
        return self.experiments.get(name)
        
    def get_results(self, experiment_name: str) -> Dict[str, Any]:
        """Get results for an experiment
        
        Args:
            experiment_name: Name of the experiment
            
        Returns:
            Experiment results summary
        """
        experiment = self.experiments.get(experiment_name)
        if not experiment:
            return {}
            
        results = {}
        for variant in experiment.variants:
            variant_results = [r for r in experiment.results if r.variant_name == variant.name]
            if not variant_results:
                continue
                
            metrics = {}
            for metric in variant_results[0].metrics.keys():
                values = [r.metrics[metric] for r in variant_results]
                metrics[metric] = {
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values)
                }
                
            results[variant.name] = {
                "metrics": metrics,
                "sample_size": len(variant_results)
            }
            
        return results 