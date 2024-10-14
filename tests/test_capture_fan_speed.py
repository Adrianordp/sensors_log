import unittest

import pytest

from src.sensors_log.__main__ import capture_fan_speeds


@pytest.fixture
def sensors_out():
    return """
    acpitz-virtual-0
    Adapter: Virtual device
    temp1:         +27.0 C  (crit = +105.0 C)

    coretemp-isa-0000
    Adapter: ISA adapter
    Core 0:       +35.0 C  (high = +80.0 C, crit = +100.0 C)

    coretemp-isa-0001
    Adapter: ISA adapter
    Core 1:       +34.0 C  (high = +80.0 C, crit = +100.0 C)

    it8720-isa-0290
    Adapter: ISA adapter
    Vcore Voltage:      +0.96 V  (min =  +0.00 V, max =  +1.74 V)
    in0:            +1.01 V  (min =  +0.00 V, max =  +1.74 V)
    3VSB Voltage:      +3.33 V  (min =  +0.00 V, max =  +3.32 V)
    CPU Temperature:   +34.0 C  (high = +80.0 C, hyst = +75.0 C)
    MB Temperature:    +27.0 C  (high = +80.0 C, hyst = +75.0 C)
    Temp3:           +35.0 C  (high = +80.0 C, hyst = +75.0 C)
    Temp4:           +27.0 C  (high = +80.0 C, hyst = +75.0 C)
    Temp5:           +27.0 C  (high = +80.0 C, hyst = +75.0 C)
    Temp6:           +29.5 C  (high = +80.0 C, hyst = +75.0 C)
    Temp7:           +27.0 C  (high = +80.0 C, hyst = +75.0 C)
    Temp8:           +29.5 C  (high = +80.0 C, hyst = +75.0 C)
    fan1:           722 RPM  (min =  616 RPM, div = 2)
    fan2:           771 RPM  (min =  616 RPM, div = 2)
    fan3:           769 RPM  (min =  616 RPM, div = 2)
    """


def test_capture_fan_speed(sensors_out):
    assert capture_fan_speeds(sensors_out.splitlines()) == "722,771,769"
