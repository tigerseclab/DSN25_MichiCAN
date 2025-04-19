from cgi import test
import cantools
import canid_generator
import json
import numpy as np
import matplotlib.pyplot as plt

total_results = []

for i in range(8):
    car_id = i + 1
    db = cantools.database.load_file('Car_DBCs/car{}.dbc'.format(car_id))
    can_ids = []
    for msg in db.messages:
        can_ids.append(msg.frame_id)

    can_ids = sorted(list(dict.fromkeys(can_ids)))

    results = canid_generator.main(
        'folder', can_ids, 0, max(can_ids) + 1, False, car_id, True)
    results2 = canid_generator.main(
        'folder', can_ids, max(can_ids) + 1, max(can_ids) + 2, False, car_id, True)
    total_results.append({"size": len(can_ids), "results": results})


def grapher():
    xpoints = []
    ypoints = []
    carx = []
    cary = []
    with open('results/stress-test-results-timed.csv', 'r') as f:
        lines = f.readlines()
        for place, line in enumerate(lines):
            if place != 0:
                xpoints.append(int(line.split(',')[0]))
                ypoints.append(int(line.split(',')[7]))

    for res in total_results:
        carx.append(res['size'])
        cary.append(res['results']['global bits'] +
                    res['results']['local prefixes'])

    plt.figure()
    plt.rcParams.update({
        'text.usetex': True,
        'text.latex.preamble': r'\usepackage{amsfonts}'
    })
    plt.plot(xpoints, ypoints, 'o', label="Randomly Generated ECU LISTS")
    plt.plot(carx, cary, 'X', label="OEM ECU LISTS")
    plt.grid(axis='y')
    plt.xlabel(r'$|\mathbb{E}|$')
    plt.ylabel('Number of If Statements in FSM')
    plt.title('Max Number of IF Statements w/ OEM CAN ID Lists')
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig("results/graphs/CANID_OEM_IFs.pdf", dpi=500)
    plt.savefig("results/graphs/CANID_OEM_IFs.png", dpi=500)
    plt.close()


grapher()
print(json.dumps(total_results, indent=4))
