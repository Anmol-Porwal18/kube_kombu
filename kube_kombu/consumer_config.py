class ConsumerConfig:
    def __init__(
        self,
        url,
        exchange=None,
        exchange_type=None,
        routing_key=None,
        queue_name=None,
        bindings=[],
    ):
        if not queue_name:
            raise ValueError("Consumer without a queue name. Really?")
        if bindings and (exchange or exchange_type or routing_key):
            raise ValueError(
                "Conflicting Input Provided: Either specify bindings or exchange parameters only"
            )
        self.url = url
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.queue_name = queue_name
        self.bindings = bindings
