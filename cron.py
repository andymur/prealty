#!/usr/bin/python3
import schedule
import time
from daemonize import Daemonize
import os
import sys

def job():
    print("I'm working...")
    f = open("/home/antti/dom.txt", "a")
    f.write(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    f.close()

schedule.every(1).hour.do(job)


def main():
    while True:
        schedule.run_pending()
        time.sleep(300)

if __name__ == "__main__":
    main()
