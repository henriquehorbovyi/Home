import os
import time


def find_device(device_name=""):
    stream = os.popen("bluetoothctl devices")
    output = stream.read()
    for item in output.split("\n"):
        device = item.split(" ", 2)
        if len(device) == 3 and device[2].lower() == device_name.replace(" / ", "").lower():
            return {'address': device[1], 'name': device[2]}

    return "I couldn't find {0}".format(device_name)


def list_devices():
    stream = os.popen("bluetoothctl devices")
    output = stream.read()
    devices = []
    for item in output.split("\n"):
        device = item.split(" ", 2)
        if len(device) == 3:
            devices.append(device[2])

    if len(devices) == 0:
        result = "no devices were found"
    else:
        result = devices

    return result


def connect(device):
    stream = os.popen("bluetoothctl pair "+device['address'])
    output = stream.read()
    if "AlreadyExists" in output:
        while True:
            stream = os.popen("bluetoothctl connect " + device['address'])
            output = stream.read()
            print(output)
            if "Connection successful" in output:
                return "connected with "+device['name']
            else:
                time.sleep(1)
                print("trying to connect")

