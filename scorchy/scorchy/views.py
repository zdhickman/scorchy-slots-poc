from django.http import HttpResponse
from django.shortcuts import render
import random
from .forms import ScorchyForm

# See: https://www.reddit.com/r/neopets/comments/xu8akc/scorchy_slots_dicearoo/
# There are only so many fruit + number combos implemented in Scorchy Slots. Not every fruit
# has a variation with every number.
#
# Further, the odds in the linked post are actually calculated based on this array,
# where some fruit + number combos are duplicated. That's why you see four cherry + 0 options
# that add up to 4/21 odds of rolling a cherry, versus three different strawberry options that
# add up to 3/21 odds of rolling a strawberry.
FRUIT_OPTIONS = [
    # Cherry 4/21
    'cherry_0', 'cherry_0', 'cherry_0', 'cherry_0',

    # Strawberry 3/21
    'strawberry_0', 'strawberry_1', 'strawberry_2',

    # Grapes 2/21
    'grapes_0', 'grapes_1',

    # Melon 3/21
    'melon_0', 'melon_1', 'melon_3',

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

# This is simplified for the POC - some outcomes here are constant, and some are random
# in some undetermined range. See https://www.jellyneo.net/?go=scorchy_slots
FEATURE_WIN_OPTIONS = [
    "It's raining Neopoints, you pick up as many as you can carry!",
    "A couple of Neopoints rain from the sky, you pick up a handful.",
    "A flock of Korbats surround you. When they leave you are 20 Neopoints poorer!",
    "An evil Scorchio flies out of the Volcano and steals 10 Neopoints from you!!",
    "One of your Neopoints erupts in flames!",
    "The Volcano says 'Sorry, out of luck mate!'",
    "You only win a single Neopoint :(",
    "Two Neopoints fall out of the sky onto your head.",
    "Twenty Neopoints fly out of the volcano!!",
    "A light faerie magically appears next to you and gives you 30 Neopoints!",
    "A bag containing 50 Neopoints falls from the sky onto your foot.",
]

# Rewards for three or four in a row - see https://www.jellyneo.net/?go=scorchy_slots
# This is also simplified for the POC.
WINS = {
    'cherry': { 3: 15, 4: 75 },
    'strawberry': { 3: 30, 4: 150 },
    'grapes': { 3: 60, 4: 300 },
    'melon': { 3: 90, 4: 450 },
    'apple': { 3: 120, 4: 500 },
    'peach': { 3: 180, 4: 900 },
    'bell': { 3: 240, 4: 1200 },
    'baggold': { 3: 600, 4: 'jackpot' },
    'mappiece': { 3: 'a map piece', 4: 'three map pieces' },
    'faerie': { 3: 'a bottled faerie', 4: '6 bottled faeries' }
}

# Check for 3 or 4 in a row
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
        return WINS[fruit1][4]
    
    # 3 in a row
    elif fruit1 == fruit0 or fruit1 == fruit3:
        return WINS[fruit1][3]
    
    # 2 in a row
    else:
        return False

def index(request):
    # feature_sum = the number of spots lit up at the bottom
    feature_sum = 0
    holds = [False, False, False, False]

    # We are checking for user-submitted values here without knowing if the UI actually gave an option
    # to manually hold. We're also passing the feature_sum blindly into the form. Both of these behaviors
    # are unsafe and open to exploitation.
    if request.method == 'POST':
        form = ScorchyForm(request.POST)
        if form.is_valid():
            feature_sum = form.cleaned_data['hold_feature_value'] or 0
            holds[0] = form.cleaned_data['scorchy_hold_fruit_1'] if form.cleaned_data['scorchy_hold_node_1'] else False
            holds[1] = form.cleaned_data['scorchy_hold_fruit_2'] if form.cleaned_data['scorchy_hold_node_2'] else False
            holds[2] = form.cleaned_data['scorchy_hold_fruit_3'] if form.cleaned_data['scorchy_hold_node_3'] else False
            holds[3] = form.cleaned_data['scorchy_hold_fruit_4'] if form.cleaned_data['scorchy_hold_node_4'] else False
    
    # roll = the middle row
    # Check for holds the user selected, if there isn't one, roll a new one
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

    # faded = top and bottom rows
    faded = []
    while len(faded) < 8:
        fruit = random.choice(FRUIT_OPTIONS)
        faded.append(fruit)

    win = calculate_win(roll)
    
    # Rolling 1 through 12 to satisfy these odds:
    # 1/6 chance that the feature rolls over to the next spin (these odds are verified to match retail)
    # If rolling over, then 1/2 chance to let the user manually hold (these odds are NOT verified)
    hold_random = random.randint(1, 12)

    # For now, if the user got 3 or 4 in a row, don't enable the feature hold (NOT verified)
    hold_feature = not win and hold_random >= 11
    manual_hold = not win and hold_random == 12

    # Superficial - pick a random feature win (odds for picking a feature win are NOT verified)
    feature_win_message = False
    if feature_sum >= 8:
        feature_win_message = random.choice(FEATURE_WIN_OPTIONS)

    return render(request, 'scorchy/index.html', {
        'feature_sum': feature_sum,
        'feature_win_message': feature_win_message,
        'roll': roll,
        'top_faded': faded[0:4],
        'bottom_faded': faded[4:8],
        'hold_feature': hold_feature,
        'manual_hold': manual_hold,
        'win': win,
    })