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


## Play on

https://grafmar.github.io/FourTic/src/build/web/

## Possible directions from top left field
15 possible directions can be achieved from the coordinate [0,0,0,0]

<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="patt1" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <rect width="20" height="20" x="0" y="00" style="fill:white;stroke-width:3;stroke:black" />
    </pattern>
  </defs>
  <defs>
    <pattern id="field1" x="0" y="0" width="90" height="90" patternUnits="userSpaceOnUse">
	  <rect width="80" height="80" x="0" y="0" stroke="black" fill="url(#patt1)" />
    </pattern>
  </defs>
  <defs>
    <pattern id="cross" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <line x1="4" y1="4" x2="16" y2="16" style="stroke:blue;stroke-width:2" />
	   <line x1="4" y1="16" x2="16" y2="4" style="stroke:blue;stroke-width:2" />
    </pattern>
  </defs>
  <rect width="350" height="350" x="0" y="0" stroke="black" fill="url(#field1)" />
  <rect width="20" height="20" x="0" y="0" stroke="red" fill="url(#cross)" style="stroke-width:3" transform="translate(0 0)"/>
  // 1,0,0,0
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(20 0)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(40 0)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(60 0)"/>
  // 0,1,0,0
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)" transform="translate(0 20)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)" transform="translate(0 40)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(0 60)"/>
  // 1,1,0,0
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)" transform="translate(20 20)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)" transform="translate(40 40)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(60 60)"/>
  // 0,0,1,0
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(90 0)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(180 0)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(270 0)"/>
  // 1,0,1,0
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(110 0)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(220 0)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(330 0)"/>
  // 0,1,1,0
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(90 20)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(180 40)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(270 60)"/>
  // 1,1,1,0
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(110 20)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(220 40)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(330 60)"/>
  // 0,0,0,1
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(0 90)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(0 180)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(0 270)"/>
  // 1,0,0,1
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(20 90)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(40 180)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(60 270)"/>
  // 0,1,0,1
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(0 110)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(0 220)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(0 330)"/>
  // 1,1,0,1
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(20 110)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(40 220)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(60 330)"/>
  // 0,0,1,1
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(90 90)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(180 180)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(270 270)"/>
  // 1,0,1,1
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(110 90)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(220 180)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(330 270)"/>
  // 0,1,1,1
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(90 110)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(180 220)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(270 330)"/>
  // 1,1,1,1
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(110 110)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(220 220)"/>
  <rect width="20" height="20" x="0" y="0" stroke="none" fill="url(#cross)"  transform="translate(330 330)"/>
</svg>

