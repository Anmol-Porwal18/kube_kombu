from abc import ABC, abstractmethod


class ConsumerAdapter(ABC):
    # property variables
    @abstractmethod
    def callback(self, body, message):
        pass
