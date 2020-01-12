from heapq import merge
import json
import pickle
from encoding import gap_decoding, gamma_encoding, gap_decoding, gamma_decoding, bitstring_to_bytes, bytes_to_bit_string

class Indexer:
    def __init__(self, name):
        self.indexer = [[]]
        self.number_of_words = 0
        self.term_id_to_term = []
        self.term_to_term_id = {}

    def add_word_to_indexer(self, word):

        insert_pos = 0

        for i in range(len(self.term_id_to_term)):
            if self.term_id_to_term[i] >= word:
                insert_pos = i
                break

        self.term_id_to_term.insert(insert_pos, [])

        for word in self.term_to_term_id.keys():
            if self.term_to_term_id[word] >= insert_pos:
                self.term_to_term_id[word] = self.term_to_term_id[word] + 1

        self.term_to_term_id[word] = insert_pos


    def add_word_to_document(self, word, doc_id):

        if word not in term_id_to_term:
            self.add_word_to_indexer(word)

        term_id = self.term_to_term_id[word]
        for pos, id in enumerate(self.indexer[term_id]):
            if id == doc_id:
                break
            if id > doc_id:
                self.indexer[term_id].insert(doc_id, pos)

        self.number_of_words = self.number_of_words + 1

    def save_indexer_to_disk(self):
        compressed_index = copy(self.indexer)

        for i in range(len(compressed_index)):
            compressed_index[i] = gap_encoding(compressed_index[i])

        for i in range(len(compressed_index)):
            compressed_index[i] = gamma_encoding(compressed_index[i])

        for i in range(len(compressed_index)):
            compressed_index[i] = bitstring_to_bytes(compressed_index[i])

        with open('term_to_term_id_{}.txt'.format(self.name), 'w') as filehandle:
            json.dump(self.term_to_term_id, filehandle)

        with open('{}_index.data'.format(self.name), 'wb') as filehandle:
            pickle.dump(compressed_index, filehandle)

    def load_indexer_from_disk(self, index_filename, dict_filename):
        self.indexer = [[]]
        self.number_of_words = 0
        self.term_id_to_term = []
        self.term_to_term_id = {}

        with open(dict_filename, 'r') as filehandle:
            self.term_to_term_id = json.load(filehandle)

        for term, term_id in self.term_to_term_id.items():
            self.term_id_to_term[term_id] = term

        with open(index_filename, 'rb') as filehandle:
            compressed_index = pickle.load(filehandle)

        for i in range(len(compressed_index)):
            compressed_index[i] = bytes_to_bit_string(compressed_index[i])

        for i in range(len(compressed_index)):
            compressed_index[i] = gamma_decoding(compressed_index[i])

        for i in range(len(compressed_index)):
            compressed_index[i] = gap_decoding(compressed_index[i])

        self.indexer = compressed_index
        for i in range(len(self.indexer)):
            self.number_of_words += len(self.indexer[i])

def merge_indexes(index_A, index_B):

    term_id_to_term = merge(index_A.term_id_to_term, index_B.term_id_to_term)
    term_to_term_id = {term : term_id for term_id, term in enumerate(term_id_to_term)}
    total_size = 0
    indexer = [list() for i in range(len(term_id_to_term))]

    for term in term_id_to_term:
        postings_1 = [] if term not in index_A.term_to_term_id else index_A.indexer[index_A.term_to_term_id[term_id]]
        postings_2 = [] if term not in index_B.term_to_term_id else index_B.indexer[index_B.term_to_term_id[term_id]]

        indexer[term_to_term_id[term]] = merge(postings_1, postings_2)

        total_size += len(indexer[term_to_term_id[term]])

    result = Indexer()
    result.term_id_to_term = term_id_to_term
    result.term_to_term_id = term_to_term_id
    result.indexer = indexer
    result.number_of_words = total_size
    return result
