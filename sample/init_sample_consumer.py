import asyncio
import logging
import os

import django
from django.conf import settings


LOGGER = logging.getLogger(__name__)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()

    from kube_kombu.healthcheck_server import HealthCheckServer
    from kube_kombu.consumer import KombuConsumer
    from sample_consumer import SampleConsumerAdapter

    consumer = KombuConsumer(
        "URL",
        "EXCHANGE",
        "EXCHANGE_TYPE",
        "ROUTING_KEY",
        "QUEUE",
        SampleConsumerAdapter,
    )

    consumer.start()
    try:
        asyncio.run(
            HealthCheckServer(
                host="127.0.0.1", port=8988, kombu_consumer=consumer
            ).serve()
        )
    except Exception as e:
        LOGGER.exception(f"Exception in running kombu consumer, Error: {e}")
        consumer.join()


if __name__ == "__main__":
    main()
