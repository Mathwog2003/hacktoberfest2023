import random
from word_list import word_list
from hangman_art import stages,logo

print(logo)
choosen_word = random.choice(word_list)

display = []
for i in range(len(choosen_word)):
    display += '_'
print(display)

end_of_loop = True
lives = 6
while end_of_loop: 
    
    guess = input("guess a letter : ").lower()

    if guess in display:
            print(f"\nyou have already guessed this {guess}")
        
    
    if guess not in choosen_word:
        lives -= 1
        print("\nYou guessed wrongly.")
        print("no of lifes are :",lives)

        if lives == 0:
            print("You lose.")
            end_of_loop = False

    for position in range(len(choosen_word)):
        
        if choosen_word[position] == guess:
            display[position] = guess

    if '_' not in display:
        end_of_loop = False
        print("\nYou won")
    
    print(stages[lives])
    print(display)