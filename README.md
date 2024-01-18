# Battery-Watch-Dog


**Battery Watch Dog** is a Python script designed to monitor and log battery information on a Linux system. It provides notifications for specific battery events and keeps a record of battery data in a CSV file.

## Features

- **Real-time Monitoring**: The script uses the `acpi` command to fetch real-time battery information, including status, percentage, and remaining time.

- **Data Logging**: Battery data is logged in a CSV file (`battery_data.csv` by default), capturing details such as timestamp, status, percentage, and remaining time.

- **Notifications**: Depending on the battery status, the script triggers notifications for specific events such as low battery and full charge.

- **Sound Alerts**: Alongside notifications, the script plays sound alerts to draw attention to critical battery conditions.

## Requirements

- **Python**: Make sure you have Python installed on your system.

- **Plyer Library**: Install the Plyer library to enable desktop notifications.

```bash
pip install plyer
```


# Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/muhammad-usama-aleem/Battery-Watch-Dog.git
    cd Battery-Watch-Dog
    ```

2. **Run the script:**

    ```bash
    python3 battery_watch_dog.py
    ```
    Cronjob:
   
   ```bash
   */5 * * * * export DISPLAY=:0 &&  /home/usama/crons/battery_reminder/run_battery_reminder.sh >> /home/usama/crons/battery_reminder/cron.log 2>&1
   ```

4. **Monitor the terminal for real-time battery information and check the `battery_data.csv` file for historical data.**


# Customization

Feel free to customize the script based on your preferences. 
Adjust the notification thresholds, sound alerts, or any other parameters to suit your needs.

Example:
 - ```bash
   notification.notify(
       title=notification_title,
       message=notification_message,
       app_name="Battery Monitor",
       app_icon=notification_icon,
       timeout=15   #Notification timeout in seconds)
   ```

- Modify sound commands:
  ```bash
  sound_command = "paplay --volume=65536 /path/to/custom_low_battery_sound.oga
  ```

# Contributing

If you encounter issues or have suggestions for improvements,# please create an issue or submit a pull request on the GitHub repository.

# License

 This project is licensed under the MIT License.
