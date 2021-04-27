import random
from words import word_list
import json 
class Scoreboard():
    def __init__(self, name):
        self.name = name

    # Save scores to file
    def save(self):
        with open('scoreboard.json', 'w') as f:
            f.write(json.dumps(self.scores))

    # Load scores from file
    def load(self):
        try:
            with open('scoreboard.json', 'r') as f:
                self.scores = json.loads(f.readline())
                if not self.name in self.scores:
                    self.scores[self.name] = 0
                    self.save()
        except (FileNotFoundError,json.JSONDecodeError) as e:
            self.scores = {
                self.name: 0
            }
            with open('scoreboard.json', 'w') as f:
                f.write(json.dumps(self.scores))
                

    # Add 10 points to score
    def add_score(self):
        self.scores[self.name] += 10
        self.save()

    # Return scores
    def get_scores(self):
        return self.scores
    
    # Print the top 10 scores
    def print_score(self):
        print('Top Scores')
        print ('\n-----------------------------------------------------------\n')
        for name, score in {k: v for k, v in sorted(self.scores.items(), key=lambda user: user[1], reverse=True)[:10]}.items():
            print(name, score)
        print ('\n-----------------------------------------------------------\n')



def play_again():
    answer = input('Would you like to play again? Yes/ No').lower()
    if answer == 'y' or 'yes':
        play_game()
    else:
        exit()

def get_word():
        word = random.choice(word_list)
        return word.lower()

def play_game():
    name = input('Please enter your name: ').lower()
    scoreboard = Scoreboard(name)
    scoreboard.load()
    scoreboard.print_score()
    


    alphabets = 'abcdefghijklmnopqrstuvwxyz '
    word = get_word()
    letters_guessed = []
    tries = 6
    guessed = False

    print('The word contains', len(word), 'letters')
    print(len(word) * '*')
    while not guessed and tries > 0:
        print('You have ' + str(tries) + ' tries')
        guess = input('Please enter one letter or the full word').lower()

        #1 - user inputs a letter.
        if len(guess) == 1:
            if guess not in alphabets:
                print('You have not entered a letter.')
            elif guess in letters_guessed:
                print('You have already guessed this letter before.')
            elif guess not in word:
                print('Sorry, that letter is not part of the word :-(')
                letters_guessed.append(guess)
                tries -= 1
            elif guess in word:
                print('Well done, that letter exists in the word!')
                letters_guessed.append(guess)
            else:
                print('An unexpcted error has occurred, investigate further!')
        #2 - user inputs the full word.
        elif len(guess) == len(word):
            if guess == word:
                print('Well done, you have guessed the word!')
                guessed = True
                scoreboard.add_score()
                scoreboard.print_score()
            else:
                print('Sorry, that was not the word we were looking for:-(')
                tries -=1
                
        #3 - user inputs letters where the total number of letters do not match total number of letters in the word.
        else:
            print('The length of your guess is not the same as the length of world we\'re looking for.')
        status = ''
        if not guessed :
            for letter in word:
                if letter in letters_guessed:
                    status += letter
                else:
                    status += '*'
            print (status)
                  
        if status == word:
            print('Well done, you have guessed the word!')
            scoreboard.add_score()
            scoreboard.print_score()
            guessed = True
        elif tries == 0:
            print ('You have run out of guesses and you haven\'t guessed the word!')
            scoreboard.print_score()
    play_again()
play_game()
