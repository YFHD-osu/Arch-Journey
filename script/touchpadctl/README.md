# SFG14-73 Touchpad Control Utility 
Enable the ability to control logo light on the touchpad and toggle the media function.

> [!WARNING]  
> Please ensure that your device model is ``SFG14-73``. Sending signal to wrong i2c device may cause hardware damage!

## Script Usage
In order to use the script, you will need to find the VID and PID of the touchpad, and place them into the ``touchpadctl.py``. <br> 
This script ususally needs root permission to be executed, or you will need to setup specfic udev rules. 

## How to find the address of the touchpad
First, I'll strongly recommend to unplug all usb peripherals to reduce the chance of misrecognition.
Then use the command below to list all input device on your machine.
```shell
cat /proc/bus/input/devices
```

We need to look for the device called, for instance, touchpad on my device is called PIXA3835:00 093A:3835 Mouse and its ``VID=093a``, ``PID=3835``
```
I: Bus=0018 Vendor=093a Product=3835 Version=0100
N: Name="PIXA3835:00 093A:3835 Mouse"
P: Phys=i2c-PIXA3835:00
S: Sysfs=/devices/pci0000:00/0000:00:15.0/i2c_designware.0/i2c-0/i2c-PIXA3835:00/0018:093A:3835.0006/input/input22
U: Uniq=
H: Handlers=event18 mouse3 
B: PROP=0
B: EV=17
B: KEY=30000 0 0 0 0
B: REL=1943
B: MSC=10
```

## Complete Command Table for Touchpad Functions

| Function (Configuration Item) | Command (Register) | Parameter (Byte 2) | Value (Status) | Corresponding Complete Payload (Hexadecimal) |
| :--- | :--- | :--- | :--- | :--- |
| Function Key Control Enable (FUNCTION_KEY_CONTROL_EN) | 118 (0x76) | 0 (0x00) | 1 (Enable) or 0 (Disable) | [0x43, 0x76, 0x00, 0x01] / [0x43, 0x76, 0x00, 0x00] |
| Media Control Enable (MEDIA_CONTROL) | 119 (0x77) | 0 (0x00) | 1 (Enable) or 0 (Disable) | [0x43, 0x77, 0x00, 0x01] / [0x43, 0x77, 0x00, 0x00] |
| Touchpad Media Function Control Enable (MEDIA_TP_FUNCTION_CONTROL) | 120 (0x78) | 0 (0x00) | 1 (Enable) or 0 (Disable) | [0x43, 0x78, 0x00, 0x01] / [0x43, 0x78, 0x00, 0x00] |
| Touchpad Lighting Function Enable (LIGHTING_FUNCTION_EN) | 121 (0x79) | 0 (0x00) | 1 (Enable) or 0 (Disable) | [0x43, 0x79, 0x00, 0x01] / [0x43, 0x79, 0x00, 0x00] |
| Touchpad Brightness Control (BRIGHTNESS_CONTROL) | 122 (0x7A) | 0 (0x00) | 0 ~ 100 | Example: Brightness 50 -> [0x43, 0x7a, 0x00, 0x32] |
| YouTube Function Control (YOUTUBE_FUNCTION_CONTROL) | 123 (0x7B) | 0 (0x00) | 1 (Enable) or 0 (Disable) | [0x43, 0x7b, 0x00, 0x01] / [0x43, 0x7b, 0x00, 0x00] |