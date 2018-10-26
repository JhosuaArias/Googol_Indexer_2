import data_model as dm
import os
import re
from collections import OrderedDict

# Global variables
vocabulary = {}
postings_terms = OrderedDict()
RESOURCES_PATH = "resources"
TOKS_PATH = RESOURCES_PATH+"/toks"
WTDS_PATH = RESOURCES_PATH+"/wtds"
VOCABULARY_PATH = RESOURCES_PATH+"/Vocabulario.txt"
POSTINGS_FILE = "Postings.txt"
INDEX_FILE = "Indice.txt"


# General Purpose
def calculate_weight(normalize_freq, inversed_freq):
    return float(normalize_freq) * float(inversed_freq)


def create_vocabulary():
    file = open(VOCABULARY_PATH, "r", encoding="utf-8")
    if file.mode == "r":
        contents = file.readlines()
        for line in contents:
            split_line = re.compile("\\s+").split(line)
            vocabulary_obj = dm.VocabularyData(split_line[0], split_line[1], split_line[2])
            vocabulary.update({vocabulary_obj.term: vocabulary_obj})


def get_term(line):
    """Given a line where the first word is a term, returns that term.
    Useful to get terms in files like Vocabulary, Postings, Index, etc."""
    return line.split(" ")[0]


def pad_string(string, padding):
    initial_length = len(string)
    for i in range(padding-initial_length):
        string += " "
    return string


# Weights Files .wtd
def calculate_weights():
    if not os.path.exists(WTDS_PATH):
        os.makedirs(WTDS_PATH)

    for filename_read in os.listdir(TOKS_PATH):
        filename_write = filename_read.replace("tok", "wtd")
        filename = filename_read.replace(".tok", "")
        file_write = open(WTDS_PATH + "/" + filename_write, "w+", encoding="utf-8")
        file_read = open(TOKS_PATH + "/" + filename_read, "r", encoding="utf-8")
        if file_read.mode == "r":
            contents = file_read.readlines()
            write_lines = []
            for line in contents:
                split_line = re.compile("\\s+").split(line)
                tok_obj = dm.TokData(split_line[0], split_line[1], split_line[2])
                vocabulary_obj = vocabulary.get(tok_obj.term)
                weight = calculate_weight(tok_obj.normalize_freq, vocabulary_obj.inverse_freq)
                wtd_obj = dm.WtdData(tok_obj.term, weight)
                pst_obj = dm.PostData(tok_obj.term, filename, weight)
                postings_terms[(tok_obj.term, pst_obj.url)] = pst_obj
                write_lines.append(pad_string(wtd_obj.term, 31) + pad_string(str(wtd_obj.weight), 20) + "\n")
            file_write.writelines(write_lines)
        file_read.close()
        file_write.close()


def write_postings():
    if not os.path.exists(RESOURCES_PATH):
        os.makedirs(RESOURCES_PATH)

    file_write = open(RESOURCES_PATH + "/" + POSTINGS_FILE, "w+", encoding="utf-8")
    write_lines = []
    temp = OrderedDict(sorted(postings_terms.items()))
    for (term, url), info in temp.items():
        write_lines.append(pad_string(term, 31) + pad_string(info.url, 40) + pad_string(str(info.weight), 20) + "\n")
    file_write.writelines(write_lines)
    file_write.close()


def write_index():
    if not os.path.exists(RESOURCES_PATH):
        os.makedirs(RESOURCES_PATH)

    # Save the data to be written in a buffer, to be written all at once at the end
    index_file_lines = []

    postings_file = open(RESOURCES_PATH + "/" + POSTINGS_FILE, "r", encoding="utf-8")
    postings_lines = postings_file.readlines()

    # Get the first term, in order to start comparing with the second term in the loop
    current_term = get_term(postings_lines[0])
    first_entry = 1
    current_term_entries = 1

    # Start in the second line because the term in the first line as already been read
    for line_number in range(1, len(postings_lines)):
        # Get the new line's term
        new_line = postings_lines[line_number]
        new_term = get_term(new_line)

        if current_term == new_term:
            # If it's the same as the current term, update its total entries
            current_term_entries += 1
        else:
            # If it's a different term, write the appropriate line to the buffer
            index_file_lines.append(pad_string(current_term, 31) + pad_string(str(first_entry), 13) +
                                    pad_string(str(current_term_entries), 12)+"\n")

            # And update the necessary variables
            current_term = new_term
            current_term_entries = 1
            first_entry = line_number + 1  # Add one because the array posting_lines is 0-indexed

    postings_file.close()

    # Write all the lines saved in the buffer
    index_file = open(RESOURCES_PATH + "/" + INDEX_FILE, "w+", encoding="utf-8")
    index_file.writelines(index_file_lines)
    index_file.close()


def index_term():
    pass


def main():
    create_vocabulary()
    calculate_weights()
    write_postings()
    write_index()


if __name__ == '__main__':
    main()
