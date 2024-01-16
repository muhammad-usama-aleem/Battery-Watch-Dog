import subprocess
import os
import csv
import time
from plyer import notification
import pygame


# to make it work with CronJob
os.environ['DISPLAY'] = ':0'
os.environ['XAUTHORITY'] = '/home/usama/.Xauthority'

dbus_session_bus_address = os.environ.get("DBUS_SESSION_BUS_ADDRESS")
os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus,guid=ed6a25fb05118cb5e2c8dca665a49d34"


def parse_data(data):
    # data format: "Battery 0: Discharging, 38%, 01:06:06 remaining"
    _, remaining_data = data.split(': ', 1)
    status, percentage, remaining_time = remaining_data.split(', ')
    remaining_time = remaining_time.strip()
    return {'Status': status, 'Percentage': percentage, 'Remaining Time': remaining_time}


def save_to_csv(data, filename='battery_data.csv'):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    absolute_path = os.path.join(script_directory, filename)
    try:
        with open(absolute_path, 'r') as csvfile:
            pass
    except FileNotFoundError:
        with open(absolute_path, 'w', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Status', 'Percentage', 'Remaining Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(absolute_path, 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Status', 'Percentage', 'Remaining Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow(data)

def battery_notifier(battery_percent, sound_command, notification_title):
    notification_message = f"Level: {battery_percent}%"
    script_directory = os.path.dirname(os.path.abspath(__file__))
    notification_icon = os.path.join(script_directory, "battery.png")

    notification.notify(
        title=notification_title,
        message=notification_message,
        app_name="Battery Monitor",
        app_icon=notification_icon,
        timeout=3
    )
    # os.system(f'notify-send "{notification_title}" "{notification_message}" -i {notification_icon}')

    pygame.mixer.init()
    pygame.mixer.music.load(sound_command)
    pygame.mixer.music.play()
    pygame.time.delay(3000)
    pygame.mixer.music.stop()

def main():
    battery_info = subprocess.check_output(["acpi", "-b"]).decode("utf-8")
    battery_percent = int(battery_info.split(", ")[1].split("%")[0])
    print(battery_info)
    parsed_data = parse_data(battery_info)
    save_to_csv(parsed_data)

    status = "Charging" in battery_info
    full_status = "Full" in battery_info
    
    if status and battery_percent > 95:
        sound_command = "usr/share/sounds/sound-icons/xylofon.wav"
        notification_title = "Battery Full"
        battery_notifier(battery_percent, sound_command, notification_title)
    elif not status and battery_percent < 15:
        sound_command = "/usr/share/sounds/Yaru/stereo/battery-low.oga"
        notification_title = "Battery Low"
        battery_notifier(battery_percent, sound_command, notification_title)
    if full_status:
        pass
    
if __name__ == "__main__":
    main()