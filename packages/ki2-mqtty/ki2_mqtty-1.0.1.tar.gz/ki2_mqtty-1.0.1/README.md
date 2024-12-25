# mqtty

**mqtty** is a flexible Python package that bridges MQTT communication with serial devices. It provides an agnostic approach to MQTT client libraries, supporting both `paho-mqtt` and `aiomqtt` through helper functions, while allowing developers to manage multiple serial devices seamlessly.

## Key Features

- **Serial Device Integration**: Easily connect serial devices using `serial_device_factory` and register them under unique MQTT topics.
- **Execution Mode Flexibility**: Choose between synchronous (threaded) or asynchronous modes to suit your application's requirements.
- **MQTT Client Agnostic**: Use your preferred MQTT library, with helper functions like `connect_paho_mqtt` and `connect_aio_mqtt`.
- **Multi-Device Management**: Use the `manager` to register and manage multiple serial devices, routing messages between MQTT topics and serial ports effortlessly.

## Installation

Install **mqtty** via pip:

```bash
pip install ki2-mqtty
```

## Quick Start

Here are examples of how to use **mqtty** in synchronous and asynchronous modes.

### Synchronous Example

```python
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from mqtty import serial_device_factory, manager_setup, connect_paho_mqtt

def main():
    mqttclient = mqtt.Client(CallbackAPIVersion.VERSION2)

    device = serial_device_factory("/dev/ttyACM0")
    manager = manager_setup("threaded").register("device-topic", device)

    connect_paho_mqtt(mqttclient, manager=manager)

    manager.start()
    mqttclient.connect("localhost", 1883, 60)
    mqttclient.loop_forever()

if __name__ == "__main__":
    main()
```

### Asynchronous Example

```python
from datetime import datetime
import asyncio

from aiomqtt import Client as AioMqttClient

from ki2_python_utils import run_parallel
from mqtty import serial_device_factory, manager_setup, connect_aio_mqtt

async def main():
    mqttclient = AioMqttClient("localhost", 1883)

    device = serial_device_factory("/dev/ttyACM0")
    manager = manager_setup("async").register("device-topic", device)

    mqtt_loop = connect_aio_mqtt(mqttclient, manager=manager)

    await run_parallel(
        manager.loop,
        mqtt_loop,
    )

if __name__ == "__main__":
    asyncio.run(main())
```

## How It Works

1. **Device Registration**: Use `serial_device_factory` to create a serial device and register it with the `manager`. Each device is associated with an MQTT topic for message routing.
2. **Manager Setup**: Initialize the `manager` in either "threaded" or "async" mode, depending on your application's requirements.
3. **MQTT Integration**: Use the provided helper functions to connect the `manager` to your MQTT client (`paho-mqtt` or `aiomqtt`).
4. **Run Your Application**: Start the `manager` and MQTT client loop to enable communication.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
