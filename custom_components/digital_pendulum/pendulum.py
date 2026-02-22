import asyncio
import os
from datetime import datetime, timedelta
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util
from .const import (
    CONF_START_HOUR,
    CONF_END_HOUR,
    CONF_PLAYER_DEVICE,
    CONF_ENABLED,
    CONF_USE_CHIME,
    CONF_CUSTOM_CHIME_PATH,
    CONF_PRESET_CHIME,
    CONF_TOWER_CLOCK,
    CONF_ANNOUNCE_HALF_HOURS,
    CONF_VOICE_ANNOUNCEMENT,
    CONF_PLAYER_TYPE,
    CONF_TTS_ENTITY,
    CONF_VOLUME,
    CONF_CHIME_DELAY,
    DEFAULT_START_HOUR,
    DEFAULT_END_HOUR,
    DEFAULT_ENABLED,
    DEFAULT_USE_CHIME,
    DEFAULT_CUSTOM_CHIME_PATH,
    DEFAULT_PRESET_CHIME,
    DEFAULT_TOWER_CLOCK,
    DEFAULT_ANNOUNCE_HALF_HOURS,
    DEFAULT_VOICE_ANNOUNCEMENT,
    DEFAULT_PLAYER_TYPE,
    DEFAULT_TTS_ENTITY,
    DEFAULT_VOLUME,
    DEFAULT_CHIME_DELAY,
    PRESET_CHIMES,
    DOMAIN,
)

# Czech hour announcements (full hours)
_CS_HOURS = {
    0:  "Je půlnoc",
    1:  "Je jedna hodina",
    2:  "Jsou dvě hodiny",
    3:  "Jsou tři hodiny",
    4:  "Jsou čtyři hodiny",
    5:  "Je pět hodin",
    6:  "Je šest hodin",
    7:  "Je sedm hodin",
    8:  "Je osm hodin",
    9:  "Je devět hodin",
    10: "Je deset hodin",
    11: "Je jedenáct hodin",
    12: "Je dvanáct hodin",
    13: "Je třináct hodin",
    14: "Je čtrnáct hodin",
    15: "Je patnáct hodin",
    16: "Je šestnáct hodin",
    17: "Je sedmnáct hodin",
    18: "Je osmnáct hodin",
    19: "Je devatenáct hodin",
    20: "Je dvacet hodin",
    21: "Je dvacet jedna hodin",
    22: "Je dvacet dvě hodiny",
    23: "Je dvacet tři hodiny",
}

