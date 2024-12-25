from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Optional, Any, Coroutine
import asyncio

from .manager import get_manager

if TYPE_CHECKING:
    from .manager import MqttyDevicesManager
    from paho.mqtt.client import Client as PahoMqttClient
    from aiomqtt import Client as AioMqttClient
    from .types import MqttCallback


def connect_paho_mqtt(
    mqtt_client: PahoMqttClient,
    *,
    manager: Optional[MqttyDevicesManager] = None,
    callback: Optional[MqttCallback] = None,
) -> None:
    if TYPE_CHECKING:
        from paho.mqtt.client import MQTTMessage, ConnectFlags
        from paho.mqtt.reasoncodes import ReasonCode
        from paho.mqtt.properties import Properties

    if manager is None:
        manager = get_manager()

    def on_paho_connect(
        client: PahoMqttClient,
        userdata: Any,
        flags: ConnectFlags,
        rc: ReasonCode,
        properties: Properties | None,
    ):
        for topic in manager.topics:
            client.subscribe(topic)

    def on_paho_message(client: PahoMqttClient, userdata: Any, msg: MQTTMessage):
        topic = msg.topic
        payload = msg.payload.decode("utf-8", "ignore")

        if manager.has_topic(topic):
            manager.send(topic, payload)

    def on_serial_message(topic: str, payload: str):
        if mqtt_client.is_connected():
            mqtt_client.publish(topic, payload)
        if callback is not None:
            callback(topic, payload)

    def on_serial_register(topic: str):
        if mqtt_client.is_connected():
            mqtt_client.subscribe(topic)

    manager.on_register = on_serial_register
    manager.on_mqtt_message = on_serial_message
    mqtt_client.on_connect = on_paho_connect
    mqtt_client.on_message = on_paho_message


def connect_aio_mqtt(
    mqtt_client: AioMqttClient,
    *,
    manager: Optional[MqttyDevicesManager] = None,
    callback: Optional[MqttCallback] = None,
    reconnection_interval: float = 5,
):
    from aiomqtt import MqttError, Message

    connected: bool = False

    if manager is None:
        manager = get_manager()

    async def on_aio_connect():
        for topic in manager.topics:
            await mqtt_client.subscribe(topic)

    async def on_aio_message(message: Message):
        topic = message.topic.value
        payload = message.payload
        if isinstance(payload, (bytes, bytearray)):
            payload = payload.decode("utf-8", errors="ignore")
        if not isinstance(payload, str):
            payload = str(payload)
        if manager.has_topic(topic):
            manager.send(topic, payload)

    def async_to_sync(coroutine: Coroutine[Any, Any, None]):
        loop = asyncio.get_running_loop()
        loop.create_task(coroutine)

    def on_serial_register(topic: str):
        async def subscribe():
            await mqtt_client.subscribe(topic)

        if connected:
            async_to_sync(subscribe())

    def on_serial_message(topic: str, payload: str):
        async def publish():
            await mqtt_client.publish(topic, payload)

        if connected:
            async_to_sync(publish())

        if callback is not None:
            callback(topic, payload)

    manager.on_register = on_serial_register
    manager.on_mqtt_message = on_serial_message

    async def loop():
        nonlocal connected
        connected = False
        while True:
            try:
                async with mqtt_client:
                    connected = True
                    await on_aio_connect()
                    async for message in mqtt_client.messages:
                        await on_aio_message(message)

            except MqttError:
                await asyncio.sleep(reconnection_interval)
            finally:
                connected = False

    return loop
