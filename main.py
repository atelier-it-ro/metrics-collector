import os
import threading
import time
import logging
from typing import Dict, Any

# Import the configuration
from config import config

from collectors.network_collector import NetworkCollector
from collectors.system_collector import SystemCollector
from collectors.ping_collector import PingCollector
from collectors.metrics_sender import MetricsSender

class MetricsAggregator:
    def __init__(self):
        """
        Initialize the metrics aggregator.
        Creates separate metrics senders for different metric types.
        """
        self.network_sender = MetricsSender(config.NETWORK_METRICS_ENDPOINT)
        self.system_sender = MetricsSender(config.SYSTEM_METRICS_ENDPOINT)
        self.ping_sender = MetricsSender(config.PING_METRICS_ENDPOINT)
        
        self.collected_metrics = {
            'network': {},
            'system': {},
            'ping': {}
        }
        self.logger = logging.getLogger(self.__class__.__name__)

    def aggregate_metrics(self, metric_type: str, metrics: Dict[str, Any]):
        """
        Aggregate metrics for a specific type.
        
        :param metric_type: Type of metrics ('network', 'system', 'ping')
        :param metrics: Metrics dictionary from a collector
        """
        self.collected_metrics[metric_type].update(metrics)

    def send_aggregated_metrics(self):
        """
        Send aggregated metrics to respective endpoints.
        """
        try:
            # Send network metrics
            if self.collected_metrics['network']:
                success = self.network_sender.send_metrics(self.collected_metrics['network'])
                self.logger.info(f"Network metrics send {'successful' if success else 'failed'}")
                if success:
                    self.collected_metrics['network'].clear()

            # Send system metrics
            if self.collected_metrics['system']:
                success = self.system_sender.send_metrics(self.collected_metrics['system'])
                self.logger.info(f"System metrics send {'successful' if success else 'failed'}")
                if success:
                    self.collected_metrics['system'].clear()

        except Exception as e:
            self.logger.error(f"Error in sending metrics: {e}")

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('MetricsCollector')
    logger.info("Metrics collection starting...")

    # Initialize metrics aggregator
    aggregator = MetricsAggregator()

    # Initialize collectors with configurations from config
    network_collector = NetworkCollector(
        collection_interval=config.NETWORK_COLLECTION_INTERVAL,
        ignored_interfaces=config.IGNORED_INTERFACES
    )
    
    system_collector = SystemCollector(
        collection_interval=config.SYSTEM_COLLECTION_INTERVAL
    )
    
    

    # Create threads for each collector
    collectors = [
        (network_collector, lambda metrics: aggregator.aggregate_metrics('network', metrics)),
        (system_collector, lambda metrics: aggregator.aggregate_metrics('system', metrics))
    ]

    # Start collector threads
    threads = []
    for collector, callback in collectors:
        thread = threading.Thread(
            target=collector.start, 
            kwargs={'callback': callback}, 
            daemon=True  # Allows thread to exit when main program exits
        )
        thread.start()
        threads.append(thread)

    # Periodic metrics sending
    try:
        while True:
            aggregator.send_aggregated_metrics()
            time.sleep(15)  # Send metrics every minute
    except KeyboardInterrupt:
        logger.info("Metrics collection interrupted. Shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error in metrics collection: {e}")
    finally:
        # Ensure clean shutdown
        for thread in threads:
            thread.join(timeout=5)
        logger.info("Metrics collection stopped.")

if __name__ == "__main__":
    main()