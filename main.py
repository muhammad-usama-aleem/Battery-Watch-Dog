import subprocess
import os
import csv
import time
from plyer import notification


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
    notification_icon = os.path.join(os.getcwd(), "battery.png")

    notification.notify(
        title=notification_title,
        message=notification_message,
        app_name="Battery Monitor",
        app_icon=notification_icon,
        timeout=10  # Notification timeout in seconds
    )
    subprocess.run(sound_command, shell=True)

def main():
    battery_info = subprocess.check_output(["acpi", "-b"]).decode("utf-8")
    battery_percent = int(battery_info.split(", ")[1].split("%")[0])
    print(battery_info)
    parsed_data = parse_data(battery_info)
    save_to_csv(parsed_data)

    status = "Charging" in battery_info
    
    if status and battery_percent > 90:
        sound_command = "paplay /usr/share/sounds/sound-icons/xylofon.wav"
        notification_title = "Battery Full"
        battery_notifier(battery_percent, sound_command, notification_title)
    elif battery_percent < 80:
        sound_command = "paplay --volume=65536 /usr/share/sounds/Yaru/stereo/battery-low.oga"
        notification_title = "Battery Low"
        battery_notifier(battery_percent, sound_command, notification_title)

if __name__ == "__main__":
    main()