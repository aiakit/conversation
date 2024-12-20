"""HomingAI conversation integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, intent
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_ACCESS_TOKEN, DOMAIN, SUPPORTED_LANGUAGES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HomingAI conversation."""
    agent = HomingAIAgent(hass, entry)
    async_add_entities([agent])

class HomingAIAgent(conversation.ConversationEntity, conversation.AbstractConversationAgent):
    """HomingAI conversation agent."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.entry = entry
        self._attr_unique_id = entry.entry_id
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="HomingAI",
            model="HomingAI Conversation",
            entry_type=dr.DeviceEntryType.SERVICE,
        )
        self.access_token = entry.data[CONF_ACCESS_TOKEN]
        self.session = async_get_clientsession(hass)

    async def async_added_to_hass(self) -> None:
        """When entity is added to Home Assistant."""
        await super().async_added_to_hass()
        
        # 设置为默认代理
        conversation.async_set_agent(self.hass, self.entry, self, is_default=True)
        
        # 设置首选本地处理命令为开启状态
        if "conversation" in self.hass.data:
            conversation_data = self.hass.data["conversation"]
            if hasattr(conversation_data, "config"):
                conversation_data.config.update({
                    "default_agent": "local",
                    "debug": False
                })
        
        # 如果需要，可以触发配置更新
        await self.hass.config.async_update()

    async def async_will_remove_from_hass(self) -> None:
        """When entity will be removed from Home Assistant."""
        conversation.async_unset_agent(self.hass, self.entry)
        await super().async_will_remove_from_hass()

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return SUPPORTED_LANGUAGES

    async def async_process(
        self,
        user_input: conversation.ConversationInput,
        context: dict[str, Any] | None = None,
        conversation_id: str | None = None,
    ) -> conversation.ConversationResult:
        """Process a sentence."""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            async with self.session.post(
                "https://api.homingai.com/ha/home/chat",
                headers=headers,
                json={
                    "content": user_input.text,
                    "language": user_input.language,
                    "conversation_id": conversation_id,
                    "context": context or {},
                },
            ) as response:
                if response.status != 200:
                    _LOGGER.error(
                        "Error calling HomingAI API: %s", response.status
                    )
                    intent_response = intent.IntentResponse(language=user_input.language)
                    intent_response.async_set_error(
                        intent.IntentResponseErrorCode.UNKNOWN,
                        "抱歉，服务器连接失败。"
                    )
                    return conversation.ConversationResult(
                        response=intent_response,
                        conversation_id=conversation_id,
                    )

                result = await response.json()
                
                intent_response = intent.IntentResponse(language=user_input.language)
                if result.get("code") == 200:
                    intent_response.async_set_speech(result.get("msg", ""))
                    return conversation.ConversationResult(
                        response=intent_response,
                        conversation_id=conversation_id,
                    )
                else:
                    _LOGGER.error(
                        "HomingAI API returned error: %s", result.get("msg")
                    )
                    intent_response.async_set_error(
                        intent.IntentResponseErrorCode.UNKNOWN,
                        f"抱歉，出现错误: {result.get('msg', '未知错误')}"
                    )
                    return conversation.ConversationResult(
                        response=intent_response,
                        conversation_id=conversation_id,
                    )

        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to HomingAI API: %s", err)
            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                "抱歉，无法连接到服务器。"
            )
            return conversation.ConversationResult(
                response=intent_response,
                conversation_id=conversation_id,
            )
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected error processing HomingAI conversation: %s", err)
            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                "抱歉，处理请求时出现意外错误。"
            )
            return conversation.ConversationResult(
                response=intent_response,
                conversation_id=conversation_id,
            )
