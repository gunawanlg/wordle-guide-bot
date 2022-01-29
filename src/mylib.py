from __future__ import annotations

import os
import math
from collections import Counter


def get_counters_from_corpus(filepath: str) -> tuple(Counter, Counter, list):
    char_counter = Counter()
    word_counter = Counter()
    char_pos_counters = [Counter(), Counter(), Counter(), Counter(), Counter()]
    with open(filepath, 'r') as f:
        for line in f:
            word = line.strip().upper()
            char_counter += Counter(set(word))
            word_counter += Counter([word])
            for i, char in enumerate(word):
                char_pos_counters[i] += Counter(char)
    return char_counter, word_counter, char_pos_counters


def get_char_pos_counters(word_counter: Counter) -> list[Counter]:
    char_pos_counters = [Counter(), Counter(), Counter(), Counter(), Counter()]
    for word, count in word_counter.items():
        for i, char in enumerate(word):
            char_pos_counters[i] += Counter(char*count)
    return char_pos_counters


def create_lookup_list_simple(char_counter: Counter, word_counter: Counter) -> tuple(list, Counter):
    # Estimation on best first guess based on most common
    # character occurence in the vocab, calculate word score
    # for every matching most common character in the word
    sorted_char_occurence = char_counter.most_common(len(char_counter))
    max_char_occurence = char_counter.most_common(1)[0][1]
    # print(char_counter.most_common(20))
    # print()
    lookup = []
    for word in word_counter:
        score = 0
        for char, count in sorted_char_occurence:
            score += count/max_char_occurence if char in word else 0
        lookup.append({
            'word': word,
            'score': score
        })
    lookup.sort(key=lambda x: x['score'], reverse=True)
    # print(lookup[:10])
    return lookup, char_counter


def smart_guess_simple(
    lookup: list,
    prev_guess: str,
    prev_state: list,
    blacklist: list
) -> tuple(str, list, list):
    if prev_guess == '' and prev_state is None:  # is first guess
        return lookup[0]['word'], lookup, blacklist
    else:
        state_char_list = [
            [],
            [],
            []
        ]
        for i, (char, state) in enumerate(zip(prev_guess, prev_state)):
            state_char_list[state] += [(char, i)]
        blacklist.append(prev_guess)

        # Update lookup list based on prev_guess and prev_state
        new_lookup = []
        for d in lookup:
            word = d['word']
            is_append = True
            for char, i in state_char_list[2]:
                if word[i] != char:
                    is_append = False
                    break

            for char, i in state_char_list[0]:
                if char in word:
                    is_append = False
                    break

            for char, i in state_char_list[1]:
                if char not in word:
                    is_append = False
                    break

            if word in blacklist:
                is_append = False

            if is_append:
                new_lookup.append(d)

        return new_lookup[0]['word'], new_lookup, blacklist


def create_lookup_list(char_pos_counters: list[Counter], word_counter: Counter) -> tuple(list):
    """We create a lookup list, not dict, so it can be sorted based on score"""
    norm_char_pos_counters = []

    max_occurences = (sum(c.values()) for c in char_pos_counters)
    for counter, max_occurence in zip(char_pos_counters, max_occurences):
        # print(char_pos_counters[i])
        keys, values = counter.keys(), counter.values()
        norm_values = [v/max_occurence for v in values]
        norm_counter = Counter(dict(zip(keys, norm_values)))
        norm_char_pos_counters.append(norm_counter)
        # print(norm_counter.most_common(3))

    lookup = []
    for word in word_counter:
        score = 0
        for char, counter in zip(word, norm_char_pos_counters):
            score += math.log(counter[char])
        lookup.append({
            'word': word,
            'score': score
        })
    lookup.sort(key=lambda x: x['score'], reverse=True)
    return lookup


def smart_guess(
    lookup: list,
    word_counter: Counter,
    prev_guess: str,
    prev_state: list[int],
    whitelist: list[str]
) -> tuple(str, list, list, float):

    if prev_guess == '':  # is first guess
        best_guess, best_score = lookup[0]['word'], lookup[0]['score']
        best_score = math.exp(best_score)
        return best_guess, best_score, lookup, word_counter, whitelist
    else:
        # Keep a whitelist of already correct word
        new_whitelist = [*whitelist]
        for char, state in zip(prev_guess, prev_state):
            if state in [1, 2]:
                new_whitelist.append(char)

        # Reduce search space by updating lookup list
        # based on prev_guess and prev_state
        new_word_counter = Counter()
        for word, count in word_counter.items():
            to_keep = True
            for i, (char, state) in enumerate(zip(prev_guess, prev_state)):
                if state == 0:
                    if char in new_whitelist:
                        if word[i] == char:
                            to_keep = False
                    else:
                        if char in word:
                            to_keep = False
                elif state == 1:
                    if word[i] == char:
                        to_keep = False
                elif state == 2:
                    if word[i] != char:
                        to_keep = False
                else:
                    raise ValueError(
                        f"Unknown state {state}. Possible states are"
                        " 0 (gray), 1 (yellow), 2 (green)."
                    )
                if not to_keep:
                    break
            if to_keep:
                new_word_counter += Counter({word: count})

        new_char_pos_counter = get_char_pos_counters(new_word_counter)
        new_lookup = create_lookup_list(new_char_pos_counter, new_word_counter)
        best_guess, best_score = new_lookup[0]['word'], new_lookup[0]['score']
        best_score = math.exp(best_score)
        return best_guess, best_score, new_lookup, new_word_counter, new_whitelist


if __name__ == "__main__":
    corpus_filepath = os.path.join('data', 'vocab_eng.txt')
    char_counter, word_counter, char_pos_counters = get_counters_from_corpus(corpus_filepath)
    lookup = create_lookup_list(char_pos_counters, word_counter)
    # print(lookup[:20])
    # print(char_counter.most_common(20))
    # print(word_counter.most_common(20))
