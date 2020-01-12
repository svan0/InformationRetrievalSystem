from indexer import Indexer
from preprocess import TokenPreprocessor
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from indexer import Indexer

nltk.download('stopwords')
nltk.download('treebank')
nltk.download('wordnet')
nltk.download('punkt')

documentsPath = 'text'


class IndexBuilder:

    def __init__(self, path: str, preprocessor: TokenPreprocessor):
        self.__tokenPreprocessor = preprocessor
        self.__documentsPath: path

    def buildIndex(self, name):
        indexer = Indexer(name)
        documentsFileNames = os.listdir(documentsPath)
        for docId, documentFileName in enumerate(documentsFileNames):
            with open(documentsPath + '/' + documentFileName, 'r+') as fileHandler:
                content = fileHandler.read()
                tokens = tokenProcessor.preprocess(nltk.word_tokenize(content))
                for token in tokens:
                    indexer.add_word_to_document(token, docId + 1)
        print(indexer)
        indexer.save_indexer_to_disk()


if __name__ == '__main__':
    tokenProcessor = TokenPreprocessor(PorterStemmer(mode='NLTK_EXTENSIONS'), stopwords.words('english'))
    indexBuilder = IndexBuilder(tokenProcessor, documentsPath)
    indexBuilder.buildIndex('myIndex')