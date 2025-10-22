# FourTic Game

FourTic is a 4D Connect Four game implemented using Pygame. Players take turns placing their markers in a 4D grid, aiming to connect four of their markers in a row, column, or diagonal across any of the four dimensions.

Try directly online:
https://grafmar.github.io/FourTic/src/build/web/

In four dimensions there are many directions to get a winning row:

15 possible directions can be achieved from the coordinate [0,0,0,0] (top left)
<img src="https://raw.github.com/grafmar/FourTic/master/directions.svg">

## Features

- Play as two players (X and O).
- Check for winners in multiple dimensions.
- Reset the game easily.
- Responsive design that adjusts to window size.

## Installation

To run the FourTic game, you need to have Python and Pygame installed. Follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/grafmar/FourTic.git
   cd FourTic
   ```

2. Install the required dependencies (pygame and pygbag):
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the game, run the following command:
```
python src/main.py
```

To start the game in a browser use:
```
python -m pygbag --app_name FourTic --title FourTic  .\main.py
```
and then connect to http://localhost:8000

Players can click on the grid to place their markers. The game will announce the winner when a player connects four markers in a row.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- Pygame for the game development framework.
- Inspiration from classic Tic Tac Toe gameplay.
