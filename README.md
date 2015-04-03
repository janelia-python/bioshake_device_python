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
dev = BioshakeDevice() # Automatically finds device if one available
dev = BioshakeDevice('/dev/ttyACM0') # Linux specific port
dev = BioshakeDevice('/dev/tty.usbmodem262471') # Mac OS X specific port
dev = BioshakeDevice('COM3') # Windows specific port
dev.get_device_info()
dev.get_methods()
devs = BioshakeDevices()  # Automatically finds all available devices
devs.items()
dev = devs[name][serial_number]
```

More Detailed Examples:

<https://github.com/JaneliaSciComp/bioshake_device_arduino>

##Installation

###Install Latest Version of Arduino on your Host Machine

<http://arduino.cc/en/Guide/HomePage>

On linux, you may need to add yourself to the group 'dialout' in order
to have write permissions on the USB port:

```shell
sudo usermod -aG dialout $USER
```

###Linux and Mac OS X

[Setup Python for Linux](./PYTHON_SETUP_LINUX.md)

[Setup Python for Mac OS X](./PYTHON_SETUP_MAC_OS_X.md)

```shell
mkdir -p ~/virtualenvs/bioshake_device
virtualenv ~/virtualenvs/bioshake_device
source ~/virtualenvs/bioshake_device/bin/activate
pip install bioshake_device
```

###Windows

[Setup Python for Windows](./PYTHON_SETUP_WINDOWS.md)

```shell
virtualenv C:\virtualenvs\bioshake_device
C:\virtualenvs\bioshake_device\Scripts\activate
pip install bioshake_device
```
