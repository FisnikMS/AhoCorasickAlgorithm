import csv, random, os, time
from os import listdir
from os.path import isfile, join
import PatternMatchingMachine;
import numpy as np
import matplotlib.pyplot as plt
import math

NUMBER_OF_CHARS_FILES = []
NUMBER_OF_KEYWORDS_FILES = []
LENGTH_OF_KEYWODS_FILES = []
MIMINUM_KEYWORD_OCCURRENCES = []
LIST_OF_GENERATED_KEYWORDS = []

rel_path_input_files = "text_files/inputs"
rel_path_keyword_files = "text_files/keywords"
rel_path_output_files = "text_files/outputs"
rel_path_plot_files = "text_files/plots"


def delete_files(directory_path):
    files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    for f in files:
        os.remove(directory_path + "/" + f)


def generate_random_text():
    for i in range(len(NUMBER_OF_CHARS_FILES)):
        number_of_min_occurrences = NUMBER_OF_CHARS_FILES[i] * MIMINUM_KEYWORD_OCCURRENCES[i]
        remaining_chars = int(NUMBER_OF_CHARS_FILES[i] - number_of_min_occurrences)
        rel_path = rel_path_input_files + "/input_text{}.txt".format(i)
        input_text = open(rel_path, "w")

        while number_of_min_occurrences > 0:
            random_keyword = random.randint(0, len(LIST_OF_GENERATED_KEYWORDS) - 1)
            new_key = [str(LIST_OF_GENERATED_KEYWORDS[random_keyword])]
            input_text.write("".join(new_key))
            number_of_min_occurrences -= len(new_key)

        input_text.write("".join([str(random.randint(0, 9)) for j in range(remaining_chars)]))


def generate_keywords():
    global LIST_OF_GENERATED_KEYWORDS
    for i in LENGTH_OF_KEYWODS_FILES:
        for j in NUMBER_OF_KEYWORDS_FILES:
            rel_path = rel_path_keyword_files + "/keywords_with_length{}.txt".format(i, j)

            if not os.path.isfile(rel_path):
                open(rel_path, "w").write(",".join([str(i)]) + "\n")

            input_text = open(rel_path, "a")
            created_keyword = [str(random.randint(pow(10, i - 1), pow(10, i) - 1)) for k in range(j)]
            LIST_OF_GENERATED_KEYWORDS += created_keyword
            input_text.write(",".join(created_keyword))
            input_text.write("\n")


def execute_time_comparison():
    keyword_files = [f for f in listdir(rel_path_keyword_files) if isfile(join(rel_path_keyword_files, f))]
    input_files = [f for f in listdir(rel_path_input_files) if isfile(join(rel_path_input_files, f))]

    for input_file_index in range(len(input_files)):
        current_input_file = open(rel_path_input_files + "/" + input_files[input_file_index], "r").read()

        rows = []
        for keyword_file in keyword_files:

            with open(rel_path_keyword_files + "/" + keyword_file, 'r') as current_keyword_file:
                content = csv.reader(current_keyword_file, delimiter=",")

                # read first row
                first_row = next(content)
                for row in content:
                    keywords = []

                    for key in row:
                        keywords.append(key)

                    automata = PatternMatchingMachine.PatternMatchingMachine(keywords)

                    start_1 = time.time()
                    automata.init_non_deterministic_pattern_matching_machine()
                    automata.non_deterministic_pattern_matching(current_input_file)
                    end_1 = time.time()

                    start_2 = time.time()
                    automata.init_deterministic_pattern_matching_machine()
                    automata.deterministic_pattern_matching(current_input_file)
                    end_2 = time.time()

                    start_3 = time.time()
                    automata.naive_approach(current_input_file)
                    end_3 = time.time()

                    rows.append([end_1 - start_1, end_2 - start_2, end_3 - start_3])

                with open(rel_path_output_files + "/output_with_keyword_length{}_{}".format(first_row[0],
                                                                                            input_file_index), "w",
                          newline='') as output_file:
                    filewriter = csv.writer(output_file, delimiter=' ')
                    first_row.append(input_file_index)
                    filewriter.writerow(first_row)
                    for i in range(len(rows)):
                        filewriter.writerow(rows[i])
                rows = []


