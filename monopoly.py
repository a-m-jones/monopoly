## Import modules
import numpy as np
import pandas as pd

## Read in the game board from csv file
gameboard = pd.read_csv('./game_board.txt', delimiter='\t')
## Property categories that can't be bought
non_properties = ['Other', 'Community Chest', 'Chance', 'Tax']
## List of all properties owned
all_owned_properties = []
    
        
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
    # return value, double
    return 5, False
    
        
def have_turn(player_dict, position, owned_properties, money):
    """
    Simulates a turn in a game (in development).

    Inputs:
    ----------
    position: current position
    owned_properties: list of properties owned by the player
    money: player's cash
    
    Returns:
    ----------
    position: current position on board
    double: whether or not a double was rolled
    current_property: current property on board
    """
    ## Roll
    roll, double = roll_dice()
    ## Update board position and ensure position number is on the board
    position = (position + roll)  % len(gameboard)
    ## Find current property, category and price
    current_property = gameboard.at[position, 'Label']
    current_category = gameboard.at[position, 'Category']
    current_price    = gameboard.at[position, 'Price']
    ## Print current values
    print("Roll: {}\nPosition: {}\nDouble: {}\nCurrent property: {}\n".format(
    roll, position, double, current_property))
    ## Tax - remove money
    if current_category == 'Tax':
        print("{}. Pay {}.".format(current_property, current_price))
        money = money - current_price
    ## Land on owned property - pay that player rent. 
    ## (This doesn't work correctly for utilities or stations yet.)
    elif current_property in all_owned_properties and current_category not in non_properties:
        print("Incomplete.")
        print("{} is owned by {}. Pay them £{}.".format(1,2,3))
    ## If player has enough money and property not already bought --> option to buy it
    elif current_price <= money and current_property not in all_owned_properties and current_category not in non_properties:
        while True:
            answer = input("Do you want to buy {} for £{}? (Y or N)\n".format(current_property, current_price))
            if answer in ['y', 'Y', 'yes', 'Yes']:
                owned_properties.append(current_property)
                all_owned_properties.append(current_property)
                money = money - current_price
                print("Bought {} for £{}.\n".format(current_property, current_price))
                break
            elif answer in ['n', 'N', 'no', 'No']:
                ## will need to implement option for others to buy in future
                print("Rejected {}\n".format(current_property))
                break
            else:
                print("Must choose either Y or N!")
    print("You have £{} left.\n".format(money))

    return position, double, money
        


def setup_game():
    """
    Set up the game, using raw inputs.
    """
    print("#"*28)
    print("Welcome to virtual monopoly!")
    print("#"*28 + '\n')

    ## Record number of players
    while True:
        N_players = int(input("No. of players: "))
        if N_players > 6:
            print("Maximum number of players = 6\n")
        else:
            break

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
        ## build player dictionary with their piece, starting money, current position and list of owned properties
        player_dict[name] = [playing_piece, 1500, 0, []]

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
            str_to_print = ("{} " * no_max_rolls) + "have rolled the same highest number. Please roll again:\n"
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


def play_minigame(N_turns):
    """
    REDUNDANT FUNCTION AS 'HAVE_TURN' HAS CHANGED.
    Simulates a player moving around the board, and collecting properties.
    Extra rolls from doubles are included within the turn. 
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


def play_game():
    """
    In development.
    """
    # player_dict, players = setup_game()
    player_dict = {'a': ['wheelbarrow', 1500, 0, []], 
                   'b': ['dog', 1500, 0, []]}
    players = ['a', 'b']

    print("#"*28)
    print("Let the game begin")
    print("#"*28 + '\n')
    input("Press enter to continue\n")

    turn = 1

    while turn < 3: # arbitrary value, can change to something meaningful later

        print("Turn {}\n".format(turn))

        for player in players:

            input("{}'s turn. Press enter to continue.\n".format(player))

            ## read in data from player dictionary
            player_entry      = player_dict[player]
            money             = player_entry[1]
            position          = player_entry[2]
            owned_properties  = player_entry[3]

            ## player has their turn
            position, double, money = have_turn(player_dict, position, owned_properties, money)

            ## if player rolls a double, they get another roll (this is currently infinite,
            ## however this will need to be changed so that 3 doubles --> jail)
            while double == True:
                input("Rolled a double! Have another roll.\n")
                position, double, money = have_turn(player_dict, position, owned_properties, money)

            ## put the data back into the dictionary
            player_entry[1] = money
            player_entry[2] = position
            player_entry[3] = owned_properties

            input("Press enter to continue\n")

        turn += 1

    ## print some values at the end of the game
    print(player_dict)
    print(all_owned_properties)


if __name__ == '__main__':
    play_game()
