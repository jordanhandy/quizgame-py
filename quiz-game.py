##################################################################
# Quiz Game 
# Description:
# This program uses the OpenTrivia API to 
# generate a list of questions for the user,
# asks these questions, and asks the user if they would like
# to play again, after tallying their score.
##################################################################

# Modules
import requests  # Http requests
import json  # parsing JSON
import pprint # printing JSON if required
import random # to randomize list of answers
import time as t # time module
import html # html

# Variable to keep track of
# user correct answers
# user incorrect answers
# the current question number
# control variable, whether user wants to continue or quit the game

userScoreCount_correct = 0
userScoreCount_incorrect = 0
questionNum = 0
endGame = ""
valid_answer = False

# Game continues while user has not quit
while endGame != "quit":
    # API call to OpenTrivia
    # If request fails, game does not continue
    r = requests.get("https://opentdb.com/api.php?amount=10&category=12&difficulty=medium&type=multiple")
    if (r.status_code != 200):
        endGame = input("Sorry, there was problem getting the questions.  Press enter to ry again, or 'quit' to quit the game").lower()
    else:
        data = json.loads(r.text)

        print("Welcome to the OpenTrivia Quiz Game!")
        print("This game will ask you 10 multiple choice questions about music, and keep track of your score.")
        print("At the end of the game, you will be asked if you would like to play again")
        input("Press any key to continue...")
        
    # 10 questions
    while(questionNum < 10):
        # Get question
        # Print escaped
        question = (data["results"][questionNum]["question"])
        print (html.unescape(question + "\n"))
        
        # Get answers in a list format
        # append the correct answer to the list
        # shuffle that list
        answers = list(data["results"][questionNum]["incorrect_answers"])
        correct_answer = (data["results"][questionNum]["correct_answer"])
        answers.append(correct_answer)
        shuffled_answers = random.sample(answers,len(answers))
        x=1
        
        #display answers
        for answer in shuffled_answers:
            print(f"{x} - {html.unescape(answer)}")
            x+=1

        # User must choose answer
        # Data validation for non ints, and ints outside array bounds
        while valid_answer != True:
            userChoice = int(input("\nSelect answer 1,2,3, or 4:  "))
            try:
                userChoice = int(userChoice)
                if (userChoice > len(shuffled_answers) or (userChoice <= 0)):
                    print("Invalid answer")
                else:
                    valid_answer = True
            except:
                print("Invalid answer.  Use only numbers")
        userChoice = userChoice-1

        # Test answer correctness
        # and update score accordingly
        if(shuffled_answers[userChoice] == correct_answer):
            print(f"\nCongratulations, you are correct!  The correct answer was {html.unescape(correct_answer)}")
            userScoreCount_correct+=1
            questionNum+=1
        else:
            print(f"\nSorry, that's not right.  You answered {shuffled_answers[userChoice]}")
            questionNum+=1
            userScoreCount_incorrect+=1

    # Display results
    print(f"\n**********************************************\nThanks for playing.\nYour scores are: Correct answers - {userScoreCount_correct}\nIncorrect answers - {userScoreCount_incorrect}\n**********************************************")
    t.sleep(5) # from time module to sleep
    # Prompt user to quit
    playAgain = input("\nPlay again? 'quit' to leave. ENTER to play again  ").lower()
print("\n Thanks for playing")
    

