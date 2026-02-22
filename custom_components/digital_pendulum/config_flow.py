import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import (
    DOMAIN,
    CONF_START_HOUR,
    CONF_END_HOUR,
    CONF_PLAYER_DEVICE,
    CONF_ENABLED,
    CONF_USE_CHIME,
    CONF_CUSTOM_CHIME_PATH,
    CONF_PRESET_CHIME,
    CONF_TOWER_CLOCK,
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
    PLAYER_TYPES,
)


def _player_type_options():
    labels = {
        "alexa": "Amazon Alexa",
        "media_player": "Media Player (Google Home, Sonos, …)",
        "browser_mod": "Browser Mod",
    }
    return [
        selector.SelectOptionDict(value=pt, label=labels.get(pt, pt))
        for pt in PLAYER_TYPES
    ]


def _interval_options():
    return [
        selector.SelectOptionDict(value="60", label="Every hour (:00)"),
        selector.SelectOptionDict(value="30", label="Every 30 min (:00, :30)"),
        selector.SelectOptionDict(value="15", label="Every 15 min (:00, :15, :30, :45)"),
    ]


def _build_schema(current=None):
    """Build the shared vol.Schema for both ConfigFlow and OptionsFlow."""
    c = current or {}

    def get(key, default):
        return c.get(key, default)

    chime_options = [
        selector.SelectOptionDict(value=key, label=info["name"])
        for key, info in PRESET_CHIMES.items()
    ]

    # Interval: stored as int or str – normalise to str for the selector
    interval_default = str(get(CONF_ANNOUNCE_INTERVAL, DEFAULT_ANNOUNCE_INTERVAL))

    return vol.Schema(
        {
            # 1) Player type
            vol.Required(
                CONF_PLAYER_TYPE,
                default=get(CONF_PLAYER_TYPE, DEFAULT_PLAYER_TYPE),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_player_type_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            # 2) Player device(s) — multiple selection (Feature 10)
            vol.Required(
                CONF_PLAYER_DEVICE,
                default=get(CONF_PLAYER_DEVICE, []),
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="media_player",
                    multiple=True,
                )
            ),
            # 3) TTS entity (for media_player / browser_mod types)
            vol.Optional(
                CONF_TTS_ENTITY,
                default=get(CONF_TTS_ENTITY, DEFAULT_TTS_ENTITY),
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="tts",
                )
            ),
            # 4) Operating window
            vol.Required(
                CONF_START_HOUR,
                default=get(CONF_START_HOUR, DEFAULT_START_HOUR),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=23,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_END_HOUR,
                default=get(CONF_END_HOUR, DEFAULT_END_HOUR),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=23,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            # 5) Enabled
            vol.Required(
                CONF_ENABLED,
                default=get(CONF_ENABLED, DEFAULT_ENABLED),
            ): bool,
            # 6) Announce interval (Feature 2)
            vol.Required(
                CONF_ANNOUNCE_INTERVAL,
                default=interval_default,
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_interval_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_VOICE_ANNOUNCEMENT,
                default=get(CONF_VOICE_ANNOUNCEMENT, DEFAULT_VOICE_ANNOUNCEMENT),
            ): bool,
            # 7) Tower Clock
            vol.Required(
                CONF_TOWER_CLOCK,
                default=get(CONF_TOWER_CLOCK, DEFAULT_TOWER_CLOCK),
            ): bool,
            # 8) Chime
            vol.Required(
                CONF_USE_CHIME,
                default=get(CONF_USE_CHIME, DEFAULT_USE_CHIME),
            ): bool,
            # 9) Preset chime
            vol.Required(
                CONF_PRESET_CHIME,
                default=get(CONF_PRESET_CHIME, DEFAULT_PRESET_CHIME),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=chime_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            # 10) Custom chime path
            vol.Optional(
                CONF_CUSTOM_CHIME_PATH,
                default=get(CONF_CUSTOM_CHIME_PATH, DEFAULT_CUSTOM_CHIME_PATH),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                )
            ),
            # 11) Chime-to-voice delay
            vol.Required(
                CONF_CHIME_DELAY,
                default=get(CONF_CHIME_DELAY, DEFAULT_CHIME_DELAY),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=15,
                    step=0.5,
                    mode=selector.NumberSelectorMode.SLIDER,
                    unit_of_measurement="s",
                )
            ),
            # 12) Volume
            vol.Required(
                CONF_VOLUME,
                default=get(CONF_VOLUME, DEFAULT_VOLUME),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=100,
                    step=5,
                    mode=selector.NumberSelectorMode.SLIDER,
                    unit_of_measurement="%",
                )
            ),
            # 13) Day-of-week announcement (Feature 8)
            vol.Required(
                CONF_ANNOUNCE_DAY_OF_WEEK,
                default=get(CONF_ANNOUNCE_DAY_OF_WEEK, DEFAULT_ANNOUNCE_DAY_OF_WEEK),
            ): bool,
            vol.Required(
                CONF_DAY_ANNOUNCE_HOUR,
                default=get(CONF_DAY_ANNOUNCE_HOUR, DEFAULT_DAY_ANNOUNCE_HOUR),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=23,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            # 14) Pause media during announcement (Feature 9)
            vol.Required(
                CONF_PAUSE_FOR_ANNOUNCEMENT,
                default=get(CONF_PAUSE_FOR_ANNOUNCEMENT, DEFAULT_PAUSE_FOR_ANNOUNCEMENT),
            ): bool,
        }
    )


class DigitalPendulumConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle initial configuration."""
        if user_input is not None:
            # Normalise interval to int
            user_input[CONF_ANNOUNCE_INTERVAL] = int(user_input[CONF_ANNOUNCE_INTERVAL])
            return self.async_create_entry(
                title="Digital Pendulum",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema(),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return DigitalPendulumOptionsFlow(config_entry)


class DigitalPendulumOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Digital Pendulum."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            user_input[CONF_ANNOUNCE_INTERVAL] = int(user_input[CONF_ANNOUNCE_INTERVAL])
            return self.async_create_entry(title="", data=user_input)

        current = self.entry.options or self.entry.data

        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(current),
        )
