import os
from dataclasses import dataclass, field
from typing import List

@dataclass
class MetricsConfig:
    # Central metrics endpoint
    CENTRAL_ENDPOINT: str = os.getenv('METRICS_ENDPOINT', 'http://genesis.linkportal.ro:61000/metrics/store/')
    NETWORK_METRICS_ENDPOINT: str = os.path.join(CENTRAL_ENDPOINT, 'network-metrics/')
    SYSTEM_METRICS_ENDPOINT: str = os.path.join(CENTRAL_ENDPOINT, 'machine-metrics/')
    PING_METRICS_ENDPOINT: str = os.path.join(CENTRAL_ENDPOINT, 'ping-metrics/')
    
    # Collector-specific configurations
    NETWORK_COLLECTION_INTERVAL: int = int(os.getenv('NETWORK_INTERVAL', 10))
    SYSTEM_COLLECTION_INTERVAL: int = int(os.getenv('SYSTEM_INTERVAL', 10))
    PING_COLLECTION_INTERVAL: int = int(os.getenv('PING_INTERVAL', 10))
    
    # Hosts to ping
    PING_HOSTS: List[str] = field(default_factory=lambda: ['google.com'])
    
    # Interfaces to ignore
    IGNORED_INTERFACES: List[str] = field(default_factory=lambda: ['lo', 'docker0'])

config = MetricsConfig()