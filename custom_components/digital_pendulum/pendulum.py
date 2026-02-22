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
    CONF_ANNOUNCE_INTERVAL,
    CONF_ANNOUNCE_DAY_OF_WEEK,
    CONF_DAY_ANNOUNCE_HOUR,
    CONF_PAUSE_FOR_ANNOUNCEMENT,
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
    DEFAULT_ANNOUNCE_INTERVAL,
    DEFAULT_ANNOUNCE_DAY_OF_WEEK,
    DEFAULT_DAY_ANNOUNCE_HOUR,
    DEFAULT_PAUSE_FOR_ANNOUNCEMENT,
    DEFAULT_VOICE_ANNOUNCEMENT,
    DEFAULT_PLAYER_TYPE,
    DEFAULT_TTS_ENTITY,
    DEFAULT_VOLUME,
    DEFAULT_CHIME_DELAY,
    PRESET_CHIMES,
    DOMAIN,
)

# ---------------------------------------------------------------------------
# Czech hour announcements (full hours)
# ---------------------------------------------------------------------------
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

# Czech accusative forms for "čtvrt na X" / "tři čtvrtě na X"
# Key = hour (0-23); next hour (H+1) in 12-hour accusative
_CS_ACC = {
    0: "jednu", 1: "dvě", 2: "tři", 3: "čtyři",
    4: "pět", 5: "šest", 6: "sedm", 7: "osm",
    8: "devět", 9: "deset", 10: "jedenáct", 11: "dvanáct",
    12: "jednu", 13: "dvě", 14: "tři", 15: "čtyři",
    16: "pět", 17: "šest", 18: "sedm", 19: "osm",
    20: "devět", 21: "deset", 22: "jedenáct", 23: "dvanáct",
}

# ---------------------------------------------------------------------------
# Day-of-week names (weekday(): 0=Monday … 6=Sunday)
# ---------------------------------------------------------------------------
_DAYS = {
    "cs": ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "de": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
    "es": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
    "it": ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"],
    "fr": ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
}

