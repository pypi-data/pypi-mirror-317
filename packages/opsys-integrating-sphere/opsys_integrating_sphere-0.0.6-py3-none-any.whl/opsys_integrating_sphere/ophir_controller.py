import pythoncom
import win32com.client

# Initialize the COM library
from .i_sphere_abstract import ISphereAbstract


class OphirController(ISphereAbstract):
    """
    Ophir Integrating Sphere Controller
    """
    
    VALID_GAIN_VALUES = range(0, 7)  # Valid gain values: 0 through 6

    def __init__(self):
        """
        Initialize parameters
        """
        self._connection = None
        self._device_port = None
        self._device_info = None

    def scan_ports(self) -> bool:
        """
        Check for device connection

        Returns:
            bool: True if the device connected, else False
        """
        device_list = self._connection.ScanUSB()
        
        if not device_list:
            return False
        else:
            for device in device_list:
                self._device_port = self._connection.OpenUSBDevice(device)
                break
            return True

    def connect(self) -> bool:
        """
        Connect to integrating sphere
        
        Returns:
            bool: True if connected successfully            
        Raises:
            ValueError: if device not connected
        """
        pythoncom.CoInitialize()
        if self._connection is not None:
            self.disconnect()
        self._connection = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")        
        if self.scan_ports():
            return self.init_optical_power()
        else:
            raise ValueError("Error connecting to Ophir device")

    def disconnect(self) -> bool:
        """
        Disconnect from integrating sphere
        
        Returns:
            bool: True if disconnected successfully
            
        Raises: 
            ValueError: if disconnection failed with error code
        """
        if self._connection and self._device_port:
            self._connection.StopAllStreams()
            self._connection.CloseAll()

            self._connection = None
            self._device_port = None
            self._device_info = None
        return True

    def init_optical_power(self) -> bool:
        """
        Initialize optical power measurement for Ophir device
        
        Returns:
            bool: True if initialization successful
        Raises:
            ValueError: if initialization failed
        """
        try:      
            self._connection.SetRange(self._device_port, 0, 0)  # set range to Auto
            self._connection.SaveSettings(self._device_port, 0)
            device_info = self._connection.GetDeviceInfo(self._device_port, 0)
            sensor_info = self._connection.GetSensorInfo(self._device_port, 0)
            self._device_info = self._format_device_info(device_info, sensor_info)

            self._connection.Write(self._device_port, "FP") # put sensor in power mode
            reply = self._connection.Read(self._device_port) # verify acknowledgement from device
            if reply != "*":
                return False # initialization failed
            else:
                return True # initialization successful
        except Exception as e:
            return e
            
    def _format_device_info(self, device_info: tuple, sensor_info: tuple) -> str:
        """
        Format the device and sensor information into a readable string.

        Args:
            device_info (tuple): Device information tuple.
            sensor_info (tuple): Sensor information tuple.

        Returns:
            str: Formatted device information string.
        """
        return (
            f"Device: {device_info[0]}\n"
            f"Device Firmware: {device_info[1]}\n"
            f"Device Serial: {device_info[2]}\n"
            f"Sensor Type: {sensor_info[1]}\n"
            f"Sensor Model: {sensor_info[2]}\n"
            f"Sensor Serial: {sensor_info[0]}\n"
        )
    
    def get_power_measure(self) -> float:
        """
        Measure optical power

        Returns:
            float: measured optical power value 
        """       
        self._connection.Write(self._device_port, "sp")
        measured_value = self._connection.Read(self._device_port)
        if 'over' in measured_value:
            return 0
        else:
            return float(measured_value.replace("*", "")) * 1000 # convert to mW

    def set_wavelength(self, wavelength: int=940) -> bool:
        """
        Set wavelength for optical power measurement

        Args:
            wavelength (int, optional): laser wavelength in nm.
                                        Defaults to 940.
        Returns:
            bool: True if the wavelength was set successfully
            
        Raises:
            ValueError: if wavelength setting failed
        """
        self._connection.ModifyWavelength(self._device_port, 0, 0, wavelength)
        self._connection.SetWavelength(self._device_port, 0, 0)
        if self._connection.IsSensorExists(self._device_port, 0):
            return True
        
    def get_wavelength(self) -> int:
        """
        Get the wavelength of the Ophir device

        Returns:
            int: wavelength in nm
        """
        res = self._connection.GetWavelengths(self._device_port, 0)
        return res[1][res[0]]
    
    def set_power_gain(self, gain: int = 0) -> bool:
        """
        Set power gain for optical power measurement.

        Gain levels correspond to the following settings:
            - 0: Gain AUTO
            - 1: Gain 4.00W
            - 2: Gain 400mW
            - 3: Gain 40.0mW
            - 4: Gain 4.00mW
            - 5: Gain 400uW
            - 6: Gain 40.0uW

        Args:
            gain (int): Power gain value.

        Returns:
            bool: True if power gain set successfully.

        Raises:
            ValueError: If the gain value is not between 0 and 6.
        """
        # Validate the gain value
        if gain not in self.VALID_GAIN_VALUES:
            raise ValueError(f"Gain value must be between 0 and 6. Received {gain}.")

        # Set the power gain using the connection object
        self._connection.SetRange(self._device_port, 0, gain)
        return True
    
    def get_power_gain(self) -> str:
        """
        Get the power gain of the Ophir device

        Returns:
            str: power gain value
        """
        res = self._connection.GetRanges(self._device_port, 0)
        return res[1][res[0]]
