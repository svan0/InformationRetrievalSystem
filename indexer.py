from heapq import merge
from nltk.corpus import brown
import json
import pickle
from encoding import gap_encoding, gamma_encoding, gap_decoding, gamma_decoding, bitstring_to_bytes, bytes_to_bit_string
from copy import deepcopy
class Indexer:
    def __init__(self, name):
        self.name = name
        self.indexer = []
        self.number_of_words = 0
        self.term_id_to_term = []
        self.term_to_term_id = {}

    def add_word_to_indexer(self, word):

        insert_pos = len(self.term_id_to_term)

        for i in range(len(self.term_id_to_term)):
            if self.term_id_to_term[i] > word:
                insert_pos = i
                break

        self.term_id_to_term.insert(insert_pos, word)
        self.indexer.insert(insert_pos, [])

        for word_iter in self.term_to_term_id.keys():
            if self.term_to_term_id[word_iter] >= insert_pos:
                self.term_to_term_id[word_iter] = self.term_to_term_id[word_iter] + 1

        self.term_to_term_id[word] = insert_pos


    def add_word_to_document(self, word, doc_id):

        if word not in self.term_id_to_term:
            self.add_word_to_indexer(word)

        term_id = self.term_to_term_id[word]
        if doc_id not in self.indexer[term_id]:
            self.indexer[term_id].append(doc_id)
            self.indexer[term_id] = sorted(self.indexer[term_id])

        self.number_of_words = self.number_of_words + 1

    def save_indexer_to_disk(self):
        compressed_index = deepcopy(self.indexer)

        for i in range(len(compressed_index)):
            compressed_index[i] = gap_encoding(compressed_index[i])

        for i in range(len(compressed_index)):
            compressed_index[i] = gamma_encoding(compressed_index[i])

        for i in range(len(compressed_index)):
            compressed_index[i] = bitstring_to_bytes(compressed_index[i])

        with open('term_to_term_id/term_to_term_id_{}.txt'.format(self.name), 'w') as filehandle:
            json.dump(self.term_to_term_id, filehandle)

        with open('indexers/{}_index.data'.format(self.name), 'wb') as filehandle:
            pickle.dump(compressed_index, filehandle)

    def load_indexer_from_disk(self):
        self.indexer = []
        self.number_of_words = 0
        self.term_id_to_term = []
        self.term_to_term_id = {}

        with open('term_to_term_id/term_to_term_id_{}.txt'.format(self.name), 'r') as filehandle:
            self.term_to_term_id = json.load(filehandle)

        self.term_id_to_term = [-1 for i in range(len(self.term_to_term_id))]
        for term, term_id in self.term_to_term_id.items():
            self.term_id_to_term[term_id] = term

        with open('indexers/{}_index.data'.format(self.name), 'rb') as filehandle:
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

    def __str__(self):
        res = ""
        for i in range(len(self.term_id_to_term)):
            res = res + self.term_id_to_term[i] + " : " + str(self.indexer[i]) + "\n"
        return res

def merge_indexes(index_A, index_B):

    term_id_to_term = sorted(list(set(merge(index_A.term_id_to_term, index_B.term_id_to_term))))
    term_to_term_id = {term : term_id for term_id, term in enumerate(term_id_to_term)}
    total_size = 0
    indexer = [list() for i in range(len(term_id_to_term))]

    for term in term_id_to_term:
        postings_1 = [] if term not in index_A.term_to_term_id else index_A.indexer[index_A.term_to_term_id[term]]
        postings_2 = [] if term not in index_B.term_to_term_id else index_B.indexer[index_B.term_to_term_id[term]]

        indexer[term_to_term_id[term]] = list(merge(postings_1, postings_2))

        total_size += len(indexer[term_to_term_id[term]])

    result = Indexer("merge_{}_{}".format(index_A.name, index_B.name))
    result.term_id_to_term = term_id_to_term
    result.term_to_term_id = term_to_term_id
    result.indexer = indexer
    result.number_of_words = total_size
    return result


if __name__ == '__main__':
    def try_on_small_data():
        docs = ["Good morning new york q",
                "Bonjour le monde",
                "Winek Pacine",
                "Good morning sna francisco",
                "Bonjour le monde",
                "Winek 7awem"]

        indexer = Indexer("my_small_index1")
        for doc_id in range(4):
            doc = docs[doc_id]
            for word in doc.split():
                indexer.add_word_to_document(word.lower(), doc_id + 1)

        print(indexer)

        indexer.save_indexer_to_disk()

        new_index = Indexer("my_small_index1")
        new_index.load_indexer_from_disk()

        print(new_index)

        indexer2 = Indexer("my_small_index2")
        for doc_id in range(4, len(docs)):
            doc = docs[doc_id]
            for word in doc.split():
                indexer2.add_word_to_document(word.lower(), doc_id + 1)

        print(indexer2)

        merge_index = merge_indexes(indexer, indexer2)
        print(merge_index)

    def try_on_larger_data():
        docs = ['ca01', 'ca02', 'ca03', 'ca04', 'ca05', 'ca06', 'ca07', 'ca08']

        index1 = Indexer("my_index1")
        for doc_id in range(4):
            doc_name = docs[doc_id]
            for word in brown.words(doc_name):
                index1.add_word_to_document(word.lower(), doc_id + 1)

        print(index1)
        index1.save_indexer_to_disk()


        index2 = Indexer("my_index2")
        for doc_id in range(4, len(docs)):
            doc_name = docs[doc_id]
            for word in brown.words(doc_name):
                index2.add_word_to_document(word, doc_id + 1)

        print(index2)
        index2.save_indexer_to_disk()

        index1.load_indexer_from_disk()
        index2.load_indexer_from_disk()

        merge_index = merge_indexes(index1, index2)
        print(merge_index)

        merge_index.save_indexer_to_disk()

    try_on_larger_data()
