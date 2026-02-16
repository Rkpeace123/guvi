"""
Performance metrics collection and reporting
"""

import time
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime
import statistics


class MetricsCollector:
    """
    Collect and analyze performance metrics
    """
    
    def __init__(self):
        """Initialize metrics collector"""
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
        self.timers = {}
    
    def record_metric(self, name: str, value: float):
        """
        Record a metric value
        
        Args:
            name: Metric name
            value: Metric value
        """
        self.metrics[name].append({
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def increment_counter(self, name: str, amount: int = 1):
        """
        Increment a counter
        
        Args:
            name: Counter name
            amount: Increment amount
        """
        self.counters[name] += amount
    
    def start_timer(self, name: str):
        """
        Start a timer
        
        Args:
            name: Timer name
        """
        self.timers[name] = time.time()
    
    def stop_timer(self, name: str) -> Optional[float]:
        """
        Stop a timer and record duration
        
        Args:
            name: Timer name
        
        Returns:
            Duration in seconds
        """
        if name not in self.timers:
            return None
        
        duration = time.time() - self.timers[name]
        self.record_metric(f"{name}_duration", duration)
        del self.timers[name]
        
        return duration
    
    def get_metric_stats(self, name: str) -> Dict:
        """
        Get statistics for a metric
        
        Args:
            name: Metric name
        
        Returns:
            Statistics dict
        """
        if name not in self.metrics or not self.metrics[name]:
            return {}
        
        values = [m["value"] for m in self.metrics[name]]
        
        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0
        }
    
    def get_counter_value(self, name: str) -> int:
        """Get counter value"""
        return self.counters.get(name, 0)
    
    def get_all_metrics(self) -> Dict:
        """Get all metrics and counters"""
        return {
            "metrics": {
                name: self.get_metric_stats(name)
                for name in self.metrics
            },
            "counters": dict(self.counters)
        }
    
    def reset(self):
        """Reset all metrics"""
        self.metrics.clear()
        self.counters.clear()
        self.timers.clear()
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        lines = ["=== Metrics Summary ==="]
        
        # Counters
        if self.counters:
            lines.append("\nCounters:")
            for name, value in sorted(self.counters.items()):
                lines.append(f"  {name}: {value}")
        
        # Metrics
        if self.metrics:
            lines.append("\nMetrics:")
            for name in sorted(self.metrics.keys()):
                stats = self.get_metric_stats(name)
                lines.append(f"  {name}:")
                lines.append(f"    Count: {stats['count']}")
                lines.append(f"    Mean: {stats['mean']:.4f}")
                lines.append(f"    Min/Max: {stats['min']:.4f} / {stats['max']:.4f}")
        
        return "\n".join(lines)


# Global metrics instance
_global_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    """Get global metrics collector"""
    return _global_metrics


# Example usage
if __name__ == "__main__":
    metrics = MetricsCollector()
    
    # Record some metrics
    metrics.increment_counter("requests")
    metrics.increment_counter("requests")
    metrics.increment_counter("scams_detected")
    
    # Time an operation
    metrics.start_timer("processing")
    time.sleep(0.1)
    duration = metrics.stop_timer("processing")
    print(f"Processing took: {duration:.4f}s")
    
    # Record values
    metrics.record_metric("risk_score", 0.85)
    metrics.record_metric("risk_score", 0.92)
    metrics.record_metric("risk_score", 0.78)
    
    # Get summary
    print(metrics.get_summary())
