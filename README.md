# GroupSoftwareEngineering
## Description
A bingo style game in which users complete sustainability type squares and tasks. Users get points (leaf coins) if they are able to complete a rows, columns or diagonals of a sustainability bingo grid. They are then able to spend these coins on different seed packets that they can grow in their garden. If you don't keep a daily streak going, plants start dying. 


## Meeting Notes
### Session 1
Date: 07/02/2025
- We came up with the Initial idea of a bingo board with tiles contianing sustainnability goals which are marked off when completed. When the user gets a bingo win condition (4 In a row either Horizontally, Vertically, or diagonally), they gain an in game currency: Leaf Coins. With these  coins they can purchase plant packets for plants to add to their virtual gardens.


- The website will consist of a home page, with an explanation of the game, and a login prompt.
- There will then be two other pages, one with the bingo board, the other with the garden.

- The grid will be 4x4, resetting every week.
- 6 or so will be a visiting tiles, requiring the user to walk to a specific location.
- Types of tiles:
   Visit Location, Visit Wesbite, Complete a quiz
- The types of plants will have different rarities:
- Common, Rare, Epic, Legendary

- Potential Plants:

  Moss - Common
  Oak tree - Common
  Grass - Common
  Dandelion - Common

  Sunflower - Rare
  Birch Tree - Rare

  Venus FlyTrap - Epic
  Dripleaf - Epic

  Bonzai tree - Legendary
  Monkey Tree - Legendary
  Dragons Blood Tree - Legendary
  Yggdrasil - Legendary

- We did research about the rarity of plants and which category they will fit.
- The first deadline will be to get the grid and win conditions working, along with recieving the Leaf Coins.

### Session 2
Date: 10/02/2025
- Reflected on initial feedback from drop-in sprint meeting and took action
- We created roles and assigned initial tasks to indivudals based on strengths
- Created and assigned branches to allow users to contribute on their own
- Initialised main branch to contain a basic django project
- Created .gitignore to solve issues when merging and pushing from mac and windows
- Created a prototype login system and sign up system
- Have an initial basic database with password hashing to store user data
- Created multiple django apps to allow for the creation of features
- Database hashing system complies with the GDPR requirements
