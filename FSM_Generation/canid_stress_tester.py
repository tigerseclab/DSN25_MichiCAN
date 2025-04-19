import numpy as np
import matplotlib.pyplot as plt
import canid_generator
import generate_graph
import random
import json
import sys
import subprocess
import time
import os

# This file is used to test the performance of the FSM generation code automatically, especially for larger ECU lists.
# Use canid_generator.py to generate the FSMs for a list of ECUs for production or testing, this file is used to stress test it, not to generate the FSMs, although it does still do this as a byproduct of testing.


class CanidStressTester:
    def __init__(self, number_of_tests=5, number_of_lists=16, min_list_size=0x001, max_list_size=0x7fe, lower_ceil_percent=20, upper_ceil_percent=80):
        self.num = number_of_tests
        self.num_lists = number_of_lists
        self.min_list_size = min_list_size
        self.max_list_size = max_list_size
        self.all_possible_ecu_combinations = range(0x001, 0x7ff)
        self.lower_ceil_percent = lower_ceil_percent
        self.upper_ceil_percent = upper_ceil_percent
        self.test_results = {}
        self.test_lists = []

    def generate_test_lists(self, size, num=False):
        if num:
            self.num = num
        # pick size random elements from all possible ECU combinations
        # return num different lists
        self.test_results[size] = {"size": size, "results": []}
        return [sorted(random.sample(self.all_possible_ecu_combinations, size)) for n in range(self.num)]

    def eval_cpp_files(self):
        # compile and run each C++ file in the FSMs folder one at a time and verify all tests pass
        # get list of all file names in FSMs folder
        # for each file, compile and run
        # verify all tests pass
        eval_start = time.time()
        passed = False
        file_names = [f for f in os.listdir(
            'results/FSMs') if f.endswith('.cpp')]
        # pick random file name
        fname = random.choice(file_names)
        # compile file
        compile = subprocess.call(
            ['g++', '-std=c++17', '-o', 'results/FSMs/' + fname[:-4] + '.exe', 'results/FSMs/' + fname])
        # run file if compile successful
        if compile == 0:
            run = subprocess.call(
                ['./results/FSMs/' + fname[:-4] + '.exe'])
            if run == 0:
                eval_end = time.time()
                eval_time = round(eval_end - eval_start, 7)
                passed = True
        # delete all files in FSMs folder
        for f in file_names:
            os.remove('results/FSMs/' + f)
        os.remove('results/FSMs/' + fname[:-4] + '.exe')
        if passed:
            return eval_time
        else:
            return -1

    def run_test_lists(self, test_lists):
        for test_list in test_lists:
            # lower_c = test_list[
            #     int(round(
            #         self.lower_ceil_percent / 100 * len(test_list)
            #     ))
            # ]
            # upper_c = test_list[
            #     int(round(
            #         self.upper_ceil_percent / 100 * len(test_list)
            #     ))
            # ]
            results = canid_generator.main(
                'folder', test_list, 0, max(test_list) + 1, True)
            test_time = self.eval_cpp_files()
            results["test time"] = test_time
            self.test_results[len(test_list)]["results"].append(results)

    def design_tests(self):
        for i in range(self.num_lists):
            list_length = random.randint(
                self.min_list_size, self.max_list_size)
            self.test_lists.append(
                self.generate_test_lists(
                    list_length
                )
            )

    def runner(self):
        self.design_tests()
        for test_list in self.test_lists:
            self.run_test_lists(test_list)
        self.test_results = sorted(
            self.test_results.values(), key=lambda x: x["size"])
        with open('results/test_results.json', 'w') as fp:
            json.dump(self.test_results, fp, indent=4)
        self.save_csv()

    def only_one(self):
        for i in range(0x001, 0x7fe):
            self.test_lists.append(
                self.generate_test_lists(
                    i, 1
                )
            )
        for test_list in self.test_lists:
            self.run_test_lists(test_list)
        self.test_results = sorted(
            self.test_results.values(), key=lambda x: x["size"])
        with open('results/test_results.json', 'w') as fp:
            json.dump(self.test_results, fp, indent=4)
        self.save_csv()

    def save_csv(self):
        with open('results/bit-length-tests.csv', 'a') as f:
            for result in self.test_results:
                for result_list in result["results"]:
                    f.write(str(result["size"]) + ",")
                    f.write(str(result_list["compile time"]) + ",")
                    f.write(str(result_list["build time"]) + ",")
                    f.write(str(result_list["write time"]) + ",")
                    f.write(str(result_list["test time"]) + ",")
                    f.write(str(result_list["global bits"]) + ",")
                    f.write(str(result_list["local prefixes"]) + ",")
                    f.write(
                        str(int(result_list["global bits"] + result_list["local prefixes"])) + ",")
                    f.write(str(result_list["avg bit length"]) + ",")
                    f.write(str(result_list["min bit length"]) + ",")
                    f.write(str(result_list["max bit length"]) + "\n")


if __name__ == "__main__":
    total_runs = 0
    while True:
        for i in range(10):
            total_runs += 1
            run_start = time.time()
            tester = CanidStressTester()
            tester.runner()
            run_end = time.time()
            print("Run {} took {} seconds".format(
                total_runs, round(run_end - run_start, 7)))
        total_runs += 1
        run_start = time.time()
        tester = CanidStressTester()
        tester.runner()
        generate_graph.main()
        run_end = time.time()
        print("Run {} took {} seconds".format(
            total_runs, round(run_end - run_start, 7)))
