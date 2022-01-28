from kombu.mixins import ConsumerMixin


class Worker(ConsumerMixin):
    def __init__(self, connection, queues, adapter, is_connected):
        self.connection = connection
        self.queues = queues
        self.adapter = adapter
        self.is_connected = is_connected

    def on_connection_revived(self):
        self.is_connected[0] = self.adapter.check_connectivity()
        super().on_connection_revived()

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        self.is_connected[0] = self.adapter.check_connectivity()
        super().on_consume_ready(connection, channel, consumers, **kwargs)

    def on_consume_end(self, connection, channel):
        self.is_connected[0] = False
        super().on_consume_end(connection, channel)

    def on_iteration(self):
        self.is_connected[0] = self.adapter.check_connectivity()
        super().on_iteration()

    def on_connection_error(self, exc, interval):
        self.is_connected[0] = False
        super().on_connection_error(exc, interval)

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues, callbacks=[self.adapter().callback])]
