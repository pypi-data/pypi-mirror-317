import os
import configparser

low_expire_timeout = 0

critical_expire_timeout = 0

discharging_enable = True
discharging_expire_timeout = 0

charging_enable = True
charging_expire_timeout = 5000


def load():
    config_file_path = os.path.expanduser('~/.config/battery_notifier/config.ini')

    # Retrun if there's no user config file
    if not os.path.exists(config_file_path):
        return

    # Load config file
    _config = configparser.ConfigParser()
    _config.read(config_file_path)

    global low_expire_timeout
    low_expire_timeout = _config.getint("low", "expire_timeout", fallback=low_expire_timeout)

    global critical_expire_timeout
    critical_expire_timeout = _config.getint("critical", "expire_timeout", fallback=critical_expire_timeout)

    global discharging_enable
    discharging_enable = _config.getboolean("discharging", "enable", fallback=discharging_enable)

    global discharging_expire_timeout
    discharging_expire_timeout = _config.getint("discharging", "expire_timeout", fallback=discharging_expire_timeout)

    global charging_enable
    charging_enable = _config.getboolean("charging", "enable", fallback=charging_enable)

    global charging_expire_timeout
    charging_expire_timeout = _config.getint("charging", "expire_timeout", fallback=charging_expire_timeout)
