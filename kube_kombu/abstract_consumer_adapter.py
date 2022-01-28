from abc import ABC, abstractmethod


class AbstractConsumerAdapter(ABC):
    # property variables
    @abstractmethod
    def callback(self, body, message):
        raise NotImplementedError

    @abstractmethod
    def check_connectivity(self):
        """
        This method can be used to check any connectivity of the application,
        for example: database connectivity
        :return_type: boolean
        """
        return True
