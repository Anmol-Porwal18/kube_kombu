
# Setup and Running Kombu consumers
## Steps:

1. Install python 3.9 or greater on your system using [pyenv](https://github.com/pyenv/pyenv)
2. Activate your project's virtual environment for installing this library
```shell
$ source <virtualenv-path>/bin/activate
```
3. Install consumer library by running 
```shell
$ pip install kube_kombu
```

If you are using django you'll need to setup the django project before running the consumer. 

There are three variables that can be defined in your django settings file or in environment variables or as constants in your project:
1. `RABBITMQ`: This will be a dictionary containing rabbitmq related variables 
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
2. `HEALTHCHECK_HOST`: Host on which the consumer thread will open a port fot liveness check
3. `HEALTHCHECK_PORT`: Port which will be opened by consumer thread for liveness check

**Example**

Sample scripts are written in the `sample` directory for defining and initializing the consumer

`check_liveness_probe.py` file is for testing the socket connection locally

**You should now be able to use tcp liveness probe in kubernetes for liveness check of the pod.**
