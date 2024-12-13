import socket
import psutil
from typing import Dict, Any, List
from .base_collector import BaseCollector
from datetime import datetime

class NetworkCollector(BaseCollector):
    def __init__(self, collection_interval: int = 30, ignored_interfaces: List[str] = None):
        """
        Initialize the network metrics collector.
        
        :param collection_interval: Time between collections in seconds
        :param ignored_interfaces: List of network interfaces to ignore
        """
        super().__init__(collection_interval)
        self.ignored_interfaces = ignored_interfaces or []

    def collect_metrics(self) -> Dict[str, Any]:
        """
        Collect detailed network metrics for each network interface.
        
        :return: List of network metrics for each interface
        """
        metrics = []
        timestamp = datetime.now().isoformat(timespec='milliseconds')
        interfaces = psutil.net_io_counters(pernic=True)
        
        for interface_name, counters in interfaces.items():
            if interface_name not in self.ignored_interfaces:
                metric_entry = {
                    "hostname": socket.gethostname(),
                    "timestamp": timestamp,
                    "interface_name": interface_name,
                    "bytes_in": counters.bytes_recv,
                    "bytes_out": counters.bytes_sent,
                    "packets_in": counters.packets_recv,
                    "packets_out": counters.packets_sent,
                    "error_count": counters.errin + counters.errout,
                    "dropped_packets": counters.dropin + counters.dropout,
                    "total_connections": len(psutil.net_connections(kind='inet'))
                }
                metrics.append(metric_entry)
        
        return {"network_metrics": metrics}