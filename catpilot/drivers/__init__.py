from .ft817 import FT817, FT818, FT857, FT897
from .sim import SimDriver

DRIVERS = {
    "Yaesu FT-817": FT817,
    "Yaesu FT-818": FT818,
    "Yaesu FT-857": FT857,
    "Yaesu FT-897": FT897,
    "Simulateur (sans poste)": SimDriver,
}


def _remote():
    from ..remote import RemoteDriver
    return RemoteDriver


DRIVERS = {**DRIVERS, "Poste distant (CAT Pilot)": _remote()
}
