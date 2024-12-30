import unittest
from unittest.mock import patch, MagicMock
from opsys_integrating_sphere.artifex_controller import ArtifexController


class TestArtifexController(unittest.TestCase):

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports", return_value=[("COM1", "OPM150 Integrating Sphere", "")])
    def test_connect_success(self, mock_comports, mock_serial):
        mock_serial_instance = MagicMock()
        mock_serial.return_value = mock_serial_instance

        mock_serial_instance.isOpen.return_value = True
        mock_serial_instance.readline.side_effect = [
            b"Detector: V1\n",  # Response during `init_optical_power`
            b"OPM150 FW2.0\n",
            b"Serial: 797\n",
            b"Date of Manufacturing: 03.11.2021\n",
            b"OK\n",  # Response for `set_power_gain`
        ]

        controller = ArtifexController()
        result = controller.connect()

        self.assertTrue(result)
        self.assertIsNotNone(controller._device_info)
        self.assertIn("OPM150 FW2.0", controller._device_info)

        mock_comports.assert_called_once()
        mock_serial.assert_called_once_with("COM1", 115200, timeout=5, parity="N")
        mock_serial_instance.isOpen.assert_called_once()
        self.assertEqual(mock_serial_instance.readline.call_count, 5)

    @patch("serial.Serial")
    def test_disconnect_success(self, mock_serial):
        # Simulate successful disconnection
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.isOpen.return_value = True
        mock_serial_instance.close.return_value = None

        controller = ArtifexController()
        controller._connection = mock_serial_instance
        result = controller.disconnect()
        self.assertTrue(result)
        mock_serial_instance.close.assert_called_once()
        self.assertIsNone(controller._connection)

    @patch("serial.Serial")
    def test_get_power_measure(self, mock_serial):
        # Simulate optical power retrieval
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.readline.return_value = b"I12,34mA\n"

        controller = ArtifexController()
        controller._connection = mock_serial_instance
        controller._power_conversion_factor = 10**3
        controller._calibration_offset = 1.0

        result = controller.get_power_measure()
        self.assertAlmostEqual(result, 12340.0)  # in mW

    @patch("serial.Serial")
    def test_set_wavelength_success(self, mock_serial):
        # Simulate successful wavelength setting
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.readline.return_value = b"KF: 1.234\n"

        controller = ArtifexController()
        controller._connection = mock_serial_instance
        result = controller.set_wavelength(940)
        self.assertTrue(result)
        mock_serial_instance.write.assert_called_with(b"$L0940\n")
        mock_serial_instance.readline.assert_called()

    @patch("serial.Serial")
    def test_set_power_gain_success(self, mock_serial):
        # Simulate successful power gain setting
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.readline.return_value = b"OK\n"

        controller = ArtifexController()
        controller._connection = mock_serial_instance
        result = controller.set_power_gain(3)
        self.assertTrue(result)
        mock_serial_instance.write.assert_called_with(b"V3\n")
        mock_serial_instance.readline.assert_called_once()

    @patch("serial.Serial")
    def test_set_power_gain_invalid_value(self, mock_serial):
        # Test invalid power gain values
        controller = ArtifexController()
        controller._connection = mock_serial.return_value

        with self.assertRaises(ValueError) as context_low:
            controller.set_power_gain(0)
        self.assertIn("Gain value must be between 1 and 5", str(context_low.exception))

        with self.assertRaises(ValueError) as context_high:
            controller.set_power_gain(6)
        self.assertIn("Gain value must be between 1 and 5", str(context_high.exception))

        with self.assertRaises(ValueError) as context_type:
            controller.set_power_gain("three")
        self.assertIn("Gain value must be an integer", str(context_type.exception))

    @patch("serial.Serial")
    def test_set_power_gain_device_error(self, mock_serial):
        # Simulate device error on power gain setting
        mock_serial_instance = mock_serial.return_value
        mock_serial_instance.readline.return_value = b"ERROR\n"

        controller = ArtifexController()
        controller._connection = mock_serial_instance

        with self.assertRaises(ValueError) as context:
            controller.set_power_gain(3)
        self.assertIn("Error setting Artifex Gain: ERROR", str(context.exception))

    @patch("serial.Serial")
    def test_set_power_gain_not_connected(self, mock_serial):
        # Simulate operation when device is not connected
        controller = ArtifexController()
        controller._connection = None

        with self.assertRaises(AttributeError):
            controller.set_power_gain(3)


if __name__ == "__main__":
    unittest.main()
