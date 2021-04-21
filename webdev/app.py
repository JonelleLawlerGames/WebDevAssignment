from flask import Flask, render_template, session, request
import random # for generating random number 
import os 
import pickle #store names and associated scores in pickle file 
import time # store time 
FNAME = "data/highscores.pickle"


app = Flask(__name__)

@app.route("/game")
def generateNumber() :

    # generate a number and make it global (session)
    number = random.randint(1, 1000)
    session["number"] = number
    session["numberOfGuesses"] = 1

    # Check the game is starting up for first time 
    session["firstVisit"] = False

    # this is the html file that should be displayed 
    return render_template(
        "intro.html"
    )   


@app.route("/playGame", methods = ["POST"])
def playGame() :   

    # start timer 
    if( session["firstVisit"] == False):
    
        session["start"] = time.perf_counter()
        guessOutcome = 0 # to pass to html - sentence to output 
        session["firstVisit"] = True 
        
    
    # get the number the user typed in
    elif(session["firstVisit"] == True):
        guessNum = int(request.form["guessNumber"])

        # check whether or not the user has typed in the correct number 
        if(guessNum > session["number"]):
        
            guessOutcome = 1
            session["numberOfGuesses"] += 1
            
        
        if(guessNum < session["number"]):
        
            guessOutcome = 2
            session["numberOfGuesses"] += 1
        
        if(guessNum == session["number"]):
        
            guessOutcome = 3
            # if the user guesses the correct number, 
            session["end"] = time.perf_counter()
            session["time_taken"] = round(session["end"] - session["start"], 2)
        


    #submission box 
    return render_template(
        "game.html", 
        guessOutcome = guessOutcome,
        theRando = session["number"] 
    )

    
    

@app.route("/recordscores", methods = ["POST"])
def record_score():

    player_name = request.form["playerName"]
    score = session["numberOfGuesses"]

    if not os.path.exists(FNAME): 
        data = []
    else:
        with open(FNAME, "rb") as pf: 
            data = pickle.load(pf)
    data.append((score, player_name, session["time_taken"]))
    with open(FNAME, "wb") as pf:
        pickle.dump(data, pf)

    return "Your score has been recorded! View at /highscores"


@app.route("/highscores")
def display_score():
    with open(FNAME, "rb") as pf:
        data = pickle.load(pf)
    return render_template(
        "highscores.html",
        the_title = "High scores:", 
        the_data=sorted(data, reverse= False),
    )




app.secret_key = (
    "omg my chemical romance are back together! :)"
)


app.run(debug = True)
