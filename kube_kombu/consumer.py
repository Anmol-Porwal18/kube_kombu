import logging
import threading

from kombu import Exchange, Queue, Connection
from kube_kombu.worker import Worker


LOGGER = logging.getLogger(__name__)


class KombuConsumer(threading.Thread):
    def __init__(
        self,
        consumer_config,
        adapter,
        *args,
        **kwargs,
    ):
        self.config = consumer_config
        self.__connection = None
        self.adapter = adapter

        self.is_connected = [False]
        super().__init__(name=f"{adapter.__name__}Thread", *args, **kwargs)

    def get_connection(self):
        if self.__connection is None or not self.__connection.connected:
            self.__connection = Connection(self.config.url, heartbeat=4)
        return self.__connection

    def run(self):
        exchange_obj = Exchange(name=self.config.exchange, type=self.config.exchange_type)
        queues = [
            Queue(
                name=self.config.queue_name,
                exchange=exchange_obj,
                routing_key=self.config.routing_key,
            )
        ]
        with self.get_connection() as conn:
            try:
                worker = Worker(conn, queues, self.adapter, self.is_connected)
                worker.run()
            except Exception as e:
                LOGGER.exception(
                    f"Exception in running thread for adapter: {self.adapter}, Error: {e}"
                )
