import PatternMatchingMachine;
import time, csv



if __name__ == '__main__':

    keywords = []
    with open('keywords.txt', 'r') as keyword_file:
        content = csv.reader(keyword_file,delimiter =",")
        for row in content:
            for key in row:
                keywords.append(key)

    input_file = open("input_text.txt", "r")
    input_string = input_file.read()

    automata = PatternMatchingMachine.PatternMatchingMachine (keywords)

    start_1 = time.time()
    automata.init_non_deterministic_pattern_matching_machine()
    automata.non_deterministic_pattern_matching(input_string)
    end_1 = time.time()


    start_2 = time.time()
    automata.init_deterministic_pattern_matching_machine()
    automata.deterministic_pattern_matching(input_string)
    end_2 = time.time()

    start_3 = time.time()
    automata.naive_approach(input_string)
    end_3 = time.time()
    print("")
    print("non deterministic: time in seconds {:0.9f}".format(end_1 - start_1))
    print("deterministic: time in seconds {:0.9f} ".format(end_2 - start_2))
    print("naive approach: time in seconds {:0.9f}".format(end_3 - start_3))




