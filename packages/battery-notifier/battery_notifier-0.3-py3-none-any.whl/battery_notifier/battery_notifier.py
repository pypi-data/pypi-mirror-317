#!/usr/bin/env python

from gi.repository import GLib
from math import floor
from pydbus import SystemBus, SessionBus
from random import randint

from . import config

UPOWER_TYPE_BATTERY = 2
UPOWER_STATE_CHARGING = 1
UPOWER_STATE_DISCHARGING = 2
UPOWER_STATE_FULLY_CHARGED = 4
UPOWER_WARNING_LEVEL_UNKNOWN = 0
UPOWER_WARNING_LEVEL_LOW = 3
UPOWER_WARNING_LEVEL_CRITICAL = 4

system_bus = SystemBus()
session_bus = SessionBus()

battery_proxy = None
prev_warning_level = UPOWER_WARNING_LEVEL_UNKNOWN
prev_state = UPOWER_STATE_CHARGING
notifications = None
replaces_id = 0


def get_level(percentage):
    return str(floor((percentage + 5.) * 0.1) * 10)


def notify(a, b, c):
    global battery_proxy, prev_warning_level, prev_state, notifications, replaces_id

    send = False

    app_icon = ""
    summary = ""
    expire_timeout = 0

    if battery_proxy.WarningLevel != prev_warning_level:  # Warning level has changed
        prev_warning_level = battery_proxy.WarningLevel

        if battery_proxy.State == UPOWER_STATE_DISCHARGING:  # Discharging
            if battery_proxy.WarningLevel == UPOWER_WARNING_LEVEL_LOW:  # Low
                app_icon = "battery-caution-symbolic"
                summary = "Battery low"
                expire_timeout = config.low_expire_timeout
                send = True

            elif battery_proxy.WarningLevel == UPOWER_WARNING_LEVEL_CRITICAL:  # Critical
                app_icon = "battery-action-symbolic"
                summary = "Battery critical"
                expire_timeout = config.critical_expire_timeout
                send = True

    if battery_proxy.State != prev_state:  # State has changed
        prev_state = battery_proxy.State

        if not send:  # Not already sending a notification
            if config.discharging_enable and battery_proxy.State == UPOWER_STATE_DISCHARGING:  # Discharging
                app_icon = "battery-level-" + get_level(battery_proxy.Percentage) + "-symbolic"
                summary = "Battery discharging"
                expire_timeout = config.discharging_expire_timeout
                send = True

            elif config.charging_enable and battery_proxy.State == UPOWER_STATE_CHARGING:  # Charging
                app_icon = "battery-level-" + get_level(battery_proxy.Percentage) + "-charging-symbolic"
                summary = "Battery charging"
                expire_timeout = config.charging_expire_timeout
                send = True

        prev_state = battery_proxy.State

    if send:
        notifications.Notify("battery_notifier", replaces_id, app_icon, summary, "", [], {}, expire_timeout)


def main():
    global replaces_id
    replaces_id = randint(65535, 4294967295)

    upower_proxy = system_bus.get("org.freedesktop.UPower")

    devices = upower_proxy.EnumerateDevices()

    global battery_proxy

    # Find the battery
    for device in devices:
        device_proxy = system_bus.get("org.freedesktop.UPower", device)

        if device_proxy.Type == UPOWER_TYPE_BATTERY:
            battery_proxy = device_proxy
            break

    if battery_proxy is None:
        print("No battery found")
        return

    global notifications
    notifications = session_bus.get(".Notifications")

    battery_proxy.PropertiesChanged.connect(notify)

    GLib.MainLoop().run()


if __name__ == "__main__":
    main()
