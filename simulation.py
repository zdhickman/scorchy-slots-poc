import random
import datetime
from collections import Counter
from scorchy.scorchy.constants import Fruit, SpecialWins, FRUIT_OPTIONS, FRUIT_WINS, FEATURE_WIN_OPTIONS

INITIAL_JACKPOT = 100
MAX_SPINS = 10_000_000

def get_feature_win():
    feature_win = random.choice(FEATURE_WIN_OPTIONS)
    amount = feature_win['amount']
    if type(amount) is not int:
        amount = amount()
    return amount

def calculate_win(roll):
    fruit0 = roll[0].split('_')[0]
    fruit1 = roll[1].split('_')[0]
    fruit2 = roll[2].split('_')[0]
    fruit3 = roll[3].split('_')[0]

    # if middle fruits are not the same, no 3 or 4 in a row possible
    if fruit1 != fruit2:
        return False
    
    # 4 in a row
    if fruit1 == fruit0 and fruit1 == fruit3:
        return FRUIT_WINS[fruit1][4]
    
    # 3 in a row
    elif fruit1 == fruit0 or fruit1 == fruit3:
        return FRUIT_WINS[fruit1][3]
    
    # 2 in a row
    else:
        return False

# either NP or a special item  
def get_win_amount(win_dict):
    global jackpot
    global jackpot_wins
    global map_piece_wins
    global three_map_piece_wins
    global bottled_faerie_wins
    global six_bottled_faerie_wins
    amount = win_dict['amount']

    if amount == SpecialWins.JACKPOT:
        temp = jackpot
        jackpot = INITIAL_JACKPOT
        jackpot_wins += 1
        return temp
    
    elif amount == SpecialWins.MAP_PIECE:
        map_piece_wins += 1
        return 0
    
    elif amount == SpecialWins.THREE_MAP_PIECES:
        three_map_piece_wins += 1
        return 0
    
    elif amount == SpecialWins.BOTTLED_FAERIE:
        bottled_faerie_wins += 1
        return 0
    
    elif amount == SpecialWins.SIX_BOTTLED_FAERIES:
        six_bottled_faerie_wins += 1
        return 0
    
    return amount

def pick_item(items):
    # Count frequency of each item, ignoring part after underscore
    counts = Counter(item.split('_')[0].upper() for item in items)

    # If mappiece has a frequency higher than all other items, return it
    if 'MAPPIECE' in counts and all(counts['MAPPIECE'] > counts[item] for item in counts if item != 'MAPPIECE'):
        return 'MAPPIECE'

    # Otherwise, return the item with the highest enum value
    return max(counts, key=lambda item: Fruit[item].value)

def pick_holds(roll):
    fruit_to_hold = pick_item(roll)
    for i in range(4):
        fruit = roll[i].split('_')[0].upper()
        if fruit_to_hold == fruit:
            holds[i] = roll[i]
        else:
            holds[i] = False

# DB stuff
spins = 0
np = 100_000_000
jackpot = INITIAL_JACKPOT
jackpot_wins = 0
map_piece_wins = 0
three_map_piece_wins = 0
bottled_faerie_wins = 0
six_bottled_faerie_wins = 0
holds = [False, False, False, False]
feature_sum = 0

# For debugging
always_manual_hold = False

def main():
    global spins
    global np
    global jackpot
    global jackpot_wins
    global map_piece_wins
    global three_map_piece_wins
    global bottled_faerie_wins
    global six_bottled_faerie_wins
    global holds
    global feature_sum

    while spins < MAX_SPINS:
        if spins % 100000 == 0:
            print(spins)
        spins += 1
        np -= 5
        roll = []

        for i in range(4):
            if holds[i]:
                fruit = holds[i]
            else:
                # Every fruit roll is entirely independent of all other rolls
                fruit = random.choice(FRUIT_OPTIONS)
            
            # We add to the feature_sum again, even if the user did a manual hold
            feature_sum += int(fruit.split('_')[1])
            roll.append(fruit)

        win_dict = calculate_win(roll)

        if win_dict:
            win_amount = get_win_amount(win_dict)
            np += win_amount
            holds = [False, False, False, False]
            feature_sum = 0

        else:
            if feature_sum >= 8:
                feature_win = get_feature_win()
                np += feature_win
            manual_hold =  random.randint(1, 6) == 6
            feature_rollover = manual_hold or random.randint(1, 6) == 6

            if manual_hold or always_manual_hold:
                pick_holds(roll)
            else:
                holds = [False, False, False, False]

            if not feature_rollover:
                feature_sum = 0

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"output-{timestamp}.txt"

    with open(file_name, "w") as file:
        file.write('Spins: {spins}\n'.format(spins = spins))
        file.write('Jackpot wins: {jackpot_wins} (1 in {ratio})\n'.format(jackpot_wins = jackpot_wins, ratio = int(spins/jackpot_wins)))
        file.write('Map piece wins: {map_piece_wins} (1 in {ratio})\n'.format(map_piece_wins = map_piece_wins, ratio = int(spins/map_piece_wins)))
        file.write('Three map piece wins: {three_map_piece_wins} (1 in {ratio})\n'.format(three_map_piece_wins = three_map_piece_wins, ratio = int(spins/three_map_piece_wins)))
        file.write('Bottled faerie wins: {bottled_faerie_wins} (1 in {ratio})\n'.format(bottled_faerie_wins = bottled_faerie_wins, ratio = int(spins/bottled_faerie_wins)))
        file.write('Six bottled faerie wins: {six_bottled_faerie_wins} (1 in {ratio})\n'.format(six_bottled_faerie_wins = six_bottled_faerie_wins, ratio = int(spins/six_bottled_faerie_wins)))

if __name__ == "__main__":
    main()