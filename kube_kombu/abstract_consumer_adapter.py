from abc import ABC, abstractmethod


class AbstractConsumerAdapter(ABC):
    # property variables
    @abstractmethod
    def callback(self, body, message):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def check_connectivity():
        """
        This method can be used to check any connectivity of the application,
        for example: database connectivity
        :return_type: boolean
        """
        return True
