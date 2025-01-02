<p align="center">
  <img src="https://github.com/user-attachments/assets/bca7fb8e-a4ad-435b-aa40-c26dbb017239" alt="hints" />
  <a href="https://www.keytilt.xyz" target="_blank">
    <img src="https://github.com/user-attachments/assets/b44f8021-7f1f-4a60-9be4-561662266e96" alt="keytilt"/>
  </a>
</p>

# Click, scroll, and drag with your keyboard

![demo](https://github.com/user-attachments/assets/838d4043-5e21-4e61-979f-bd8fae7d4d36)

Navigate GUIs without a mouse by typing hints in combination with modifier keys.

- click once (<kbd>j</kbd><kbd>k</kbd>)
- click multiple times (<kbd>2</kbd><kbd>j</kbd><kbd>k</kbd>)
- right click (<kbd>SHIFT</kbd> + <kbd>j</kbd><kbd>k</kbd>)
- drag (<kbd>ALT</kbd> + <kbd>j</kbd><kbd>k</kbd>)
- hover (<kbd>CTRL</kbd> + <kbd>j</kbd><kbd>k</kbd>)
- scroll/move the mouse using vim key bindings (<kbd>h</kbd>,<kbd>j</kbd>,<kbd>k</kbd>,<kbd>l</kbd>)

Don't like the keybindings? That's ok, you can change them.

# Installing

## System Requirements

1. You will need to have some sort of [compositing](https://wiki.archlinux.org/title/Xorg#Composite) setup so that you can properly overlay hints over windows with the correct level of transparency. Otherwise, the overlay will just cover the entire screen; not allowing you to see what is under the overlay.

2. You will need to enable accessibility for your system. If you use a Desktop Environment, this might already be enabled by default. If you find that hints does not work or works for some apps and not others add the following to `/etc/environment`

```
ACCESSIBILITY_ENABLED=1
GTK_MODULES=gail:atk-bridge
OOO_FORCE_DESKTOP=gnome
GNOME_ACCESSIBILITY=1
QT_ACCESSIBILITY=1
QT_LINUX_ACCESSIBILITY_ALWAYS_ON=1
```

3. Install hints:

Below you will find installation instructions for some popular linux distros bases. The setup is as follows:

- Install the python/system dependencies (including [pipx](https://pipx.pypa.io/stable/installation/)).
- Setup pipx.
- Use pipx to install hints.

Ubuntu

```
sudo apt update && \
    sudo apt install git ydotool libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-4.0 pipx && \
    pipx ensurepath && \
    pipx install git+https://github.com/AlfredoSequeida/hints.git
```

Fedora

```
sudo dnf install git ydotool gcc gobject-introspection-devel cairo-gobject-devel pkg-config python3-devel gtk4 pipx && \
    pipx ensurepath && \
    pipx install git+https://github.com/AlfredoSequeida/hints.git
```

Arch

```
sudo pacman -Sy && \
    sudo pacman -S git ydotool python cairo pkgconf gobject-introspection gtk4 libwnck3 python-pipx && \
    pipx ensurepath && \
    pipx install git+https://github.com/AlfredoSequeida/hints.git
```

Finally, source your shell config or restart your terminal.

## Setup

1. Hints uses ydotool for mouse movements to support both wayland and x11. Ydotool has a service that must be started:

NOTE: There is currently an issue when using the drag feature with ydotool (if you are using the drag feature in a file manager you might notice your input becomes locked up. If this happens you will need to quit hints by switching to another [tty session](#development-tips) or restarting your system). This is not a bug with hints, but rather a bug with ydotool as it can be replicated without hints.

enable the service so that it starts on its own with every reboot:

```
systemctl --user enable ydotool.service
```

start the service for the current session:

```
systemctl --user start ydotool.service
```

2. Window manager specific setups:

### Sway

1. Ydotool won't work as expected if mouse acceleration for the ydotool virtual devices is not disabled.

Find the ydotoold mouse virtual device

```
> swaymsg -t get_inputs
...
Input device: ydotoold virtual device
  Type: Mouse
  Identifier: 9011:26214:ydotoold_virtual_device
  Product ID: 26214
  Vendor ID: 9011
  Libinput Send Events: enabled
...
```

Add a rule in your sway config file to remove acceleration for this input device using the `Identifier` you found.

```
input 9011:26214:ydotoold_virtual_device {
    accel_profile "flat"
}
```

reload your sway session.

```
swaymsg reload
```

2. Other dependencies:

   - Install [grim](https://sr.ht/~emersion/grim/) so the opencv backend can take screenshots.
   - Install [jq](https://github.com/jqlang/jq) to parse `swaymsg`.

3. At this point, hints should be installed, you can verify this by running `hints` in your shell. You will want to bind a keyboard shortcut to `hints` so you don't have to keep typing in a command to open it. This will depend on your OS/ window manager / desktop environment.

Here is an example of a binding on i3 by editing `.conf/i3/config`:

```
bindsym $mod+i exec hints
```

This will bind <kbd>mod</kbd> + <kbd>i</kbd> to launch hints. To stop showing hints (quit hints), press the <kbd>Esc</kbd> key on your keyboard.

Hints also has a scroll mode to scroll, which can also be bound to a key combination. For example:

```
bindsym $mod+y exec hints --mode scroll
```

If you still don't see any hints, the application you're testing could need a bit of extra setup. Please see the [Help,-hints-doesn't-work-with-X-application](https://github.com/AlfredoSequeida/hints/wiki/Help,-hints-doesn't-work-with-X-application) page in the wiki.

# Documentation

For a guide on configuring and using hints, please see the [Wiki](https://github.com/AlfredoSequeida/hints/wiki).

# Contributing

The easiest ways to contribute are to:

- [Become a sponsor](https://github.com/sponsors/AlfredoSequeida). Hints is a passion project that I really wanted for myself and I am working on it in my spare time. I chose to make it free and open source so that others can benefit. If you find it valuable, donating is a nice way to say thanks. You can donate any amount you want.
- Report bugs. If you notice something is not working as expected or have an idea on how to make hints better, [open up an issue](https://github.com/AlfredoSequeida/hints/issues/new). This helps everyone out.
- If you can code, feel free to commit some code! You can see if any issues need solutions or you can create a new feature. If you do want to create a new feature, it's a good idea to create an issue first so we can align on why this feature is needed and if it has a possibility of being merged.

## Development

If you want to help develop hints, first setup your environment:

1. Create a virtual environment for the project.

```
python3 -m venv venv
```

2. Activate your virtual environment for development. This will differ based on OS/shell. See the table [here](https://docs.python.org/3/library/venv.html#how-venvs-work) for instructions.

3. Install hints as an editable package (from the repositorie's root directory):

```
pip install -e .
```

At this point, hints should be installed locally in the virtual environment, you can run `hints` in your shell to launch it. Any edits you make to the source code will automatically update the installation. For future development work, you can simply re-enable the virtual environment (step 2).

## Development tips

- If you are making updates that impact hints, you will most likely need to test displaying hints and might find yourself executing hints but not being quick enough to switch to a window to see hints. To get around this, you can execute `hints` with a short pause in your shell: `sleep 0.5; hints`. This way you can have time to switch to a window and see any errors / logs in your shell.
- If `hints` is consuming all keyboard inputs and you're trapped: switch to a virtual terminal with e.g. <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>F2</kbd>, login, and run `killall hints`. You can then exit with `exit` and switch back to the the previous session (most likely 1): <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>F1</kbd>
