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
    dev = BioshakeDevice()
    dev = BioshakeDevice() # Automatically finds device if one available
    dev = BioshakeDevice('/dev/ttyACM0') # Linux specific port
    dev = BioshakeDevice('/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = BioshakeDevice('COM3') # Windows specific port
    dev.get_description()
    dev.set_shake_target_speed(1000)
    dev.shake_on()
    dev.shake_off()
    dev.set_temp_target(45)
    dev.temp_on()
    dev.temp_off()
    devs = BioshakeDevices()  # Automatically finds all available devices
    dev = devs[0]

