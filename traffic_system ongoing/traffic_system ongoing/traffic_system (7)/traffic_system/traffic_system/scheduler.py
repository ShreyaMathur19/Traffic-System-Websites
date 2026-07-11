# scheduler.py
import random, datetime

def pick_random_time(window):
    start_str, end_str = window
    start = datetime.datetime.strptime(start_str, "%H:%M").time()
    end = datetime.datetime.strptime(end_str, "%H:%M").time()

    start_m = start.hour * 60 + start.minute
    end_m = end.hour * 60 + end.minute
    m = random.randint(start_m, end_m)

    return datetime.time(m // 60, m % 60)
