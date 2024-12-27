import re
import random
import nltk
from nltk.tokenize import word_tokenize
from cleantweet import CleanTweet
from collections import Counter, defaultdict
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


class PredictionTweet(CleanTweet):
    def _ngram_model(self, n: int = 2):
        ngrams = [tuple(self.clean().split(' ')[i:i + n]) for i in range(len(self.clean().split(' ')) - n + 1)]
        model = defaultdict(Counter)
        # print(ngrams)
        for ngram in ngrams:
            prefix, next_word = ngram[:-1], ngram[-1]
            model[prefix][next_word] += 1
        return model

    def ngram(self, start_word: str, ngram_size: int = 2, max_length: int = 10):
        """
        a method to use the bag of words ngram model for next word prediction.
        :param start_word: the starting word for the prediction
        :param ngram_size: amount of ngrams you want, default is 2 (recommended)
        :param max_length: length of the predicted word or sentence
        :return: a predicted string of words
        """
        sentence = [start_word]
        prefix = tuple(sentence[-(ngram_size-1):])

        for _ in range(max_length):
            ngram_model = self._ngram_model(n=ngram_size)
            ngram_list = list(ngram_model.keys())
            ngram_list = [item for tup in ngram_list for item in tup]
            if prefix[0] not in ngram_list:
                print('Start Word is not in your Ngram model, choose a word that is presently in the model')
                return None

            next_word = random.choices(
                list(ngram_model[prefix].keys()),
                weights=ngram_model[prefix].values()
            )[0]
            sentence.append(next_word)

            if next_word in {'.', '!', '?'}:
                break

            prefix = tuple(sentence[-(ngram_size-1):])

        return ' '.join(sentence)

    def ngram_count(self):
        """
        method to know the ngram count
        :return: an integer of the ngram count
        """
        ngrams = self._ngram_model()
        ngram_count = list(ngrams.keys())
        ngram_count = [item for tup in ngram_count for item in tup]
        return len(ngram_count)

    def hmm(self):
        pass

    def rnn(self):
        pass

    def transformer(self):
        pass

    def bert_context(self):
        pass



