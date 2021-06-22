from datetime import datetime


def what_time_is_it():
    now = datetime.now()
    hour, minute = now.hour, now.minute
    if int(hour) <= 1:
        hour_t = "hour"
    else:
        hour_t = "hours"

    if int(hour) <= 1:
        min_t = "minute"
    else:
        min_t = "minutes"

    return "it's {0} {1} and {2} {3}".format(hour, hour_t, minute, min_t)


def when_is_it_today():
    now = datetime.now()
    template = now.strftime("%B %d, year %Y")

    return "today is {}".format(template)
