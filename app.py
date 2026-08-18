from supabase import create_client, Client
from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_quiz'

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://somnbanbnkhzfqyhmxnb.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_Tx6_X9LQu1TYR3oaPZ4YyQ_gJSPse7b")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def hub():
    return render_template('hub.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    subject_id = request.args.get('subject', '1')
    
    if subject_id == '1':
        subject_name = "การประยุกต์ใช้เทคโนโลยีดิจิทัลในอาชีพ"
    else:
        subject_name = "การใช้เทคโนโลยีดิจิทัลเพื่ออาชีพ"
        
    if request.method == 'POST':
        student_code = request.form['student_code'].strip()
        fullname = request.form['fullname'].strip()
        
        if len(student_code) != 3 or not student_code.isdigit():
            return render_template('index.html', error="รหัสนักศึกษาต้องเป็นตัวเลข 3 หลักสุดท้ายเท่านั้น", subject_name=subject_name, subject_id=subject_id)
            
        if not fullname:
            return render_template('index.html', error="กรุณากรอกชื่อ-นามสกุลให้ครบถ้วน", subject_name=subject_name, subject_id=subject_id)
            
        # Append subject to fullname to separate them in DB
        db_fullname = f"{fullname} [{subject_name}]"
        
        # Check if student exists
        response = supabase.table('students').select('id, fullname').eq('student_code', int(student_code)).eq('fullname', db_fullname).execute()
        student_data = response.data
        
        if len(student_data) > 0:
            student_id = student_data[0]['id']
            
            # Check if this student already took the exam
            score_resp = supabase.table('scores').select('id').eq('student_id', student_id).execute()
            if len(score_resp.data) > 0:
                return render_template('index.html', error="คุณได้ส่งข้อสอบไปแล้ว ไม่สามารถทำซ้ำได้ (สอบได้เพียงครั้งเดียว)", subject_name=subject_name, subject_id=subject_id)
                
            # Update name (just in case)
            supabase.table('students').update({'fullname': db_fullname}).eq('id', student_id).execute()
        else:
            insert_response = supabase.table('students').insert({'student_code': int(student_code), 'fullname': db_fullname}).execute()
            student_id = insert_response.data[0]['id']
            
        session['student_id'] = student_id
        session['student_name'] = db_fullname
        session['start_time'] = datetime.now().isoformat()
        return redirect(url_for('quiz'))
        
    return render_template('index.html', subject_name=subject_name, subject_id=subject_id)

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
                
        start_time_str = session.get('start_time')
        time_taken_str = "ไม่ทราบเวลา"
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.now()
            diff = end_time - start_time
            minutes, seconds = divmod(diff.seconds, 60)
            time_taken_str = f"{minutes} นาที {seconds} วินาที"
                
        # Save score
        student_id = session['student_id']
        supabase.table('scores').insert({
            'student_id': student_id,
            'score': score,
            'total_score': total,
            # We add time_taken if the DB column was created, but for backward compatibility in case it failed, 
            # we will not save time_taken to DB right now to prevent 500 error, just pass to session.
        }).execute()
        
        session['last_score'] = score
        session['last_total'] = total
        session['time_taken'] = time_taken_str
        return redirect(url_for('result'))

    # Load quiz data for GET request
    response = supabase.table('categories').select('*, questions(*)').execute()
    categories = response.data
    
    all_questions = []
    for cat in categories:
        for q in cat['questions']:
            q['category_name'] = cat['name']
            all_questions.append(q)
        
    random.shuffle(all_questions)
    
    return render_template('quiz.html', all_questions=all_questions, student_name=session['student_name'])

@app.route('/result')
def result():
    if 'last_score' not in session:
        return redirect(url_for('index'))
        
    score = session['last_score']
    total = session['last_total']
    time_taken = session.get('time_taken', 'ไม่ทราบเวลา')
    
    return render_template('result.html', score=score, total=total, student_name=session['student_name'], time_taken=time_taken)

@app.route('/admin')
def admin():
    # Fetch all scores with student details from Supabase
    response = supabase.table('scores').select('id, score, total_score, timestamp, students(student_code, fullname)').order('timestamp', desc=True).execute()
    return render_template('admin.html', scores=response.data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
