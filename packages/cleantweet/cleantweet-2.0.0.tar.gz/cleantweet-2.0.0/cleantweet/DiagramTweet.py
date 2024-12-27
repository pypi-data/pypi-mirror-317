import nltk
import pandas as pd
from cleantweet import CleanTweet
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


class DiagramTweet(CleanTweet):
    def word_cloud(self, width: int = 1400, height: int = 800, max_words: int = 100,
                   background_color: str = 'black', *args):
        """
        method to draw a wordcloud from a text/document.

        :param width: the width of the wordcloud, default is 1400px
        :param height: the height of the wordcloud, default is 800px
        :param max_words: how many words do you want to appear in the wordcloud, default is 100
        :param background_color: the background color of the wordcloud. You can enter the colors
        or hex codes as a string
        :param args: you can pass any other argument that is expected of the Wordcloud library method; as
        this method is a wrapper for that.
        :return: a wordcloud display image
        """

        words = self.clean()
        plt.imshow(WordCloud(width=width, height=height, max_words=max_words,
                             background_color=background_color).generate(words))
        plt.show()

    def frequency_distribution(self, amount: int = 2):
        """
        method for showing the frequency distribution (amount of times a particular word occurs) in the text/document
        :param amount: how many words do you want to know their frequency amount? the default is 2. The argument must
        be an integer and not a float value.
        :return: a frequency distribution image
        """

        tokens = word_tokenize(self.clean())
        text = nltk.FreqDist(tokens)
        text.plot(amount, cumulative=True)

    def tabulate(self, word_amount: int = 2):
        """
        method for showing the frequency distribution in a tabular format.
        :param word_amount: amount of words whose frequencies you want to see; default is 2
        :return: a horizontal table showing the related words and their corresponding frequencies
        """

        words = self.clean()
        words = nltk.word_tokenize(words)
        freq_dist = nltk.FreqDist(words)
        return freq_dist.tabulate(word_amount)

    def bar_chart(self, amount_of_bars: int = 10, bar_color: str = '#a4b2e2', background_color: str = 'lightgray',
                  xlabel_name: str = 'Word', ylabel_name: str = 'Frequency', title: str = 'Most Frequent Words',
                  x_ticks_rotation: int = 90, grid_color: str = '#272727', grid_alpha: float = 0.1):
        """
        a method for showing the bar chart with the word on the x-axis and their frequencies on the y-axis
        :param amount_of_bars: the amount of bars to show in the bar chart; default value is 10 and maximum is 20. It's
        advisable to keep it below 15 for pleasing visual results.
        :param bar_color: the color of the bars you want. It should be a string of either html color value names, or a
        valid color hex code.
        :param background_color: change the background color of the bar chart, the default value is lightgray.
        :param xlabel_name: the name of the xlabel, must be a string. The default value is Word.
        :param ylabel_name: the name of the ylabel, must be a string. The default value is Frequency
        :param title: the title of the bar graph, to add a title, pass a string as an argument.
        :param x_ticks_rotation: the angle you want the xticks to be in, default is 90 degrees.
        :param grid_color: the grid color you want, it must be a string.
        :param grid_alpha: how much transparency do you want, default is 0.1. it must be a floating point value.
        e.g. 0.1, 0.2 etc. if unsure, leave as it is.
        :return: a bar chart of the most frequent words in the document.

        """

        words = self.clean()
        words = nltk.word_tokenize(words)
        freq_dist = nltk.FreqDist(words)
        words_from_freq_dist = [word for word in freq_dist.keys()]
        values_from_freq_dist = [word for word in freq_dist.values()]

        data_freq = {xlabel_name: words_from_freq_dist, ylabel_name: values_from_freq_dist}
        dataframe = pd.DataFrame(data_freq)
        dataframe_sorted_freq = dataframe.sort_values(by='Frequency', ascending=False)

        # Plot the bar chart
        bars = plt.bar(dataframe_sorted_freq[xlabel_name][0:amount_of_bars],
                       dataframe_sorted_freq[ylabel_name][0:amount_of_bars],
                       color=bar_color, zorder=2)
        bars[(amount_of_bars//2)].set_color(background_color)
        plt.xlabel(xlabel_name)
        plt.ylabel(ylabel_name)
        plt.title(title)
        plt.xticks(rotation=x_ticks_rotation)
        plt.grid(color=grid_color, alpha=grid_alpha, zorder=1)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['left'].set_visible(True)
        plt.gca().spines['bottom'].set_visible(True)
        plt.show()

    def _bubble_chart(self):
        pass

    def _heatmap(self):
        pass

