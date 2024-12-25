"""Http data source classes.

Data acquisition classes for reading information, e.g forecast, through
http url.
"""

from .homewizardwatermeter import HomeWizardWaterMeter
from .spothintafi import SpotHintaFi

__all__ = [
    "HomeWizardWaterMeter",
    "SpotHintaFi",
]
