import unittest
from unittest.mock import patch, MagicMock
from opsys_integrating_sphere.ophir_controller import OphirController


class TestOphirController(unittest.TestCase):

    @patch("win32com.client.Dispatch")
    def test_connect(self, mock_dispatch):
        mock_connection = MagicMock()
        mock_dispatch.return_value = mock_connection
        
        # Simulate successful scan_ports
        mock_connection.ScanUSB.return_value = ["MockDevice"]
        mock_connection.OpenUSBDevice.return_value = "MockPort"
        
        # Simulate successful init_optical_power
        mock_connection.SetRange.return_value = 0
        mock_connection.SaveSettings.return_value = 0
        mock_connection.GetDeviceInfo.return_value = ("Device", "Firmware", "Serial")
        mock_connection.GetSensorInfo.return_value = ("Serial", "Type", "Model")
        mock_connection.Write.return_value = None
        mock_connection.Read.return_value = "*"
        
        controller = OphirController()
        result = controller.connect()
        self.assertTrue(result)
        mock_connection.ScanUSB.assert_called_once()
        mock_connection.OpenUSBDevice.assert_called_once_with("MockDevice")
        mock_connection.Write.assert_called_once_with("MockPort", "FP")
        mock_connection.Read.assert_called_once_with("MockPort")

    @patch("win32com.client.Dispatch")
    def test_disconnect(self, mock_dispatch):
        mock_connection = MagicMock()
        mock_dispatch.return_value = mock_connection

        controller = OphirController()
        controller._connection = mock_connection
        controller._device_port = "MockPort"

        result = controller.disconnect()
        self.assertTrue(result)
        mock_connection.StopAllStreams.assert_called_once()
        mock_connection.CloseAll.assert_called_once()
        self.assertIsNone(controller._connection)
        self.assertIsNone(controller._device_port)

    @patch("win32com.client.Dispatch")
    def test_init_optical_power(self, mock_dispatch):
        mock_connection = MagicMock()
        mock_dispatch.return_value = mock_connection

        # Simulate expected behavior of methods called in init_optical_power
        mock_connection.SaveSettings.return_value = 0
        mock_connection.GetDeviceInfo.return_value = ("Device", "Firmware", "Serial")
        mock_connection.GetSensorInfo.return_value = ("Serial", "Type", "Model")
        mock_connection.Write.return_value = None
        mock_connection.Read.return_value = "*"  # Simulate successful acknowledgment

        controller = OphirController()
        controller._connection = mock_connection
        controller._device_port = "MockPort"

        result = controller.init_optical_power()
        self.assertTrue(result)
        mock_connection.SetRange.assert_called_once_with("MockPort", 0, 0)
        mock_connection.SaveSettings.assert_called_once_with("MockPort", 0)
        mock_connection.Write.assert_called_once_with("MockPort", "FP")
        mock_connection.Read.assert_called_once_with("MockPort")

    @patch("win32com.client.Dispatch")
    def test_get_power_measure(self, mock_dispatch):
        mock_connection = MagicMock()
        mock_dispatch.return_value = mock_connection
        mock_connection.Read.return_value = "123.45"

        controller = OphirController()
        controller._connection = mock_connection
        controller._device_port = "MockPort"

        result = controller.get_power_measure()
        self.assertEqual(result, 123.45 * 1000)
        mock_connection.Write.assert_called_once_with("MockPort", "sp")
        mock_connection.Read.assert_called_once_with("MockPort")

    @patch("win32com.client.Dispatch")
    def test_set_wavelength(self, mock_dispatch):
        mock_connection = MagicMock()
        mock_dispatch.return_value = mock_connection

        controller = OphirController()
        controller._connection = mock_connection
        controller._device_port = "MockPort"

        result = controller.set_wavelength(940)
        self.assertTrue(result)
        mock_connection.ModifyWavelength.assert_called_once_with("MockPort", 0, 0, 940)
        mock_connection.SetWavelength.assert_called_once_with("MockPort", 0, 0)

    @patch("win32com.client.Dispatch")
    def test_get_wavelength(self, mock_dispatch):
        mock_connection = MagicMock()
        mock_dispatch.return_value = mock_connection
        mock_connection.GetWavelengths.return_value = (0, [940])

        controller = OphirController()
        controller._connection = mock_connection
        controller._device_port = "MockPort"

        result = controller.get_wavelength()
        self.assertEqual(result, 940)
        mock_connection.GetWavelengths.assert_called_once_with("MockPort", 0)

    @patch("win32com.client.Dispatch")
    def test_set_power_gain(self, mock_dispatch):
        mock_connection = MagicMock()
        mock_dispatch.return_value = mock_connection

        controller = OphirController()
        controller._connection = mock_connection
        controller._device_port = "MockPort"

        result = controller.set_power_gain(3)
        self.assertTrue(result)
        mock_connection.SetRange.assert_called_once_with("MockPort", 0, 3)

    @patch("win32com.client.Dispatch")
    def test_get_power_gain(self, mock_dispatch):
        mock_connection = MagicMock()
        mock_dispatch.return_value = mock_connection
        mock_connection.GetRanges.return_value = (0, ["AUTO", "4.00W", "400mW"])

        controller = OphirController()
        controller._connection = mock_connection
        controller._device_port = "MockPort"

        result = controller.get_power_gain()
        self.assertEqual(result, "AUTO")
        mock_connection.GetRanges.assert_called_once_with("MockPort", 0)


if __name__ == "__main__":
    unittest.main()
