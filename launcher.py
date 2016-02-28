# -*- coding: utf-8 -*-


import subprocess
import signal
import time


def handler(signum, frame):
    print 'Start kill "run.py" ...'
    subprocess.Popen(['pkill', '-SIGINT', 'run.py'])


if __name__ == "__main__":

    process_count = 10
    for i in range(process_count):
        subprocess.Popen(['python', 'run.py'])

    signal.signal(signal.SIGINT, handler)

    while True:
        time.sleep(1)
