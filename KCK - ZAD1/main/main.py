import csv
import matplotlib.pyplot as plt

algotrithms = ["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"]
file_paths = ["rsel.csv", "cel-rs.csv", "2cel-rs.csv", "cel.csv", "2cel.csv"]

def read_file(file_path):
    data = [[],[]]
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            data[0].append(int(row[1]) / 1000)
            runs = [float(value) * 100 for value in row[2:]]
            data[1].append(sum(runs) / len(runs))
    return data

def read_last_row(file_path):
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file)
        last_row = [float(item) * 100 for item in list(reader)[-1][2:]]
    return last_row

def main():
    plt.rcParams["font.family"] = "Times New Roman"
    colors = ['b', 'g', 'r', 'k', 'm']
    markers = ['o', '^', 'D', 's', 'd']

    fig, (plot1, plot2) = plt.subplots(1, 2, figsize=(10, 5))

    plot1 = plt.subplot(1, 2, 1)
    plt.xlabel("Rozegranych gier (x1000)", fontsize=11, fontfamily='Times New Roman')
    plt.ylabel("Odsetek wygranych gier [%]", fontsize=11, fontfamily='Times New Roman')

    plot2 = plt.subplot(1, 2, 2)
    plot2_data = []

    ax2 = plot1.twiny()

    for i in range(len(algotrithms)):
        data = read_file(file_paths[i])
        plot1.plot(data[0], data[1],f'{colors[i]}{markers[i]}' , ls='-', ms=6.5, markevery=25, markeredgecolor='black', label=algotrithms[i])
        plot2_data.append(read_last_row(file_paths[i]))

    plot1.set_xlim(0, 500)
    plot1.grid(color='lightblue', linestyle='dotted')
    plot1.legend(numpoints=2)

    plot2.boxplot(
        plot2_data,
        tick_labels=algotrithms,
        notch=True,
        showmeans=True,
        boxprops=dict(color="blue"),
        flierprops=dict(marker='+', markeredgecolor='blue', markersize=6),
        medianprops=dict(color='red'),
        meanprops=dict(marker='o', markeredgecolor='black', markerfacecolor='blue', markersize=4),
        whiskerprops=dict(linestyle='dashed', color='blue')
    )

    plot2.set_ylim(ymin=60, ymax=100)
    plot2.yaxis.tick_right()
    plt.xticks(rotation=25)
    plot2.grid(color='lightblue', linestyle='dotted')

    additional_x_values = [0, 40, 80, 120, 160, 200]
    ax2.set_xticks(additional_x_values)
    ax2.set_xticklabels(additional_x_values, rotation=0)
    ax2.set_xlabel("Pokolenie", fontsize=11)

    plt.tight_layout()
    plt.savefig('myplot.pdf')
    plt.show()
    plt.close()

if __name__ == '__main__':
    main()