from flask import Flask, render_template, request, flash, redirect, session

from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

resp_key = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "123-456-789"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
    def show_start():
    """Displays start page."""

    return render_template("start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clears responses for current session and begins survey."""

    session[resp_key] = []

    return redirect("/questions/0")


@app.route('answer', method = ['POST'])
    def handle_question():
        '''Handles response, posts in '/answers', redirects to next qestion'''

        answer = request.form('answer')

        responses = session[resp_key]
        responses.append(answer)
        session[resp_key] = responses

        return redirect(f'/questions/{len(responses)}')


@app.route("/questions/<int:question_id>")
def show_question(question_id):
    '''Displays proper question'''
    responses = session.get(resp_key)

    if (responses is None):
        return redirect('/')

    if (len(responses) == len(survey.questions)):
        return redirect('/thankyou')

    if (len(responses) != question_id):
        flash(f'Invalid question id: {question_id}.')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[question_id]
    return render_template('question.html', question_num=question_id, question=question)

@app.route('/thankyou')
def thankyou():
    '''Completion page at the end of survey'''

    return render_template('/thankyou.html')
