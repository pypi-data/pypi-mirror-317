from typing import Any
from typing_extensions import override
import json

from masterpiece.mqtt import MqttMsg
from juham.core import Juham
from juham.core.time import timestamp, epoc2utc


class WaterCirculator(Juham):
    """Hot water circulation automation.

    Monitors motion sensor data to detect home occupancy.

    When motion is detected: Activates the water circulator pump, ensuring hot water
    is instantly available when the tap is turned on.
    When no motion is detected for a specified uptime (in seconds): Automatically switches
    off the pump to conserve energy.
    """

    uptime = 60 * 60
    min_temperature = 37
    # motion_sensor_topic = "shellies/shellymotion2/info"
    # motion_topics = "shellies/shellymotion2/#"

    def __init__(self, name: str, temperature_sensor: str) -> None:
        super().__init__(name)

        # input topics
        self.motion_topic = self.make_topic_name("motion")  # motion detection
        self.temperature_topic = self.make_topic_name(temperature_sensor)

        # relay to be controlled
        self.topic_power = self.make_topic_name("power")

        # for the pump controlling logic
        self.current_motion: bool = False
        self.relay_started_ts: float = 0
        self.water_temperature: float = 0
        self.water_temperature_updated: float = 0
        self.initialized = False

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.motion_topic)
            self.subscribe(self.temperature_topic)
            # reset the relay to make sure the initial state matches the state of us
            self.publish_power(0)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.temperature_topic:
            m = json.loads(msg.payload.decode())
            self.on_temperature_sensor(m, timestamp())
        elif msg.topic == self.motion_topic:
            m = json.loads(msg.payload.decode())
            self.on_motion_sensor(m, timestamp())
        else:
            super().on_message(client, userdata, msg)

    def on_temperature_sensor(self, m: dict[str, Any], ts_utc_now: float) -> None:
        """Handle message from the hot water pipe temperature sensor.
        Records the temperature and updates the water_temperature_updated attribute.

        Args:
            m (dict): temperature reading from the hot water blump sensor
            ts_utc_now (float): _current utc time
        """

        self.water_temperature = m["temperature"]
        self.water_temperature_updated = ts_utc_now
        # self.info(
        #    f"Temperature of circulating water updated to {self.water_temperature} C"
        # )

    def on_motion_sensor(self, m: dict[str, dict[str, Any]], ts_utc_now: float) -> None:
        """Control the water cirulator bump.

        Given message from the motion sensor consider switching the
        circulator bump on.

        Args:
            msg (dict): directionary holding motion sensor data
            ts_utc_now (float): current time stamp
        """
        sensor = m["sensor"]
        vibration: bool = bool(m["vibration"])
        motion: bool = bool(m["motion"])

        if motion or vibration:
            self.info(f"Life form detected in {sensor}")
            # honey I'm home
            if not self.current_motion:
                if self.water_temperature > self.min_temperature:
                    self.publish_power(0)
                    # self.info(
                    #    f"Circulator: motion detected but water warm already {self.water_temperature} > {self.min_temperature} C"
                    # )
                else:
                    self.current_motion = True
                    self.relay_started_ts = ts_utc_now
                    self.publish_power(1)
                    self.initialized = True
                    self.info(
                        f"Circulator pump started, will run for {int(self.uptime / 60)} minutes "
                    )
            else:
                self.publish_power(1)
                self.relay_started_ts = ts_utc_now
                # self.info(
                #    f"Circulator pump has been running for {int(ts_utc_now - self.relay_started_ts)/60} minutes",
                #    " ",
                # )
        else:
            if self.current_motion or not self.initialized:
                elapsed: float = ts_utc_now - self.relay_started_ts
                if elapsed > self.uptime:
                    self.publish_power(0)
                    self.info(
                        f"Circulator  pump stopped, no motion in {elapsed}/60 minutes detected",
                        "",
                    )
                    self.current_motion = False
                    self.initialized = True
                else:
                    self.publish_power(1)
                    # self.info(
                    #    f"Circulator bump stop countdown {int(self.uptime - (ts_utc_now - self.relay_started_ts ))/60} min"
                    # )
            else:
                self.publish_power(0)
                # self.info(
                #    f"Circulator bump off already, temperature {self.water_temperature} C",
                #    "",
                # )

    def publish_power(self, state: int) -> None:
        """Publish power status.

        Args:
            state (int): 1 for on, 0 for off, as defined by Juham 'power' topic
        """
        heat = {"Unit": self.name, "Timestamp": timestamp(), "State": state}
        self.publish(self.topic_power, json.dumps(heat), 1, False)
