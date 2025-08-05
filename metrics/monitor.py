"""
Performance and resource monitoring utilities.
"""
import psutil
import time

def get_system_info():
    """Get basic system information."""
    return {
        'cpu_count': psutil.cpu_count(),
        'memory_total': psutil.virtual_memory().total,
        'memory_available': psutil.virtual_memory().available
    }

def monitor_resources():
    """Monitor current resource usage."""
    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'memory_used': psutil.virtual_memory().used
    }