_DAY_PREFIX = {
    "cs": "Dnes je",
    "en": "Today is",
    "de": "Heute ist",
    "es": "Hoy es",
    "it": "Oggi è",
    "fr": "Aujourd'hui c'est",
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
        self.enabled = config.get(CONF_ENABLED, DEFAULT_ENABLED)
        self.use_chime = config.get(CONF_USE_CHIME, DEFAULT_USE_CHIME)
        self.preset_chime = config.get(CONF_PRESET_CHIME, DEFAULT_PRESET_CHIME)
        self.custom_chime_path = config.get(CONF_CUSTOM_CHIME_PATH, DEFAULT_CUSTOM_CHIME_PATH)
        self.tower_clock = config.get(CONF_TOWER_CLOCK, DEFAULT_TOWER_CLOCK)
        self.voice_announcement = config.get(CONF_VOICE_ANNOUNCEMENT, DEFAULT_VOICE_ANNOUNCEMENT)
        self.player_type = config.get(CONF_PLAYER_TYPE, DEFAULT_PLAYER_TYPE)
        self.tts_entity = config.get(CONF_TTS_ENTITY, DEFAULT_TTS_ENTITY)
        self.volume = int(config.get(CONF_VOLUME, DEFAULT_VOLUME))
        self.chime_delay = float(config.get(CONF_CHIME_DELAY, DEFAULT_CHIME_DELAY))
        self.announce_day_of_week = config.get(CONF_ANNOUNCE_DAY_OF_WEEK, DEFAULT_ANNOUNCE_DAY_OF_WEEK)
        self.day_announce_hour = int(config.get(CONF_DAY_ANNOUNCE_HOUR, DEFAULT_DAY_ANNOUNCE_HOUR))
        self.pause_for_announcement = config.get(CONF_PAUSE_FOR_ANNOUNCEMENT, DEFAULT_PAUSE_FOR_ANNOUNCEMENT)

        # Feature 10: player(s) as list (backward compat with single string)
        raw_player = config.get(CONF_PLAYER_DEVICE)
        if isinstance(raw_player, list):
            self.players = raw_player
        elif raw_player:
            self.players = [raw_player]
        else:
            self.players = []

        # Feature 2: announce interval in minutes (15 / 30 / 60)
        # Backward compat: if new key missing, derive from old announce_half_hours bool
        if CONF_ANNOUNCE_INTERVAL in config:
            self.announce_interval = int(config[CONF_ANNOUNCE_INTERVAL])
        elif config.get(CONF_ANNOUNCE_HALF_HOURS, DEFAULT_ANNOUNCE_HALF_HOURS):
            self.announce_interval = 30
        else:
            self.announce_interval = 60

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

        # Feature 2: interval-based trigger (15 / 30 / 60 min)
        if minute % self.announce_interval != 0:
            return

        if hour < self.start_hour or hour > self.end_hour:
            return
        if hour == self.end_hour and minute > 0:
            return

        text = self._build_text(hour, minute, local_time)
        await self._speak(text, hour, minute)

    # ------------------------------------------------------------------
    # Text building
    # ------------------------------------------------------------------

    def _build_text(self, hour: int, minute: int, local_time=None) -> str:
        """Build announcement text using translations."""
        language = self.hass.config.language
        translations = self._get_translations(language)

        # --- time portion ---

        if language == "cs":
            text = self._build_text_cs(hour, minute)

        elif language == "de" and minute == 30:
            next_hour = (hour + 1) % 24
            text = translations.get("hour_and_half", "Es ist halb {next_hour}").format(next_hour=next_hour)

        elif language == "de" and minute == 15:
            text = f"Es ist Viertel nach {hour}"

        elif language == "de" and minute == 45:
            text = f"Es ist Viertel vor {(hour + 1) % 24}"

        elif language == "es" and (hour % 12 == 1):
            if minute == 0:
                text = "Es la una"
            elif minute == 15:
                text = "Es la una y cuarto"
            elif minute == 30:
                text = "Es la una y media"
            elif minute == 45:
                text = "Son las dos menos cuarto"
            else:
                text = f"Es la una y {minute:02d}"

        elif language == "it":
            hour_text = "una" if hour == 1 else str(hour)
            if minute == 0:
                text = f"Ore {hour_text}"
            elif minute == 15:
                text = f"Ore {hour_text} e quindici"
            elif minute == 30:
                text = f"Ore {hour_text} e trenta"
            elif minute == 45:
                text = f"Ore {hour_text} e quarantacinque"
            else:
                text = f"Ore {hour_text} e {minute:02d}"

        else:
            # English, French, Spanish (non-1 o'clock), and fallback
            if minute == 0:
                text = translations.get("hour", f"Ore {hour}").format(hour=hour)
            elif minute == 15:
                text = translations.get("hour_and_quarter", f"It's {hour} fifteen").format(hour=hour)
            elif minute == 30:
                text = translations.get("hour_and_half", f"Ore {hour} e trenta").format(hour=hour)
            elif minute == 45:
                text = translations.get("hour_and_three_quarter", f"It's {hour} forty-five").format(hour=hour)
            else:
                text = translations.get("hour_and_minutes", f"Ore {hour} e {minute:02d}").format(
                    hour=hour, minutes=f"{minute:02d}"
                )

        # Feature 8: day-of-week suffix at the configured hour on :00
        if self.announce_day_of_week and minute == 0 and hour == self.day_announce_hour and local_time is not None:
            day_names = _DAYS.get(language, _DAYS["en"])
            prefix = _DAY_PREFIX.get(language, "Today is")
            day_name = day_names[local_time.weekday()]
            text = f"{text}. {prefix} {day_name}."

        return text

    def _build_text_cs(self, hour: int, minute: int) -> str:
        if minute == 0:
            return _CS_HOURS.get(hour, f"Je {hour} hodin")
        elif minute == 15:
            acc = _CS_ACC.get(hour, str(hour + 1))
            return f"Je čtvrt na {acc}"
        elif minute == 30:
            return _CS_HALF.get(hour, f"Je půl {(hour + 1) % 24}")
        else:  # 45
            acc = _CS_ACC.get(hour, str(hour + 1))
            return f"Je tři čtvrtě na {acc}"

    def _get_translations(self, language: str) -> dict:
        """Get translations for the given language."""
        fallback = {
            "hour": "It's {hour} o'clock",
            "hour_and_quarter": "It's {hour} fifteen",
            "hour_and_half": "It's {hour} thirty",
            "hour_and_three_quarter": "It's {hour} forty-five",
            "hour_exact": "It's {hour} o'clock exactly",
            "hour_and_minutes": "It's {hour} {minutes}",
        }

        translations = {
            "it": {
                "hour": "Ore {hour}",
                "hour_and_quarter": "Ore {hour} e quindici",
                "hour_and_half": "Ore {hour} e trenta",
                "hour_and_three_quarter": "Ore {hour} e quarantacinque",
                "hour_exact": "Ore {hour} in punto",
                "hour_and_minutes": "Ore {hour} e {minutes}",
            },
            "en": {
                "hour": "It's {hour} o'clock",
                "hour_and_quarter": "It's {hour} fifteen",
                "hour_and_half": "It's {hour} thirty",
                "hour_and_three_quarter": "It's {hour} forty-five",
                "hour_exact": "It's {hour} o'clock exactly",
                "hour_and_minutes": "It's {hour} {minutes}",
            },
            "fr": {
                "hour": "Il est {hour} heures",
                "hour_and_quarter": "Il est {hour} heures et quart",
                "hour_and_half": "Il est {hour} heures trente",
                "hour_and_three_quarter": "Il est {hour} heures moins le quart",
                "hour_exact": "Il est {hour} heures pile",
                "hour_and_minutes": "Il est {hour} heures {minutes}",
            },
            "de": {
                "hour": "Es ist {hour} Uhr",
                "hour_and_quarter": "Es ist Viertel nach {hour}",
                "hour_and_half": "Es ist halb {next_hour}",
                "hour_and_three_quarter": "Es ist Viertel vor {next_hour}",
                "hour_exact": "Es ist genau {hour} Uhr",
                "hour_and_minutes": "Es ist {hour} Uhr {minutes}",
            },
            "es": {
                "hour": "Son las {hour}",
                "hour_and_quarter": "Son las {hour} y cuarto",
                "hour_and_half": "Son las {hour} y media",
                "hour_and_three_quarter": "Son las {hour} y cuarenta y cinco",
                "hour_exact": "Son las {hour} en punto",
                "hour_and_minutes": "Son las {hour} y {minutes}",
            },
            "cs": {
                "hour": "Je {hour} hodin",
                "hour_and_quarter": "Je čtvrt na {next_hour}",
                "hour_and_half": "Je půl {next_hour}",
                "hour_and_three_quarter": "Je tři čtvrtě na {next_hour}",
                "hour_exact": "Je přesně {hour} hodin",
                "hour_and_minutes": "Je {hour} hodin a {minutes} minut",
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
                    "target": self.players,
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
                        "target": self.players,
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
                        "target": self.players,
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
                "entity_id": self.players,
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
                "entity_id": self.players,
                "volume_level": round(self.volume / 100, 2),
            },
            blocking=False,
        )

    # ------------------------------------------------------------------
    # Voice announcement
    # ------------------------------------------------------------------

    async def _speak(self, text: str, hour: int = None, minute: int = None):
        # Feature 9: pause players that are currently playing
        paused_players = []
        if self.pause_for_announcement and self.player_type in ("media_player", "browser_mod"):
            for player in self.players:
                state = self.hass.states.get(player)
                if state and state.state == "playing":
                    await self.hass.services.async_call(
                        "media_player",
                        "media_pause",
                        {"entity_id": player},
                        blocking=True,
                    )
                    paused_players.append(player)

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

        # Feature 9: resume after estimated TTS playback duration
        if paused_players:
            tts_wait = max(4.0, len(text) * 0.1 + 2.0)
            await asyncio.sleep(tts_wait)
            for player in paused_players:
                await self.hass.services.async_call(
                    "media_player",
                    "media_play",
                    {"entity_id": player},
                    blocking=False,
                )

    async def _speak_alexa(self, text: str):
        """Announce via Alexa Media Player."""
        data = {"type": "tts"}
        if self.volume > 0:
            data["volume"] = self.volume
        await self.hass.services.async_call(
            "notify",
            "alexa_media",
            {
                "target": self.players,
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
        for player in self.players:
            await self.hass.services.async_call(
                "tts",
                "speak",
                {
                    "entity_id": self.tts_entity,
                    "media_player_entity_id": player,
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

        elif language == "es" and (hour % 12 == 1):
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
