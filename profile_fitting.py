class Job:
    def __init__(self, name, time_needed_on_machines, num_of_machines):
        self.name = name
        self.num_of_machines = num_of_machines
        self.time_needed_on_machines = time_needed_on_machines
        self.leaving_time_on_machines = [0] * num_of_machines

    def cumulative_time_on_machines(self, num_of_seen_machines):
        sum = 0
        for i in range(num_of_seen_machines):
            sum += self.time_needed_on_machines[i]
        return sum

    def overall_time_on_machines(self):
        temp = self.cumulative_time_on_machines(self.num_of_machines)
        # print("overall time on machines for JOB " + str(self.name) + " is : " + str(temp))
        return temp

    def update_leaving_time_on_machines(self, last_job_done):
        if last_job_done == None:
            #         first job scenario
            for i in range(self.num_of_machines):
                self.leaving_time_on_machines[i] = self.cumulative_time_on_machines(i + 1)
        else:

            self.leaving_time_on_machines[0] = max(
                last_job_done.leaving_time_on_machines[0] + self.time_needed_on_machines[0],
                last_job_done.leaving_time_on_machines[1])

            for i in range(1, num_of_machines - 1, 1):
                self.leaving_time_on_machines[i] = max(
                    self.leaving_time_on_machines[i - 1] + self.time_needed_on_machines[i],
                    last_job_done.leaving_time_on_machines[i + 1])

            self.leaving_time_on_machines[self.num_of_machines - 1] = max(
                self.leaving_time_on_machines[self.num_of_machines - 2],
                last_job_done.leaving_time_on_machines[self.num_of_machines - 1]) + self.time_needed_on_machines[
                                                                          self.num_of_machines - 1]

        # print("name: " + str(self.name) + " D: " + str(self.leaving_time_on_machines))

    def compute_total_idle_time(self, last_job_done):
        self.update_leaving_time_on_machines(last_job_done)
        sum = 0
        for i in range(self.num_of_machines):
            sum += self.leaving_time_on_machines[i] - last_job_done.leaving_time_on_machines[i] - \
                   self.time_needed_on_machines[i]
        # print("name: " + str(self.name), " : idle time: ", str(sum))
        return sum

    def __str__(self):
        return str(self.name)


def input_util(name, num_of_machines):
    s = []
    for i in range(num_of_machines):
        temp = "P [M: " + str(i + 1) + " ][J: " + str(name) + " ]"
        s.append(temp)
    return ", ".join(s)


# main
selected_jobs = []
not_yet_selected_jobs = []
num_of_jobs = int(input("Enter num of jobs: \t"))
num_of_machines = int(input("Enter num of machines: \t"))
for i in range(num_of_jobs):
    name = input("Please enter JOB[ " + str(i + 1) + " ] 's name: \t")
    my_input = input(
        "Please enter process time on machines respect to following format\n"
        + str(input_util(name, num_of_machines)) + "\t")
    needed_time_on_machines = list(map(float, my_input.split(",")))
    not_yet_selected_jobs.append(Job(name, needed_time_on_machines, num_of_machines))
# sample
# num_of_jobs = 5
# num_of_machines = 4
# not_yet_selected_jobs.append(Job(1, [5, 4, 4, 3], num_of_machines))
# not_yet_selected_jobs.append(Job(2, [5, 4, 4, 6], num_of_machines))
# not_yet_selected_jobs.append(Job(3, [3, 2, 3, 3], num_of_machines))
# not_yet_selected_jobs.append(Job(4, [6, 4, 4, 2], num_of_machines))
# not_yet_selected_jobs.append(Job(5, [3, 4, 1, 5], num_of_machines))

not_yet_selected_jobs.sort(key=lambda x: x.overall_time_on_machines(), reverse=True)
selected_job = not_yet_selected_jobs.pop()
selected_job.update_leaving_time_on_machines(None)
selected_jobs.append(selected_job)
for i in range(num_of_jobs - 1):
    last_selected_job = selected_jobs[len(selected_jobs) - 1]
    not_yet_selected_jobs.sort(key=lambda x: x.compute_total_idle_time(selected_job), reverse=True)
    selected_job = not_yet_selected_jobs.pop()
    selected_jobs.append(selected_job)
time_span = 0
for job in selected_jobs:
    time_span = max(job.leaving_time_on_machines[num_of_machines - 1], time_span)

sorted_jobs = list(map(str, selected_jobs))
print("Time Span: ", time_span, " & The Sequence is : ", end=' ')
print(', '.join(sorted_jobs))
