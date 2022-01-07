import json
import logging

from kube_kombu.consumer import ConsumerAdapter

LOGGER = logging.getLogger(__name__)


class SampleConsumerAdapter(ConsumerAdapter):
    @classmethod
    def handle_event1(cls, data):
        pass

    @classmethod
    def handle_event2(cls, data):
        pass

    def callback(self, data, message):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            if data["event"] == "event1":
                SampleConsumerAdapter.handle_event1(data["payload"])
            elif data["event"] == "event2":
                SampleConsumerAdapter.handle_event2(data["payload"])
        except Exception as e:
            LOGGER.exception(f"Exception in callback, Error: {e}")
        message.ack()
