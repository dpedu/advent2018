#!/usr/bin/env python3


from a import load_schedule


def main():
    sleepsched = load_schedule()
    fat_minutes = {}  # guard ID -> (bestminute, percentage)

    # Find the minute spent asleep the most for each guard
    for guard, schedule in sleepsched.items():
        best_minute = -1
        best_minute_time = -1
        for minute in range(0, 60):
            if schedule[minute] > best_minute_time:
                best_minute_time = schedule[minute]
                best_minute = minute
        fat_minutes[guard] = (best_minute, best_minute_time)

    # Find the guard who spent the most time asleep on their best minute
    best_guard = -1
    best_minute = -1
    best_minsaslp = -1
    for guard, guardinfo in fat_minutes.items():
        minute, minsaslp = guardinfo
        if minsaslp > best_minsaslp:
            best_guard = guard
            best_minute = minute
            best_minsaslp = minsaslp

    print("Guard {} minute {} ({}m)".format(best_guard, best_minute, minsaslp))
    print("Final answer: {}".format(best_guard * best_minute))


if __name__ == '__main__':
    main()
