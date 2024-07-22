from flask import Flask, request, render_template, jsonify, redirect, session, url_for
from pdf2image import convert_from_path
 
import os, uuid, datetime, mysql.connector, random

import model
import compilation

app = Flask(__name__)

# Путь сохрания файлов
UPLOAD_FOLDER = 'static/image_analysis/first_image'

# Настройки конфига сайта
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = str(uuid.uuid4())
app.permanent_session_lifetime = datetime.timedelta(days=31)

# Класс подключения к бд
class DataBaseManager:
    def __init__(self):
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'PASSWORD',
            'database': 'electric',
            'raise_on_warnings': True
        }

        self.cnx = mysql.connector.connect(**config)

# Класс работы с бд
class UserImageManager(DataBaseManager):
    def __init__(self):
        super().__init__()
        
    def check_user_data(self, login: str, password_hash: str) -> None:
        query = "SELECT * FROM users WHERE login=%s AND password_hash=%s"
        with self.cnx.cursor() as cursor:
            cursor.execute(query, (login, password_hash))
            result = cursor.fetchone()
            return result is not None

    def get_user_image_names(self, login: str) -> list:
        query = "SELECT image_name FROM loaded_images_names WHERE author_login=%s"
        with self.cnx.cursor() as cursor:
            cursor.execute(query, (login,))
            result = cursor.fetchall()
            return [name[0] for name in result]
    
    def insert_image_name(self, login: str, image_name: str) -> None:
        query = "INSERT INTO loaded_images_names (author_login, image_name) VALUES (%s, %s)"
        with self.cnx.cursor() as cursor:
            cursor.execute(query, (login, image_name))
            self.cnx.commit()
    
# Класс работы с input данными
class Working_files():
    def __init__(self) -> None:
        self.list_type = ['png', 'jpeg', 'jpg', 'pdf']
        
    def main(self, index_action, image_name, image_format):
        if index_action == 0:
            return model.improve_image(image_name, image_format)
        elif index_action == 1:
            return model.inferens_yolo_img(image_name, image_format)
        elif index_action == 2:
            comp = compilation.Compositor()
            return comp.process_response(model.inferens(image_name, image_format))
        else:
            return {
                'status': 0,
                'message': 'Не верный индекс'
            }
    
    def names_files_folder(self):
        folder_path = "static/image_analysis/first_image"

        file_list = []

        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                file_list.append(filename)
        return file_list
        
    def check_file(self, file_name, file_type):
        if file_name == '':
            return {
                'status': 1,
                'message': 'Нет файла'
            }

        if file_type not in self.list_type:
            return {
                'status': 2,
                'message': 'Ошибка формата'
            }
            
        return {'status': 200}
    
# Мэин роут с главной страницей работы
@app.route('/')
@app.route('/main')
def main():
    if 'Login' not in session or not session['Login']:
        return redirect(url_for("authorization"))
    return render_template('index.html')

# Роут авторизации
@app.route('/authorization')
def authorization():
    session.permanent = True
    if 'Login' not in session:
        session['Login'] = ''
        session['Password'] = ''
        session.modified = True
    return render_template('authorization.html')

# Роут принимающий пост запросы для авторизации
@app.route('/log', methods=['POST'])
def log():
    if 'Login' not in session:
        return redirect(url_for("authorization"))
    db = UserImageManager()
    if request.method == 'POST':
        login = request.json['login']
        password = request.json['password']
        if db.check_user_data(login, password):
            session.permanent = True
            session['Login'] = login
            session['Password'] = password
            session['History'] = db.get_user_image_names(login)
            session.modified = True
            return jsonify({'status': 200})
        return jsonify({'status': 0})
    
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
            'status': 200,
            'message': 'Успешный выход'
        })
        
    return jsonify({
        'status': 0,
        'message': 'Произошла ошибка'
    })
    
# Роут для загрузки изображения
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({
            'status': 0,
            'message': 'Ошибка запроса'
        })
    
    file = request.files['file']
    
    main = Working_files()
    db = UserImageManager()
    
    num_name = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZйцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ', k=20))
    
    file_format = (file.content_type).split("/")[1]
    
    if main.check_file(file.filename, file_format)['status'] != 200:
        return jsonify(main.check_file(file.filename, file_format))
    
    if file_format == 'pdf':
        file_name = ((file.filename).split(".")[0])+'.png'
        if file_name in main.names_files_folder() or file.filename in main.names_files_folder():
            name, ext = (file.filename).split('.')
            new_file = f"{name}_{num_name}.{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, new_file))
            pages = convert_from_path(f'static/image_analysis/first_image/{new_file}', poppler_path='help/bin')
            for page in pages:
                page.save(f'static/image_analysis/first_image/{name}_{num_name}.png', 'PNG')
            os.remove(f'static/image_analysis/first_image/{new_file}')
            db.insert_image_name(session['Login'], f'{name}_{num_name}.png')
            session['History'].append(f'{name}_{num_name}.png')
            session.modified = True
        else:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            pages = convert_from_path(f'static/image_analysis/first_image/{file.filename}', poppler_path='help/bin')
            for page in pages:
                page.save(f'static/image_analysis/first_image/{file_name}', 'PNG')
            os.remove(f'static/image_analysis/first_image/{file.filename}')
            db.insert_image_name(session['Login'], file_name)
            session['History'].append(file_name)
            session.modified = True
    else:
        if file.filename in main.names_files_folder():
            name, ext = (file.filename).split('.')
            new_file = f"{name}_{num_name}.{ext}"
            db.insert_image_name(session['Login'], new_file)
            session['History'].append(str(new_file))
            session.modified = True
            file.save(os.path.join(UPLOAD_FOLDER, new_file))
        else:
            db.insert_image_name(session['Login'], str(file.filename))
            session['History'].append(str(file.filename))
            session.modified = True
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    
    return jsonify({
        'status': 200,
        'message': 'Успешная загрузка'
    })

# Роут для работы нейронки и вывода ком. предложения
@app.route('/heandler_post', methods=['POST'])
def heandler_post():
    ml = Working_files()
    
    data = request.get_json()
    
    file_name = (session['History'][-1]).split(".")[0]
    file_format = (session['History'][-1]).split(".")[1]
    
    return jsonify(ml.main(data.get('index_action'), file_name, file_format))

if __name__ == '__main__':
    app.run(debug=True)