# Czech half-hour announcements ("půl druhé" = 1:30, "půl třetí" = 2:30, …)
_CS_HALF = {
    0:  "Je půl jedné",
    1:  "Je půl druhé",
    2:  "Je půl třetí",
    3:  "Je půl čtvrté",
    4:  "Je půl páté",
    5:  "Je půl šesté",
    6:  "Je půl sedmé",
    7:  "Je půl osmé",
    8:  "Je půl deváté",
    9:  "Je půl desáté",
    10: "Je půl jedenácté",
    11: "Je půl dvanácté",
    12: "Je půl jedné",
    13: "Je půl druhé",
    14: "Je půl třetí",
    15: "Je půl čtvrté",
    16: "Je půl páté",
    17: "Je půl šesté",
    18: "Je půl sedmé",
    19: "Je půl osmé",
    20: "Je půl deváté",
    21: "Je půl desáté",
    22: "Je půl jedenácté",
    23: "Je půl dvanácté",
}


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
        self.preset_chime = config.get(CONF_PRESET_CHIME, DEFAULT_PRESET_CHIME)
        self.custom_chime_path = config.get(CONF_CUSTOM_CHIME_PATH, DEFAULT_CUSTOM_CHIME_PATH)
        self.tower_clock = config.get(CONF_TOWER_CLOCK, DEFAULT_TOWER_CLOCK)
        self.announce_half_hours = config.get(CONF_ANNOUNCE_HALF_HOURS, DEFAULT_ANNOUNCE_HALF_HOURS)
        self.voice_announcement = config.get(CONF_VOICE_ANNOUNCEMENT, DEFAULT_VOICE_ANNOUNCEMENT)
        self.player_type = config.get(CONF_PLAYER_TYPE, DEFAULT_PLAYER_TYPE)
        self.tts_entity = config.get(CONF_TTS_ENTITY, DEFAULT_TTS_ENTITY)
        self.volume = int(config.get(CONF_VOLUME, DEFAULT_VOLUME))
        self.chime_delay = float(config.get(CONF_CHIME_DELAY, DEFAULT_CHIME_DELAY))

    def update_config(self):
        """Update configuration when options change."""
        self._load_config()

    async def async_start(self):
        self._unsub_timer = async_track_time_change(
            self.hass,
            self._time_tick,
            second=0,
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

        if minute == 30 and not self.announce_half_hours:
            return

        if hour < self.start_hour or hour > self.end_hour:
            return
        if hour == self.end_hour and minute > 0:
            return

        text = self._build_text(hour, minute)
        await self._speak(text, hour, minute)

    def _build_text(self, hour: int, minute: int) -> str:
        """Build announcement text using translations."""
        language = self.hass.config.language
        translations = self._get_translations(language)

        # Czech — grammatically correct forms for each hour and half-hour
        if language == "cs":
            if minute == 30:
                return _CS_HALF.get(hour, f"Je půl {(hour + 1) % 24}")
            else:
                return _CS_HOURS.get(hour, f"Je {hour} hodin")

        # German — "halb X" means half an hour before X
        if language == "de" and minute == 30:
            next_hour = (hour + 1) % 24
            return translations.get("hour_and_half", "Es ist halb {next_hour}").format(next_hour=next_hour)

        # Spanish — singular "la una" for 1 o'clock
        if language == "es" and (hour == 1 or hour == 13):
            if minute == 30:
                return "Es la una y media"
            else:
                return "Es la una"

        # Italian — "una" instead of "1"
        if language == "it":
            hour_text = "una" if hour == 1 else str(hour)
            if minute == 30:
                return f"Ore {hour_text} e trenta"
            else:
                return f"Ore {hour_text}"

        # All other languages (English, French, …)
        if minute == 30:
            return translations.get("hour_and_half", f"Ore {hour} e trenta").format(hour=hour)
        else:
            return translations.get("hour", f"Ore {hour}").format(hour=hour)

    def _get_translations(self, language: str) -> dict:
        """Get translations for the given language."""
        fallback = {
            "hour": "Ore {hour}",
            "hour_and_half": "Ore {hour} e trenta",
            "hour_exact": "Ore {hour} in punto",
            "hour_and_minutes": "Ore {hour} e {minutes}"
        }

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
            },
            "cs": {
                "hour": "Je {hour} hodin",
                "hour_and_half": "Je půl {next_hour}",
                "hour_exact": "Je přesně {hour} hodin",
                "hour_and_minutes": "Je {hour} hodin a {minutes} minut"
            },
        }

        return translations.get(language, fallback)

    # ------------------------------------------------------------------
    # Chime playback
    # ------------------------------------------------------------------

    async def _play_chime(self, hour: int = None, minute: int = None):
        """Play chime sound (custom, default, or Westminster for tower clock)."""
        if self.tower_clock and hour == 12 and minute == 0:
            await self._play_westminster()
            return

        if self.preset_chime or self.custom_chime_path:
            await self._play_custom_chime()
        else:
            await self._play_default_chime()

    async def _play_default_chime(self):
        """Play default announce chime (Alexa only; skipped for other player types)."""
        if self.player_type == "alexa":
            data = {"type": "announce"}
            if self.volume > 0:
                data["volume"] = self.volume
            await self.hass.services.async_call(
                "notify",
                "alexa_media",
                {
                    "target": self.player,
                    "data": data,
                    "message": " ",
                },
                blocking=False,
            )

    async def _play_westminster(self):
        """Play Westminster chime for tower clock at 12:00."""
        westminster_url = "https://raw.githubusercontent.com/Dregi56/digital_pendulum/main/sounds/westminster.mp3"

        if self.player_type == "alexa":
            try:
                data = {"type": "tts"}
                if self.volume > 0:
                    data["volume"] = self.volume
                await self.hass.services.async_call(
                    "notify",
                    "alexa_media",
                    {
                        "target": self.player,
                        "message": f"<audio src='{westminster_url}'/>",
                        "data": data,
                    },
                    blocking=False,
                )
            except Exception:
                await self._play_default_chime()
        else:
            await self._play_media_url(westminster_url)

    async def _play_custom_chime(self):
        """Play custom audio file or preset chime."""
        chime_url = None

        if self.preset_chime and self.preset_chime != "custom":
            chime_info = PRESET_CHIMES.get(self.preset_chime)
            if chime_info and chime_info["url"]:
                chime_url = chime_info["url"]
        elif self.preset_chime == "custom" and self.custom_chime_path and self.custom_chime_path.strip():
            chime_url = self.custom_chime_path.strip()

        if not chime_url:
            await self._play_default_chime()
            return

        if self.player_type == "alexa":
            try:
                data = {"type": "tts"}
                if self.volume > 0:
                    data["volume"] = self.volume
                await self.hass.services.async_call(
                    "notify",
                    "alexa_media",
                    {
                        "target": self.player,
                        "message": f"<audio src='{chime_url}'/>",
                        "data": data,
                    },
                    blocking=False,
                )
            except Exception:
                await self._play_default_chime()
        else:
            await self._play_media_url(chime_url)

    async def _play_media_url(self, url: str):
        """Play an audio URL on a generic HA media_player or browser_mod entity."""
        if self.volume > 0:
            await self._set_volume_media_player()
        await self.hass.services.async_call(
            "media_player",
            "play_media",
            {
                "entity_id": self.player,
                "media_content_id": url,
                "media_content_type": "music",
            },
            blocking=False,
        )

    async def _set_volume_media_player(self):
        """Set volume on generic media_player entity (0–100 → 0.0–1.0)."""
        await self.hass.services.async_call(
            "media_player",
            "volume_set",
            {
                "entity_id": self.player,
                "volume_level": round(self.volume / 100, 2),
            },
            blocking=False,
        )

    # ------------------------------------------------------------------
    # Voice announcement
    # ------------------------------------------------------------------

    async def _speak(self, text: str, hour: int = None, minute: int = None):
        if self.use_chime:
            await self._play_chime(hour, minute)
            await asyncio.sleep(self.chime_delay)

        if self.voice_announcement:
            if self.player_type == "alexa":
                await self._speak_alexa(text)
            elif self.player_type == "media_player":
                await self._speak_media_player(text)
            elif self.player_type == "browser_mod":
                await self._speak_browser_mod(text)

    async def _speak_alexa(self, text: str):
        """Announce via Alexa Media Player."""
        data = {"type": "tts"}
        if self.volume > 0:
            data["volume"] = self.volume
        await self.hass.services.async_call(
            "notify",
            "alexa_media",
            {
                "target": self.player,
                "message": text,
                "data": data,
            },
            blocking=False,
        )

    async def _speak_media_player(self, text: str):
        """Announce via any HA media_player using tts.speak (e.g. Google Home)."""
        if not self.tts_entity:
            return
        if self.volume > 0:
            await self._set_volume_media_player()
        await self.hass.services.async_call(
            "tts",
            "speak",
            {
                "entity_id": self.tts_entity,
                "media_player_entity_id": self.player,
                "message": text,
                "language": self.hass.config.language,
            },
            blocking=False,
        )

    async def _speak_browser_mod(self, text: str):
        """Show a browser notification via browser_mod."""
        await self.hass.services.async_call(
            "browser_mod",
            "notification",
            {
                "message": text,
                "duration": 10000,
            },
            blocking=False,
        )

    # ------------------------------------------------------------------
    # Test announcement
    # ------------------------------------------------------------------

    async def async_test_announcement(self):
        """Immediate announcement with the full current time."""
        now = dt_util.now()
        hour = now.hour
        minute = now.minute

        language = self.hass.config.language

        if language == "cs":
            hour_sentence = _CS_HOURS.get(hour, f"Je {hour} hodin")
            if minute == 0:
                text = hour_sentence
            else:
                text = f"{hour_sentence} a {minute} minut"

        elif language == "it":
            hour_text = "una" if hour == 1 else str(hour)
            if minute == 0:
                text = f"Ore {hour_text} in punto"
            else:
                text = f"Ore {hour_text} e {minute:02d}"

        elif language == "es" and (hour == 1 or hour == 13):
            if minute == 0:
                text = "Es la una en punto"
            else:
                text = f"Es la una y {minute:02d}"

        else:
            translations = self._get_translations(language)
            if minute == 0:
                text = translations.get("hour_exact", f"Ore {hour} in punto").format(hour=hour)
            else:
                text = translations.get("hour_and_minutes", f"Ore {hour} e {minute:02d}").format(
                    hour=hour, minutes=f"{minute:02d}"
                )

        await self._speak(text)
