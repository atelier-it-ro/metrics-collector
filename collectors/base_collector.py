import abc
import time
from typing import Dict, Any

class BaseCollector(abc.ABC):
    def __init__(self, collection_interval: int = 30):
        """
        Initialize the base collector with a specific collection interval.
        
        :param collection_interval: Time between metric collections in seconds
        """
        self.collection_interval = collection_interval
        self.is_running = False

    @abc.abstractmethod
    def collect_metrics(self) -> Dict[str, Any]:
        """
        Abstract method to collect metrics.
        Must be implemented by subclasses.
        
        :return: Dictionary of collected metrics
        """
        pass

    def start(self, callback=None):
        """
        Start continuous metric collection.
        
        :param callback: Optional callback function to process collected metrics
        """
        self.is_running = True
        while self.is_running:
            metrics = self.collect_metrics()
            if callback:
                callback(metrics)
            time.sleep(self.collection_interval)

    def stop(self):
        """
        Stop the metric collection process.
        """
        self.is_running = False