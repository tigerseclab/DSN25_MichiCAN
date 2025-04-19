import numpy as np
import matplotlib.pyplot as plt


def main():
    stess_test_timed()
    bit_length_graph()


def stess_test_timed():
    xpoints = []
    if_statements = []
    test_time = []
    time_dict = {}
    with open('results/stress-test-results-timed.csv', 'r') as f:
        lines = f.readlines()
        for place, line in enumerate(lines):
            if place != 0:
                xpoints.append(int(line.split(',')[0]))
                if int(line.split(',')[0]) not in time_dict:
                    time_dict[int(line.split(',')[0])] = []
                if_statements.append(int(line.split(',')[7]))
                test_time.append(float(line.split(',')[4]))
                time_dict[int(line.split(',')[0])].append(
                    float(line.split(',')[4]))
    for key in time_dict:
        avg = np.mean(time_dict[key])
        max = np.max(time_dict[key])
        min = np.min(time_dict[key])
        std_dev = np.std(time_dict[key])
        lower_bound = avg - (std_dev * 2)
        upper_bound = avg + (std_dev * 2)
        time_dict[key] = {'avg': avg, 'max': max, 'min': min,
                          'std_dev': std_dev, 'lower': lower_bound, 'upper': upper_bound}
    avg_l = []
    max_l = []
    min_l = []
    lower_l = []
    upper_l = []
    xvalues = []
    for key in time_dict:
        xvalues.append(key)
        avg_l.append(time_dict[key]['avg'])
        max_l.append(time_dict[key]['max'])
        min_l.append(time_dict[key]['min'])
        lower_l.append(time_dict[key]['lower'])
        upper_l.append(time_dict[key]['upper'])

    plt.figure()
    plt.plot(xpoints, if_statements, 'o')
    plt.grid(axis='y')
    plt.xlabel('Number of CAN IDs')
    plt.ylabel('Number of If Statements in FSM')
    plt.title('Max Number of IF Statements for Randomly Generated CAN ID Lists')
    plt.tight_layout()
    plt.savefig("results/graphs/CANID_IF_Statements.pdf", dpi=500)
    plt.savefig("results/graphs/CANID_IF_Statements.png", dpi=500)
    plt.close()

    plt.figure()
    plt.plot(xpoints, test_time, 'o', label="Test Time")
    xrange = np.linspace(0, 2047, 2048)
    avg_p = np.poly1d(np.polyfit(xvalues, avg_l, 3))
    max_p = np.poly1d(np.polyfit(xvalues, max_l, 3))
    min_p = np.poly1d(np.polyfit(xvalues, min_l, 3))
    lower_p = np.poly1d(np.polyfit(xvalues, lower_l, 3))
    upper_p = np.poly1d(np.polyfit(xvalues, upper_l, 3))
    plt.plot(xrange, avg_p(xrange), '-', label=r'$\mu$')
    plt.plot(xrange, lower_p(xrange), '--', label=r'$\mu - \sigma$')
    plt.plot(xrange, upper_p(xrange), '-.', label=r'$\mu - \sigma$')
    plt.grid(axis='y')
    plt.rcParams.update({
        'text.usetex': True,
        'text.latex.preamble': r'\usepackage{amsfonts}'
    })
    plt.xlabel(r'$|\mathbb{E}|$')
    plt.ylabel('Estimated Time to Run FSM (in Seconds)')
    plt.title('Time to Fully Test FSM for Randomly Generated CAN ID Lists')
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/graphs/CANID_Run_Time.pdf", dpi=500)
    plt.savefig("results/graphs/CANID_Run_Time.png", dpi=500)
    plt.close()


def bit_length_graph():
    xpoints = []
    bit_dict = {}
    avg_bit_len = []
    min_bit_len = []
    max_bit_len = []
    with open('results/bit-length-tests.csv', 'r') as f:
        lines = f.readlines()
        for place, line in enumerate(lines):
            if place != 0:
                xpoints.append(int(line.split(',')[0]))
                if int(line.split(',')[0]) not in bit_dict:
                    bit_dict[int(line.split(',')[0])] = []
                avg_bit_len.append(float(line.split(',')[8]))
                min_bit_len.append(int(line.split(',')[9]))
                max_bit_len.append(int(line.split(',')[10]))
                bit_dict[int(line.split(',')[0])].append({"avg": float(line.split(',')[
                    8]), "min": int(line.split(',')[9]), "max": int(line.split(',')[10])})
    for key in bit_dict:
        avg = np.mean([i["avg"] for i in bit_dict[key]])
        max = np.max([i["max"] for i in bit_dict[key]])
        min = np.min([i["min"] for i in bit_dict[key]])
        bit_dict[key] = {'avg': avg, 'max': max, 'min': min}

    avg_bl = []
    max_bl = []
    min_bl = []
    bl_xvalues = []
    for key in bit_dict:
        bl_xvalues.append(key)
        avg_bl.append(bit_dict[key]['avg'])
        max_bl.append(bit_dict[key]['max'])
        min_bl.append(bit_dict[key]['min'])

    plt.figure()
    plt.plot(xpoints, avg_bit_len, 'o',
             c="tab:orange", label="Mean Bit Length")
    plt.plot(xpoints, min_bit_len, 'X', c="tab:olive",
             label="Minimum Bit Length")
    plt.plot(xpoints, max_bit_len, 's', c="tab:cyan",
             label="Maximum Bit Length")
    bl_xrange = np.linspace(0, 2047, 20)
    avg_pb = np.poly1d(np.polyfit(bl_xvalues, avg_bl, 10))
    max_pb = np.poly1d(np.polyfit(bl_xvalues, max_bl, 10))
    min_pb = np.poly1d(np.polyfit(bl_xvalues, min_bl, 10))
    plt.plot(bl_xrange, avg_pb(bl_xrange),
             marker='.', ls='-', c='k', label="µ")
    plt.plot(bl_xrange, max_pb(bl_xrange), marker='+',
             ls='-.', c='k', label="max")
    plt.plot(bl_xrange, min_pb(bl_xrange), marker='x',
             ls='--', c='k', label="min")
    plt.grid(axis='y')
    plt.rcParams.update({
        'text.usetex': True,
        'text.latex.preamble': r'\usepackage{amsfonts}'
    })
    plt.xlabel(r'$|\mathbb{E}|$')
    plt.ylabel('Number of Bits in Local Prefixes')
    plt.title('Number of Bits Required to Determine if Malicious')
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/graphs/CANID_Bit_Lengths.pdf", dpi=500)
    plt.savefig("results/graphs/CANID_Bit_Lengths.png", dpi=500)
    plt.close()


if __name__ == "__main__":
    main()
