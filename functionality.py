import data_model as dm
import os
import re

# Global variables
vocabulary = {}


# General Purpose
def calculate_weight(normalize_freq, inversed_freq):
    return float(normalize_freq) * float(inversed_freq)


def create_vocabulary():
    path = "resources/Vocabulario.txt"
    file = open(path, "r", encoding="utf-8")
    if file.mode == "r":
        contents = file.readlines()
        for line in contents:
            split_line = re.compile("\\s+").split(line)
            vocabulary_obj = dm.VocabularyData(split_line[0], split_line[1], split_line[2])
            vocabulary.update({vocabulary_obj.term: vocabulary_obj})


def pad_string(string, padding):
    initial_length = len(string)
    for i in range(padding-initial_length):
        string += " "
    return string

# Weights Files .wtd


def calculate_weights():
    path_read_file = "resources/toks"
    path_write_file = "resources/wtds"

    if not os.path.exists(path_write_file):
        os.makedirs(path_write_file)

    for filename_read in os.listdir(path_read_file):
        filename_write = filename_read.replace("tok", "wtd")
        file_write = open(path_write_file + "/" + filename_write, "w+", encoding="utf-8")
        file_read = open(path_read_file + "/" + filename_read, "r", encoding="utf-8")
        if file_read.mode == "r":
            contents = file_read.readlines()
            write_lines = []
            for line in contents:
                split_line = re.compile("\\s+").split(line)
                tok_obj = dm.TokData(split_line[0], split_line[1], split_line[2])
                vocabulary_obj = vocabulary.get(tok_obj.term)
                weight = calculate_weight(tok_obj.normalize_freq, vocabulary_obj.inverse_freq)
                wtd_obj = dm.WtdData(tok_obj.term, weight)
                write_lines.append(pad_string(wtd_obj.term, 31) + pad_string(str(wtd_obj.weight), 20) + "\n")
            file_write.writelines(write_lines)


def post_term():
    pass


def index_term():
    pass


def main():
    create_vocabulary()
    calculate_weights()


if __name__ == '__main__':
    main()
