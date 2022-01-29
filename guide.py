import os
import math
from src.mylib import create_lookup_list, get_counters_from_corpus, smart_guess


def play(debug: bool = True) -> any:
    corpus_filepath = os.path.join('data', 'vocab_eng.txt')
    char_counter, word_counter, char_pos_counters = get_counters_from_corpus(corpus_filepath)
    lookup = create_lookup_list(char_pos_counters, word_counter)

    # Game initialization
    # obj_word = random.sample(set(word_counter.keys()), k=1)[0]
    max_trials = 6
    curr_trial = 1
    guess_state = [0]*5
    prev_guess = ''
    prev_state = guess_state
    whitelist = []

    while curr_trial <= max_trials:
        guess_word, guess_score, lookup, word_counter, whitelist = smart_guess(
            lookup, word_counter, prev_guess, prev_state, whitelist
        )

        suggestions = lookup[:10]
        print("Suggestions: ")
        for suggestion in suggestions:
            print(suggestion['word'], round(suggestion['score'], 3))
        print()

        guess_word = input("Your guess: ").strip()
        guess_state = list(map(int, input("Your state: ").strip()))

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
        is_win = 0
    else:
        if debug:
            print("You Win!")
        is_win = 1

    result = [is_win]
    return ",".join(map(str, result))


if __name__ == "__main__":
    _ = play(debug=True)
