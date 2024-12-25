from typing_extensions import override

from masterpiece import Application
from juham.core import Juham
from juham.app import JApp
from juham.simulation import EnergyMeterSimulator
from juham.shelly import ShellyPlusAddOnSimulator
from juham.automation import RPowerPlan


class MyHomeApp(JApp):
    """Juham home automation application."""

    shelly_temperature = "shellyplus1-a0a3b3c309c4"  # temperature sensors
    shelly_boilerradiator = "shellyplus1-alakerta"  # hot water heating relay

    def __init__(self, name: str = "myhome"):
        """Creates home automation application with the given name."""
        super().__init__(name)
        self.instantiate_classes()

    @override
    def instantiate_classes(self) -> None:
        super().instantiate_classes()
        # generate simulated energy meter readings
        self.add(EnergyMeterSimulator("powerconsumption"))

        # generate simulated  temperature readings
        self.add(ShellyPlusAddOnSimulator(self.shelly_temperature))

        # Heating plan for the main boiler
        self.add(RPowerPlan("boiler", "temperature/102", 0, 3, 0.15))

        # .todo: actual relay controllers that perate on the power plan

        # print the instance hierarchy
        self.print()


def main() -> None:
    id = "myhome"
    Juham.mqtt_root_topic = id
    Application.init_app_id(id)
    Application.register_plugin_group(id)
    MyHomeApp.load_plugins()
    app = MyHomeApp(id)
    app.run_forever()


if __name__ == "__main__":
    main()
