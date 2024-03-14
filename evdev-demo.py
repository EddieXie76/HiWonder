import evdev

# python -m evdev.evtest

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)
    if 'Xbox Wireless Controller' == device.name:
        for event in device.read_loop():
            print(evdev.categorize(event))
