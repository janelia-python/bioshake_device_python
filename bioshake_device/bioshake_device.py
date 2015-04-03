from __future__ import print_function, division
import serial
import time
import atexit
import platform
import os
from exceptions import Exception

from serial_device2 import SerialDevice, SerialDevices, find_serial_device_ports, WriteFrequencyError

try:
    from pkg_resources import get_distribution, DistributionNotFound
    _dist = get_distribution('bioshake_device')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'bioshake_device')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except (ImportError,DistributionNotFound):
    __version__ = None
else:
    __version__ = _dist.version


DEBUG = False
BAUDRATE = 9600

class BioshakeError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BioshakeDevice(object):
    '''
    This Python package (bioshake\_device) creates a class named
    BioshakeDevice, which contains an instance of
    serial\_device2.SerialDevice and adds methods to it to interface to
    Q.instruments BioShake devices.

    Example Usage:

    dev = BioshakeDevice() # Automatically finds device if one available
    dev = BioshakeDevice('/dev/ttyUSB0') # Linux
    dev = BioshakeDevice('/dev/tty.usbmodem262471') # Mac OS X
    dev = BioshakeDevice('COM3') # Windows
    dev.get_device_info()
    dev.get_methods()
    '''
    _TIMEOUT = 0.05
    _WRITE_WRITE_DELAY = 0.05
    _RESET_DELAY = 2.0
    _DEFAULT_TARGET_SPEED = 1000
    _SHAKE_STATE_DESCRIPTIONS = {
        0: 'Shaking is active',
        1: 'Shaker has a stop command detect',
        2: 'Shaker in the braking mode',
        3: 'Arrived in the home position',
        4: 'Manual mode',
        5: 'Acceleration',
        6: 'Deceleration',
        7: 'Deceleration with stopping',
        90: 'ECO mode',
        99: 'Boot process running',
        -1: '',
    }

    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG
        if 'try_ports' in kwargs:
            try_ports = kwargs.pop('try_ports')
        else:
            try_ports = None
        if 'baudrate' not in kwargs:
            kwargs.update({'baudrate': BAUDRATE})
        elif (kwargs['baudrate'] is None) or (str(kwargs['baudrate']).lower() == 'default'):
            kwargs.update({'baudrate': BAUDRATE})
        if 'timeout' not in kwargs:
            kwargs.update({'timeout': self._TIMEOUT})
        if 'write_write_delay' not in kwargs:
            kwargs.update({'write_write_delay': self._WRITE_WRITE_DELAY})
        if ('port' not in kwargs) or (kwargs['port'] is None):
            port =  find_bioshake_device_port(baudrate=kwargs['baudrate'],
                                              try_ports=try_ports,
                                              debug=kwargs['debug'])
            kwargs.update({'port': port})

        t_start = time.time()
        self._serial_device = SerialDevice(*args,**kwargs)
        atexit.register(self._exit_bioshake_device)
        time.sleep(self._RESET_DELAY)
        t_end = time.time()
        self._debug_print('Initialization time =', (t_end - t_start))

    def _debug_print(self, *args):
        if self.debug:
            print(*args)

    def _exit_bioshake_device(self):
        pass

    def _args_to_request(self,*args):
        request = ''.join(map(str,args))
        request = request + '\r';
        return request

    def _send_request(self,*args):

        '''Sends request to bioshake device over serial port and
        returns number of bytes written'''

        request = self._args_to_request(*args)
        self._debug_print('request', request)
        bytes_written = self._serial_device.write_check_freq(request,delay_write=True)
        return bytes_written

    def _send_request_get_response(self,*args):

        '''Sends request to device over serial port and
        returns response'''

        request = self._args_to_request(*args)
        self._debug_print('request', request)
        response = self._serial_device.write_read(request,use_readline=True,check_write_freq=True)
        response = response.strip()
        if (response == 'e'):
            request = request.strip()
            raise BioshakeError(request)
        return response

    def close(self):
        '''
        Close the device serial port.
        '''
        self._serial_device.close()

    def get_port(self):
        return self._serial_device.port

    def get_version(self):
        '''
        Send back the current version number.
        '''
        return self._send_request_get_response('getVersion')

    def get_description(self):
        '''
        Send back the current model information.
        '''
        return self._send_request_get_response('getDescription')

    def reset_device(self):
        '''
        Restart the controller.
        '''
        return self._send_request_get_response('resetDevice')

    def get_error_list(self):
        '''
        Return a semicolon separated list with warnings and errors that
        occurred.
        '''
        return self._send_request_get_response('getErrorList')

    def set_eco_mode(self):
        '''
        Switch the shaker into economical mode. It will reduce electricity
        consumption by switching off the solenoid for the home
        position and the deactivation of the ELM function. Warning:
        No home position!!! ELM is in locked position!!!
        '''
        return self._send_request_get_response('setEcoMode')

    def leave_eco_mode(self):
        '''
        Leave the economical mode and change in the normal operating state
        with finding the home position.
        '''
        return self._send_request_get_response('leaveEcoMode')

    def shake_on(self):
        '''
        Start the shaking with the current mixing speed or with the default
        mixing speed if an error occurs.
        '''
        try:
            return self._send_request_get_response('shakeOn')
        except BioshakeError:
            self.set_shake_target_speed()
        return self._send_request_get_response('shakeOn')

    def shake_on_with_runtime(self,runtime):
        '''
        Start the shaking with the current mixing speed for a defined time
        in seconds or with the default mixing speed if an error
        occurs. Allowable range: 0 – 99999 seconds
        '''
        try:
            return self._send_request_get_response('shakeOnWithRuntime'+str(runtime))
        except BioshakeError:
            self.set_shake_target_speed()
        return self._send_request_get_response('shakeOnWithRuntime'+str(runtime))

    def get_shake_remaining_time(self):
        '''
        Return the remaining time in seconds.
        '''
        return self._send_request_get_response('getShakeRemainingTime')

    def shake_off(self):
        '''
        Stop the shaking and return to the home position.
        '''
        return self._send_request_get_response('shakeOff')

    def shake_emergency_off(self):
        '''
        High-Speed stop for the shaking. Warning: No defined home
        position !!!
        '''
        return self._send_request_get_response('shakeEmergencyOff')

    def shake_go_home(self):
        '''
        Shaker goes to the home position and lock in.
        '''
        return self._send_request_get_response('shakeGoHome')

    def get_shake_state(self):
        '''
        Return the state of shaking.
        '''
        shake_state_value = self._send_request_get_response('getShakeState')
        if len(shake_state_value) > 0:
            shake_state_value = int(shake_state_value)
        else:
            shake_state_value = -1
        return {'value': shake_state_value,
                'description': self._SHAKE_STATE_DESCRIPTIONS[shake_state_value]}

    def get_shake_target_speed(self):
        '''
        Return the target mixing speed.
        '''
        return self._send_request_get_response('getShakeTargetSpeed')

    def set_shake_target_speed(self,target_speed=_DEFAULT_TARGET_SPEED):
        '''
        Set the target mixing speed. Allowable range: 0 – 3000 rpm
        '''
        return self._send_request_get_response('setShakeTargetSpeed'+str(target_speed))


