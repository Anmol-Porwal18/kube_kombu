def main(host, port):
    # setup django before everything
    """
    import django
    from django.conf import settings
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    """

    from sample_consumer import SampleConsumerAdapter
    from kube_kombu.consumer_config import ConsumerConfig
    from kube_kombu.start_consumer import start_consumer

    consumer_config = ConsumerConfig(
        "URL",
        "EXCHANGE",
        "EXCHANGE_TYPE",
        "ROUTING_KEY",
        "QUEUE",
    )
    start_consumer(consumer_config, SampleConsumerAdapter, host, port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Setup Host and Port for Kube Liveness check"
    )
    parser.add_argument(
        "--port",
        type=int,
        metavar="path",
        default=8988,
        help="Post to start TCP healthCheck server on. Default is 8988",
    )
    parser.add_argument(
        "--host",
        metavar="path",
        default="0.0.0.0",
        help="IP host to start health check server on. Default is 0.0.0.0",
    )
    args = parser.parse_args()
    main(args.host, args.port)
