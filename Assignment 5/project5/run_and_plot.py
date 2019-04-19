import matplotlib.pyplot as plt
import csv
import numpy as np
file_names = ["READ UNCOMMITTED.csv", "READ COMMITED.csv", "REPEATABLE READ.csv", "SERIALIZABLE.csv"]


file_name = file_names[1]
ps = []
times = []
corrects = []

with open(file_name) as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        ps.append(int(row[1]))
        corrects.append(float(row[3]))
        times.append(float(row[4]))

print len(times)
print len(corrects)

p_corrects = []
p_times = []
distinct_ps = []
for i in range(len(ps)/20):
    start = i*20
    end = (i+1)*20
    p_corrects.append(corrects[start:end])
    p_times.append(times[start:end])
    distinct_ps.append(ps[start])

# print avg_times
# print avg_corrects
print np.asarray(p_corrects)

def draw_plot(data, offset,edge_color, fill_color):
    pos = np.arange(data.shape[1])+offset
    bp = ax.boxplot(data, positions= pos, widths=0.3, patch_artist=True, manage_xticks=False)
    for element in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)
    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)



fig, ax = plt.subplots()
# draw_plot(np.asarray(p_corrects), 0, "tomato", "white")

bp = ax.boxplot(np.asarray(p_corrects).T, showmeans=True)
ax.set_xticklabels(distinct_ps)
ax.set_xlabel("Number of subprocesses")
ax.set_ylabel("Correctness")

plt.show()







