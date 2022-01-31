class ConsumerConfig:
    def __init__(self, url, exchange, exchange_type, routing_key, queue_name):
        self.url = url
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.queue_name = queue_name
