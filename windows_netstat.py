import subprocess
import time
from datetime import datetime
import os
import csv
import time
import argparse

# python3 windows_netstat.py :80
# netstat -ano | find ":80" | find "ESTABLISHED" /c

parser = argparse.ArgumentParser()
parser.add_argument("port", type=str, help="port")
args = parser.parse_args()

timeFormat = "%Y-%m-%d %H:%M:%S.%f"

starTimeTitle = "时间"
connectionsTitle = "连接数"

while True:
    starTime = datetime.now()
    timeNow = starTime.strftime(timeFormat)

    try:
        output = subprocess.check_output(
            'netstat -ano | find "{0}" | find "ESTABLISHED" /c'.format(args.port), shell=True)
        connections = output.decode('utf-8').strip()

        nowTime = datetime.now()
        csvFileName = "netstat_{0}.csv".format(nowTime.strftime("%Y-%m-%d"))
        if os.path.exists(csvFileName) is not True:
            with open(csvFileName, "w", encoding="utf-8", newline="") as csvfile:
                fieldnames = [starTimeTitle, connectionsTitle]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

        with open(csvFileName, "a", encoding="utf-8", newline="") as csvfile:
            fieldnames = [starTimeTitle, connectionsTitle]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(
                {starTimeTitle: timeNow, connectionsTitle: connections})
    except subprocess.CalledProcessError as e:
        print(
            "command '{0}' return with error (code {1}): {2}".format(
                e.cmd,
                e.returncode,
                e.output))

    time.sleep(0.2)
