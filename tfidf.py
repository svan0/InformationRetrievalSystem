from preprocess import TokenPreprocessor
import os
import nltk
from nltk import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

documentsPath = 'text'


class TfidfBuilder:

    def __init__(self, path: str, preprocessor: TokenPreprocessor):
        self.__tokenPreprocessor = preprocessor
        self.__documentsPath = path
        self.__tfidf = None

    def tokenizer(self, text):
        return self.__tokenPreprocessor.preprocess(nltk.word_tokenize(text))

    def buildTfidf(self):
        docsToContent = {}
        documentsFileNames = os.listdir(self.__documentsPath)
        for docId, documentFileName in enumerate(documentsFileNames):
            with open(self.__documentsPath + '/' + documentFileName, 'r+') as fileHandler:
                content = fileHandler.read()
                docsToContent[docId] = content

        tfidf = TfidfVectorizer(tokenizer=self.tokenizer, use_idf=True)
        tfidf.fit_transform(docsToContent.values())
        return Tfidf(tfidf)


class Tfidf:

    def __init__(self, tfidf):
        self.tfidf = tfidf

    def resolveQuery(self, query):
        feature_names = self.tfidf.get_feature_names()
        response = self.tfidf.transform([query])
        for col in response.nonzero()[1]:
            print(feature_names[col], ' - ', response[0, col])


if __name__ == '__main__':
    tfidfBuilder = TfidfBuilder(documentsPath, TokenPreprocessor(PorterStemmer(mode='NLTK_EXTENSIONS'), stopwords.words('english')))
    tfidf = tfidfBuilder.buildTfidf()
    query = 'this sentence has unseen text such as computer but also king lord juliet.'
    tfidf.resolveQuery(query)