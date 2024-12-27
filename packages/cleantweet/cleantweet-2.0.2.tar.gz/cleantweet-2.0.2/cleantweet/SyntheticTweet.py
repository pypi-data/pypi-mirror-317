import random
import pandas as pd
from cleantweet import CleanTweet
from cleantweet import StatsTweet


class SyntheticTweet:
    def __init__(self, text):
        self.text = text

    def rule_based(self, amount_of_sentences: int = 10, amount_of_pos: int = 5, percentage: float = 0.25):
        """
        this method uses a rule-based algorithm to generate synthetic data.
        :param amount_of_sentences: the amount of synthetic sentences you want to generate.
        :param amount_of_pos: the amount of each part of speech you want, you only need to choose
        one amount, it will be the same for nouns, verbs, and adverbs. The higher this amount,
        the more random your synthetic data will be.
        :param percentage: a float value that represents the salt value of the synthetic sentences that
        will be generated. It must be a float and the default is below 0.25 which will be ->
        noun -> verbs -> adverbs. Increasing the float value will give: noun -> verbs -> adverbs -> adjectives
        etc.
        :return: a string of the different synthetic data generated from the text object
        """

        figures_of_speech = StatsTweet(self.text)
        nouns = [figures_of_speech.amount_of_nouns(amount_of_pos)]
        pronouns = []
        verbs = [figures_of_speech.amount_of_verbs(amount_of_pos)]
        adjectives = [figures_of_speech.amount_of_adjectives(amount_of_pos)]
        adverbs = [figures_of_speech.amount_of_adverbs(amount_of_pos)]
        articles = ['the']
        subjects = [nouns + pronouns]
        predicates = [verbs]

        print(random.choice(nouns[0]['words']))

        def sentence():
            if percentage > 0.25:
                synthetic_sentence = (f"{random.choice(nouns[0]['words'])} {random.choice(verbs[0]['words'])} "
                                      f"{random.choice(adverbs[0]['words'])} "
                                      f"{random.choice(nouns[0]['words'])} "
                                      f"{random.choice(adjectives[0]['words'])}")
            else:
                synthetic_sentence = (f"{random.choice(nouns[0]['words'])} "
                                      f"{random.choice(verbs[0]['words'])} "
                                      f"{random.choice(adverbs[0]['words'])} "
                                      f"{random.choice(nouns[0]['words'])}")

            return synthetic_sentence

        if nouns[0]['words'] == [] or verbs[0]['words'] == [] or adverbs[0]['words'] == []:
            print('Your text document must have a noun, a verb, and an adverb.')
        else:
            for _ in range(amount_of_sentences):
                print(sentence())

    def _amount_of_synthetic_data(self):
        """
        method for knowing the total count of synthetic data generated
        :return:
        """
        pass
