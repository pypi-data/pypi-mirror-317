"""CCL device mapping."""

from __future__ import annotations

import logging
import time
from typing import Callable

from .sensor import CCLSensor, CCL_SENSORS

_LOGGER = logging.getLogger(__name__)

CCL_DEVICE_INFO_TYPES = ("serial_no", "mac_address", "model", "fw_ver")


class CCLDevice:
    """Mapping for a CCL device."""
    _binary_sensors: dict[str, CCLSensor] | None = {}
    _fw_ver: str | None
    _last_updated_time: float | None
    _mac_address: str | None
    _model: str | None
    _new_binary_sensor_callbacks = set()
    _new_sensors: list[CCLSensor] | None = []
    _new_sensor_callbacks = set()
    _sensors: dict[str, CCLSensor] | None = {}
    _serial_no: str | None
    _update_callbacks = set()
    

    def __init__(self, passkey: str):
        """Initialize a CCL device."""
        _LOGGER.debug("Initializing CCL Device: %s", self)
        self._passkey = passkey

    @property
    def passkey(self) -> str:
        """Return the passkey."""
        return self._passkey

    @property
    def device_id(self) -> str | None:
        """Return the device ID."""
        return self._mac_address.replace(":", "").lower()[-6:]

    @property
    def name(self) -> str | None:
        """Return the display name."""
        return self._model + " - " + self.device_id

    @property
    def mac_address(self) -> str | None:
        """Return the MAC address."""
        return self._mac_address

    @property
    def model(self) -> str | None:
        """Return the model."""
        return self._model

    @property
    def fw_ver(self) -> str | None:
        """Return the firmware version."""
        return self._fw_ver

    @property
    def binary_sensors(self) -> dict[str, CCLSensor] | None:
        """Store binary sensor data under this device."""
        return self._binary_sensors

    @property
    def sensors(self) -> dict[str, CCLSensor] | None:
        """Store sensor data under this device."""
        return self._sensors

    def update_info(self, info: dict[str, None | str]) -> None:
        """Add or update device info."""
        self._mac_address = info.get("mac_address")
        self._model = info.get("model")
        self._fw_ver = info.get("fw_ver")

    def update_sensors(self, sensors: dict[str, None | str | int | float]) -> None:
        """Add or update all sensor values."""
        for key, value in sensors.items():
            if CCL_SENSORS.get(key).binary:
                if key not in self._binary_sensors:
                    self._binary_sensors[key] = CCLSensor(key)
                    self._new_sensors.append(self._binary_sensors[key])
                self._binary_sensors[key].value = value
            else:
                if key not in self._sensors:
                    self._sensors[key] = CCLSensor(key)
                    self._new_sensors.append(self._sensors[key])
                self._sensors[key].value = value
        self._publish_new_sensors()
        self._publish_updates()
        self._last_updated_time = time.monotonic()
        _LOGGER.debug("Sensors Updated: %s", self._last_updated_time)

    def register_update_cb(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Sensor changes state."""
        self._update_callbacks.add(callback)

    def remove_update_cb(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._update_callbacks.discard(callback)

    def _publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        try:
            for callback in self._update_callbacks:
                callback()
        except Exception as err:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Error while publishing sensor updates: %s", err)

    def register_new_binary_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Sensor changes state."""
        self._new_binary_sensor_callbacks.add(callback)

    def remove_new_binary_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._new_binary_sensor_callbacks.discard(callback)

    def register_new_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Sensor changes state."""
        self._new_sensor_callbacks.add(callback)

    def remove_new_sensor_cb(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._new_sensor_callbacks.discard(callback)

    def _publish_new_sensors(self) -> None:
        """Schedule call all registered callbacks."""
        for sensor in self._new_sensors[:]:
            try:
                _LOGGER.debug("Publishing new sensor: %s", sensor)
                if sensor.binary:
                    for callback in self._new_binary_sensor_callbacks:
                        callback(sensor)
                else:
                    for callback in self._new_sensor_callbacks:
                        callback(sensor)
                self._new_sensors.remove(sensor)
            except Exception as err:  # pylint: disable=broad-exception-caught
                _LOGGER.warning("Error while publishing new sensors: %s", err)
