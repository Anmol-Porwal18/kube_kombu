import asyncio
import logging
import threading
from abc import ABC, abstractmethod

from kombu import Exchange, Queue, Connection
from kombu.mixins import ConsumerMixin

LOGGER = logging.getLogger(__name__)


class ConsumerAdapter(ABC):
    # property variables
    @abstractmethod
    def callback(self, body, message):
        pass


class KombuConsumer(threading.Thread):
    def __init__(
        self,
        url,
        exchange,
        exchange_type,
        routing_key,
        queue_name,
        adapter,
        *args,
        **kwargs,
    ):
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.url = url
        self.queue_name = queue_name
        self.__connection = None
        self.adapter = adapter
        self.routing_key = routing_key
        self.is_connected = [False]
        super().__init__(name=f"{adapter.__name__}Thread", *args, **kwargs)

    def get_connection(self):
        if self.__connection is None or not self.__connection.connected:
            self.__connection = Connection(self.url, heartbeat=4)
        return self.__connection

    def run(self):
        exchange_obj = Exchange(name=self.exchange, type=self.exchange_type)
        queues = [
            Queue(
                name=self.queue_name,
                exchange=exchange_obj,
                routing_key=self.routing_key,
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


class Worker(ConsumerMixin):
    def __init__(self, connection, queues, adapter, is_connected):
        self.connection = connection
        self.queues = queues
        self.adapter = adapter
        self.is_connected = is_connected

    def on_connection_revived(self):
        self.is_connected[0] = True
        super().on_connection_revived()

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        self.is_connected[0] = True
        super().on_consume_ready(connection, channel, consumers, **kwargs)

    def on_consume_end(self, connection, channel):
        self.is_connected[0] = False
        super().on_consume_end(connection, channel)

    def on_iteration(self):
        self.is_connected[0] = True
        super().on_iteration()

    def on_connection_error(self, exc, interval):
        self.is_connected[0] = False
        super().on_connection_error(exc, interval)

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues, callbacks=[self.adapter().callback])]


class HealthCheckServer(object):
    def __init__(self, host, port, kombu_consumer):
        self.host = host
        self.port = port
        self.kombu_consumer = kombu_consumer
        self.server = None

    async def handle_message(self, reader, writer):
        is_connected = self.kombu_consumer.is_connected[0]
        if not is_connected:
            writer.write(b"Not Connected")
            await writer.drain()
            writer.close()
            for sock in self.server.sockets:
                sock.close()

        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info("peername")

        LOGGER.info(f"Received {message!r} from {addr!r}")

        LOGGER.info(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

        LOGGER.info("Close the Connection")
        writer.close()

    async def serve(self):
        self.server = await asyncio.start_server(
            self.handle_message, self.host, self.port
        )

        addrs = ", ".join(str(sock.getsockname()) for sock in self.server.sockets)
        LOGGER.info(f"Serving on {addrs}")

        async with self.server:
            await self.server.serve_forever()
