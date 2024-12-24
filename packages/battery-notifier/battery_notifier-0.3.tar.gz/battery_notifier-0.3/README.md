# battery_notifier

Sends desktop notifications for low and critical battery warnings, and optionally when charging/discharging state
changes

## Installation

battery_notifier has the following dependencies available on PyPI:

- `pydbus`
- `PyGObject`

The package can be installed using [pipx](https://pipx.pypa.io/stable/installation/), e.g.:

```bash
pipx install battery_notifier
```

## Configuration

battery_notifier can be configured with a file located at `~/.config/battery_notifier/config.ini`, e.g.

```ini
[low]
expire_timeout = 0

[critical]
expire_timeout = 0

[discharging]
enable = true
expire_timeout = 0

[charging]
enable = true
expire_timeout = 5000
```

## Starting with systemd

A systemd service file is included in this repository which can be enabled and started like so:

```bash
# Copy the service file
cp battery_notifier.service ~/.local/share/systemd/user/

# Enable the service
systemctl --user enable battery_notifier

# Start the service
systemctl --user start battery_notifier
```
