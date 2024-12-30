import json
from typing import Any, Dict
from typing_extensions import override

from masterpiece.mqtt import MqttMsg

from juham.core.time import epoc2utc, timestamp
from .shelly import Shelly


class ShellyDHT22(Shelly):
    """Shelly Plus add-on with DHT22 humidity, temperature sensor.

    Listens MQTT messages from dht22 (am2302) humidity sensor attached to
    Shelly add-on module and writes them to time series database.
    """

    _DHT22: str = "_dht22"
    shelly_topic = "/events/rpc"  # source topic

    def __init__(self, name: str, mqtt_prefix: str) -> None:
        super().__init__(name, mqtt_prefix)
        self.relay_started: float = 0
        self.temperature_topic = self.make_topic_name("temperature/")  # target topic
        self.humidity_topic = self.make_topic_name("humidity/")  # target topic

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.mqtt_prefix + self.shelly_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        # optimize out excessive notifications
        tsnow = timestamp()
        self.relay_started = tsnow

        m = json.loads(msg.payload.decode())
        mth = m["method"]
        if mth == "NotifyStatus":
            params = m["params"]
            self.on_sensor(params)
        else:
            self.warning("Unknown method " + mth, str(m))

    def on_sensor(self, params: dict[str, Any]) -> None:
        """Map Shelly Plus 1GM specific event to juham format and post it to
        temperature topic.

        Args:
            params (dict): message from Shelly Plus 1 wifi relay
        """
        ts = params["ts"]
        for key, value in params.items():
            if key.startswith("humidity:"):
                self.on_value(ts, key, value, "humidity", "rh")
            elif key.startswith("temperature:"):
                self.on_value(ts, key, value, "temperature", "tC")
            else:
                # self.warning(
                #    f"Unknown msg {self.name} {self.mqtt_prefix}: {key}", value
                # )
                pass

    def on_value(
        self, ts: float, key: str, value: dict[str, Any], attr: str, unit: str
    ) -> None:
        sensor_id = key.split(":")[1]
        humidity = value[unit]

        msg = {
            "sensor": sensor_id,
            "timestamp": ts,
            attr: float(humidity),
        }
        self.publish(self.humidity_topic + sensor_id, json.dumps(msg), 1, True)
        # self.debug(
        #    f"Sensor reading {self.humidity_topic}{sensor_id} {attr} = {humidity}"
        # )
        try:
            point = (
                self.measurement(self.name)
                .tag("sensor", sensor_id)
                .field(attr, humidity)
                .time(epoc2utc(ts))
            )
            self.write(point)
        except Exception as e:
            self.error(f"Writing to influx failed {str(e)}")

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data[self._DHT22] = {
            "shelly_topic": self.shelly_topic,
            "temperature_topic": self.temperature_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if self._DHT22 in data:
            for key, value in data[self._DHT22].items():
                setattr(self, key, value)
