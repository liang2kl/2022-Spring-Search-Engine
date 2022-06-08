import os
import matplotlib.pyplot as plt
import numpy as np

def plot_hist(data, x_label, y_label, file_name):
    _, bins, _ = plt.hist(data, bins=50)
    logbins = np.logspace(np.log10(bins[0]) if bins[0] else 0, np.log10(bins[-1]), len(bins))

    _, ax = plt.subplots()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    ax.hist(data, bins=logbins, linewidth=0.1, edgecolor="white")
    plt.savefig(file_name)

def plot_scatter(x, y, x_label, y_label, file_name):
    _, ax = plt.subplots()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    ax.scatter(x, y ,s=0.5)
    plt.savefig(file_name)

if __name__ == "__main__":

    pr = {}

    if not os.path.isdir("./plots"):
        os.mkdir("./plots")

    # page rank
    with open("./output.txt", "r") as file:
        for line in file:
            tokens = line.split(" ")
            pr[int(tokens[0])] = float(tokens[1])

    plot_hist(np.array([pr[k] for k in pr]),
        "page rank", "# of pages", "plots/out.png")

    # in links and out links
    outs = {}
    ins = {}
    with open("wiki.graph", "r") as file:
        for line in file:
            line = line.strip()
            parts = line.split(":")
            arr = np.array([int(i) for i in parts[1].split(",") if i])

            head = int(parts[0])

            if head in outs:
                outs[head] += len(arr)
            else:
                outs[head] = len(arr)
            
            for node in arr:
                if node not in ins:
                    ins[node] = 1
                else:
                    ins[node] += 1

    plot_hist(np.array([ins[k] for k in ins]),
        "in links", "# of pages", "plots/in.png")
    plot_hist(np.array([outs[k] for k in outs]),
        "out links", "# of pages", "plots/out.png")

    # relation
    arrs = [(ins[k], pr[k], k) for k in pr if k in ins]
    plot_scatter(
        np.array([e[0] for e in arrs]),
        np.array([e[1] for e in arrs]),
        "in links", "page rank", "plots/in-pr.png"
    )

    # top and bottom 5
    sorted_arrs = sorted(arrs, key=lambda e: e[1])
    for i in range(5):
        print(sorted_arrs[i][2], sorted_arrs[i][1])
    
    for i in range(1, 6):
        print(sorted_arrs[-i][2], sorted_arrs[-i][1])
