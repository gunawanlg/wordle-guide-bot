# Wordle Guide Bot

For each trial, it will output list of word suggestions ranked with highest chance of winning. Simply input your guess word and guess state on each trial. For example, the following output from
program:

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

would represent following scenario:

![Sample Scenario](/wordle_sample.png)

## How It Works

Win condition for wordle is for 

It maximizes probability of winning by maximizing probability of guessing each character correctly on each position.

P(Winning) = P(Correct char at pos 0) * P(Correct char at pos 1) * ... * P(Correct char at pos 4)

Where it maximize P(Correct char at pos x) by choosing character with highest occurence at pos x, relative to all character occurences at pos x, more formally:

argmax(P(Correct char at pos 0)) = ....

The score for each word in the known vocab would be the 



## Adjustment 

You can modify