# Hyprland

## Copilot Key Binding
For those laptop having copilot key on the keyboard. You can bind it for other purpose in hyprland:

p.s. Copilot key is often a macro key on the keyboard, pressing it will send ``Windows Key``+``Shift``+``F23`` to the motherboard 
```conf
bind = SUPER SHIFT, 201, <do action here>
```

## Scaling Applications
If the high DPI monitor is used, some application may not scale properly on hyprland. There are some ways to get them scaled correctly.

### XWayland Applications
First, create an file in ``~/.Xresources`` then put the following arguments:
```
Xft.dpi: <The DPI you want>
```

Then, add the auto start command to hyprland config to apply the changes on hyprland starts:

```conf
exec-once = xrdb -merge ~/.Xresources
```

## KDE Software not themed correctly
It is suggested to use ``qt6ct-kde`` package instead of ``qt6ct``, because it has more compability to KDE series application compared to qt6ct.

[Reference 1](https://github.com/shell-ninja/hyprconf/wiki/Dolphin-setup)


## KDE Dolphin empty "Open with ..." menu
If the "Open with ..." menu is empty in dolphin file manager, you can link the ``.menu`` file to make dolphin find the application list:
```bash
ln -sf /etc/xdg/menus/plasma-applications.menu ~/.config/menus/applications.menu
```

[Reference 1](https://busyogg.github.io/article/687e4eb8a728/#dolphin-%E9%BB%98%E8%AE%A4%E6%96%87%E4%BB%B6%E6%89%93%E5%BC%80%E6%96%B9%E5%BC%8F)
