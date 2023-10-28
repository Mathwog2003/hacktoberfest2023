#importing module
import random

while True:
#game code
    print("\tWelcome to the game (ROCK PAPER SCISSOR)")
    print("\n\trules for this game:\n\t\'Rock wins against scissors \n\tpaper wins against rock\t\n \tscissors wins against paper\'")
    user_input = input('Enter rock|paper|scissor and if you need to quit enter q ').lower()
    if user_input == 'q':
        print("See you later buddy")
        break
#user input image
    if user_input == "rock":
    
#Rock
        print('''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
''')
    elif user_input == "paper":
    #paper
        print('''
    _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
''')
    elif user_input == "scissor":
    #scissor
        print('''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)

    ''')
    else:
        print("Earth can't able to hadle so talented people")
        print("so kindly follow the rules")
        break
    
    print("Your choice : ",user_input)
#movements computer
    movements = ['rock','paper','scissor']
    computer = random.choice(movements)

    if computer == "rock":
    
    #Rock
        print('''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
''')
    elif computer =="paper":
    #paper
        print('''
    _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
''')
    elif computer =="scissor":
    #scissor
        print('''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)

    ''')
    print("Computer choice : ",computer)

#Game logic Rock wins against scissors; \npaper wins against rock;\n and scissors wins against paper
    if user_input == 'rock':
        if computer == 'paper':
            print('Computer won ')
        elif computer == 'scissor':
            print('You won')
        elif computer == 'rock':
            print('Match draw')
    elif user_input == 'paper':
        if computer == 'paper':
            print('Match draw')
        elif computer == 'rock':
            print('You won')
        elif computer == 'scissor':
            print('Computer won')
    elif user_input == 'scissor':
        if computer == 'paper':
            print('You won')
        elif computer == 'stone':
            print('Computer won')
        elif computer == 'scissor':
            print('Match draw')
 