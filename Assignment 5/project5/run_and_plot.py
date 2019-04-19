import matplotlib.pyplot as plt
import csv
import numpy as np
file_names = ["READ UNCOMMITTED.csv", "READ COMMITTED.csv", "REPEATABLE READ.csv", "SERIALIZABLE.csv"]


for file_name in file_names:
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
    user_correct_mean = []
    user_time_mean = []
    for i in range(len(ps)/20):
        start = i*20
        end = (i+1)*20
        p_corrects.append(corrects[start:end])
        p_times.append(times[start:end])
        distinct_ps.append(ps[start])
        user_correct_mean.append(np.average(corrects[start:end]))
        user_time_mean.append(np.average(times[start:end]))

    type = file_name.replace(".csv", "")
    p_corrects = np.asarray(p_corrects).T
    p_times = np.asarray(p_times).T
    distinct_ps = np.asarray(distinct_ps)

    # fig, ax = plt.subplots()
    # bp = ax.boxplot(np.asarray(p_corrects).T, usermedians=user_correct_mean, whis="range")
    # ax.set_xticklabels(distinct_ps)
    # ax.set_xlabel("Number of subprocesses")
    # ax.set_ylabel("Correctness")
    # ax.set_title(type)
    # plt.savefig(file_name.replace(".csv", "-correctness.png"))
    #
    # fig, ax2 = plt.subplots()
    # bp2 = ax2.boxplot(np.asarray(p_times).T, usermedians=user_time_mean, whis="range")
    # ax2.set_xticklabels(distinct_ps)
    # ax2.set_xlabel("Number of subprocesses")
    # ax2.set_ylabel("Time(s)")
    # ax2.set_title(type)
    # plt.savefig(file_name.replace(".csv", "-time.png"))

    # mins = p_corrects.min(0)
    # maxes = p_corrects.max(0)
    # means = p_corrects.mean(0)
    # std = p_corrects.std(0)
    #
    # # create stacked errorbars:
    # plt.errorbar(np.arange(11), means, std, fmt='ok', lw=3)
    # plt.errorbar(np.arange(11), means, [means - mins, maxes - means],
    #              fmt='.k', ecolor='gray', lw=1)
    # plt.xlim(-1, 11)

    x = p_times
    mins = x.min(0)
    maxes = x.max(0)
    means = x.mean(0)
    std = x.std(0)

    # create stacked errorbars:
    fig, ax = plt.subplots()
    ax.errorbar(distinct_ps/10, means, std, fmt='o', lw=15, alpha=0.3, ecolor='blue')
    ax.errorbar(distinct_ps/10, means, [means - mins, maxes - means],
                 fmt='.k', ecolor='black', lw=1)
    ax.set_xticks(distinct_ps/10)
    ax.set_xticklabels(distinct_ps)
    ax.set_xlabel("Number of subprocesses")
    ax.set_ylabel("Time(s)")
    ax.set_title(type)
    plt.savefig(file_name.replace(".csv", "-time.png"))

    x = p_corrects
    mins = x.min(0)
    maxes = x.max(0)
    means = x.mean(0)
    std = x.std(0)

    # create stacked errorbars:
    fig, ax1 = plt.subplots()
    ax1.errorbar(distinct_ps/10, means, std, fmt='o', lw=10, alpha=0.5, ecolor='green')
    ax1.errorbar(distinct_ps/10, means, [means - mins, maxes - means],
                 fmt='.k', ecolor='gray', lw=1)
    ax1.set_xticks(distinct_ps/10)
    ax1.set_xticklabels(distinct_ps)
    ax1.set_xlabel("Number of subprocesses")
    ax1.set_ylabel("Correctness")
    ax1.set_title(type)
    plt.savefig(file_name.replace(".csv", "-correctness.png"))











