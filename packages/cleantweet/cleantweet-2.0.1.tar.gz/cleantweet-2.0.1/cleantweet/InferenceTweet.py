import re
import nltk
from collections import Counter
from cleantweet import CleanTweet
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


class _InferenceTweet(CleanTweet):
    def _fbs(self, amount_of_sentences: int = 5):
        sentences = sent_tokenize(self.clean())
        words = word_tokenize(self.clean().lower())
        word_frequency = Counter(words)
        sentence_scores = {sent: sum(word_frequency[word] for word in word_tokenize(sent.lower()))
                           for sent in sentences}
        ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
        print(ranked_sentences[:amount_of_sentences])
        return None

