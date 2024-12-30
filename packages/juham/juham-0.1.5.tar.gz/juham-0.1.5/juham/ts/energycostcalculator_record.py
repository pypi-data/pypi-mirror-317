from typing import Any
from typing_extensions import override
import json

from masterpiece.mqtt import MqttMsg

from juham.core import Juham
from juham.core.time import (
    epoc2utc,
    timestampstr,
)


class EnergyCostCalculatorRecord(Juham):
    """The EnergyCostCalculator recorder."""

    def __init__(self, name: str = "ecc_record") -> None:
        super().__init__(name)
        self.topic_net_energy_balance = self.make_topic_name("net_energy_cost")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic_net_energy_balance)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        super().on_message(client, userdata, msg)
        if msg.topic == self.topic_net_energy_balance:
            m = json.loads(msg.payload.decode())
            self.record_powerconsumption(m)

    def record_powerconsumption(self, m: dict[str, Any]) -> None:
        """Record powerconsumption

        Args:
            m (dict[str, Any]): to be recorded
        """
        site: str = m["site"]
        cost_hour: float = m["cost_hour"]
        cost_day: float = m["cost_day"]
        ts: float = m["ts"]

        try:
            point = (
                self.measurement("energycost")
                .tag("site", site)
                .field("cost", cost_hour)
                .field("cost_day", cost_day)
                .time(epoc2utc(ts))
            )
            self.write(point)

        except Exception as e:
            self.error(f"Cannot write energycost at {timestampstr(ts)}", str(e))
