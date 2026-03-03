from app.device.adb import ADBDevice


def test_adb_device_creation():
    device = ADBDevice(device_id="test123", model_name="Pixel", status="online")
    assert device.device_id == "test123"
    assert device.status == "online"


def test_wifi_detection():
    usb_device = ADBDevice(device_id="abc123", connection_type="usb")
    wifi_device = ADBDevice(device_id="192.168.1.100:5555", connection_type="wifi")
    assert usb_device.connection_type == "usb"
    assert wifi_device.connection_type == "wifi"
