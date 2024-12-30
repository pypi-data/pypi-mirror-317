# README #

This repository is a part of opsys automation infrastructure and provides an integrating sphere controller implementation for Artifex and Ophir devices.

### What is this repository for? ###

* Integrating sphere controller implementation for Artifex/Ophir devices.
* Provides an interface to connect, measure optical power, and manage settings for these devices.

### Supported Devices ###

#### Artifex OPM150
* [Artifex OPM150 Datasheet](https://artifex-engineering.com/wp-content/uploads/opm150engl_revb8_klein.pdf)

#### Ophir LM Measurement
* [Ophir LM Measurement Datasheet](https://www.ophiropt.com/medias/OphirLMMeasurement-COM-Object-0?context=bWFzdGVyfG9wcmVzb3VyY2VzfDg3Nzc1MHxhcHBsaWNhdGlvbi9wZGZ8YUdFeUwyaGpOeTg1T1RBek1EQTROREUxTnpjMEwwOXdhR2x5VEUxTlpXRnpkWEpsYldWdWRGOURUMDFmVDJKcVpXTjBYekF8MjE3YmNkMGIyZTc4YWM2ODI0MzM2ZGI4NjhmOTI4YTk3MTU4YWExMzEzMWEyN2YzYjI5NzYzMTY0MGE5ZWUxOA)

### How do I get set up? ###

* Install the package using pip:
  ```sh
  pip install opsys-integrating-sphere
  ```

### Unit Testing ###

* Run unit tests using:
  ```sh
  python -m unittest -v
  ```

### Usage Example ###

```python
from opsys_integrating_sphere.i_sphere_controller import ISphereController

# Create an instance of ISphereController for Artifex device
i_sphere = ISphereController(i_sphere_type='Artifex')

i_sphere.connect()
print(i_sphere.get_power_measure())
i_sphere.disconnect()

# Create an instance of ISphereController for Ophir device
i_sphere = ISphereController(i_sphere_type='Ophir')

i_sphere.connect()
print(i_sphere.get_power_measure())
i_sphere.disconnect()
```