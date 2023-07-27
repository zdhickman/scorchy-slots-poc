from enum import Enum
import random

class Fruit(Enum):
    CHERRY = 1
    STRAWBERRY = 2
    GRAPES = 3
    MELON = 4
    APPLE = 5
    PEACH = 6
    BELL = 7
    FAERIE = 8
    MAPPIECE = 9
    BAGGOLD = 10

class SpecialWins(Enum):
    JACKPOT = 1
    MAP_PIECE = 2
    THREE_MAP_PIECES = 3
    BOTTLED_FAERIE = 4
    SIX_BOTTLED_FAERIES = 5

INITIAL_JACKPOT = 10_000

# Tweaked odds from the original
# Simulation estimate:
# Spins: 10000000
# Jackpot wins: 252 (1 in 39682)
# Map piece wins: 5023 (1 in 1990)
# Three map piece wins: 245 (1 in 40816)
# Bottled faerie wins: 4503 (1 in 2220)
# Six bottled faerie wins: 194 (1 in 51546)
FRUIT_OPTIONS = [
    # Cherry 4/21
    'cherry_0', 'cherry_0', 'cherry_0',

    # Strawberry 3/21
    'strawberry_0', 'strawberry_1', 'strawberry_2',

    # Grapes 2/21
    'grapes_0', 'grapes_1',

    # Melon 3/21
    'melon_0', 'melon_1',

    # Apple 2/21
    'apple_0', 'apple_1',

    # Peach 2/21
    'peach_1', 'peach_0',

    # Bell 2/21
    'bell_0', 'bell_3',

    # Faerie 1/21
    'faerie_0',

    # Map Piece 1/21
    'mappiece_0',

    # Gold Bag 1/21
    'baggold_0',
]

FEATURE_WIN_OPTIONS = [
    {
        'message': "It's raining Neopoints, you pick up as many as you can carry!",
        'amount': lambda : random.randrange(4, 8),
    },
    {
        'message': "A couple of Neopoints rain from the sky, you pick up a handful.",
        'amount': lambda : random.randrange(1, 6),
    },
    {
        'message': "A flock of Korbats surround you. When they leave you are 20 Neopoints poorer!",
        'amount': -20,
    },
    {
        'message': "An evil Scorchio flies out of the Volcano and steals 10 Neopoints from you!!",
        'amount': -10,
    },
    {
        'message': "One of your Neopoints erupts in flames!",
        'amount': -1,
    },
    {
        'message': "The Volcano says 'Sorry, out of luck mate!'",
        'amount': 0,
    },
    {
        'message': "You only win a single Neopoint :(",
        'amount': 1,
    },
    {
        'message': "Two Neopoints fall out of the sky onto your head.",
        'amount': 2,
    },
    {
        'message': "Twenty Neopoints fly out of the volcano!!",
        'amount': 20,
    },
    {
        'message': "A light faerie magically appears next to you and gives you 30 Neopoints!",
        'amount': 30,
    },
    {
        'message': "A bag containing 50 Neopoints falls from the sky onto your foot.",
        'amount': 50,
    }
]

FRUIT_WINS = {
    'cherry': {
        3: {
            'amount': 15,
            'message': "3 cherries! You win 15 Neopoints!",
        },
        4: {
            'amount': 75,
            'message': "4 cherries! You win 25 Neopoints!",
        },
    },
    'strawberry': {
        3: {
            'amount': 30,
            'message': "3 strawberries!! You win 30 Neopoints!",
        },
        4: {
            'amount': 150,
            'message': "4 strawberries! You win 150 Neopoints!",
        }
    },
    'grapes': {
        3: {
            'amount': 60,
            'message': "3 grapes!!  You win 60 Neopoints!",
        },
        4: {
            'amount': 300,
            'message': "4 grapes!! Yeah! You win 300 Neopoints!",
        },
    },
    'melon': {
        3: {
            'amount': 90,
            'message': "3 melons!! Yippee! You win 90 Neopoints!",
        },
        4: {
            'amount': 450,
            'message': "4 melons!!! Way to go!!! You win 450 Neopoints!",
        },
    },
    'apple': {
        3: {
            'amount': 120,
            'message': "3 APPLES!! Yippee!  You win 120 Neopoints!",
        },
        4: {
            'amount': 500,
            'message': "4 APPLES!!! Way to go!!! You win 500 Neopoints!",
        },
    },
    'peach': {
        3: {
            'amount': 180,
            'message': "3 PEACHES!! Woohoo! You win 180 Neopoints!",
        },
        4: {
            'amount': 900,
            'message': "4 PEACHES!!! Wahey!!!! You win 900 Neopoints!",
        },
    },
    'bell': {
        3: {
            'amount': 240,
            'message': "3 BELLS!! Fantastic! You win 240 Neopoints!",
        },
        4: {
            'amount': 1200,
            'message': "4 BELLS!!! Great!!!! You win 1200 Neopoints!",
        },
    },
    'baggold': {
        3: {
            'amount': 600,
            'message': "3 BAGS OF GOLD!! That's nearly the jackpot!! You win 600 Neopoints!",
        },
        4: {
            'amount': SpecialWins.JACKPOT,
            'message': lambda jackpot : "4 BAGS OF GOLD!!! JACKPOT!!!!!!! You win {jackpot} Neopoints!".format(jackpot),
        },
    },
    'mappiece': {
        3: {
            'amount': SpecialWins.MAP_PIECE,
            'message': "3 Pieces of Map!!!",
        },
        4: {
            'amount': SpecialWins.THREE_MAP_PIECES,
            'message': "4 MAP PIECES ON THE WINLINE!!! You win three pieces of the treasure map!!!!",
        },
    },
    'faerie': {
        3: {
            'amount': SpecialWins.BOTTLED_FAERIE,
            'message': "3 Faeries!!!",
        },
        4: {
            'amount': SpecialWins.SIX_BOTTLED_FAERIES,
            'message': "4 FAERIES!! All six faeries float down into your inventory!!!",
        },
    },
}