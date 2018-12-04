#!/usr/bin/env python3


from collections import defaultdict


def load_schedule():
    sleepsched = defaultdict(lambda: defaultdict(int))  # keyed by guard then minute
    guard = None  # which guard is on shift now
    fell_at = None  # (hour, minute) tuple of when the guard fell asleep. None if not asleep

    with open("input.txt") as f:
        records = sorted([i.strip() for i in f.readlines()])

    for line in records:
        minute = int(line[15:17])
        hour = int(line[12:14])
        msg = line[19:]

        if msg[0] == 'G':  # new guard comes on shift
            guard = int(msg[7:].split(" ", 1)[0])
            fell_at = None

        elif msg[0] == 'f':  # guard falls asleep
            fell_at = (hour, minute)

        elif msg[0] == 'w':  # guard wakes
            if guard and fell_at:
                """
                Called when a guard wakes up. Updates their sleep schedule.
                NOTE: in my sample the guard never falls asleep outside of hour 0 so, we're disregarding f_hour
                """
                for i in range(fell_at[1], minute):
                    sleepsched[guard][i] += 1
    return sleepsched


def main():
    sleepsched = load_schedule()
    # Find guard with most total time asleep
    guard_sleepsmost = -1
    guard_max_mins = 0
    for guard, schedule in sleepsched.items():
        total = sum(schedule.values())
        if total > guard_max_mins:
            guard_max_mins = total
            guard_sleepsmost = guard

    print("Sleepiest guard is {}, total minutes asleep {}".format(guard_sleepsmost, guard_max_mins))

    # Find minute the above guard spend the most time asleep
    best_minute = -1
    max_time = -1
    for minute, duration in sleepsched[guard_sleepsmost].items():
        if duration > max_time:
            max_time = duration
            best_minute = minute

    print("best minute is {} for a total of {}".format(best_minute, max_time))
    print("Final answer: {}".format(best_minute * guard_sleepsmost))


if __name__ == '__main__':
    main()
