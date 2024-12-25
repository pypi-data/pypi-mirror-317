from abc import ABC, abstractmethod


class ISphereAbstract(ABC):  
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def init_optical_power(self):
        pass
    
    @abstractmethod
    def get_power_measure(self):
        pass
    
    @abstractmethod
    def set_wavelength(self, wavelength: int):
        pass
    
    @abstractmethod
    def get_wavelength(self):
        pass
    
    @abstractmethod
    def set_power_gain(self, gain: int):
        pass
    
    @abstractmethod
    def get_power_gain(self):
        pass
