from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Digital Pendulum binary sensor."""
    pendulum = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DigitalPendulumStatusSensor(pendulum, entry)])


class DigitalPendulumStatusSensor(BinarySensorEntity):
    """Binary sensor che mostra se l'integrazione è disabilitata."""

    _attr_has_entity_name = True
    _attr_name = "Status Warning"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, pendulum, entry):
        self.pendulum = pendulum
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_status_warning"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Digital Pendulum",
            "manufacturer": "Custom",
            "model": "Digital Pendulum",
        }

    @property
    def is_on(self):
        """Return True if integration is disabled (warning state)."""
        return not self.pendulum.enabled  # True = warning

    @property
    def icon(self):
        """Return icon based on state."""
        if self.is_on:  # Disabled = warning
            return "mdi:alert-circle"
        return "mdi:check-circle"

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {
            "integration_enabled": self.pendulum.enabled,
            "start_hour": self.pendulum.start_hour,
            "end_hour": self.pendulum.end_hour,
        }
