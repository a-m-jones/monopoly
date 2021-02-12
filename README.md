## Monopoly

This is a working project, designed to simulate a game of monopoly.

### Functions

- **roll_dice** Randomly rolls 2 dice, and saves the result and whether a double was rolled.
- **setup_game** Takes user inputs and creates a dictionary with an entry for each player. Information includes player names, pieces, starting money, starting position and list of owned properties. Also calculates who goes first, depending on who rolls the highest.
- **have_turn** Main function that moves the player's piece around the board and allows user to make decisions. Currently only allows player to buy a property.
- **play_game** Implements have_turn function in 2 loops (for players and turns) in order to allow the game to progress. Currently allows double rolls to have another go. 

### To do list

- 3 rolls --> go to jail
- Being in Jail
- Pay rent to other players
- Trading
- Purchase houses/hotels
- Collect money when passing Go
- Paying tax
- Chance/community chest
- Mortgaging
- Graphics