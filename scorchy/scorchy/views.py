from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
from .forms import ScorchyForm
from .constants import SpecialWins, FEATURE_WIN_OPTIONS, FRUIT_OPTIONS, FRUIT_WINS, INITIAL_JACKPOT
from .models import Holds, Roll, Jackpot

def get_feature_win():
    feature_win = random.choice(FEATURE_WIN_OPTIONS)
    message = feature_win['message']
    amount = feature_win['amount']
    if type(amount) is not int:
        amount = amount()
    return {
        'message': message,
        'amount': amount,
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
    elif fruit1 == fruit0 and fruit1 == fruit3:
        return FRUIT_WINS[fruit1][4]
    
    # 3 in a row
    elif fruit1 == fruit0 or fruit1 == fruit3:
        return FRUIT_WINS[fruit1][3]
    
    # 2 in a row
    else:
        return False
    
def get_win_amount(win_dict, jackpot):
    amount = win_dict['amount']

    if amount == SpecialWins.JACKPOT:
        return jackpot
    elif amount in [SpecialWins.MAP_PIECE, SpecialWins.THREE_MAP_PIECES, SpecialWins.BOTTLED_FAERIE, SpecialWins.SIX_BOTTLED_FAERIES]:
        return 0
    
    return amount

def get_win_message(win_dict, jackpot):
    amount = win_dict['amount']
    message = win_dict['message']

    if amount == SpecialWins.JACKPOT:
        return message.format(jackpot)
    
    return message

def handle_win(win_dict, jackpot):
    amount = win_dict['amount']

    if amount == SpecialWins.JACKPOT:
        update_np(temp_user_id, jackpot)
        reset_jackpot()
    elif amount == SpecialWins.MAP_PIECE:
        # add a random map piece
        pass
    elif amount == SpecialWins.THREE_MAP_PIECES:
        # add three random map pieces
        pass
    elif amount == SpecialWins.BOTTLED_FAERIE:
        # add a bottled faerie
        pass
    elif amount == SpecialWins.SIX_BOTTLED_FAERIES:
        # add six bottled faeries
        pass
    else:
        update_np(temp_user_id, amount)
    


############
# DB Stuff #
############

temp_user_id = '123456'

def fetch_jackpot():
    try:
        jackpot_row = Jackpot.objects.get(id=1)
        return jackpot_row.jackpot
    except Exception as e:
        print(e)
        return 0

def update_jackpot():
    try:
        jackpot_row = Jackpot.objects.get(id=1)
        jackpot_row.jackpot += 5
        jackpot_row.save()
    except Exception as e:
        print(e)

def reset_jackpot():
    try:
        jackpot_row = Jackpot.objects.get(id=1)
        jackpot_row.jackpot = INITIAL_JACKPOT
        jackpot_row.save()
    except Exception as e:
        print(e)

def fetch_hold(user_id):
    try:
        holds_row = Holds.objects.get(user_id=user_id)
        holds = []
        holds.append(holds_row.hold_0)
        holds.append(holds_row.hold_1)
        holds.append(holds_row.hold_2)
        holds.append(holds_row.hold_3)
        return holds
    except Holds.DoesNotExist:
        return [False, False, False, False]

# TODO: migrate fruits to 0 index    
def fetch_roll(user_id):
    try:
        most_recent_roll = Roll.objects.filter(user_id=user_id).latest('id')
        most_recent_roll.roll = []
        most_recent_roll.roll.append(most_recent_roll.fruit_0)
        most_recent_roll.roll.append(most_recent_roll.fruit_1)
        most_recent_roll.roll.append(most_recent_roll.fruit_2)
        most_recent_roll.roll.append(most_recent_roll.fruit_3)
        return most_recent_roll
    except Roll.DoesNotExist:
        # Handle the case when there are no rolls for the given user_id
        return None
    
def insert_new_roll(user_id, roll, is_holdable, is_rollover, feature_sum):
    try:
        new_roll = Roll.objects.create(
            user_id=user_id,
            fruit_0=roll[0],
            fruit_1=roll[1],
            fruit_2=roll[2],
            fruit_3=roll[3],
            is_holdable=is_holdable,
            is_rollover=is_rollover,
            feature_sum=feature_sum
        )
        return new_roll
    except Exception as e:
        print(e)
        # Handle any exceptions that may occur during the creation and save process
        # For example, you can log the error or return None to indicate failure
        return None
    
def clear_hold(user_id):
    return insert_or_update_hold(user_id, [False, False, False, False])

# TODO: upsert?    
def insert_or_update_hold(user_id, holds):
    try:
        hold_instance = Holds.objects.get(user_id=user_id)
    except Holds.DoesNotExist:
        # If the row doesn't exist, create a new one with the given user_id
        hold_instance = Holds(user_id=user_id)

    try:
        # Update the values for hold_0, hold_1, hold_2, and hold_3
        hold_instance.hold_0 = holds[0]
        hold_instance.hold_1 = holds[1]
        hold_instance.hold_2 = holds[2]
        hold_instance.hold_3 = holds[3]

        # Save the instance (either the newly created one or the updated one)
        hold_instance.save()

    except Exception as e:
        # Handle any exceptions that may occur during the creation and save process
        # For example, you can log the error or return None to indicate failure
        return None

# Placeholder - update NPs for user
def update_np(temp_user_id, np):
    return True
    # return False

##########
# Render #
##########

def index(request):
    jackpot = fetch_jackpot()
    return render(request, 'scorchy/index.html', {
        'jackpot': jackpot,
    })

def slotwins(request):
    return render(request, 'scorchy/slotwins.html')

def process_slots(request):
    if request.method == 'POST':
        last_roll = fetch_roll(temp_user_id)

        if last_roll and last_roll.is_holdable:
            form = ScorchyForm(request.POST)
            if form.is_valid():
                holds = []
                holds.append(form.cleaned_data['scorchy_hold_0'])
                holds.append(form.cleaned_data['scorchy_hold_1'])
                holds.append(form.cleaned_data['scorchy_hold_2'])
                holds.append(form.cleaned_data['scorchy_hold_3'])
                insert_or_update_hold(temp_user_id, holds)
    
    return redirect('/slots')


def slots(request):
    if not update_np(temp_user_id, -5):
        return render(request, 'scorchy/no_np.html')

    jackpot = fetch_jackpot()
    update_jackpot()
    holds = fetch_hold(temp_user_id)
    last_roll = fetch_roll(temp_user_id)
    feature_sum = last_roll.feature_sum if last_roll and last_roll.is_rollover else 0
    
    roll = []
    for i in range(4):
        if holds[i]:
            fruit = last_roll.roll[i]
        else:
            fruit = random.choice(FRUIT_OPTIONS)
        
        feature_sum += int(fruit.split('_')[1])
        roll.append(fruit)

    clear_hold(temp_user_id)

    win_dict = calculate_win(roll)
    win_amount = 0
    win_message = ""
    feature_win_message = False
    feature_win_amount = 0

    # Prioritize fruit wins over feature wins
    if win_dict:
        handle_win(win_dict, jackpot)
        win_amount = get_win_amount(win_dict, jackpot)
        win_message = get_win_message(win_dict, jackpot)
    elif feature_sum >= 8:
        feature_sum = 8
        feature_win = get_feature_win()
        feature_win_message = feature_win['message']
        feature_win_amount = feature_win['amount']
        update_np(temp_user_id, feature_win_amount)
    
    # Intentionally allowing manual holds + rollovers even if you get a fruit win or feature win
    is_holdable =  random.randint(1, 6) == 6
    is_rollover = is_holdable or random.randint(1, 6) == 6

    insert_new_roll(user_id=temp_user_id, roll=roll, is_holdable=is_holdable, is_rollover=is_rollover, feature_sum=feature_sum)

    button_text = 'Play Again'
    if win_amount or feature_win_amount > 0:
        button_text = 'Collect Winnings'

    return render(request, 'scorchy/slots.html', {
        'feature_sum': feature_sum,
        'feature_win_message': feature_win_message,
        'roll': roll,
        'top_faded': [random.choice(FRUIT_OPTIONS) for _ in range(4)],
        'bottom_faded': [random.choice(FRUIT_OPTIONS) for _ in range(4)],
        'is_rollover': is_rollover,
        'is_holdable': is_holdable,
        'win_amount': win_amount,
        'win_message': win_message,
        'button_text': button_text,
        'lit_feature_range': list(range(1, min(feature_sum + 1, 9))),
        'dull_feature_range': list(range(max(feature_sum + 1, 1), 9))
    })