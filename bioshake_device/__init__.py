'''
This Python package (bioshake_device) creates a class named
BioshakeDevice, which contains an instance of
serial_device2.SerialDevice and adds methods to it to interface to
Q.instruments BioShake devices.
'''
from bioshake_device import BioshakeDevice, BioshakeDevices, BioshakeError, find_bioshake_device_ports, find_bioshake_device_port, __version__
