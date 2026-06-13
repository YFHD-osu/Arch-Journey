# Fctix5

Fcitx5 是一個 Linux 系統設計的輸入法框架。

### Input Method
[小麥注音](https://github.com/openvanilla/fcitx5-mcbopomofo?tab=readme-ov-file)
is a smart and easy to use input method for chewing.

### Theme
I use
[fcitx5-themes-candlelight](https://github.com/thep0y/fcitx5-themes-candlelight?tab=readme-ov-file)
for a macOS like candidate theme.

## Electron Applications (e.g. Discord, VScode)
### Problem 
Application based on electron (e.g. ``vscode``, ``discord``) cannot use ``fcitx5``.

### Solution 
Add those parameter after the application startup command:
```
--ozone-platform-hint=auto
--enable-wayland-ime
--wayland-text-input-version=3
```

If you are using [visual-studio-code-bin](https://aur.archlinux.org/packages/visual-studio-code-bin) you can put these argument in ``~/.config/code-flags.conf``

[Reference 1](https://github.com/electron/electron/issues/33662#issuecomment-2299180561)
[Reference 2](https://yangqiuyi.com/blog/linux/%E5%9C%A8wayland%E6%A8%A1%E5%BC%8F%E7%9A%84vscode%E4%B8%AD%E4%BD%BF%E7%94%A8fcitx5%E8%BE%93%E5%85%A5%E4%B8%AD%E6%96%87/)

## Google Chrome
If fcitx5 not willing to work on Google Chrome, try adding below to the startup paramenter:
```bash
--enable-features=UseOzonePlatform
--ozone-platform=wayland
--ozone-platform-hint=auto 
--enable-wayland-ime 
--wayland-text-input-version=3
```
[Reference 1](https://askubuntu.com/questions/1472847/google-chrome-is-blurry-on-ubuntu-23-04-wayland-nvidia-3050-ti-hidpi-screen-w) 
[Reference 2](https://github.com/fcitx/fcitx5/issues/263#issuecomment-977384950)