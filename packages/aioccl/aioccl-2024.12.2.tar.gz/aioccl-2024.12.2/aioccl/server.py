"""CCL API server and handler."""

from __future__ import annotations

import logging
from typing import Callable

from aiohttp import web

from .device import CCLDevice, CCL_DEVICE_INFO_TYPES
from .sensor import CCL_SENSORS

_LOGGER = logging.getLogger(__name__)


class CCLServer:
    """Represent a CCL server manager."""

    LISTEN_PORT = 42373

    devices: dict[str, CCLDevice] = {}

    @staticmethod
    def register(device: CCLDevice) -> None:
        """Register a device with a passkey."""
        CCLServer.devices.setdefault(device.passkey, device)
        _LOGGER.debug("Device registered: %s", CCLServer.devices)

    @staticmethod
    def get_handler() -> Callable[[web.BaseRequest], web.Response]:
        """Get the handler."""
        return CCLServer._handler
    
    @staticmethod
    async def _handler(request: web.BaseRequest) -> web.Response:
        """Handle POST requests for data updating."""
        _body: dict[str, None | str | int | float] = {}
        _device: CCLDevice = None
        _info: dict[str, None | str] = {}
        _passkey: str = ''
        _sensors: dict[str, None | str | int | float] = {}
        _status: None | int = None
        _text: None | str = None

        try:
            for passkey, _device in CCLServer.devices.items():
                if passkey == request.match_info["passkey"]:
                    _passkey = passkey
                    break
            assert _device, 404

            assert request.content_type == "application/json", 400
            assert 0 < request.content_length <= 5000, 400

            _body = await request.json()

        except Exception as err:  # pylint: disable=broad-exception-caught
            _status = err.args[0]
            if _status == 400:
                _text = "400 Bad Request"
            elif _status == 404:
                _text = "404 Not Found"
            else:
                _status = 500
                _text = "500 Internal Server Error"
            _LOGGER.debug("Request exception occured: %s", err)
            return web.Response(status=_status, text=_text)

        
        for key, value in _body.items():
            if key in CCL_DEVICE_INFO_TYPES:
                _info.setdefault(key, value)
            elif key in CCL_SENSORS:
                _sensors.setdefault(key, value)

        _device.update_info(_info)
        _device.update_sensors(_sensors)
        _status = 200
        _text = "200 OK"
        _LOGGER.debug("Request processed: %s", _passkey)
        return web.Response(status=_status, text=_text)

    app = web.Application()
    app.add_routes([web.get('/{passkey}', _handler)])
    runner = web.AppRunner(app)

    @staticmethod
    async def run() -> None:
        """Try to run the API server."""
        try:
            _LOGGER.debug("Trying to start the API server.")
            await CCLServer.runner.setup()
            site = web.TCPSite(CCLServer.runner, port=CCLServer.LISTEN_PORT)
            await site.start()
        except Exception as err:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Failed to run the API server: %s", err)
        else:
            _LOGGER.debug("Successfully started the API server.")

    @staticmethod
    async def stop() -> None:
        """Stop running the API server."""
        await CCLServer.runner.cleanup()
