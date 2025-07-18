# Tron-AI
An AI bot to play Tron against

## Libraries

- [pygame](https://www.pygame.org/)
- [numpy](https://numpy.org/)

## Code Structure
*environment.py* contains the code for displaying the game state and performing actions

*human.py* and *control.py* are, respectively, the human game agent and the AI game agent

*play.py* contains the code for initalizing the agents and the environment and running the game

## Play

To play against the AI:

`python play.py`

By default the human controls use the arrow keys to change direction, but to use a preferred set of keys simply edit the *predict* method in *play.py*.