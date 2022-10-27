import logging

from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import json

from django.conf import settings

logger = logging.getLogger(__name__)


def _connect_aws_iot(iot_server, client_id, cert_path, key_path, root_cert_path):
    """
    Connect to AWS IoT Server

    :param iot_server: str, URL to iot Server
    :param client_id: str, Name of device/thing
    :param cert_path: path to certificate file
    :param key_path: path to private key file
    :param root_cert_path: path to root certificate file

    :return: awscrt.mqtt.Connection
    """
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=iot_server,
        cert_filepath=cert_path,
        pri_key_filepath=key_path,
        client_bootstrap=client_bootstrap,
        ca_filepath=root_cert_path,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=6
    )
    logger.info("Connecting to {} with client ID '{}'".format(
        iot_server, client_id
    ))

    # Make the connect() call
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()

    logger.info("Connected!")
    return mqtt_connection


def mqtt_connection():
    """
    Get AWS IoT MQTT Connection

    :return: awscrt.mqtt.Connection
    """
    if not getattr(settings, "AWS_IOT_ENABLED", False):
        logger.info("AWS IoT is not enabled")
        return

    credentials = {
        "iot_server": getattr(settings, "AWS_IOT_SERVER"),
        "client_id": getattr(settings, "AWS_IOT_CLIENT_ID"),
        "cert_path": getattr(settings, "AWS_IOT_CERT_PATH"),
        "key_path": getattr(settings, "AWS_IOT_KEY_PATH"),
        "root_cert_path": getattr(settings, "AWS_IOT_ROOT_CERT_PATH"),
    }

    return _connect_aws_iot(**credentials)


def mqtt_publish(topic, data):
    """
    Publish a message to AWS IoT by providing a topic path and data object

    :param topic: str, Topic path
    :param data: dict, JSON serializable message to be published
    """
    if not getattr(settings, "AWS_IOT_ENABLED", False):
        logger.info("AWS IoT is not enabled")
        return

    logger.info("Begin Publish")

    connection = mqtt_connection()
    connection.publish(
        topic=topic,
        payload=json.dumps(data),
        qos=mqtt.QoS.AT_LEAST_ONCE,
    )
    logger.info("Published: '" + json.dumps(data) + "' to the topic: " + topic)

    disconnect_future = connection.disconnect()
    disconnect_future.result()
    logger.info('Disconnected!')
