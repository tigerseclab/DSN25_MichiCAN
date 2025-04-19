class TestCaseFail(Exception):
    pass


class algs:
    def __init__(self, ECU_LIST):
        self.ECU_LIST = ECU_LIST
        self.MAX_BIT_LENGTH = None
        self.AVG_BIT_LENGTH = None
        self.MIN_BIT_LENGTH = None
        self.BINARY_ECU_LIST = [self.padded_binary(ecu) for ecu in ECU_LIST]
        self.GLOBALLY_MALICIOUS_DICT = self.get_globally_malicious(
            self.BINARY_ECU_LIST)
        self.MALICIOUS_OUTLIERS_LIST = self.get_malicious_outliers()
        self.LOCALLY_MALICIOUS_PREFIXES = self.get_last_difference_XOR()

    def padded_binary(self, n):
        # take a base 10 number and return a binary string of length 11
        # format n as a 13 bit binary string and then cut off the "0b" prefix
        return format(n, '#013b')[2:]

    def get_globally_malicious(self, input_list):
        # If there are no either 0s or 1s at that spot in any of the ECUs that it is immediately invalidated
        malicious_bits = {}
        is_0 = []
        is_1 = []

        for i in range(11):
            is_0.append(0)
            is_1.append(0)
            for ecu in input_list:
                if ecu[i] == '0':
                    is_0[i] = 1
                else:
                    is_1[i] = 1
            if is_0[i] == 0:
                malicious_bits[i] = '0'
            if is_1[i] == 0:
                malicious_bits[i] = '1'
        return malicious_bits

    def is_globally_malicious(self, n):
        # check if a padded binary is globally malicious
        for place, character in enumerate(n):
            if place in self.GLOBALLY_MALICIOUS_DICT and self.GLOBALLY_MALICIOUS_DICT[place] == character:
                return True
        return False

    def get_malicious_outliers(self):
        # find every 11 bit binary number that is not globally malicious but that is not one of the numbers in the BINARY_ECU_LIST
        malicious_numbers = []
        for i in range(2**11):
            n = self.padded_binary(i)
            if not self.is_globally_malicious(n) and n not in self.BINARY_ECU_LIST:
                malicious_numbers.append(n)
        return malicious_numbers

    def remove_duplicate_differences(self, differences):
        # remove duplicate differences
        to_remove = []
        for place, diff in enumerate(differences):
            for place2, diff2 in enumerate(differences):
                if place != place2:
                    if len(diff) != len(diff2) and diff2[:len(diff)] == diff:
                        to_remove.append(place2)
        purged_differences = []
        for place, diff in enumerate(differences):
            if place not in to_remove and diff not in purged_differences:
                purged_differences.append(diff)
        self.AVG_BIT_LENGTH = sum(
            len(diff) for diff in purged_differences) / len(purged_differences)
        self.MAX_BIT_LENGTH = max(len(diff) for diff in purged_differences)
        self.MIN_BIT_LENGTH = min(len(diff) for diff in purged_differences)
        return purged_differences

    def get_last_difference(self):
        # find the latest difference between each element in the MALICIOUS_OUTLIERS_LIST and the BINARY_ECU_LIST
        differences = []
        for outlier in self.MALICIOUS_OUTLIERS_LIST:
            largest_diff = 0
            largest_diff_length = 0
            for ecu in self.BINARY_ECU_LIST:
                for i in range(11):
                    if outlier[i] != ecu[i]:
                        if i > largest_diff_length:
                            largest_diff_length = i
                            largest_diff = outlier[:i+1]
                        else:
                            break
            differences.append(largest_diff)
        differences = sorted(differences, key=len)
        return self.remove_duplicate_differences(differences)

    def get_last_difference_XOR(self):
        # find the latest difference between each element in the MALICIOUS_OUTLIERS_LIST and the BINARY_ECU_LIST
        differences = []
        for outlier in self.MALICIOUS_OUTLIERS_LIST:
            outlier = int(outlier, 2)
            smallest_diff = 2048
            for ecu in self.BINARY_ECU_LIST:
                ecu = int(ecu, 2)
                diff = outlier ^ ecu
                if diff < smallest_diff:
                    smallest_diff = diff
            differences.append(
                self.padded_binary(outlier)[0:12 - (len(bin(smallest_diff)) - 2)])
        differences = sorted(differences, key=len)
        return self.remove_duplicate_differences(differences)

    def test_case(self, can_id):
        # the below three lines are supposed to simulate the idea of one bit coming in at a time
        binary_can_id = self.padded_binary(can_id)
        input_buffer = ''
        for place, character in enumerate(binary_can_id):
            # all code below this point will then need to be expanded out to work on the Arduino
            if place in self.GLOBALLY_MALICIOUS_DICT and self.GLOBALLY_MALICIOUS_DICT[place] == character:
                return False  # false if the bit is malicious
            else:
                input_buffer += character
                if input_buffer in self.LOCALLY_MALICIOUS_PREFIXES:
                    return False  # false if the bit is malicious
        return True  # true if the bit is not malicious

    def run_test_cases(self):
        fails = 0
        fail_list = []
        successes = 0
        for can_id in range(2**11):
            if self.test_case(can_id):
                if can_id not in self.ECU_LIST:
                    fails += 1
                    fail_list.append(can_id)
                else:
                    successes += 1
        if successes != len(self.ECU_LIST) or fails > 0:
            raise TestCaseFail(
                "Test cases failed. Successes: {}. ECUs: {} Fails: {}. Fails list: {}".format(successes, len(self.ECU_LIST), fails, fail_list))
        return True
