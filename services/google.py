import requests
from datetime import datetime

base_url = "http://127.0.0.1:1880"
upcoming_event_url = base_url + "/upcoming_event"
upcoming_events_url = base_url + "/upcoming_events"
date_mask = "%Y-%m-%dT%H:%M:%S.%fZ"


def upcoming_events():
    response = requests.get(upcoming_events_url)
    events = response.json()


def upcoming_event():
    now = datetime.strftime(datetime.now(), date_mask)
    now = datetime.strptime(now, date_mask)

    response = requests.get(upcoming_event_url)
    event = response.json()
    title = event['title']
    when = ""
    event_time = datetime.strptime(event['start'], date_mask)
    event_time = event_time.replace(hour=event_time.hour - 3)
    delta_day = event_time.day - now.day

    if delta_day == 1:  # event is tomorrow
        if event_time.minute == 0:
            m = ""
        else:
            m = "and {}".format(event_time.minute)
        when = "tomorrow at {0} {1}".format(event_time.hour, m)
    elif delta_day > 1:  # event is someday after tomorrow
        if event_time.minute == 0:
            m = ""
        else:
            m = "and {}".format(event_time.minute)
        when = "in {0} {1} at {2} {3}".format(event_time.strftime("%B"), event_time.day, event_time.hour, m)
    elif delta_day == 0:  # event is today
        delta_hour = event_time.hour - now.hour
        delta_min = event_time.minute - now.minute

        if delta_hour == 0:  # same hour
            if delta_min > 0:  # some minutes in the future
                if delta_min == 1:
                    m = " minute"
                else:
                    m = " minutes"
                m = str(delta_min) + m
                when = "and you have {0} left".format(m)

            elif delta_min == 0:  # right now (run)
                when = "has started right now. I advice you to hurry"

            else:  # it already started :O
                late_by = abs(delta_min)

                if late_by == 1:
                    m = " minute"
                else:
                    m = " minutes"
                m = str(late_by) + m
                when = "and you're late by {0}".format(m)

        elif delta_hour > 0:  # some hour(s) in the future
            if delta_hour == 1:
                h = "hour"
            else:
                h = "hours"

            when = "in {0} {1}".format(delta_hour, h)
        else:
            late_hour = abs(delta_hour)
            if late_hour == 1:
                h = "hour"
            else:
                h = "hours"

            when = "the event started {0} {1} ago".format(late_hour, h)

    return "Your upcoming event is {0}, {1}".format(title, when)


print(upcoming_event())
