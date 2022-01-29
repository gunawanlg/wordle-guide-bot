import random
import math
from src.mylib import create_lookup_list, get_counters_from_corpus, smart_guess
from guide import parse_args


def play(corpus_filepath: str, debug: bool = True) -> str:
    char_counter, word_counter, char_pos_counters = get_counters_from_corpus(corpus_filepath)
    lookup = create_lookup_list(char_pos_counters, word_counter)

    # Game initialization
    obj_word = random.sample(set(word_counter.keys()), k=1)[0]
    max_trials = 6
    curr_trial = 1
    guess_state = [0]*5
    prev_guess = ''
    prev_state = guess_state
    whitelist = []

    guess_words, guess_states, guess_scores = [], [], []
    while curr_trial <= max_trials:
        guess_word, guess_score, lookup, word_counter, whitelist = smart_guess(
            lookup, word_counter, prev_guess, prev_state, whitelist
        )

        for i, (char, obj_char) in enumerate(zip(guess_word, obj_word)):
            if char == obj_char:
                guess_state[i] = 2
            elif char in obj_word:
                guess_state[i] = 1
            else:
                guess_state[i] = 0

        # Run info log, to be redirected
        guess_words.append(guess_word)
        guess_states.append("".join(map(str, guess_state)))
        guess_scores.append(round(math.log(guess_score), 6))

        if debug:
            out_str = (
                f"Trial {curr_trial}:\n"
                f"{''.join(map(str, guess_state))}\n"
                f"{guess_word}\n"
                f"Prob of win:  {guess_score:.2f}\n"
                f"Logp of win: {math.log(guess_score):.2f}\n"
                "=================\n"
            )
            print(out_str)
        if all([x == 2 for x in guess_state]):
            break

        # Iteration
        prev_guess = guess_word
        prev_state = guess_state
        curr_trial += 1

    if curr_trial > max_trials:
        if debug:
            print("You Lose!")
            print(f"Objective word: {obj_word}")
        is_win = 0
    else:
        if debug:
            print("You Win!")
        is_win = 1

    pad_empty = ['']*(max_trials-curr_trial)
    guess_words += pad_empty
    guess_states += pad_empty
    guess_scores += pad_empty
    result = [is_win, *guess_words, *guess_states, *guess_scores, obj_word, curr_trial]
    return ",".join(map(str, result))


if __name__ == "__main__":
    args = parse_args()
    corpus_filepath = args.path
    _ = play(corpus_filepath, debug=True)
