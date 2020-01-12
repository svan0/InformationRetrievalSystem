from nltk.corpus import brown
from indexer import Indexer
from indexer import merge_indexes

def try_on_small_data():
    docs = ["Good morning new york q",
            "Bonjour le monde",
            "Winek Pacine"]

    indexer = Indexer("pcine")
    for doc_id, doc in enumerate(docs):
        for word in doc.split():
            indexer.add_word_to_document(word.lower(), doc_id + 1)

    print(indexer)

    indexer.save_indexer_to_disk()

    new_index = Indexer("pcine")
    new_index.load_indexer_from_disk()

    print(new_index)

    docs2 = ["Good morning sna francisco",
            "Bonjour le monde",
            "Winek 7awem"]

    indexer2 = Indexer("pcine2")
    for doc_id, doc in enumerate(docs2):
        for word in doc.split():
            indexer2.add_word_to_document(word.lower(), doc_id + 4)

    print(indexer2)

    merge_index = merge_indexes(indexer, indexer2)
    print(merge_index)

def try_on_larger_data():
    docs1 = ['ca01', 'ca02', 'ca03', 'ca04']
    index1 = Indexer("my_index1")

    for doc_id, doc_name in enumerate(docs1):
        for word in brown.words(doc_name):
            index1.add_word_to_document(word.lower(), doc_id + 1)


    print(index1)
    index1.save_indexer_to_disk()

    docs2 = ['ca05', 'ca06', 'ca07', 'ca08']
    index2 = Indexer("my_index2")

    for doc_id, doc_name in enumerate(docs1):
        for word in brown.words(doc_name):
            index2.add_word_to_document(word, doc_id + len(docs1) + 1)

    print(index2)
    index2.save_indexer_to_disk()

    index1.load_indexer_from_disk()
    index2.load_indexer_from_disk()


    merge_index = merge_indexes(index1, index2)
    print(merge_index)

    merge_index.save_indexer_to_disk()

if __name__ == '__main__':
    try_on_larger_data()
