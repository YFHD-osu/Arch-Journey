# Fingerprint Sensor

The fingerprint sensor on the SFG14 Laptop is ``LighTuning Technology Inc. ETU905A88-E`` (ID: ``1c7a:0584``) which doesn't have the official [libfprint](https://gitlab.freedesktop.org/libfprint/libfprint) support.

## SDCP Fix (2026/03/08)
A project called [libfprint-egismoc-sdcp-fix](https://github.com/antoskuu/libfprint-egismoc-sdcp-fix#) was created by [antoskuu](https://github.com/antoskuu/libfprint-egismoc-sdcp-fix/commits?author=antoskuu) fixed the SDCP.

## SDCP Failed (2026/02/20)
I found out the [TenSeventy7](https://github.com/TenSeventy7/libfprint-egismoc-sdcp)'s patch stop working after I boot into Windows 11. I assume that the firmware of the fingerprint sensor is updated by the Windows Update.

