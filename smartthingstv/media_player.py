"""Support for interface with an Samsung TV."""
import logging
import voluptuous as vol

from .smartthingstv.api import smartthingstv as smarttv

from homeassistant.components.media_player import (
    MediaPlayerDevice,
    PLATFORM_SCHEMA,
    DEVICE_CLASS_SPEAKER,
)
from homeassistant.components.media_player.const import (
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_SELECT_SOURCE,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_STEP,
    SUPPORT_VOLUME_SET
)
from homeassistant.const import (
    CONF_NAME, CONF_API_KEY, CONF_DEVICE_ID
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "SamsungTVRemote"

SUPPORT_SAMSUNGTV = (
        SUPPORT_PAUSE
        | SUPPORT_VOLUME_STEP
        | SUPPORT_VOLUME_MUTE
        | SUPPORT_VOLUME_SET
        | SUPPORT_SELECT_SOURCE
        | SUPPORT_TURN_OFF
        | SUPPORT_TURN_ON
        | SUPPORT_PLAY
        | SUPPORT_PAUSE
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_DEVICE_ID): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Samsung TV platform."""
    name = config.get(CONF_NAME)
    api_key = config.get(CONF_API_KEY)
    device_id = config.get(CONF_DEVICE_ID)
    add_entities([smartthingstv(name, api_key, device_id)])


class smartthingstv(MediaPlayerDevice):
    """Representation of a Samsung TV."""

    def __init__(self, name, api_key, device_id):
        """Initialize the Samsung device."""

        # Save a reference to the imported classes
        self._name = name
        self._device_id = device_id
        self._api_key = api_key
        self._volume = 1
        self._muted = False
        self._playing = True
        self._state = "on"
        self._source = ""
        self._source_list = []
        self._media_title = ""

    def update(self):
        """Update state of device."""
        smarttv.device_update(self)

    def turn_off(self):
        arg = ""
        cmdtype = "switch_off"
        smarttv.send_command(self, arg, cmdtype)

    def turn_on(self):
        arg = ""
        cmdtype = "switch_on"
        smarttv.send_command(self, arg, cmdtype)

    def set_volume_level(self, arg, cmdtype="setvolume"):
        VOLUME_LEVEL = int(arg * 100)
        smarttv.send_command(self, VOLUME_LEVEL, cmdtype)

    def mute_volume(self, mute, cmdtype="audiomute"):
        smarttv.send_command(self, mute, cmdtype)

    def volume_up(self, cmdtype="stepvolume"):
        """Volume up the media player."""
        arg = "up"
        smarttv.send_command(self, arg, cmdtype)

    def volume_down(self, cmdtype="stepvolume"):
        arg = ""
        smarttv.send_command(self, arg, cmdtype)

    def select_source(self, source, cmdtype="selectsource"):
        smarttv.send_command(self, source, cmdtype)

    @property
    def device_class(self):
        """Set the device class to TV."""
        return DEVICE_CLASS_SPEAKER

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_SAMSUNGTV

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def media_title(self):
        """Title of current playing media."""
        return self._media_title

    def media_play(self):
        """Send play command."""
        arg = ""
        cmdtype = "play"
        smarttv.send_command(self, arg, cmdtype)

    def media_pause(self):
        """Send pause command."""
        arg = ""
        cmdtype = "pause"
        smarttv.send_command(self, arg, cmdtype)

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def is_volume_muted(self):
        """Boolean if volume is currently muted."""
        return self._muted

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def source(self):
        return self._source

    @property
    def source_list(self):
        return self._source_list
