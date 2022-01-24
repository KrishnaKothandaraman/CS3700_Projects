# CS3700_Projects

## Project 1

Implement basic socket connection to play the game Wordle

### Journey through my Wordle game logic development

#### Iteration 1(Submitted)

The motivation for the strategy is based on how I play the game of Wordle. In a nutshell, each guess is made such that is 
does not waste any intelligence gathered from previous guesses. The next guess is filtered based on these three rules:

- Next guess has past green letters in the same position
- Next guess has past orange letters, but in different positions to those guessed before
- Next guess has no past grey letters 

The response of the server to the guess is then used to make the next guess better by attempting to minimize the wastage
of knowledge gained from past guesses.

For example:

First Guess: about
Server Response: [2,0,0,1,0]
Now, the only candidates for the next guess are words that have 'a' in the first position, 'u' not in the 4th position 
and no 'b', 'o' and 't'.

Pros
- Easy to implement
- Low number of guesses to get the right answer. Average 6.53 guesses per answer taken over 30 games(can I make this better??)
- Designed to imitate how humans solve Wordle.

Cons
- Word lookup is slow
- Use basic data structure list to represent words so O(n) for each guess(can I make this better?)