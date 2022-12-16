from flask import Flask,flash,request,render_template,redirect,session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.wrappers import response
from surveys import satisfaction_survey as survey

#this is the key name that will remain constant so you dont have to 
#worry about the spelling
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config["SECRET_KEY"] = "random12345"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"]=False

debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """allowing the user to select a survey"""
    #set the survey var to equal survey , then can use this to get methods
    #will use inheritance
    return render_template("start_page.html" , survey=survey)





@app.route("/start", methods=["POST"])
def start_survey():
    """this clears the session response every time user reaches page"""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")





@app.route("/answer",methods=["POST"])
def handle_question():
    """this will save each response in the session the redirect to the next question"""


    #need to get the response from the query in the URL
    choice = request.form["answer"]

    #when you get the response , add it to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(survey.questions)):
        #this checks if all questions are ansrewed and redirects to complete page 
        return redirect("/complete")
    else:
        #if all not answered , redirects to cureent question
        return redirect(f"/questions/{len(responses)}")







@app.route("/questions/<int:qid>")
def current_question(qid):
    """this will display current question according to its id"""
    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        #if there is no set response , user is tryint to access question page to early , redirect back to home
        return redirect("/")
    if (len(responses) == len(survey.questions)):
        #again checks if all questions answered
        return redirect("/complete")
    if (len(responses) != qid):
        #checks to see if trying to access questions out of order, redirects back to correct order
        flash(f"please answer question {qid} before moving on")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html" ,question_num = qid, question =question)
    


@app.route("/complete")
def complete():
    """Survey complete. thank the user."""

    return render_template("completion.html")