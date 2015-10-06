bioshake_device_python
======================

This Python package (bioshake\_device) creates a class named
BioshakeDevice, which contains an instance of
serial\_device2.SerialDevice and adds methods to it to interface to
Q.instruments BioShake devices.

Authors::

    Peter Polidoro <polidorop@janelia.hhmi.org>

License::

    BSD

Example Usage::

    from bioshake_device import BioshakeDevice
    dev = BioshakeDevice() # Might automatically find device if one available
    # if it is not found automatically, specify port directly
    dev = BioshakeDevice(port='/dev/ttyUSB0') # Linux
    dev = BioshakeDevice(port='/dev/tty.usbmodem262471') # Mac OS X
    dev = BioshakeDevice(port='COM3') # Windows
    dev.get_description()
    dev.shake_on(speed_target=1000) # speed_target (rpm)
    dev.get_shake_actual_speed()
    dev.shake_off()
    dev.temp_on(temp_target=45) # temp_target (°C)
    dev.get_temp_actual()
    dev.temp_off()
    devs = BioshakeDevices()  # Might automatically find all available devices
    # if they are not found automatically, specify ports to use
    devs = BioshakeDevices(use_ports=['/dev/ttyUSB0','/dev/ttyUSB1']) # Linux
    devs = BioshakeDevices(use_ports=['/dev/tty.usbmodem262471','/dev/tty.usbmodem262472']) # Mac OS X
    devs = BioshakeDevices(use_ports=['COM3','COM4']) # Windows
    dev = devs[0]

