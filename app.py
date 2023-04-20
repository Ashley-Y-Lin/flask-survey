from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def start():
    """renders survey start page"""

    return render_template('survey_start.html')

@app.post('/begin')
def begin():
    """handle button to begin survey"""

    return redirect('/questions/0')

@app.get('/questions/<prompt_num>')
def questions(prompt_num):

    question = survey.questions[int(prompt_num)]

    return render_template('question.html', question = question)

#@app.post('/answer')
