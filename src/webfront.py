from flask import Blueprint, request, render_template, flash, redirect, url_for, session
import uuid
from .llm_request import request_llm


webstart = Blueprint('webstart', __name__)

@webstart.route('/', methods=['GET'])
def start_page():
    return render_template('start.html')

@webstart.route('/', methods=['POST'])
def start_page_post():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        vacancy_text = form_data['vacancy_info']
        cand_info = form_data['cand_info']
        if len(vacancy_text) < 30 or len(cand_info) < 30:
            flash('Введите данные вакансии и/или данные кандидата', 'error')
            return redirect(url_for('webstart.start_page'))
        session.permanent = True
        session['session_id'] = str(uuid.uuid4())
        session['vacancy_text'] = vacancy_text
        session['cand_info'] = cand_info
        return redirect(url_for('webstart.request_info'))


@webstart.route('/info', methods=['GET'])
def request_info():
    if request.method == 'GET':
        vacancy_text = session['vacancy_text']
        cand_info = session['cand_info']
        if not session.get('session_id'):
            return redirect(url_for('webstart.start_page'))
        llm_response = request_llm(vacancy_text, cand_info)
        if len(llm_response) < 30:
            flash('Ошибка подключения к серверу', 'error')
            return redirect(url_for('webstart.start_page'))
        return render_template('info.html', llm_response=llm_response)







