from flask import Flask, request, render_template, jsonify, redirect, session, url_for
from werkzeug.utils import secure_filename

import os, uuid, datetime, random

import db
import bus_logic

# Путь сохрания бд
UPLOAD_FOLDER = 'static/db'
# Расширения бд, которые разрешено загружать
ALLOWED_EXTENSIONS = {'db', 'json', 'csv', 'sql'}

app = Flask(__name__)

# Настройки конфига сайта
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = str(uuid.uuid4())
app.permanent_session_lifetime = datetime.timedelta(days=31)

# Мэин роут с главной страницей работы
@app.route('/')
@app.route('/main')
def main():
    if 'Login' not in session or not session['Login']:
        return redirect(url_for("authorization"))
    return render_template('admin.html')

# Роут авторизации
@app.route('/authorization')
def authorization():
    session.permanent = True
    if 'Login' not in session:
        session['Login'] = ''
        session['Password'] = ''
        session['DB'] = list()
        session.modified = True
    return render_template('index.html')

# Роут для пост запроса от фронта для авторизации, идёт проверка в бд
@app.route('/log', methods=['POST'])
def log():
    if 'Login' not in session:
        return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})
    
    if request.method == 'POST':
        login = request.json['login']
        password = request.json['password']
        ed = db.EmployeesDatabase()
        if ed.authenticate_user(login, password):
            session.permanent = True
            session['Login'] = login
            session['Password'] = password
            session.modified = True
            return jsonify({'status_result': 200, 'message': 'Успешная авторизация'})
        return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})
    
# Роут для выхода с аккаунта, очищается сессия
@app.route('/exit', methods=['POST'])
def exit():
    index_action = request.json['index_action']
    
    if index_action == -1:
        session.permanent = True
        session['Login'] = ''
        session['Password'] = ''
        session.modified = True
        return jsonify({
            'status_result': 200,
            'message': 'Успешный выход'
        })
    return jsonify({
        'status_result': 0,
        'message': 'Произошла ошибка'
    })
    
# Функция проверки расширения файла
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
# Функция проверки всех бд на сервере для создания нового имени для бд
def names_files_folder():
    folder_path = "static/db"

    file_list = []

    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_list.append(filename)
    return file_list

# Роут загрузки бд на сервер и возвращения ответа в json с общей статистикой и информацией о всех пользователях
@app.route('/up_db', methods=['POST'])
def up_db():
    if 'Login' not in session:
        return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})
    
    if 'file' not in request.files:
        return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})
    
    if file:
        if allowed_file(file.filename) == False:
            return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})
        else:    
            if file.filename in names_files_folder():
                num_name = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZйцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ', k=20))
                name, ext = (file.filename).split('.')
                new_file = f"{name}_{num_name}.{ext}"
                session['DB'].append(str(new_file))
                session.modified = True
                file.save(os.path.join(UPLOAD_FOLDER, new_file))
            else:
                session['DB'].append(str(file.filename))
                session.modified = True
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            
            path_db = f'static/db/{session["DB"][-1]}'
            cd = db.ClientsDatabase('hackaton_client_data')
            
            cd.insert_data_in_mysql(path_db)
            
            return bus_logic.general_Statistics(cd.get_formatted_data(path_db))
    else:
        return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})

# Роут для вычисления услуги или продукта, который может пригодиться клиенту в дальнейшем
@app.route('/stat_user', methods = ['POST'])
def stat_user():
    if 'Login' not in session:
        return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})
    
    if request.json['index_action'] == 1:
        return jsonify({'status_result': 200, 'FIO': 'Лебедев Максим Владимирович', 'products': ['Автомобиль', 'Автокредит', 'Телевизор']}) # bus_logic.user_Statistics() ###
    return jsonify({'status_result': 0, 'message': 'Произошла ошибка'})

if __name__ == '__main__':
    app.run()