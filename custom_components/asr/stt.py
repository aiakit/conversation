"""The HomingAI STT integration."""


from __future__ import annotations
import logging
import voluptuous as vol
from collections.abc import AsyncIterable
import aiohttp

from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY
from homeassistant.components import stt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
)

_LOGGER = logging.getLogger(__name__)

# 简化配置，只需要API密钥
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
    }
)

SUPPORTED_LANGUAGES = ["zh-CN"]  # 支持的语言
DEFAULT_LANG = "zh-CN"


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HomingAISTT(hass, config_entry)])


class HomingAISTT(stt.SpeechToTextEntity):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Init HomingAI STT Entity."""
        hass.data.setdefault(DOMAIN, {})
        self.api_key = config_entry.data[CONF_API_KEY]
        self._attr_name = 'HomingAI_STT'
        self._attr_unique_id = f"{config_entry.entry_id[:7]}-stt"
        self.api_url = "https://api.homingai.com/ha/home/asr"

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return SUPPORTED_LANGUAGES

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return a list of supported formats."""
        return [AudioFormats.WAV]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        """Return a list of supported bitrates."""
        return [AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        """Return a list of supported samplerates."""
        return [AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        """Return a list of supported channels."""
        return [AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
            self, metadata: SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> SpeechResult:
        """Process audio stream to text using HomingAI API."""
        _LOGGER.debug("HomingAI Speech to text process started")

        # 收集音频数据
        audio_data = bytes()
        async for chunk in stream:
            audio_data += chunk

        _LOGGER.debug(f"Processing audio stream: {len(audio_data)} bytes")

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/octet-stream"
                }

                async with session.post(
                        self.api_url,
                        data=audio_data,
                        headers=headers
                ) as response:
                    response_json = await response.json()

                    if response.status == 200:
                        text = response_json.get("text", "")
                        return SpeechResult(text, SpeechResultState.SUCCESS)
                    else:
                        error_msg = response_json.get("error", "Unknown error")
                        _LOGGER.error(f"API Error: {error_msg}")
                        return SpeechResult(
                            f"识别失败: {error_msg}",
                            SpeechResultState.ERROR
                        )

        except Exception as err:
            _LOGGER.exception("Error processing audio stream: %s", err)
            return SpeechResult(
                "语音识别服务连接失败，请检查网络或API密钥",
                SpeechResultState.ERROR
            )
