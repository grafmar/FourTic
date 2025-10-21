# FourTic Game

FourTic is a 4D Connect Four game implemented using Pygame. Players take turns placing their markers in a 4D grid, aiming to connect four of their markers in a row, column, or diagonal across any of the four dimensions.

## Features

- Play as two players (X and O).
- Check for winners in multiple dimensions.
- Reset the game easily.
- Responsive design that adjusts to window size.

## Installation

To run the FourTic game, you need to have Python and Pygame installed. Follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/FourTic.git
   cd FourTic
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the game, run the following command:
```
python src/FourTic.py
```

Players can click on the grid to place their markers. The game will announce the winner when a player connects four markers in a row.

## Running Tests

To ensure the game logic is functioning correctly, you can run the unit tests located in the `tests` directory. Use the following command:
```
pytest tests/test_fourtic.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- Pygame for the game development framework.
- Inspiration from classic Connect Four gameplay.