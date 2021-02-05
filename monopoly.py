## Import modules
import numpy as np
import pandas as pd

## Read in the game board from csv file
gameboard = pd.read_csv('./game_board.txt')
## 
non_properties = ['Other', 'Community Chest', 'Chance', 'Tax']
    
        
def roll_dice():
    """
    Mimics the output of rolling two 6-faced dice.
    
    Returns: 
    ----------
    - value: total value of dice
    - double: True if double rolled, else False
    """
    die_1 = np.random.randint(low=1, high=7)
    die_2 = np.random.randint(low=1, high=7)
    value = die_1 + die_2
    double = True if die_1 == die_2 else False
    return value, double
    
        
def have_turn(position, owned_properties):
    """
    Simulates a turn in a game (in development).
    
    Returns:
    ----------
    roll: what was rolled
    position: current position on board
    double: whether or not a double was rolled
    current_property: current property on board
    """
    roll, double = roll_dice()
    position += roll
    position = position - len(gameboard) if position > len(gameboard)-1 else position
    current_property = gameboard.at[position, 'Label']
    current_category = gameboard.at[position, 'Category']
    if current_property not in owned_properties and current_category not in non_properties:
        owned_properties.append(current_property)
    return roll, position, double, current_property
        
        
def play_minigame(N_turns):
    """
    Simulates a player moving around the board, and collecting properties.
    Extra rolls from doubles are included within the turn, however have not
    included 3 doubles in a row --> go to jail. Still in development.
    """
    position = 0
    owned_properties = []

    print("{:<10} {:<10} {:<10} {:<10} {:<10}\n".format('Turn', 'Roll', 'Position', 'Double', 'Property'))
    for i in range(N_turns):
        roll, position, double, current_property = have_turn(position, owned_properties)
        print("{:<10} {:<10} {:<10} {:<10} {:<10}".format(i+1, roll, position, double, current_property))
        while double == True:
            roll, position, double, current_property = have_turn(position, owned_properties)
            print("{:<10} {:<10} {:<10} {:<10} {:<10}".format('', roll, position, double, current_property))
        print("")
    
    print("Owned properties:\n")
    for prop in owned_properties:
        print(prop)


def setup_game():
    """
    Set up the game, using raw inputs.
    """
    print("#"*28)
    print("Welcome to virtual monopoly!")
    print("#"*28 + '\n')

    ## Record number of players
    N_players = int(input("No. of players: "))

    ## Save player names and pieces to dictionary
    player_dict = {}
    pieces = ['dog', 'hat', 'thimble', 'boot', 'wheelbarrow', 'cat', 'racing car', 'battleship']

    for i in range(N_players):

        name = input("Player {}: ".format(i+1))
        print("")
        print('Choose your playing piece. Options are:\n')

        for piece in pieces:
            print(piece)

        print("")

        while True:
            playing_piece = input()
            if playing_piece in pieces:
                break
            else:
                print("{} is not in list. Please choose another.".format(playing_piece))

        print("")
        pieces.remove(playing_piece)
        player_dict[name] = [playing_piece]

    ## Roll to see who goes first - highest wins!
    print("\nRoll to see who goes first!\n")
    players = sorted(player_dict.keys())
    rolls = []

    for player in players:
        input("{}: press enter to roll".format(player))
        roll = roll_dice()[0]
        rolls.append(roll)
        print("{} rolls a {}\n".format(player, roll))

    all_players = np.asarray(players)
    players = np.asarray(players) # this will be modified if more than 1 person rolls a maximum
    rolls = np.asarray(rolls)

    while True:
        
        max_roll = np.max(rolls) # the maximum roll
        max_roll_idxs = np.where(rolls == max_roll)[0] # the list indexes of the players who rolled the maximum 
        no_max_rolls = len(max_roll_idxs) # the number of people who rolled the maximum
        player_max_rolls = players[max_roll_idxs] # the players who rolled the maximum
        ## If more than 1 person rolled the maximum, get them to roll again. This continues until a winner is decided.
        
        if no_max_rolls > 1:
            str_to_print = ("{} " * no_max_rolls) + "have rolled the same highest number. Please roll again:"
            print(str_to_print.format(*player_max_rolls))
            rolls = []

            for player in player_max_rolls:
                input("{}: press enter to roll".format(player))
                roll = roll_dice()[0]
                rolls.append(roll)
                print("{} rolls a {}\n".format(player, roll))

            rolls = np.asarray(rolls)
            players = player_max_rolls

        ## Once only one player has rolled the maximum, that person goes first!
        else:
            first_player = player_max_rolls[0]
            first_player_idx = max_roll_idxs[0]
            players = np.roll(all_players, -first_player_idx) # re-orders player list so that first player goes first
            break

    print("{} to roll first!\n".format(first_player))

    return player_dict, players


def play_game():
    """
    In development. Plans to include computer players in future.
    """
    player_dict, players = setup_game()
    position = 0
    owned_properties = []
    print(player_dict, players)


if __name__ == '__main__':
    play_game()
