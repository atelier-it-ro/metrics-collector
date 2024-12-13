import time
import subprocess
import platform
import socket
from typing import Dict, List, Any
from .base_collector import BaseCollector

class PingCollector(BaseCollector):
    def __init__(self, hosts: List[str], collection_interval: int = 60):
        super().__init__(collection_interval)
        self.hosts = hosts

    def _ping_host(self, host: str) -> Dict[str, Any]:
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '4', host]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                rtt_lines = [line for line in lines if 'time=' in line]
                
                if rtt_lines:
                    rtts = [float(line.split('time=')[1].split()[0]) for line in rtt_lines]
                    packet_loss = (4 - len(rtt_lines)) / 4 * 100
                    
                    return {
                        "hostname": socket.gethostname(),
                        "host": host,
                        "avg": sum(rtts) / len(rtts),
                        "packet_loss": packet_loss
                    }
            
            return None
        
        except Exception:
            return None

    def collect_metrics(self) -> List[Dict[str, Any]]:
        ping_metrics = [result for result in (self._ping_host(host) for host in self.hosts) if result is not None]
        return ping_metrics