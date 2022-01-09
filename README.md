# Kube Kombu

This project wraps the [kombu](https://pypi.org/project/kombu/) consumer of python for the use with writing consumer for RabbitMQ custom pubsub.
Since Kombu Consumer doesn't come with liveness check this package provides liveness check on the top
of kombu consumers. This package exposes a TCP port which can be added to [kubernetes liveness](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) probe.

Logic for liveness probe is as follows:-
1. Open an asnycio server TCP port in the same process as Consumer. 
2. On Message Received of TCP checks for liveness of the threads and connection of the Kombu Consumers. 
3. If the rabbit consumers are found to be inactive this closes the TCP port.
4. Once the port is closed liveness checks will fail the next time leading to restart of pod


# Setup and Running Kombu consumers

## Installation Steps:

1. Install python 3.9 or greater on your system using [pyenv](https://github.com/pyenv/pyenv)
2. Activate your project's virtual environment for installing this library
```shell
$ source <virtualenv-path>/bin/activate
```
3. Install consumer library by running 
```shell
$ pip install kube_kombu
```

## Implementation Steps

If you are using django you'll need to setup the django project before running the `start_consumer`. 

Example :- 

```python
import django
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

```

There are three variables that can be defined in your django settings file or in environment variables or as constants in your project:
1. `RABBITMQ`: This can be a dictionary containing rabbitmq related variables 
    ####Example:
```python
RABBITMQ = {
    "URL": "<RABBIT_URL>",
    "EXCHANGE": "<RABBIT_EXCHANGE>",
    "EXCHANGE_TYPE": "<RABBIT_EXCHANGE_TYPE>",
    "ROUTING_KEY": "<RABBIT_ROUTING_KEY>",
    "QUEUE": "<RABBIT_QUEUE>"
}
```
Once you have defined the rabbit config you need to define consumer_config :- 
```python
from kube_kombu.consumer_config import ConsumerConfig
consumer_config = ConsumerConfig(
        "URL",
        "EXCHANGE",
        "EXCHANGE_TYPE",
        "ROUTING_KEY",
        "QUEUE",
    )
```

`AbstractConsumerAdapter` defines the abstract method `callback` which you need to extend your class with and implement your own adapter on what you want to do on receiving the message.

Sample Adapter Can be written as :- 

```python
import json
import logging

from kube_kombu.abstract_consumer_adapter import AbstractConsumerAdapter

LOGGER = logging.getLogger(__name__)


class SampleConsumerAdapter(AbstractConsumerAdapter):
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
```
**DONOT FORGET TO ACK THE MESSAGE at the end of callback**

Once you have implemented the Adapters and config of your own you will now need to start the consumer which can be done as follows:- 

```python
from kube_kombu.start_consumer import start_consumer
start_consumer(
        consumer_config,
        SampleConsumerAdapter,
        host,
        port
    )
```

At the end if you want to run the Kombu Consumers on Pod you can implement the `__main__` as follows:- 
```python
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Setup Host and Port for Kube Liveness check')
    parser.add_argument('--port', type=int, metavar='path', default=8988,
                        help='Post to start TCP healthCheck server on. Default is 8988')
    parser.add_argument('--host', metavar='path', default="0.0.0.0",
                        help='IP host to start health check server on. Default is 0.0.0.0')
    args = parser.parse_args()
    main(args.host, args.port)
```

This will help you to pass the post and host from docker `RUN` command instead. 


2. `HEALTHCHECK_HOST`: Host on which the consumer thread will open a port fot liveness check. Keep it `0.0.0.0` for use with Kubernetes liveness check.
3. `HEALTHCHECK_PORT`: Port which will be opened by consumer thread for liveness check. Use the same port as you would use with `EXPOSE` command in docker

**Example**

Sample scripts are written in the `sample` directory for defining and initializing the consumer

`check_liveness_probe.py` file is for testing the socket connection locally

**You should now be able to use tcp liveness probe in kubernetes for liveness check of the pod.**
