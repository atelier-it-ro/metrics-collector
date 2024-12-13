import psutil
import socket
from typing import Dict, Any
from .base_collector import BaseCollector

class SystemCollector(BaseCollector):
    def collect_metrics(self) -> Dict[str, Any]:
        """
        Collect system-level metrics including CPU, memory, and disk usage.
        
        :return: Dictionary of system metrics
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        virtual_mem = psutil.virtual_memory()
        
        try:
            load1, load5, load15 = psutil.getloadavg()
        except AttributeError:
            # Fallback for systems without load average
            load1 = load5 = load15 = 0
        
        return {
            "system_metrics": {
                "hostname": socket.gethostname(),
                "cpu_usage": cpu_usage,
                "mem_total": virtual_mem.total,
                "mem_usage": virtual_mem.used,
                "disk_usage": psutil.disk_usage('/').percent,
                "sys_load1": round(load1, 2),
                "sys_load5": round(load5, 2),
                "sys_load15": round(load15, 2)
            }
        }