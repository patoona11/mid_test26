from supabase import create_client, Client
from flask import Flask, render_template, request, redirect, url_for, session
import os
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_quiz'

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://somnbanbnkhzfqyhmxnb.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_Tx6_X9LQu1TYR3oaPZ4YyQ_gJSPse7b")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_code = request.form['student_code'].strip()
        fullname = request.form['fullname'].strip()
        
        if not student_code or not fullname:
            return render_template('index.html', error="กรุณากรอกข้อมูลให้ครบถ้วน")
            
        # Check if student exists
        response = supabase.table('students').select('id, fullname').eq('student_code', int(student_code)).execute()
        student_data = response.data
        
        if len(student_data) > 0:
            student_id = student_data[0]['id']
            # Update name
            supabase.table('students').update({'fullname': fullname}).eq('id', student_id).execute()
        else:
            insert_response = supabase.table('students').insert({'student_code': int(student_code), 'fullname': fullname}).execute()
            student_id = insert_response.data[0]['id']
            
        session['student_id'] = student_id
        session['student_name'] = fullname
        return redirect(url_for('quiz'))
        
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'student_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Grade the quiz
        questions_resp = supabase.table('questions').select('id, correct_answer').execute()
        questions = questions_resp.data
        
        score = 0
        total = len(questions)
        
        for q in questions:
            q_id = str(q['id'])
            ans = request.form.get(f'question_{q_id}')
            if ans and ans == q['correct_answer']:
                score += 1
                
        # Save score
        student_id = session['student_id']
        supabase.table('scores').insert({
            'student_id': student_id,
            'score': score,
            'total_score': total
        }).execute()
        
        session['last_score'] = score
        session['last_total'] = total
        return redirect(url_for('result'))

    # Load quiz data for GET request
    cat_resp = supabase.table('categories').select('*').execute()
    categories = cat_resp.data
    
    quiz_data = []
    for cat in categories:
        cat_dict = dict(cat)
        q_resp = supabase.table('questions').select('*').eq('category_id', cat['id']).execute()
        questions_list = q_resp.data
        random.shuffle(questions_list)  # Shuffle questions within the category
        cat_dict['questions'] = questions_list
        quiz_data.append(cat_dict)
    
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
