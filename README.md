bioshake_device_python
======================

This Python package (bioshake\_device) creates a class named
BioshakeDevice, which contains an instance of
serial\_device2.SerialDevice and adds methods to it to interface to
Q.instruments BioShake devices.

Authors:

    Peter Polidoro <polidorop@janelia.hhmi.org>

License:

    BSD

##Example Usage


```python
from bioshake_device import BioshakeDevice
dev = BioshakeDevice() # Might automatically find device if one available
# if it is not found automatically, specify port directly
dev = BioshakeDevice(port='/dev/ttyUSB0') # Linux specific port
dev = BioshakeDevice(port='/dev/tty.usbmodem262471') # Mac OS X specific port
dev = BioshakeDevice(port='COM3') # Windows specific port
dev.get_description()
dev.shake_on(speed_target=1000) # speed_target (rpm)
dev.get_shake_actual_speed()
dev.shake_off()
dev.temp_on(temp_target=45) # temp_target (°C)
dev.get_temp_actual()
dev.temp_off()
devs = BioshakeDevices()  # Automatically finds all available devices
dev = devs[0]
```

```python
devs = BioshakeDevices()  # Might automatically find all available devices
# if they are not found automatically, specify ports to try
devs = BioshakeDevices(try_ports=['/dev/ttyUSB0','/dev/ttyUSB1']) # Linux
devs = BioshakeDevices(try_ports=['/dev/tty.usbmodem262471','/dev/tty.usbmodem262472']) # Mac OS X
devs = BioshakeDevices(try_ports=['COM3','COM4']) # Windows
dev = devs[0]
```

##Installation

[Setup Python](https://github.com/janelia-pypi/python_setup)

###Linux and Mac OS X

```shell
mkdir -p ~/virtualenvs/bioshake_device
virtualenv ~/virtualenvs/bioshake_device
source ~/virtualenvs/bioshake_device/bin/activate
pip install bioshake_device
```

###Windows

```shell
virtualenv C:\virtualenvs\bioshake_device
C:\virtualenvs\bioshake_device\Scripts\activate
pip install bioshake_device
```