def generate_plot():
    output_files = [f for f in listdir(rel_path_output_files) if isfile(join(rel_path_output_files, f))]

    for output_file in output_files:

        non_deterministic_speed = []
        deterministic_speed = []
        naive_speed = []
        current_length_of_keywords = None
        with open(rel_path_output_files + '/' + output_file, 'r') as csv_file:
            content = csv.reader(csv_file, delimiter=" ", quoting=csv.QUOTE_NONNUMERIC)
            first_row = next(content)
            current_length_of_keywords = int(first_row[0])
            current_input_text = int(first_row[1])

            for row in content:
                for i in range(len(row)):
                    if i % 3 == 0:
                        non_deterministic_speed.append(row[i])
                    elif i % 3 == 1:
                        deterministic_speed.append(row[i])
                    else:
                        naive_speed.append(row[i])

        x = np.array(range(len(non_deterministic_speed)))
        n_det_y = non_deterministic_speed
        det_y = deterministic_speed
        naiv_y = naive_speed
        my_xticks = NUMBER_OF_KEYWORDS_FILES

        create_plot(current_input_text, current_length_of_keywords, det_y, my_xticks, n_det_y, naiv_y, x, 4, 4, 7)


def create_plot(current_input_text, current_length_of_keywords, det_y, my_xticks, n_det_y, naiv_y, x, figure_width,
                figure_height, font_size):
    plt.figure(figsize=(figure_width, figure_height))

    plt.xticks(x, my_xticks)
    plt.plot(x, det_y, label="next move function", linestyle="-")
    plt.plot(x, n_det_y, label="goto function", linestyle="-")
    plt.plot(x, naiv_y, label="naive approach", linestyle="-")
    plt.grid(axis='y', linestyle='-')

    power = int(math.log10(NUMBER_OF_CHARS_FILES[current_input_text]))
    plt.title(
        "number of characters: 10^{} \n length of the keywords: {} \n minimum keyword occurrences: {}%".format(power,
                                                                                                               current_length_of_keywords,
                                                                                                               int(100 *
                                                                                                                   MIMINUM_KEYWORD_OCCURRENCES[
                                                                                                                       current_input_text])))
    plt.xlabel('number of keywords')
    plt.ylabel('time in seconds')
    plt.legend(loc='upper left', fontsize=font_size)

    plot_path = rel_path_plot_files + "/plot_with_keyword_length_{}_{}.pdf".format(current_length_of_keywords,
                                                                                   current_input_text)
    plt.savefig(plot_path, bbox_inches='tight')
    plt.clf()


def init_list(list, list_name):
    with open('text_files/' + list_name, 'r') as csv_file:
        content = csv.reader(csv_file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)

        for row in content:
            for key in row:
                if list_name == "number_of_chars.txt":
                    list.append(pow(10, int(key)))
                elif list_name == "minimum_keyword_occurrences.txt":
                    list.append(float(key))
                else:
                    list.append(int(key))


if __name__ == '__main__':
    init_list(NUMBER_OF_CHARS_FILES, "number_of_chars.txt")
    init_list(NUMBER_OF_KEYWORDS_FILES, "number_of_keywords.txt")
    init_list(LENGTH_OF_KEYWODS_FILES, "length_of_keywords.txt")
    init_list(MIMINUM_KEYWORD_OCCURRENCES, "minimum_keyword_occurrences.txt")

    assert len(MIMINUM_KEYWORD_OCCURRENCES) == len(
        NUMBER_OF_CHARS_FILES), "please make sure to determine a value in minimum_keyword_occurrences.txt for each" \
                                " entry in number_of_chars.txt"

    # remove files from previous calculation
    # remove input files
    delete_files(rel_path_input_files)

    # remove keyword files
    delete_files(rel_path_keyword_files)

    # remove output files
    delete_files(rel_path_output_files)

    # remove plots
    delete_files(rel_path_plot_files)

    # generate keywords
    generate_keywords()

    # generate random text
    generate_random_text()

    execute_time_comparison()

    generate_plot()
