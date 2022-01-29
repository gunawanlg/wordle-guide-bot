# Wordle Guide Bot

For each trial, it will output list of word suggestions ranked with highest chance of winning. Simply input your guess word and guess state on each trial. 

For example, this scenario will be represented by its following program output:

<p align="center">
    <img src="https://github.com/Arc-rendezvous/wordle-guide-bot/blob/master/wordle_sample.png">
</p>

```
Suggestions: 
SANES -9.907
SORES -9.917
SALES -10.063
SERES -10.063
CARES -10.103
SONES -10.138
BARES -10.15
SAREE -10.206
SIRES -10.229
SOLES -10.293

Your guess: SANES
Your state: 00000
Trial 1:
00000
SANES
Prob of win:  0.00
Logp of win: -9.91
=================

Suggestions: 
COOLY -8.674
COOTY -8.686
BOOLY -8.888
BOOTY -8.901
POOLY -9.091
POOTY -9.104
COLLY -9.249
COOMY -9.252
DOOLY -9.29
FOOTY -9.294

Your guess: COOLY
Your state: 22020
Trial 2:
22020
COOLY
Prob of win:  0.00
Logp of win: -8.67
=================

Suggestions: 
COULD 0.0

Your guess: COULD
Your state: 22222
Trial 3:
22222
COULD
Prob of win:  1.00
Logp of win: 0.00
=================

You Win!
```

## Usage

To use default english version with 10 suggestions, run

```
python guide.py
```

To change to other version and reduce number of suggestion to 5, define your corpus file and the number:

```
python guide.py -p "my_own_corpus.txt" -n 5
```

## How It Works

It maximizes probability of winning by maximizing probability of guessing each character correctly on each position.

$$
P(Winning) = P(Correct\_char\_at\_pos 0) * P(Correct\_char\_at\_pos 1) * ... * P(Correct\_char\_at\_pos 4)
$$

Where it maximize <img src="https://render.githubusercontent.com/render/math?math=P(Correct\_char\_at\_pos\_i)"> by choosing character with highest occurence at pos i, relative to all character occurences at pos i, more formally if we have a vocabulary set of:

<img src="https://render.githubusercontent.com/render/math?math=V=\{APPLE, AWARD, BEACH\}">

then 

$$
argmax(P(Correct\_char\_at\_pos\_0)) = A
$$

where

$$
P(Correct\_char\_at\_pos\_0)) = 2/3
$$

The score for each word in the known vocab would be then product of each character position probability of being cocrect. In this example,

$$
P(Winning|APPLE) = 2/3 * 1/3 * 1/3 * 1/3 * 1/3=0.00823
$$
