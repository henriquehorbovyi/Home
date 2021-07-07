import random

import wikipedia


def random_presearch_answer(term):
    return random.choice([
        'just a minute',
        'give me a minute',
        'let me check',
        'searching {} on wikipedia'.format(term)
    ])


def search(term):
    wikipedia.set_lang("en")
    result = wikipedia.search(term)
    answer = "couldn't find any results about " + term

    if len(result) != 0:
        answer = "the top results are: {}".format(", ".join(result[:3]))

    return answer

    # TODO >>> LATER

    #
    # try:
    #     answer = "accordingly with wikipedia, " + wikipedia.page(term).summary
    # except wikipedia.DisambiguationError as e:
    #     answer = "I have three options for you\n{0}\n{1}\n{2}" \
    #         .format(e.options[0], e.options[1], e.options[2])
    #
    # return answer


if __name__ == '__main__':
    s = search("Google")
    print(s)
