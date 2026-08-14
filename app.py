import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, session
import os
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_quiz'

DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:midtest%402026@db.somnbanbnkhzfqyhmxnb.supabase.co:5432/postgres")

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_code = request.form['student_code'].strip()
        fullname = request.form['fullname'].strip()
        
        if not student_code or not fullname:
            return render_template('index.html', error="กรุณากรอกข้อมูลให้ครบถ้วน")
            
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Check if student exists, else insert
        cursor.execute('SELECT id FROM students WHERE student_code = %s', (student_code,))
        student = cursor.fetchone()
        
        if student:
            student_id = student['id']
            # Update name just in case it changed
            cursor.execute('UPDATE students SET fullname = %s WHERE id = %s', (fullname, student_id))
        else:
            cursor.execute('INSERT INTO students (student_code, fullname) VALUES (%s, %s) RETURNING id', (student_code, fullname))
            student_id = cursor.fetchone()['id']
            
        conn.commit()
        conn.close()
        
        session['student_id'] = student_id
        session['student_name'] = fullname
        return redirect(url_for('quiz'))
        
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'student_id' not in session:
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if request.method == 'POST':
        # Grade the quiz
        cursor.execute('SELECT id, correct_answer FROM questions')
        questions = cursor.fetchall()
        
        score = 0
        total = len(questions)
        
        for q in questions:
            q_id = str(q['id'])
            ans = request.form.get(f'question_{q_id}')
            if ans and ans == q['correct_answer']:
                score += 1
                
        # Save score
        student_id = session['student_id']
        cursor.execute('INSERT INTO scores (student_id, score, total_score) VALUES (%s, %s, %s)', (student_id, score, total))
        conn.commit()
        conn.close()
        
        session['last_score'] = score
        session['last_total'] = total
        return redirect(url_for('result'))

    # Load quiz data for GET request
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    
    quiz_data = []
    for cat in categories:
        cat_dict = dict(cat)
        cursor.execute('SELECT * FROM questions WHERE category_id = %s', (cat['id'],))
        questions_list = [dict(q) for q in cursor.fetchall()]
        random.shuffle(questions_list)  # Shuffle questions within the category
        cat_dict['questions'] = questions_list
        quiz_data.append(cat_dict)
        
    conn.close()
    
    return render_template('quiz.html', quiz_data=quiz_data, student_name=session['student_name'])

@app.route('/result')
def result():
    if 'last_score' not in session:
        return redirect(url_for('index'))
        
    score = session['last_score']
    total = session['last_total']
    
    return render_template('result.html', score=score, total=total, student_name=session['student_name'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
