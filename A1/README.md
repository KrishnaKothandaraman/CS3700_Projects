# CS3700_Projects

## Project 1

Implement basic socket connection to play the game Wordle

### Journey through my Wordle game logic development

#### Iteration 1

First iteration of working solution based on memory of past guesses. Implemented simple logic to save letter status as
orange(incorrect position), green(correct position) or grey(does not exist). Then, filtered next guess so that the
letters in the next guess satisfy the learning from past guesses.
- Next guess has past green letters in the same position
- Next guess has past orange letters and in different positions as guessed before
- Next guess has no past grey letters 

Pros
- Easy to implement
- Low number of guesses to get the right answer. Average 24.15 guesses per answer taken over 20 tries(can I make this better??)
- Designed to imitate how humans solve Wordle.

Cons
- Word lookup is slow
- Use basic data structure list to represent words so O(n) for each guess(can I make this better?)