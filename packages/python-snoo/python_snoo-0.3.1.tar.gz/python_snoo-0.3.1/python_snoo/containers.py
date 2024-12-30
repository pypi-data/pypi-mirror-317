import dataclasses
from enum import StrEnum

from mashumaro.mixins.json import DataClassJSONMixin


class SnooStates(StrEnum):
    baseline = "BASELINE"
    level1 = "LEVEL1"
    level2 = "LEVEL2"
    level3 = "LEVEL3"
    level4 = "LEVEL4"
    stop = "ONLINE"
    pretimeout = "PRETIMEOUT"
    timeout = "TIMEOUT"


class SnooEvents(StrEnum):
    ACTIVITY_BUTTON = "activity_button"
    TIMER = "timer"
    POWER_BUTTON = "power_button"
    CRY = "cry"
    COMMAND = "command"
    SAFETY_CLIP = "safety_clip"
    LONG_ACTIVITY_PRESS = "long_activity_press"
    RESTART = "restart"
    INITIAL_STATUS_REQUESTED = "initial_status_requested"
    STATUS_REQUESTED = "status_requested"


@dataclasses.dataclass
class AuthorizationInfo:
    snoo: str
    aws_access: str
    aws_id: str
    aws_refresh: str


@dataclasses.dataclass
class SnooDevice(DataClassJSONMixin):
    serialNumber: str
    deviceType: int
    firmwareVersion: str
    babyIds: list[str]
    name: str
    presence: dict
    presenceIoT: dict
    awsIoT: dict
    lastSSID: dict
    provisionedAt: str


@dataclasses.dataclass
class SnooStateMachine(DataClassJSONMixin):
    up_transition: str
    since_session_start_ms: int
    sticky_white_noise: str
    weaning: str
    time_left: int
    session_id: str
    state: SnooStates
    is_active_session: bool
    down_transition: str
    hold: str
    audio: str


@dataclasses.dataclass
class SnooData(DataClassJSONMixin):
    left_safety_clip: int
    rx_signal: dict
    right_safety_clip: int
    sw_version: str
    event_time_ms: int
    state_machine: SnooStateMachine
    system_state: str
    event: SnooEvents
