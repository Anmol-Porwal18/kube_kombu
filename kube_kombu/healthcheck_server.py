import asyncio
import logging

LOGGER = logging.getLogger(__name__)


class HealthCheckServer(object):
    def __init__(self, host, port, kombu_consumer):
        self.host = host
        self.port = port
        self.kombu_consumer = kombu_consumer
        self.server = None

    async def handle_message(self, reader, writer):
        is_connected = (
            self.kombu_consumer.is_connected[0]
            and self.kombu_consumer.adapter.check_connectivity()
        )
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
