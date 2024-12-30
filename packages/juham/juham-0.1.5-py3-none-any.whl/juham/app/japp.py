from masterpiece import Application
from juham.core import Juham
from juham.ts import (
    ForecastRecord,
    PowerRecord,
    PowerPlanRecord,
    PowerMeterRecord,
    LogRecord,
    EnergyCostCalculatorRecord,
)
from juham.web import SpotHintaFi
from juham.automation import EnergyCostCalculator


class JApp(Application):
    """Juham home automation application base class. Registers new plugin
    group 'juham' on which general purpose Juham plugins can be written on.
    """

    def __init__(self, name: str) -> None:
        """Creates home automation application with the given name.
        If --enable_plugins is False create hard coded configuration
        by calling instantiate_classes() method.

        Args:
            name (str): name for the application
        """
        super().__init__(name, Juham(name))

    def instantiate_classes(self) -> None:
        """Instantiate automation classes .

        Returns:
            None
        """
        self.add(ForecastRecord())
        self.add(PowerRecord())
        self.add(PowerPlanRecord())
        self.add(PowerMeterRecord())
        self.add(LogRecord())
        self.add(SpotHintaFi())
        self.add(EnergyCostCalculator())
        self.add(EnergyCostCalculatorRecord())

        # install plugins
        self.add(self.instantiate_plugin_by_name("SystemStatus"))
        self.add(self.instantiate_plugin_by_name("VisualCrossing"))
        self.add(self.instantiate_plugin_by_name("OpenWeatherMap"))

    @classmethod
    def register(cls) -> None:
        """Register plugin group `juham`."""
        Application.register_plugin_group("juham")
