class TokData:
    def __init__(self, term, freq, normalize_freq):
        self.term = term
        self.freq = freq
        self.normalize_freq = normalize_freq


class VocabularyData:
    def __init__(self, term, numDocuments, inverse_freq):
        self.term = term
        self.numDocuments = numDocuments
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
    def __init__(self, term, initialPos, numEntries):
        self.term = term
        self.initialPos = initialPos
        self.numEntries = numEntries
