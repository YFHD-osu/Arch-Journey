import argparse
import os
import glob
import fcntl
import struct
import time

# Repalce the value below according to your machine
VID = 0x093A
PID = 0x3835

# ---------------------------------------------------------------------------
# Linux ioctl 號碼計算 (Logicically eauql to C macro _IOC / _IOR / _IOWR)
# Reference to <linux/hidraw.h>
# ---------------------------------------------------------------------------
_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = 8
_IOC_SIZESHIFT = 16
_IOC_DIRSHIFT = 30

_IOC_READ = 2
_IOC_WRITE = 1


def _IOC(direction, type_char, nr, size):
    return (
        (direction << _IOC_DIRSHIFT)
        | (ord(type_char) << _IOC_TYPESHIFT)
        | (nr << _IOC_NRSHIFT)
        | (size << _IOC_SIZESHIFT)
    )


# struct hidraw_devinfo { __u32 bustype; __s16 vendor; __s16 product; };
_HIDRAW_DEVINFO_FMT = "<IHH"
_HIDRAW_DEVINFO_SIZE = struct.calcsize(_HIDRAW_DEVINFO_FMT)  # 8 bytes

HIDIOCGRAWINFO = _IOC(_IOC_READ, "H", 0x03, _HIDRAW_DEVINFO_SIZE)


def HIDIOCSFEATURE(length):
    return _IOC(_IOC_WRITE | _IOC_READ, "H", 0x06, length)


def HIDIOCGFEATURE(length):
    return _IOC(_IOC_WRITE | _IOC_READ, "H", 0x07, length)


# ---------------------------------------------------------------------------
# Find / Open devices
# ---------------------------------------------------------------------------
def find_hidraw_paths(vid, pid):
    """掃描 /dev/hidraw*，用 HIDIOCGRAWINFO 比對 VID/PID，回傳符合的路徑清單"""
    matches = []
    for path in sorted(glob.glob("/dev/hidraw*")):
        try:
            fd = os.open(path, os.O_RDWR)
        except OSError:
            continue
        try:
            buf = bytearray(_HIDRAW_DEVINFO_SIZE)
            fcntl.ioctl(fd, HIDIOCGRAWINFO, buf, True)
            _bustype, vendor, product = struct.unpack(_HIDRAW_DEVINFO_FMT, buf)
            if vendor == vid and product == pid:
                matches.append(path)
        except OSError:
            pass
        finally:
            os.close(fd)
    return matches


def open_touchpad_device(vid=VID, pid=PID):
    """回傳打開的 fd；若找到多個符合的節點，會全部印出來讓你判斷"""
    paths = find_hidraw_paths(vid, pid)
    if not paths:
        return None, None

    if len(paths) > 1:
        print(f"找到多個符合 VID={vid:04x} PID={pid:04x} 的節點: {paths}")
        print("預設使用第一個，若指令沒反應可改用其他節點測試")

    path = paths[0]
    fd = os.open(path, os.O_RDWR)
    return fd, path


# ---------------------------------------------------------------------------
# Feature report read/write
# ---------------------------------------------------------------------------
def send_feature_report(fd, data):
    """data 需包含 Report ID 作為第一個 byte，等同 hidapi 的 send_feature_report"""
    buf = bytearray(data)
    fcntl.ioctl(fd, HIDIOCSFEATURE(len(buf)), buf, True)


def get_feature_report(fd, report_id, length):
    """length 需包含 Report ID 那個 byte，等同 hidapi 的 get_feature_report(report_id, length)"""
    buf = bytearray(length)
    buf[0] = report_id
    fcntl.ioctl(fd, HIDIOCGFEATURE(length), buf, True)
    return buf


def write_register(fd, cmd, param, value):
    """複現 main_formatted.js 中的 writeRegister(e, t, r)"""
    report = bytearray(4)
    report[0] = 0x43  # Report ID (67)
    report[1] = cmd  # e
    report[2] = param  # t
    report[3] = value  # r

    print(f"寫入指令: {[hex(x) for x in report]}")
    send_feature_report(fd, report)


def read_register(fd, cmd, param):
    """複現 main_formatted.js 中的 readRegister(e, t)"""
    report = bytearray(4)
    report[0] = 0x43
    report[1] = cmd
    report[2] = 0x10 | param
    report[3] = 0

    send_feature_report(fd, report)

    result = get_feature_report(fd, 0x43, 10) 
    return result

# Get brightness of 'SWIFT' logo on the touchpad
def get_brightness(fd):
    result = read_register(fd, 0x7A, 0x00)
    if result and len(result) >= 4:
        brightness = result[3]
        return brightness
    else:
        return None

# Set brightness of 'SWIFT' logo on the touchpad
def set_brightness(fd, level: float):
    if level < 0 or level > 1:
        raise ValueError("Brightness level should between 0.0 - 1.0")

    send_level = int(level * 100)
    return write_touchpad_feature(fd, [0x43, 0x7A, 0x00, send_level])

def set_function_key_control_en(fd, enable: bool):
    send_value = 1 if enable else 0
    return write_touchpad_feature(fd, [0x43, 0x76, 0x00, send_value])

def set_media_control(fd, enable: bool):
    send_value = 1 if enable else 0
    return write_touchpad_feature(fd, [0x43, 0x77, 0x00, send_value])

def write_touchpad_feature(fd, payload_bytes):
    send_feature_report(fd, bytearray(payload_bytes))

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Available sub-commands", dest="command", required=True)

    parser_set_brightness = subparsers.add_parser("set-brightness", help="Set brightness of the touchpad")
    parser_set_brightness.add_argument("value", help="Apply the brightness value (0.0 - 1.0) to the touchpad")

    parser_get_brightness = subparsers.add_parser("get-brightness", help="Get brightness of the touchpad")

    parser_set_media_control = subparsers.add_parser("set-media", help="Toggle media function of the touchpad")
    parser_set_media_control.add_argument("value", 
                                       help="Toggle the media button while swipping on the SWIFT logo", 
                                       choices=[True, False])
    
    parser_fade_brightness = subparsers.add_parser("fade-brightness", help="Fade brightness of the touchpad")
    parser_fade_brightness.add_argument("value", help="The target value of the end brightness",)
    parser_fade_brightness.add_argument("interval", help="The interval between each step of fade", default=0.01)
    
    return parser.parse_args()

def fade_brightness(fd, target_value: float, interval: float):
    if target_value < 0 or target_value > 1:
        raise ValueError("Brightness level should between 0.0 - 1.0")
    
    target_brightness = int( target_value * 100 )
    current_brightness = int( get_brightness(fd) )

    step = 1 if current_brightness < target_brightness else -1

    for i in range(current_brightness, target_brightness, step):
        set_brightness(fd, i/100)
        time.sleep(interval)
    
    set_brightness(fd, target_value)

def main():
    args = parse_args()

    if os.geteuid() != 0:
        print("This script is currently not run by root, it may cause difficult for opening devices")

    fd, path = open_touchpad_device()
    
    if fd is None:
        print(f"Cannot find the touchpad hidraw node with VID={VID:04x} PID={PID:04x}")
        return

    if args.command == "set-brightness":
        set_brightness(fd, float(args.value))
        return
    
    if args.command == "get-brightness":
        current_brightness = get_brightness(fd)
        print(current_brightness)
        return
    
    if args.command == "fade-brightness":
        fade_brightness(fd, float(args.value), float(args.interval))
        return
    
    os.close(fd)
    raise NotImplementedError(f"Command {args.command} is not implemenmted yet")

if __name__ == "__main__":
    main()