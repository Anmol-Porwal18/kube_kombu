from kube_kombu.healthcheck_server import HealthCheckServer
from kube_kombu.consumer import KombuConsumer
import asyncio
import logging

LOGGER = logging.getLogger(__name__)


def start_consumer(consumer_config, adapter, host="0.0.0.0", port=8988):
    consumer = KombuConsumer(
        consumer_config,
        adapter,
    )

    consumer.start()
    try:
        asyncio.run(
            HealthCheckServer(
                host=host, port=port, kombu_consumer=consumer
            ).serve()
        )
    except Exception as e:
        LOGGER.exception(f"Exception in running kombu consumer, Error: {e}")
        consumer.join()
