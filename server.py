from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        total_questions = int(request.form['num_questions'])
        session['total_questions'] = total_questions
        session['current_question'] = 1
        session['start_time'] = datetime.now().isoformat()
        session['times'] = [0] * total_questions  # Initialize times with zeros
        return redirect(url_for('question', question_number=1))

    return render_template('index.html')

@app.route('/question/<int:question_number>', methods=['GET', 'POST'])
def question(question_number):
    if 'total_questions' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form.get('action')
        end_time = datetime.now()
        start_time = datetime.fromisoformat(session['start_time'])
        time_spent = (end_time - start_time).total_seconds()
        time_spent_rounded = round(time_spent)
        current_question = session['current_question']

        session['times'][current_question - 1] += time_spent_rounded

        if action == 'next':
            session['current_question'] += 1
        elif action == 'prev':
            session['current_question'] -= 1
        elif action == 'done':
            return redirect(url_for('results'))

        if session['current_question'] < 1:
            session['current_question'] = 1
        elif session['current_question'] > session['total_questions']:
            session['current_question'] = session['total_questions']

        session['start_time'] = datetime.now().isoformat()
        return redirect(url_for('question', question_number=session['current_question']))

    session['current_question'] = question_number
    session['start_time'] = datetime.now().isoformat()
    return render_template('question.html', question_number=question_number)

@app.route('/results')
def results():
    if 'times' not in session:
        return redirect(url_for('index'))

    times = session['times']
    session.clear()
    return render_template('results.html', times=times)

if __name__ == '__main__':
    
    app.run(debug=True)
