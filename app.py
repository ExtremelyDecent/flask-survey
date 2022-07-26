from flask import Flask, request, render_template, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] =False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_home():
    """Initial homepage for surveys"""

    return render_template("survey_home.html", survey = survey)


@app.route("/begin", methods = ["POST"])
def begin_survey():
    """Starts a new survey with cleared responses"""
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """displays the current question"""
    responses = session.get(RESPONSES_KEY)
    if responses is None:
        """Cannot get responses from server"""
        return redirect("/")

    if (len(responses)== len(survey.questions) ):
        """Last question complete"""
        return redirect("/complete")

    if (len(responses)!= qid):
        """Question id is in the wrong order from response"""
        flash(f"Invalid question ID = {qid}.")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")