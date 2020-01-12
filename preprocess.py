from streams import Stream


class TokenPreprocessor:

    def __init__(self, stemmer, stopWords):
        self.__stemmer = stemmer
        self.__stopWords = stopWords

    def stem(self, token: str):
        return self.__stemmer.stem(token)

    def preprocess(self, tokens: [str]):
        result = Stream(tokens) \
            .filter(lambda token: token.isalpha()) \
            .filter(lambda token: token not in self.__stopWords) \
            .map(lambda token: token.lower()) \
            .map(lambda token: self.stem(token))
        return list(result)
