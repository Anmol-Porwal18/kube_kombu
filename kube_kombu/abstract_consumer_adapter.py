from abc import ABC, abstractmethod


class AbstractConsumerAdapter(ABC):
    # property variables
    @abstractmethod
    def callback(self, body, message):
        pass
