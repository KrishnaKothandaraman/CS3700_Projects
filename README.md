# CS3700_Project1

## Assignment 1

Implement basic socket connection to play the game Wordle

### Wordle game logic iterations

#### Iteration 1

First iteration of working solution based on memory of past guesses. Implemented simple logic to save letter status as
orange(incorrect position), green(correct position) or grey(does not exist). Then, filtered next guess so that the
letters in the next guess satisfy the learning from past guesses.

Pros
- Easy to implement
- Low number of guesses to get the right answer. Average 6.7 guesses per answer taken over 100 tries
- Designed to imitate how humans solve Wordle

Cons
- Word lookup is slow
- Use basic data structure list to represent words so O(n) for each guess(can I make this better?)