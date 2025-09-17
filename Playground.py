import random

twin_intro = random.choice(["Hello, nice to see you!", "Howdy, kindly to see you partner."])

print(twin_intro)

print(random.choice(["What's your name?", "What's your name 'ore there?"]))
input_name = input()

it_dont_work = random.choice(["Nice to meet you!", "This town ain't big enough for the bothin of us, but I'll humor ya."])
print(it_dont_work,)

print(random.choice(["What kind of music do you like?", "What sorta tunes you got goin on 'ore there?"]))
music_input = input()

music_respo = [f'I love {music_input}!', f'{music_input}, huh? Pathetic.']
print(random.choice(music_respo))

print(random.choice(["Wanna play a game?", "How 'bout a little bet?"],), "y/n")
answer = input()

if answer == "y":
    print(random.choice(["Yessss!", "Didn't think you had the guts."]))
else:
    print(random.choice(["Awww man.", "Figured you were too scared to take up a real man on a bet."]))

print(random.choice(["How about a dice roll? You call it higher or lower than 3!", "How 'bout a bit of dice? I'm sure you already know the rules"]))
print("Higher or Lower?")

dice_roll = input("Higher", "Lower")
if dice_roll == "higher":


