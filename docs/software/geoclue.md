# GeoClue
GeoClue is a modular D-Bus geoinformation service providing location data to Linux applications through diverse sources while maintaining user privacy and strict access control.

## Setup
To utilize geoclue in hyprland, first we need to make sure agent is running, by executing the command (or add it to ``exec-once``): 
```bash
/usr/lib/geoclue-2.0/demos/agent
```

To test the location result, run:
```bash
/usr/lib/geoclue-2.0/demos/where-am-i
```

## Config
Config file for geoclue is stored in ``/etc/geoclue/geoclue.conf``

```conf
[agent]
whitelist=geoclue-demo-agent;gnome-shell;io.elementary.desktop.agent-geoclue2;sm.puri.Phosh;lipstick

[ip]
enable=true
method=reallyfreegeoip
# Set accuracy to mock application like google map displaying precise location.  
accuracy=1000.0

# WiFi source configuration options
[wifi]

# Enable WiFi source
enable=true
url=https://api.beacondb.net/v1/geolocate
submit-data=false
submission-nick=geoclue

[gnome-datetime-panel]
allowed=true
system=true
users=

[gnome-color-panel]
allowed=true
system=true
users=

[org.gnome.Shell]
allowed=true
system=true
users=

[io.elementary.desktop.agent-geoclue2]
allowed=true
system=true
users=

[sm.puri.Phosh]
allowed=true
system=true
users=

[epiphany]
allowed=true
system=false
users=

[firefox]
allowed=true
system=false
users=

[lipstick]
allowed=true
system=true
users=

[google-chrome]
allowed=true
system=false
users=

[zen]
allowed=true
system=false
users=

[page.codeberg.tpikonen.geobug]
allowed=true
system=false
users=

```

## Browser Compatibility
### Google Chrome
Google Chrome uses its bulit-in Location Service API, it will determine the geo location by requesting system wifi list. So if you are using flatpak, it is required to grant ``org.freedesktop.NetworkManager.*`` permission for it.

### Firefox
If the browser is not in sandbox (flatpak), then after geoclue install, everything would be fine.
If not, you can open ``about:config`` and changes the settings below:

- ``geo.enabled`` = ``true``
- ``geo.provider.use_geoclue`` = ``true``

Flatpak firefox will use DBus to get the location. You can install ``xdg-desktop-portal-gnome``, and set ``~/.config/xdg-desktop-portal/portals.conf`` to the value below:
```conf
[preferred]

org.freedesktop.impl.portal.Location=xdg-desktop-portal-gnome
```

Finally, turn the ``Location`` switch on for firefox in flatseal, and it should work fine.

## Enable / Disable Location Services
You can use the CLI to toggle the location services in ``xdg-desktop-portal-gnome``
```bash
gsettings set org.gnome.system.location enabled true  # 開啟定位服務
gsettings set org.gnome.system.location enabled false # 關閉定位服務
```