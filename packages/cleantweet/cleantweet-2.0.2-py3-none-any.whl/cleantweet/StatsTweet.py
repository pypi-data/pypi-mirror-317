import nltk
from cleantweet import CleanTweet
from nltk.tokenize import word_tokenize
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download('stopwords', quiet=True)


# module for textual statistics
class StatsTweet(CleanTweet):

    def show_special_characters(self):
        """
        method to show the special characters in the document
        :return: a list of special characters in the text/document.
        """
        with open(self.text, "r", encoding='utf8', errors='ignore') as character_object:
            characters = character_object.read()
            self.special_characters = [character for character in characters if not character.isalnum()
                                       if not character == ' ']
            return self.special_characters

    def count_special_characters(self):
        """
        :return: the amount of special characters in the text
        """
        return len(self.show_special_characters())

    def count_of_empty_strings(self):
        """
        method to return the amount of empty strings
        :return: a list of empty strings
        """
        spaces = [space for space in self.text.clean() if space == '' or space == ' ' or space == '  ']
        return len(spaces)

    def _ner(self):
        pass

    def _vocab_size(self):
        pass

    # todo
    # need to get the total amount of pos tags in the .txt file

    def figure_of_speech(self, figure_of_speech: str, amount: int):
        """
        method for splitting the text into the different parts of speech
        :param figure_of_speech: the specific type of figure of speech e.g. Nouns, Pronouns etc.
        :param amount: the amount of words whose pos tags you want to see
        :return: a dictionary of words and frequencies for the keys and values respectively
        """
        tagged_tokens = nltk.pos_tag(nltk.word_tokenize(self.clean()))
        figures = [word for word, pos in tagged_tokens if pos.startswith(figure_of_speech)]
        figures_frequency_distribution = nltk.FreqDist(figures)
        most_common_figures = figures_frequency_distribution.most_common(amount)
        all_figures = []
        all_figure_frequencies = []

        # print('Top Adjectives:')
        for figure, frequency in most_common_figures:
            all_figures.append(figure)
            all_figure_frequencies.append(frequency)

        figures_and_frequencies = {'words': all_figures, 'frequency': all_figure_frequencies}

        return figures_and_frequencies

    def amount_of_nouns(self, amount: int, plural: bool = False):
        """
        total amount of singular nouns in the text. for plural nouns,
        change the plural parameter to True.
        :param amount: the amount of adjectives you want to view, you can only pass an integer
        :param plural: do you want to use singular or plural nouns? the default is singular and it expects
        a boolean argument.
        :return: prints out the total number of nouns in the text
        along with their frequencies; if plural is true does same
        but for plural nouns.
        """

        if plural is True:
            return self.figure_of_speech('NNS', amount)

        return self.figure_of_speech('NN', amount)

    def amount_of_proper_nouns(self, amount: int, plural: bool = False):
        """
        method for knowing the amount of proper nouns in the given text object
        :param plural: is it a singular or plural pronoun? The default is singular.
        :param amount: how many pronouns do you want to see?
        :return: a dictionary of each pronoun and their frequency
        """

        if plural is True:
            return self.figure_of_speech('NNPS', amount)

        return self.figure_of_speech('NNP', amount)

    def amount_of_verbs(self, amount: int, tense: str = ''):
        """
        get the amount of verbs in the text. the default values will return
        the verbs in the base form e.g. run, eat, stand etc.
        :param amount: the amount of verbs you want to view, you can only pass an integer
        :param tense: this parameter expects a string and will get the verbs in
        other forms. Here are the allowed arguments: 'past tense', 'gerund' or
        'present participle', 'past participle', 'non-third person',
        'third person' or '3rd person' for past tense verbs e.g. ran, present participle
        verbs e.g. running, past participle verbs e.g. run, non-3rd person singular present
        verbs e.g. run, and third-person singular present verbs e.g. runs

        :return: it will print out the verbs and their related frequency in the text.
        """

        if tense == 'past tense':
            return self.figure_of_speech('VBD', amount)
        if tense == 'gerund' or tense == 'present participle':
            return self.figure_of_speech('VBG', amount)
        if tense == 'past participle':
            return self.figure_of_speech('VBN', amount)
        if tense == 'non-third person':
            return self.figure_of_speech('VBP', amount)
        if tense == 'third person' or tense == '3rd person':
            return self.figure_of_speech('VBZ', amount)

        return self.figure_of_speech('VBZ', amount)

    def amount_of_articles(self, amount: int):
        """
        method for knowing the amount of articles in the text object
        :param amount: the amount of articles you want to see
        :return: a dictionary of articles and their corresponding frequencies
        """
        return self.figure_of_speech('DT', amount)

    def amount_of_adjectives(self, amount: int, modifier: str = ''):
        """
        get the total amount of adjectives in the text
        :param amount: the amount of adjectives you want to view, you can only pass an integer
        :param modifier: to view the other types of adjectives,
        you can pass two string values: 'comparative' e.g. quicker
        or 'superlative' e.g. quickest.
        :return: it will print out the adjectives and their related frequency in the text.
        """

        if modifier == 'comparative':
            return self.figure_of_speech('JJR', amount)
        if modifier == 'superlative':
            return self.figure_of_speech('JJS', amount)

        return self.figure_of_speech('JJ', amount)

    def amount_of_adverbs(self, amount: int):
        """
        method for determining the amount of adverbs in the text object
        :param amount: the amount of adverbs you want to see
        :return: a dictionary of the adverbs and their corresponding frequencies
        """
        return self.figure_of_speech('RB', amount)

    def amount_of_conjunctions(self, amount: int = 10):
        """
        method for determining the amount of conjunctions in the text object
        :param amount: the amount of conjunctions you want to see
        :return: a dictionary of the conjunctions and their corresponding frequencies
        """
        return self.figure_of_speech('CC', amount)

    def amount_of_pronouns(self, amount: int, modifier: str = ''):
        """
        method for determining the amount of pronouns in the text object
        :param amount: the amount of pronouns you want to see.
        :param modifier: choose the type of pronoun; pass it as string - 'possessive' or 'POSSESSIVE' or 'pos' or 'POS'.
        The default is a regular pronoun.
        :return: a dictionary of the pronouns and their corresponding frequencies.
        """

        if modifier.lower() == 'possessive' or modifier.lower() == 'pos':
            return self.figure_of_speech('PRP$', amount)

        return self.figure_of_speech('PRP', amount)

    def amount_of_prepositions(self, amount: int = 10):
        """
        method for determining the amount of prepositions in the text object
        :param amount: the amount of prepositions you want to see.
        :return: a dictionary of the prepositions and their corresponding frequencies.
        """
        return self.figure_of_speech('IN', amount)

    def amount_of_cardinal_number(self, amount: int):
        """
        amount of cardinal number e.g. one four, 5, 6
        :return: the amount of cardinal numbers in the text as dictionary of cardinal numbers and their corresponding
        frequencies.
        """
        return self.figure_of_speech('CD', amount)

    def amount_of_existential_there(self, amount: int):
        """
        if the phrase 'there is' is present in the text
        :return: the amount of 'there is' in the text as dictionary of cardinal numbers and their corresponding
        frequencies.
        """
        return self.figure_of_speech('EX', amount)

    def amount_of_foreign_word(self, amount: int):
        """
        if there are foreign words e.g. foreign language words like french d'accord etc.
        or other foreign language words.
        :return: the amount of foreign words in the text.
        """
        return self.figure_of_speech('FW', amount)

    def amount_of_list_item_marker(self, amount: int):
        """
        how many list item markers are present in the text e.g. 1., A., i. etc.
        :return: the amount of list item markers in the text
        """
        return self.figure_of_speech('LS', amount)

    def amount_of_modal(self, amount: int):
        """
        examples of modals include can, should, will, would etc.
        :return: the amount of modals present in the text
        """
        return self.figure_of_speech('MD', amount)

    def amount_of_predeterminer(self, amount: int):
        """
        predeterminers include all, both, half etc.
        :return: the amount of predeterminers present in the text
        """
        return self.figure_of_speech('PDT', amount)

    def amount_of_possessive_ending(self, amount: int):
        """
        possessive endings e.g. 's, ' etc.
        :return: a dictionary of possessive ending words and their corresponding frequencies in the text.
        """
        self.figure_of_speech('POS', amount)

    def amount_of_particle(self, amount: int):
        """
        examples include up, off etc.
        :return: a dictionary of particle words and their corresponding frequencies in the text.
        """
        return self.figure_of_speech('RP', amount)

    def amount_of_symbol(self, amount: int):
        """
        this method is similar to the show_special_characters method in the CleanTweet class;
        it shows the amount of special characters in the text e.g. &, %, &, * etc.
        :return: a dictionary of the different symbols and their corresponding frequencies in the text.
        """
        return self.figure_of_speech('SYM', amount)

    def amount_of_to(self, amount: int):
        """
        literally the word 'to'
        :return: a dictionary of 'to' and their corresponding frequencies in the text.
        """
        return self.figure_of_speech('TO', amount)

    def amount_of_interjections(self, amount: int):
        """
        examples of interjections include oh, wow, oops etc.
        :return: a dictionary of interjections and their corresponding frequencies in the text.
        """
        return self.figure_of_speech('UH', amount)

    def amount_of_wh_determiner(self, amount: int):
        """
        examples include which, that etc.
        :return: a dictionary of wh-determiners and their corresponding frequencies in the text.
        """
        return self.figure_of_speech('WDT', amount)

    def amount_of_wh_pronoun(self, amount: int):
        """
        examples include who, what etc.
        :return: a dictionary of wh-pronouns and their corresponding frequencies in the text.
        """
        self.figure_of_speech('WP', amount)

    def amount_of_possessive_wh_pronoun(self, amount: int):
        """
        the possessive wh-pronoun - 'whose'
        :return: a dictionary of possessive wh pronouns and their corresponding frequencies in the text.
        """
        return self.figure_of_speech('WP$', amount)

    def amount_of_wh_adverb(self, amount: int):
        """
        examples include where, when etc.
        :return: a dictionary of wh adverbs and their corresponding frequencies in the text.
        """
        return self.figure_of_speech('WRB', amount)

    def _word_token_size(self):
        pass

    def _sentence_token_size(self):
        pass
