# Davinci Resolve
A professional video editing application combining advanced color grading, visual effects, and audio post-production into a powerful workflow, widely utilized by Hollywood experts for high-end cinematic productions.

## Fcitx5 Input Method
Resolve didn't support the fcitx5 input method by default (At least in Davinci Resolve 20.0). But because of the Qt version it use is not that outdated, we can replace the system Qt input method plugin with it to get fctix5 working.


### 1. Install ``fcitx-qt5``
You will need to install the package ``fcitx-qt5`` to have the plugin file on the system.

### 2. Find the system fcitx5 plugin
Plugin will be installed in these possible path, select the one wich contains the file:
- ``/usr/lib64/qt5/plugins/platforminputcontexts/libfcitx5platforminputcontextplugin.so``
- ``/usr/lib/qt/plugins/platforminputcontexts/libfcitx5platforminputcontextplugin.so ``

### 3. Create the ``platforminputcontexts`` for resolve
```bash
sudo mkdir -p /opt/resolve/libs/plugins/platforminputcontexts
```

### 4. Link the plugin to the folder
```bash
sudo ln -s <SOURCE> /opt/resolve/libs/plugins/platforminputcontexts
```
[Reference 1](https://sh.alynx.one/posts/Input-Method-Support-for-DaVinci-Resolve-on-Linux/)
[Reference 2](https://www.csslayer.info/wordpress/fcitx-dev/build-im-module-for-wps/)
[Reference 3](https://szclsya.me/posts/linux/fcitx5-im-module-for-proprietary/)
[Reference 4](https://www.csslayer.info/wordpress/fcitx-dev/a-case-study-how-to-compile-a-fcitx-platforminputcontext-plugin-for-a-proprietary-software-that-uses-qt-5/)

#### 5. Add environment variable
QT_IM_MODULE=fcitx
XMODIFIERS="@im=fcitx"

## Symbol lookup error (libgmodule)
If resolve encounter the symbol lookup error and failed to startup like below:
```log
/opt/resolve/bin/resolve: symbol lookup error: /usr/lib/libpango-1.0.so.0: undefined symbol: g_once_init_leave_pointer
```

We can remove the file below to force resolve to use the system version of the files:
```bash
sudo rm /opt/resolve/libs/libglib-2.0.so* \
/opt/resolve/libs/libgio-2.0.so* \
/opt/resolve/libs/libgmodule-2.0.so* \
/opt/resolve/libs/libgobject-2.0.so*
```

## 100% CPU Usage
If resolve takes 100% CPU usage under any scenario, it is better to use [davincibox](https://github.com/zelikos/davincibox).
This method also can do the fcitx5 patch as long as you intall the required packages, and do the operation shown [here](#fcitx5-input-method).

```bash
/usr/bin/distrobox enter davincibox # 進入環境
sudo dnf install fcitx5-qt5  # 還沒安裝 fcitx5 的話，先安裝 fcitx5
sudo dnf copr enable apicalshark/fcitx5-mcbopomofo
sudo dnf install fcitx5-mcbopomofo
sudo ln -s <SOURCE> /opt/resolve/libs/plugins/platforminputcontexts
```
