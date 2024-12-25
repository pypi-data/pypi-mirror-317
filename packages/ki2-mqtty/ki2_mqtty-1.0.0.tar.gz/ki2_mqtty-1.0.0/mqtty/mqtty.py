from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Optional, Self, Buffer, Protocol
import json


if TYPE_CHECKING:
    from ki2_python_utils import Json
    from .types import MqttCallback


class SerialLike(Protocol):
    def write(self, data: Buffer, /) -> int | None: ...

    def read(self, size: int = 1) -> bytes: ...

    def reset_input_buffer(self) -> None: ...

    def reset_output_buffer(self) -> None: ...

    @property
    def in_waiting(self) -> int: ...

    @property
    def out_waiting(self) -> int: ...


class MqttyDevice:
    _serial: SerialLike

    on_mqtt_message: Optional[MqttCallback]

    __endline_char: str
    __mqtt_start_char: str
    __mqtt_separator_char: str

    __message_buffer: str

    def __init__(
        self,
        serial: SerialLike,
        endline_char: str = "\n",
        mqtt_start: str = "@",
        mqtt_separator: str = ":",
    ) -> None:
        self.on_mqtt_message = None
        self._serial = serial
        self.__endline_char = endline_char
        self.__mqtt_start_char = mqtt_start
        self.__mqtt_separator_char = mqtt_separator
        self.__message_buffer = ""

        if len(self.__endline_char) != 1:
            raise ValueError("endline_char must be a single character")

    def set_callback(self, cb: MqttCallback, /) -> Self:
        self.on_mqtt_message = cb
        return self

    def _raw_send(self, payload: str) -> Self:
        payload += self.__endline_char
        self._serial.write(payload.encode("utf-8"))
        return self

    def send(self, payload: str | Json) -> Self:
        if isinstance(payload, str):
            return self._raw_send(payload)
        return self._raw_send(json.dumps(payload))

    def _handle_unique_message(self, message: str) -> None:
        if message.startswith(self.__mqtt_start_char):
            message = message[1:]
            split_idx = message.find(self.__mqtt_separator_char)
            if split_idx < 0:
                print(f"Invalid message: {message}")
                return
            topic = message[:split_idx]
            payload = message[split_idx + 1 :]
            if self.on_mqtt_message is not None:
                self.on_mqtt_message(topic, payload)
            else:
                print(f"Unhandled message: {message}")
            return

    def _handle_stream(self, new_data: str) -> None:
        split_idx = new_data.find(self.__endline_char)
        if split_idx < 0:
            self.__message_buffer += new_data
            return

        base = new_data[:split_idx]
        rest = new_data[split_idx + 1 :]

        unique_message = self.__message_buffer + base
        self.__message_buffer = ""
        self._handle_unique_message(unique_message)

        if len(rest) > 0:
            self._handle_stream(rest)

        return

    def tick_read(self) -> None:
        if self._serial.in_waiting <= 0:
            return

        new_data = self._serial.read(self._serial.in_waiting).decode("utf-8")

        self._handle_stream(new_data)

    def reset_input_buffer(self) -> None:
        self._serial.reset_input_buffer()


def serial_device_factory(
    port: str | None = None,
    baudrate: int = 9600,
    bytesize: int = 8,
    parity: str = "N",
    stopbits: float = 1,
    timeout: float | None = None,
    xonxoff: bool = False,
    rtscts: bool = False,
    write_timeout: float | None = None,
    dsrdtr: bool = False,
    inter_byte_timeout: float | None = None,
    exclusive: bool | None = None,
    endline_char: str = "\n",
    mqtt_start: str = "@",
    mqtt_separator: str = ":",
) -> MqttyDevice:
    from serial import Serial

    serial = Serial(
        port,
        baudrate,
        bytesize,
        parity,
        stopbits,
        timeout,
        xonxoff,
        rtscts,
        write_timeout,
        dsrdtr,
        inter_byte_timeout,
        exclusive,
    )
    return MqttyDevice(serial, endline_char, mqtt_start, mqtt_separator)
