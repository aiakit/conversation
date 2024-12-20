"""Config flow for HomingAI Conversation integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_ACCESS_TOKEN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_TOKEN): str,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """验证用户输入的配置。"""
    session = async_get_clientsession(hass)
    headers = {
        "Authorization": f"Bearer {data[CONF_ACCESS_TOKEN]}",
        "Content-Type": "application/json"
    }

    try:
        async with session.post(
            "https://api.homingai.com/ha/home/validate",
            headers=headers,
            json={},
        ) as response:
            if response.status != 200:
                _LOGGER.error("验证失败，状态码: %s", response.status)
                raise InvalidAuth

            result = await response.json()
            if result.get("code") != 200:
                _LOGGER.error("验证失败，返回码: %s", result.get("code"))
                raise InvalidAuth

    except aiohttp.ClientError as err:
        _LOGGER.error("连接到 HomingAI API 失败: %s", err)
        raise CannotConnect from err

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HomingAI Conversation."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # 创建唯一ID，防止重复配置
                await self.async_set_unique_id(user_input[CONF_ACCESS_TOKEN])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="HomingAI Conversation",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

class CannotConnect(Exception):
    """Error to indicate we cannot connect."""

class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
