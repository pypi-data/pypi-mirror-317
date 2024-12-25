from typing_extensions import override

from masterpiece import Application

from juham.web import HomeWizardWaterMeter
from juham.shelly import (
    ShellyPlus1,
    ShellyPlusAddOn,
    Shelly1G3,
    ShellyPro3EM,
    ShellyMotion,
    ShellyPro3,
)
from juham.automation import RPowerPlan, WaterCirculator
from juham.app import JApp


class Kerttula(JApp):
    """Kerttula home automation application."""

    shelly_temperature = "shellyplus1-a0a3b3c309c4"  # four temperature sensors
    shelly_mainboilerradiator = "shellyplus1-alakerta"  # hot water heating relay
    shelly_sunboilerradiator = "shellypro3-alakerta"  # sun pre-heating relay

    def __init__(self, name: str = "kerttula") -> None:
        """Creates home automation application with the given name.
        If --enable_plugins is False create hard coded configuration
        by calling instantiate_classes() method.

        Args:
            name (str): name for the application
        """
        super().__init__(name)
        self.instantiate_classes()

    @override
    def instantiate_classes(self) -> None:
        super().instantiate_classes()
        self.add(HomeWizardWaterMeter())

        # for publishing temperature sensor readings to Juham mqtt network
        self.add(ShellyPlusAddOn(self.shelly_temperature))  # for temperature sensors
        self.add(ShellyPlusAddOn(self.shelly_mainboilerradiator))  # main boiler heating

        self.add(Shelly1G3())  # humidity

        self.add(ShellyPro3EM())  # energy meter
        self.add(ShellyMotion())  # motion sensor

        # heating plans for the both heating boiler radiators
        self.add(RPowerPlan("main_boiler", "temperature/102", 0, 3, 0.15))
        self.add(RPowerPlan("sun_boiler", "temperature/101", 3, 2, 0.02))

        # relay controllers
        self.add(
            ShellyPlus1(
                "main_boiler_relay", "main_boiler", self.shelly_mainboilerradiator
            )
        )
        self.add(
            ShellyPro3(
                "sun_boiler_relay",
                "sun_boiler",
                self.shelly_sunboilerradiator,
                True,
                False,
                False,
            )
        )

        self.add(WaterCirculator())

        # show the instance hierarchy
        self.print()


def main() -> None:
    id: str = "kerttula"
    Kerttula.init_app_id(id)
    Application.register_plugin_group(id)
    Kerttula.load_plugins()
    Application.load_configuration()

    app = Kerttula(id)

    # app.serialize()

    # start the network loops
    app.run_forever()


if __name__ == "__main__":
    main()
