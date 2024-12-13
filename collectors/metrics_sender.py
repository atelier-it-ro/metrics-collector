import requests
from typing import Dict, Any, List

class MetricsSender:
    def __init__(self, central_endpoint: str):
        """
        Initialize the metrics sender.
        
        :param central_endpoint: URL of the central logging host
        """
        self.central_endpoint = central_endpoint

    def send_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        Send collected metrics to the central logging host.
        
        :param metrics: Dictionary of metrics to send
        :return: Boolean indicating successful transmission
        """
        try:
            response = requests.post(self.central_endpoint, json=metrics)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error sending metrics: {e}")
            return False