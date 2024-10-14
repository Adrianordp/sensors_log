"""
Author: Adriano Rodrigues de Paula

sensors_log.py

Consult "sensors" API tp read fan speed and CPU temperature

Log format:
%Y-%m-%d %H:%M:%S fan_speed_1,fan_speed_2,cpu_temp

"""

import os
import re
import subprocess
import time

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

log_file = os.environ.get("SENSORS_LOG_FILE", "sensors.log")
date_format = "%Y-%m-%d %H:%M:%S"
oldest_date = 31 * 24 * 60 * 60


def delete_old_logs(
    log_file=log_file, date_format=date_format, oldest_date=oldest_date
):
    print(f"__main__.py>>delete_old_logs")
    print(f"Deleting logs older than {oldest_date} seconds")
    now = time.time()
    try:
        with open(log_file, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate(0)
            for line in lines:
                # print(f"line: {line.strip()}")
                line_time = time.mktime(time.strptime(line[:19], date_format))
                # print(f"line_time: {line_time}")
                delta_time = now - line_time
                # print(f"delta_time: {delta_time}")
                if delta_time <= oldest_date:
                    # print(f"Writing line: {line}")
                    f.write(line)
                else:
                    # print(f"Skipping line: {line}")
                    pass
    except FileNotFoundError:
        # print(f"File {log_file} not found")
        # print("Skipping...")
        pass


def capture_fan_speeds(sensors_out_split):
    print("__main__.py>>capture_fan_speeds")
    print("Capturing fan speeds...")
    fan_speed_lines = [line for line in sensors_out_split if "fan" in line]
    fan_speeds = ",".join([line.split()[1] for line in fan_speed_lines])
    return fan_speeds


def capture_cpu_temp(sensors_out_split):
    print("__main__.py>>capture_cpu_temp")
    print("Capturing CPU temperature...")
    cpu_temp_line = [line for line in sensors_out_split if "CPU:" in line]
    cpu_temp = cpu_temp_line[0].split()[1]
    cpu_temp = re.match("\+(\d+\.\d+).*", cpu_temp).group(1)
    return cpu_temp


def read_sensors():
    print("__main__.py>>read_sensors")
    print("Reading sensors process...")
    sensors_out = subprocess.check_output(["sensors"]).decode("utf-8")
    return sensors_out


def read_sensors_split():
    print("__main__.py>>read_sensors_split")
    print("Reading sensors process as a list...")
    sensors_out = read_sensors()
    sensors_out_split = sensors_out.splitlines()
    return sensors_out_split


def capture_sensors_reads():
    print("__main__.py>>capture_sensors_reads")
    print("Capturing sensor reads...")
    sensors_out_split = read_sensors_split()
    fan_speeds = capture_fan_speeds(sensors_out_split)
    cpu_temp = capture_cpu_temp(sensors_out_split)
    sensor_reads = ",".join((fan_speeds, cpu_temp))
    return sensor_reads


def write_logs(sensor_reads, log_file=log_file, date_format=date_format):
    print("__main__.py>>write_logs")
    print("Writing logs...")
    time_str = time.strftime(date_format)
    with open(log_file, "a") as f:
        print(f"{time_str} {sensor_reads}")
        f.write(f"{time_str} {sensor_reads}\n")


def plot_log(log_file=log_file, date_format=date_format):
    print("__main__.py>>plot_log")
    print("Plotting logs...")

    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {log_file} not found")
        print("Skipping...")
        return

    dates = [line[:19] for line in lines]
    dates = [time.strptime(date, date_format) for date in dates]
    dates = [time.mktime(date) for date in dates]
    dates = np.array(dates)

    fan_speeds = [line[20:].strip() for line in lines]
    fan_speeds = [line.split(",") for line in fan_speeds]
    fan_speeds = [
        [float(number) if number != "N/A" else 0 for number in line]
        for line in fan_speeds
    ]
    fan_speeds = np.array(fan_speeds, dtype=float)

    fig, ax = plt.subplots()
    plt.rcParams["date.converter"] = "concise"
    plt.rcParams["timezone"] = "America/Manaus"
    # ax.xaxis_date(tz="America/Manaus")
    ax.plot(dates.astype("datetime64[s]"), fan_speeds, "b-")
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_minor_locator(mdates.MinuteLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_ylim(0, 4500)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.show()


def main():
    print("__main__.py>>main")
    delete_old_logs()
    while True:
        sensor_reads = capture_sensors_reads()
        write_logs(sensor_reads)
        time.sleep(1)


if __name__ == "__main__":
    main()
