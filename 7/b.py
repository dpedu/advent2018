#!/usr/bin/env python3


class Job(object):
    def __init__(self, id, reqs, duration):
        self.id = id
        self.reqs = reqs
        self.duration = duration

    def __repr__(self):
        return "<Job '{}'' ({}s) reqs:{}>".format(self.id, self.duration, self.reqs)


class Worker(object):
    def __init__(self):
        self.task = None
        self.busy = 0

    def __repr__(self):
        return "<Worker {} (busy for {}s) (job:{})>".format(id(self), self.busy, self.task)


def main():
    num_workers = 5
    workers = [Worker() for i in range(0, num_workers)]

    jobs = {}

    def makejob(jobid):
        if jobid not in jobs:
            jobs[jobid] = Job(jobid, set(), ord(jobid) - 64 + 60)

    with open("input.txt") as f:
        for line in f.readlines():
            _, stepid, _, _, _, _, _, blocks, _, _ = line.split()
            makejob(stepid)
            makejob(blocks)
            jobs[blocks].reqs.update([stepid])

    duration = 0  # the answer
    completed = set()
    while True:
        # do worker accounting
        remainings = [worker.busy for worker in workers if worker.task is not None]

        # find the next worker(s) to complete
        if remainings:
            next_done = min(remainings)

            # fast-forward time to that point
            duration += next_done
            for worker in workers:
                if worker.task:
                    worker.busy -= next_done
                    if worker.busy == 0:
                        print("finished task:", worker.task)
                        completed.update([worker.task.id])
                        worker.task = None

        if not jobs and all([worker.task is None for worker in workers]):
            break

        # find available tasks
        available = [task for taskid, task in jobs.items() if task.reqs.issubset(completed)]

        # sort by weight
        available.sort(key=lambda x: x.duration)

        # assign tasks to available workers
        for worker in workers:
            if worker.task is None:
                if not available:
                    break
                task = available.pop()
                worker.task = task
                worker.busy = task.duration
                print("assigned", task, "to", worker)
                del jobs[task.id]  # remove job from work queue

    print(duration)


if __name__ == '__main__':
    main()
