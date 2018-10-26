class TokData:
    def __init__(self, term, freq, normalize_freq):
        self.term = term
        self.freq = freq
        self.normalize_freq = normalize_freq


class VocabularyData:
    def __init__(self, term, num_documents, inverse_freq):
        self.term = term
        self.num_documents = num_documents
        self.inverse_freq = inverse_freq


class WtdData:
    def __init__(self, term, weight):
        self.term = term
        self.weight = weight


class PostData:
    def __init__(self, term, url, weight):
        self.term = term
        self.url = url
        self.weight = weight


class IndexData:
    def __init__(self, term, initial_pos, num_entries):
        self.term = term
        self.initial_pos = initial_pos
        self.num_entries = num_entries
