import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from cleantweet import CleanTweet
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('vader_lexicon', quiet=True)


class SentimentTweet(CleanTweet):
    """
    class for getting the sentiments contained within a body of text. Currently,
    the only implementation is the VADER algorithm
    """
    def vader(self):
        """
        Vader Sentiment method, this relies on the same algorithm used in nltk.
        :return: sentiment scores for each sentence in the body of text.
        """
        sentiment = SentimentIntensityAnalyzer()
        sentences = nltk.sent_tokenize(self.clean(tokenize_method=True))
        print(sentences)
        sentiment_scores = [sentiment.polarity_scores(sentence)['compound'] for sentence in sentences]
        return sentiment_scores

    def _bert(self):
        pass

    def _gloria(self):
        # this will be our custom sentiment model.
        pass
