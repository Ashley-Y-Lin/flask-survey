from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get("/")
def start():
    """Renders survey start page"""

    return render_template("survey_start.html")


@app.post("/begin")
def begin():
    """Handle button to begin survey"""

    return redirect("/questions/0")


# you can turn it into an int in the file path!
@app.get("/questions/<int:prompt_num>")
def questions(prompt_num):
    """Show a single question on the page"""

    question = survey.questions[prompt_num]

    return render_template("question.html", question=question, prompt_num=prompt_num)


@app.post("/answer")
def answer():
    """Receive answer and either redirect to next question, or the complete page
    if all questions have been answered"""

    answer = request.form.get("answer")

    next_question = int(request.form.get("prompt_num")) + 1

    responses.append(answer)

    if next_question >= len(survey.questions):
        return redirect("/completion")

    return redirect(f"/questions/{next_question}")


@app.get("/completion")
def show_complete():
    """Show the complete page after user completes survey"""

    responses_length = len(responses)

    return render_template(
        "completion.html", survey=survey, responses=responses, length=responses_length
    )
