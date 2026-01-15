import asyncio
from datetime import datetime, timedelta

from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import dt as dt_util

from .const import (
    CONF_START_HOUR,
    CONF_END_HOUR,
    CONF_PLAYER_DEVICE,
    CONF_ENABLED,
    CONF_USE_CHIME,
    DEFAULT_START_HOUR,
    DEFAULT_END_HOUR,
    DEFAULT_ENABLED,
    DEFAULT_USE_CHIME,
    DOMAIN, 
)


class DigitalPendulum:
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self._unsub_timer = None
        self._load_config()

    def _load_config(self):
        """Load configuration from entry (options or data)."""
        config = self.entry.options or self.entry.data
        
        self.start_hour = config.get(CONF_START_HOUR, DEFAULT_START_HOUR)
        self.end_hour = config.get(CONF_END_HOUR, DEFAULT_END_HOUR)
        self.player = config.get(CONF_PLAYER_DEVICE)
        self.enabled = config.get(CONF_ENABLED, DEFAULT_ENABLED)
        self.use_chime = config.get(CONF_USE_CHIME, DEFAULT_USE_CHIME)

    def update_config(self):
        """Update configuration when options change."""
        self._load_config()

    async def async_start(self):
        self._unsub_timer = async_track_time_interval(
            self.hass,
            self._time_tick,
            timedelta(minutes=1),
        )

    async def async_stop(self):
        if self._unsub_timer:
            self._unsub_timer()
            self._unsub_timer = None

    async def _time_tick(self, now: datetime):
        if not self.enabled:
            return

        local_time = dt_util.as_local(now)
        
        hour = local_time.hour
        minute = local_time.minute

        if minute not in (0, 30):
            return

        if not (self.start_hour <= hour <= self.end_hour):
            return

        text = self._build_text(hour, minute)
        await self._speak(text)

    def _build_text(self, hour: int, minute: int) -> str:
        """Build announcement text using translations."""
        # Ottieni la lingua di Home Assistant
        language = self.hass.config.language
        
        # Carica le traduzioni
        translations = self._get_translations(language)
        
        if minute == 30:
            # Gestione speciale per tedesco (halb = mezza)
            if language == "de":
                next_hour = (hour + 1) % 24
                return translations.get("hour_and_half", "Es ist halb {next_hour}").format(next_hour=next_hour)
            else:
                return translations.get("hour_and_half", f"Ore {hour} e trenta").format(hour=hour)
        else:
            return translations.get("hour", f"Ore {hour}").format(hour=hour)

    def _get_translations(self, language: str) -> dict:
        """Get translations for the given language."""
        # Traduzioni di fallback (italiano)
        fallback = {
            "hour": "Ore {hour}",
            "hour_and_half": "Ore {hour} e trenta",
            "hour_exact": "Ore {hour} in punto",
            "hour_and_minutes": "Ore {hour} e {minutes}"
        }
        
        # Dizionario completo delle traduzioni
        translations = {
            "it": {
                "hour": "Ore {hour}",
                "hour_and_half": "Ore {hour} e trenta",
                "hour_exact": "Ore {hour} in punto",
                "hour_and_minutes": "Ore {hour} e {minutes}"
            },
            "en": {
                "hour": "It's {hour} o'clock",
                "hour_and_half": "It's {hour} thirty",
                "hour_exact": "It's {hour} o'clock exactly",
                "hour_and_minutes": "It's {hour} {minutes}"
            },
            "fr": {
                "hour": "Il est {hour} heures",
                "hour_and_half": "Il est {hour} heures trente",
                "hour_exact": "Il est {hour} heures pile",
                "hour_and_minutes": "Il est {hour} heures {minutes}"
            },
            "de": {
                "hour": "Es ist {hour} Uhr",
                "hour_and_half": "Es ist halb {next_hour}",
                "hour_exact": "Es ist genau {hour} Uhr",
                "hour_and_minutes": "Es ist {hour} Uhr {minutes}"
            },
            "es": {
                "hour": "Son las {hour}",
                "hour_and_half": "Son las {hour} y media",
                "hour_exact": "Son las {hour} en punto",
                "hour_and_minutes": "Son las {hour} y {minutes}"
            }
        }
        
        return translations.get(language, fallback)

    async def _speak(self, text: str):
        if self.use_chime:
            await self.hass.services.async_call(
                "notify",
                "alexa_media",
                {
                    "target": self.player,
                    "data": {"type": "announce"},
                    "message": " ",
                },
                blocking=False,
            )
            
            await asyncio.sleep(1.5)
        
        await self.hass.services.async_call(
            "notify",
            "alexa_media",
            {
                "target": self.player,
                "message": text,
                "data": {"type": "tts"},
            },
            blocking=False,
        )

    async def async_test_announcement(self):
        """Test immediato dell'annuncio con orario completo."""
        now = dt_util.now()
        hour = now.hour
        minute = now.minute
        
        language = self.hass.config.language
        translations = self._get_translations(language)
        
        if minute == 0:
            text = translations.get("hour_exact", f"Ore {hour} in punto").format(hour=hour)
        else:
            text = translations.get("hour_and_minutes", f"Ore {hour} e {minute:02d}").format(hour=hour, minutes=f"{minute:02d}")
        
        await self._speak(text)