class BioshakeDevices(dict):
    '''
    BioshakeDevices inherits from dict and automatically populates it with
    BioshakeDevices on all available serial ports. Access each individual
    device with two keys, the device name and the serial_number. If you
    want to connect multiple BioshakeDevices with the same name at the
    same time, first make sure they have unique serial_numbers by
    connecting each device one by one and using the set_serial_number
    method on each device.

    Example Usage:

    devs = BioshakeDevices()  # Automatically finds all available devices
    devs.items()
    dev = devs[name][serial_number]
    '''
    def __init__(self,*args,**kwargs):
        pass
        # if ('use_ports' not in kwargs) or (kwargs['use_ports'] is None):
        #     bioshake_device_ports = find_bioshake_device_ports(*args,**kwargs)
        # else:
        #     bioshake_device_ports = use_ports

        # for port in bioshake_device_ports:
        #     kwargs.update({'port': port})
        #     self._add_device(*args,**kwargs)

    def _add_device(self,*args,**kwargs):
        pass
        # dev = BioshakeDevice(*args,**kwargs)
        # device_info = dev.get_device_info()
        # name = device_info['name']
        # serial_number = device_info['serial_number']
        # if name not in self:
        #     self[name] = {}
        # self[name][serial_number] = dev


def find_bioshake_device_ports(baudrate=None, try_ports=None, debug=DEBUG):
    pass
    # serial_device_ports = find_serial_device_ports(try_ports=try_ports, debug=debug)
    # os_type = platform.system()
    # if os_type == 'Darwin':
    #     serial_device_ports = [x for x in serial_device_ports if 'tty.usbmodem' in x or 'tty.usbserial' in x]

    # bioshake_device_ports = {}
    # for port in serial_device_ports:
    #     try:
    #         dev = BioshakeDevice(port=port,baudrate=baudrate,debug=debug)
    #         device_info = dev.get_device_info()
    #         if ((model_number is None ) and (device_info['model_number'] is not None)) or (device_info['model_number'] in model_number):
    #             if ((serial_number is None) and (device_info['serial_number'] is not None)) or (device_info['serial_number'] in serial_number):
    #                 bioshake_device_ports[port] = {'model_number': device_info['model_number'],
    #                                               'serial_number': device_info['serial_number']}
    #         dev.close()
    #     except (serial.SerialException, IOError):
    #         pass
    # return bioshake_device_ports

def find_bioshake_device_port(baudrate=None, model_number=None, serial_number=None, try_ports=None, debug=DEBUG):
    pass
    # bioshake_device_ports = find_bioshake_device_ports(baudrate=baudrate,
    #                                                    model_number=model_number,
    #                                                    serial_number=serial_number,
    #                                                    try_ports=try_ports,
    #                                                    debug=debug)
    # if len(bioshake_device_ports) == 1:
    #     return bioshake_device_ports.keys()[0]
    # elif len(bioshake_device_ports) == 0:
    #     serial_device_ports = find_serial_device_ports(try_ports)
    #     err_string = 'Could not find any Bioshake devices. Check connections and permissions.\n'
    #     err_string += 'Tried ports: ' + str(serial_device_ports)
    #     raise RuntimeError(err_string)
    # else:
    #     err_string = 'Found more than one Bioshake device. Specify port or model_number and/or serial_number.\n'
    #     err_string += 'Matching ports: ' + str(bioshake_device_ports)
    #     raise RuntimeError(err_string)


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = BioshakeDevice(debug=debug)
