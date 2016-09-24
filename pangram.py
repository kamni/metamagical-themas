"""
J Leadbetter <jleadbet@gmail.com>
MIT License

A pangram is a self-documenting sentence in the form similar to:

    This pangram tallies five a's, one b, one c, two d's, twenty-eight e's,
    eight f's, six g's, eight h's, thirteen i's, one j, one k, three l's, two
    m's, eighteen n's, fifteen o's, two p's, one q, seven r's, twenty-five s's,
    twenty-two t's, four u's, four v's, nine w's, two x's, four y's, and one z.

Lee Sallows proposes the following:

    I'll wager ten guilders that nobody will succeed in producing a perfect
    self-documenting solution (or proof of its non-existence) to the sentence
    beginning, 'This computer-generated pangram contains ...' within the next
    ten years. No tricks allowed. The format to be exactly as in the above
    pangrams. Either 'and' or '&' is permissible. Result to be derived
    exclusively by von Neumann architecture digital computer (no super
    computers, no parallel processing). Fancy your chances?

Of course, this was proposed sometime in the early 80's, and I'm not sure
whether my laptop would count as a 'supercomputer' by those standards, but I'm
going to try it for fun.
"""

from __future__ import print_function

import re
import string


def generate_pangram(base_sentence, last_sentence=None, num_loops=1000):
    tried_sentences = []
    counts_to_try = [count_letters(last_sentence or base_sentence,
                                   initialize_from_base=bool(last_sentence))]

    while counts_to_try and num_loops > 0:
        base_count = counts_to_try.pop()
        base_count_str = str(base_count)
        if base_count_str in tried_sentences:
            continue
        else:
            counts_to_try += generate_new_counts(base_count)
            tried_sentences.append(base_count_str)

        new_sentence = generate_sentence(base_sentence, base_count)
        print(new_sentence)
        new_count = count_letters(new_sentence)

        if new_count == base_count:
            return new_sentence

        num_loops -= 1

    return (
        'Could not find a viable sentence within the specified number of '
        'loops. Last tried sentence: "{}"'.format(new_sentence)
    )


def count_letters(sentence, initialize_from_base=False):
    alphacount = dict([(letter, 0) for letter in string.ascii_lowercase])
    sentence = re.sub(r"[-'\s,]", '', sentence)

    for letter in sentence:
        alphacount[letter] += 1


    if initialize_from_base:
        for key in alphacount:
            if alphacount[key] == 0:
                alphacount[key] = 1

    alphacount = list(alphacount.items())
    alphacount.sort()
    simplified_alphacount = [count[1] for count in alphacount]

    return simplified_alphacount


def generate_new_counts(count_base):
    new_counts = []
    for idx, count in enumerate(count_base):
        new_count = count_base[:]
        new_count[idx] += 1
        new_counts.append(new_count)

    return new_counts


def generate_sentence(base_sentence, letter_count):
    written_letter_counts = []

    # TODO: variations on different ways of saying things
    # &/and; twelve hundred fifty-nine; twelve hundred and fifty-nine;
    # one thousand, two hundred fifty-nine; one thousand, two hun

    for idx, count in enumerate(letter_count):
        written_letter_counts.append('{} {}{}'.format(
            spell_out_number(count),
            string.ascii_lowercase[idx],
            get_plural(count)
        ))

    # TODO: return sentences


def spell_out_number(number):
    # TODO: spell out in a myriad of ways
    pass


def get_plural(count):
    return ["'s", ''][count == 1]


if __name__ == '__main__':
    sentence = 'This computer-generated pangram contains '
    pangram = generate_pangram(sentence)
    print(pangram)
