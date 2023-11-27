import logging
import threading

from kombu import Connection, Exchange, Queue, binding

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

    def get_configured_queues(self):
        def get_bindings():
            _bindings = []
            for _binding in self.config.bindings:
                exchange = Exchange(
                    _binding["exchange"]["name"], _binding["exchange"]["type"]
                )
                routing_key = _binding["routing_key"]
                binding_obj = binding(exchange, routing_key)
                _bindings.append(binding_obj)
            return _bindings

        return (
            [Queue(name=self.config.queue_name, bindings=get_bindings())]
            if self.config.bindings
            else [
                Queue(
                    name=self.config.queue_name,
                    exchange=Exchange(
                        name=self.config.exchange, type=self.config.exchange_type
                    ),
                    routing_key=self.config.routing_key,
                )
            ]
        )

    def run(self):
        queues = self.get_configured_queues()
        with self.get_connection() as conn:
            try:
                worker = Worker(conn, queues, self.adapter, self.is_connected)
                worker.run()
            except Exception as e:
                LOGGER.exception(
                    f"Exception in running thread for adapter: {self.adapter}, Error: {e}"
                )
