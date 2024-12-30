import serial
from serial import SerialException
import re
from .i_sphere_abstract import ISphereAbstract

# avoild COMs detection at deployment
try:
    import serial.tools.list_ports
except Exception as e:
    raise ImportError("Error importing serial.tools.list_ports") from e


class ArtifexController(ISphereAbstract):
    """
    OPM150 Artifex Integrating Sphere Controller
    """

    DEVICE_MODEL = "OPM150"
    BAUDRATE = 115200
    TIMEOUT = 5
    DETECTOR_ERROR_MSG = "DET ERR"
    POWER_ERROR_MSG = "PWR ERR"
    POWER_SUCCESS_MSG = "PWR OK"
    DETECTOR_SUCCESS_MSG = "DET OK"
    GAIN_SUCCESS_MSG = "OK"

    def __init__(self) -> None:
        """
        Initialize parameters
        """
        self._connection = None
        self._device_port = None
        self._power_conversion_factor = None
        self._calibration_offset = None
        self._device_info = None

    def scan_ports(self) -> bool:
        """
        Scan for available COM ports and set the Artifex port if found.

        Returns:
            bool: True if a valid COM port is detected.

        Raises:
            SerialException: If no valid COM port is detected.
        """
        ports = serial.tools.list_ports.comports()

        for port, desc, _ in sorted(ports):
            if self.DEVICE_MODEL in desc:
                self._device_port = port
                break

        if self._device_port is None:
            raise SerialException("No valid COM port detected")
        else:
            return True

    def connect(self, baudrate=BAUDRATE, timeout=TIMEOUT) -> bool:
        """
        Connect Artifex device to the COM port

        Args:
            baudrate (int, optional): port baud rate. Defaults to 15200.
            timeout (int, optional): port timeout. Defaults to 5.

        Returns:
            bool: True if connected successfully
        Raises:
            SerialException: Error opening COM port
        """
        self.scan_ports()  # get port
        self._connection = serial.Serial(
            self._device_port, baudrate, timeout=timeout, parity=serial.PARITY_NONE
        )

        if self._connection.isOpen() == True:
            return self.init_optical_power()
        else:
            raise SerialException("Error opening COM port")

    def disconnect(self) -> bool:
        """
        Disconnect from integrating sphere

        Returns:
            bool: True if disconnected successfully

        Raises:
            ValueError: If there is an error disconnecting the device.
        """
        if self._connection.isOpen() == True:
            self._connection.close()
            self._connection = None
            return True
        else:
            raise ValueError("Error disconnecting Artifex device")

    def init_optical_power(self) -> bool:
        """
        Initialize the Artifex device.

        Returns:
            bool: True if the device is successfully initialized.
        Raises:
            ValueError: If there is an error initializing the device.
        """
        info = ""
        detector_info = ""
        lines_to_read = 4

            
        self._connection.write("$I\n".encode())  # Send the command

        for _ in range(lines_to_read):  # Read 4 lines
            line = (self._connection.readline().decode("utf-8", errors="ignore").strip())  # Decode with error handling
            info += line + "\n"
            if "Detector:" in line:
                detector_info = line  # Extract the detector line

        # Extract the power multiplier
        if detector_info:
            match = re.search(r"([UVWX])(\d+)", detector_info)
            if match:
                power_exponent = int(match.group(2)[0])  # First digit indicates the power of 10
                self._power_conversion_factor = (10**power_exponent)  # Calculate the multiplier
        self._device_info = info
        self.set_power_gain()  # Set the default gain level

        return True

    def get_power_measure(self) -> float:
        """
        Get the optical power from the Artifex device.

        Returns:
            float: The measured optical power in milliwatts (mW).

        Raises:
            ValueError: If there is an error reading the measured value.
        """
        try:
            # Send command to Artifex device to initiate measurement
            self._connection.write("$E".encode() + "\n".encode())
        except Exception:
            raise ValueError("Error sending command to Artifex device")

        # Read the measured value from the device
        measuredvalue = self._connection.readline().decode().strip()

        # Extract the numeric part and unit (e.g.,'I3uA', 'I0,36uA', 'I0,36mA', 'I0,36nA')
        match = re.search(r"I(\d+)(?:,(\d+))?([u|m|n]A)", measuredvalue)

        if match:
            # Combine the extracted parts into a float (e.g.,'3', '0,36' -> 0.36)
            measured_value = float(match.group(1))
            if match.group(2):
                measured_value += float(f"0.{match.group(2)}")
            unit = match.group(3).lower()  # Extract the unit and convert to lowercase

            # Convert the value to amperes (A) based on the unit
            if unit == "ua":  # Microamperes (µA)
                measured_value *= 10**-6  # Convert to amperes (A)
            elif unit == "ma":  # Milliamperes (mA)
                measured_value *= 10**-3  # Convert to amperes (A)
            elif unit == "na":  # Nanoamperes (nA)
                measured_value *= 10**-9  # Convert to amperes (A)
            else:
                measured_value = None  # Invalid unit
        else:
            measured_value = None  # If no match, set to None

        # Calculate the optical power in mW using the formula:
        # Optical Power (mW) = (measured_value (A) / calibration_value) * power_multiplier * 1000 [mW]
        if measured_value is not None:
            return (
                (measured_value / self._calibration_offset)
                * self._power_conversion_factor
                * 1000
            )  # in mW
        else:
            raise ValueError("Invalid measured value")

    def set_wavelength(self, wavelength: int = 940) -> bool:
        r"""
        Set the pulse length for the Artifex device and confirm the setting.

        Args:
            wavelength (int, optional): The wavelength to set (e.g., 940\905).
                                        Defaults to 940.

        Raises:
            ValueError: If there is an error setting the pulse length.
        """
        # Send the wavelength command
        self._connection.write(f"$L0{wavelength}\n".encode())

        # Read and parse the response
        response = self._connection.readline().decode().strip()

        # Handle specific device messages
        if self.DETECTOR_ERROR_MSG in response:
            raise ValueError("Error: Defective or missing optical head.")
        elif self.POWER_ERROR_MSG in response:
            raise ValueError("Error: Insufficient USB port power supply.")
        elif self.POWER_SUCCESS_MSG in response:
            raise ValueError("Info: Power supply is reinstated.")
        elif self.DETECTOR_SUCCESS_MSG in response:
            raise ValueError("Info: A valid optical head was detected.")

        # Extract the calibration value (e.g., KF: <calibration value>)
        match = re.search(r"KF:\s*(\d+\.\d+)", response.replace(",", "."))
        if match:
            self._calibration_offset = float(match.group(1))
        else:
            raise ValueError("Invalid calibration value")  # Raise an error if the calibration value is invalid
        return True
    
    def get_wavelength(self) -> None:
        """
        Get the wavelength for the Artifex device not implemented.
        """
        return NotImplementedError("Method not implemented")
        

    def set_power_gain(self, gain: int = 5) -> bool:
        """
        Set the power gain level for the Artifex device and confirm the setting.

        Gain levels correspond to the following multipliers:
            - 1: Gain ×1
            - 2: Gain ×10
            - 3: Gain ×100
            - 4: Gain ×1000
            - 5: Gain ×10000

        Args:
            gain (int, optional): The gain level to set (e.g., 3 for "V3"). 
                                  Defaults to 3 (Gain ×100).

        Returns:
            bool: True if the gain level was successfully set.

        Raises:
            ValueError: If the gain value is not between 1 and 5 or if there is 
                        an error setting the gain level or the device 
                        returns an unexpected response.
        """
        # Validate the gain value
        if not isinstance(gain, int):
            raise ValueError(f"Gain value must be an integer between 1 and 5. Received type {type(gain)}.")
        if gain < 1 or gain > 5:
            raise ValueError(f"Gain value must be between 1 and 5. Received {gain}.")

        # Send the gain command to the device
        gain_command = f"V{gain}\n".encode()
        self._connection.write(gain_command)
        response = self._connection.readline().decode().strip()

        # Confirm if the gain was set correctly
        if self.GAIN_SUCCESS_MSG not in response:
            raise ValueError(f"Error setting Artifex Gain: {response}")
        return True
    
    def get_power_gain(self) -> str:
        """
        Get the power gain level for the Artifex device.

        Returns:
            str: The power gain level.

        Raises:
            ValueError: If there is an error reading the power gain level.
        """
        # Send the gain command
        self._connection.write(b"V?\n")

        # Read and parse the response
        response = self._connection.readline().decode().strip()
        response = self._connection.readline().decode().strip()

        # Extract the gain value (e.g., "V3: 100")
        match = re.search(r"V(\d+)", response)
        if match:
            return match.group()
        else:
            raise ValueError("Error: Unable to read power gain level")
