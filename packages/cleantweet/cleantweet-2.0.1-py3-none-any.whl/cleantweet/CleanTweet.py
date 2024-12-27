import re
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


class CleanTweet:
    def __init__(self, text, *args):
        """
        a class for cleaning and preprocessing the text
        :param text: .txt file containing the textual data you want to use for the Natural Language Processing task.
        :param args: pass any argument that you want (leave this empty).
        """
        self.text = text
        self.word_count = 0
        self.special_characters = ""

    def clean(self, tokenize_method: bool = False):
        """
        method to clean the text
        :param tokenize_method: if set to True, it wil sentence tokenize else it will
        word tokenize. The default is word tokenize
        :return: the word tokens as a string
        """
        with open(self.text, "r", encoding='utf8', errors='ignore') as read_object:
            lines = read_object.read()

            # remove special characters and punctuations
            lines = re.sub('#', '', lines)
            lines = re.sub('\\n\\n', '', lines)
            lines = re.sub('[\\n\\n]', '', lines)
            lines = re.sub('(\n\n)', '', lines)
            lines = re.sub('[{}:_@\[\]0-9,%&*""?!/-]', '', lines)

            # remove the id and text tag
            lines = re.sub('(id)', '', lines)
            lines = re.sub('(text)', '', lines)
            lines = re.sub('(RT)', '', lines)

            # remove paragraph space/indentation
            lines = re.sub('  ', '', lines)
            if tokenize_method is True:
                lines = nltk.sent_tokenize(lines)
                self.word_count = len(lines)
                lines = ' '.join(lines)
            else:
                lines = word_tokenize(lines)
                lines = [line for line in lines if line.isalpha()]
                self.word_count = len(lines)
                lines = ' '.join(lines)
        return lines

    def show_word_collocations(self):
        """
        method to show the corresponding Word Collocations in the document
        :return: a list of the word collocations
        """
        text = nltk.Text(self.text)
        return text.collocation_list()

    def remove_curse_words(self):
        """
        method to remove curse words like 'fuck', 'hell', and 'damn'
        :return: a list of appropriate words in the text/corpus
        """
        data = self.clean()
        data_list = data.split()
        for datum in range(0, len(data_list)):
            if data_list[datum].strip().lower() == 'fuck' or data_list[datum].strip().lower() == 'hell'\
                    or data_list[datum].strip().lower() == 'damn':
                data_list[datum] = '****'
        return data_list
