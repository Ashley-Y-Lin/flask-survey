from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.get("/")
def start():
    """Renders survey start page"""
    session[RESPONSES_KEY] = []

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin():
    """Handle button to begin survey"""
    responses_length = len(session.get(RESPONSES_KEY))

    return redirect(f"/questions/{responses_length}")


@app.get("/questions/<int:prompt_num>")
def display_question(prompt_num):
    """Show a single question on the page"""
    responses_length = len(session.get(RESPONSES_KEY))

    if responses_length >= len(survey.questions):
        return redirect("/completion")

    if prompt_num != responses_length:
        flash("You were trying to access an invalid question!")

        return redirect(f"/questions/{responses_length}")

    question = survey.questions[prompt_num]

    return render_template("question.html", question=question)


@app.post("/answer")
def answer_question():
    """Receive answer and either redirect to next question, or the complete page
    if all questions have been answered"""

    answer = request.form.get("answer")

    responses = session.get(RESPONSES_KEY)
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    responses_length = len(session.get(RESPONSES_KEY))

    if responses_length >= len(survey.questions):
        return redirect("/completion")

    return redirect(f"/questions/{responses_length}")


@app.get("/completion")
def show_complete():
    """Show the complete page after user completes survey"""
    responses_length = len(session.get(RESPONSES_KEY))

    if responses_length < len(survey.questions):
        flash("You have more questions to answer!")

        return redirect(f"/questions/{responses_length}")

    return render_template(
        "completion.html", survey=survey, responses=session.get(RESPONSES_KEY)
    )
