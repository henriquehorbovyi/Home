import time
from datetime import datetime


def set_alarm_for(t, on_time_up):
    alarm_hour = t[0:2]
    alarm_min = t[3:5]
    alarm_period = t[6:].upper()

    while True:
        now = datetime.now()
        current_hour = now.strftime("%I")
        current_min = now.strftime("%M")
        current_period = now.strftime("%p")

        if alarm_period == current_period and alarm_hour == current_hour and alarm_min == current_min:
            print("Wake Up!")
            on_time_up()
            break
        print("tic-toc...")
        time.sleep(5)

