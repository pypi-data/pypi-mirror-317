from .i_sphere_abstract import ISphereAbstract
from .ophir_controller import OphirController
from .artifex_controller import ArtifexController


from typing import Union


class ISphereController(ISphereAbstract):
    """
    Integrating Sphere controller class to manage different types of integrating spheres.
    """

    def __init__(self, i_sphere_type: str):
        """
        Initialize the ISphereController with the specified integrating sphere type.

        Args:
            i_sphere_type (str): The type of the integrating sphere, e.g., "OPHIR" or "ARTIFEX".

        Raises:
            ValueError: If the specified integrating sphere type is not supported.
        """
        self._i_sphere_type = i_sphere_type.upper()
        self._i_sphere = self._create_controller()
        self._device_info = None

    def _create_controller(self) -> Union['OphirController', 'ArtifexController']:
        """
        Create a controller instance for the specified integrating sphere type.
        
        Returns:
            Controller instance for the specified integrating sphere type.

        Raises:
            ValueError: If the specified integrating sphere type is not supported.
        """
        if self._i_sphere_type == "OPHIR":
            from .ophir_controller import OphirController
            return OphirController()
        elif self._i_sphere_type == "ARTIFEX":
            from .artifex_controller import ArtifexController
            return ArtifexController()
        else:
            raise ValueError(
                f"Unsupported integrating sphere type: '{self._i_sphere_type}'. "
                "Supported types are 'OPHIR' and 'ARTIFEX'."
            )

    def connect(self) -> str:
        """
        Connect to the integrating sphere.
        
        Returns:
            str: The sensor information - model, serial number, firmware version, etc.
            
        Raises:
            ValueError: If the device is not connected.
        """
        return self._i_sphere.connect()

    def disconnect(self) -> bool:
        """
        Disconnect from the integrating sphere.
        
        Returns:
            bool: True if disconnected successfully.
            
        Raises:
            ValueError: If there is an error disconnecting the device.
        """
        return self._i_sphere.disconnect()

    def init_optical_power(self) -> bool:
        """
        Initialize optical power measurement.
        
        Returns:
            bool: True if the device is successfully initialized.            
        Raises:
            ValueError: If there is an error initializing the device.
        """
        res = self._i_sphere.init_optical_power()
        if res == True:
            self._device_info = self._i_sphere._device_info
            return True
        else:
            raise res

    def get_power_measure(self) -> float:
        """
        Measure the optical power.

        Returns:
            float: The measured optical power value in [mW].
            
        Raises:
            ValueError: If there is an error measuring the optical power.
        """
        return self._i_sphere.get_power_measure()

    def set_wavelength(self, wavelength: int) -> bool:
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
        return self._i_sphere.set_wavelength(wavelength=wavelength)
    
    def get_wavelength(self) -> int:
        """
        Get the wavelength for optical power measurement

        Returns:
            int: The wavelength in nm
        """
        return self._i_sphere.get_wavelength()

    def set_power_gain(self, gain: int) -> bool:
        """
        Set gain for optical power measurement

        Args:
            gain (int): gain value 
            
        Returns:
            bool: True if the gain was set successfully
            
        Raises:
            ValueError: if gain setting failed
        """
        return self._i_sphere.set_power_gain(gain=gain)
    
    def get_power_gain(self) -> int:
        """
        Get the gain for optical power measurement

        Returns:
            int: The gain value
        """
        return self._i_sphere.get_power_gain()
