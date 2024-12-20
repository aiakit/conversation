"""The HomingAI Conversation integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the HomingAI Conversation component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HomingAI Conversation from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Forward the setup to the conversation platform using the new method
    await hass.config_entries.async_forward_entry_setups(entry, ["conversation"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload HomingAI Conversation config entry."""
    # Use the corresponding unload method
    await hass.config_entries.async_unload_platforms(entry, ["conversation"])
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
