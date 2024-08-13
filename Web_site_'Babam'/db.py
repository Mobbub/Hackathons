import re, json, sqlite3, mysql.connector, bcrypt

from pathlib import Path

from config import HOST, USER, PASSWORD, DATABASE

class MySQLConnection:
    def __init__(self):
        config = {
            'host': HOST,
            'user': USER,
            'password': PASSWORD,
            'database': DATABASE,
            'raise_on_warnings': True
        }
        self._cnx = mysql.connector.connect(**config)

    def __del__(self):
        if self._cnx.is_connected():
            self._cnx.close()


class EmployeesDatabase(MySQLConnection):
    def __init__(self):
        super().__init__()

    def register_employee(self, login: str, password: str) -> str:
        """Зарегистрировать работника"""
        if not self._user_exists(login):
            with self._cnx.cursor() as cursor:
                query = "INSERT INTO employees (login, password_hash) VALUES (%s, %s)"
                hashed_password = self._hash_password(password)
                cursor.execute(query, (login, hashed_password))
                self._cnx.commit()

            return json.dumps({'success': True})
        return json.dumps({'success': False})

    def _user_exists(self, username: str) -> bool:
        """Проверить, существует ли пользователь в базе данных."""
        with self._cnx.cursor() as cursor:
            query = "SELECT COUNT(*) FROM employees WHERE login = %s"
            cursor.execute(query, (username,))
            count = cursor.fetchone()[0]
        return count > 0

    def _get_user_password_hash(self, username: str) -> str:
        """Получить хэш пароля пользователя из базы данных."""
        with self._cnx.cursor() as cursor:
            query = "SELECT password_hash FROM employees WHERE login = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
        return result[0] if result else None

    def authenticate_user(self, username: str, password: str) -> bool:
        """Аутентификация пользователя."""
        if self._user_exists(username):
            stored_hash = self._get_user_password_hash(username)
            if stored_hash and self._check_password(stored_hash, password):
                return True
        return False

    @staticmethod
    def _hash_password(password: str) -> str:
        """Хэшировать пароль."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _check_password(stored_hash: str, password: str) -> bool:
        """Проверить пароль."""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


class ClientsDatabase(MySQLConnection):
    def __init__(self, table_name: str):
        super().__init__()
        self._table_name = table_name
        self._columns = []
        self._data_from_file = []

    @staticmethod
    def _extract_insert_statements(sql_dump_file: str) -> list:
        """Извлечь команды INSERT INTO из SQL дампа."""
        with open(sql_dump_file, 'r', encoding='utf-8') as file:
            sql_dump = file.read()

        insert_statements = re.findall(
            r"INSERT INTO `([^`]+)` VALUES\s*((?:\([^)]*\),?\s*)+);",
            sql_dump, re.DOTALL
        )

        return insert_statements

    def _get_column_names(self) -> list:
        """Получить имена столбцов из таблицы MySQL."""
        cursor = self._cnx.cursor()
        cursor.execute(f"SHOW COLUMNS FROM `{self._table_name}`")
        columns = [row[0] for row in cursor.fetchall()]
        return columns

    def _fetch_data_from_sqlite(self, db_file_path: str) -> list:
        """Извлечь данные из SQLite базы данных."""
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {self._table_name}")
        rows = cursor.fetchall()
        self._columns = [description[0] for description in cursor.description]
        conn.close()

        self._data_from_file = self._exclude_id_column(rows)

        return rows

    def _exclude_id_column(self, rows: list) -> list:
        """Исключить столбец 'id' из данных, если он есть."""
        if self._columns and self._columns[0] == 'id':
            self._columns.pop(0)  # Удаляем 'id' из списка столбцов
            return [row[1:] for row in rows]  # Удаляем первый элемент (id) из каждой строки
        return rows

    @staticmethod
    def _format_client_take_products(data_dict: dict) -> dict:
        """Преобразовать строку продуктов в объект с полями."""
        if 'client_take_products' in data_dict and data_dict['client_take_products']:
            products = data_dict['client_take_products'].split(';')
            data_dict['client_take_products'] = {i + 1: product.strip() for i, product in enumerate(products)}
        return data_dict

    def _process_data(self, data: list) -> dict:
        """Обработать данные и форматировать их для вывода."""
        formatted_data = dict()
        full_columns = self._columns.copy()
        full_columns.insert(0, "id")
        for i, row in enumerate(data, 1):
            data_dict = dict(zip(full_columns, row))
            data_dict = self._format_client_take_products(data_dict)
            formatted_data[i] = data_dict
        return formatted_data

    def _fetch_data_from_file(self, db_file_path: str) -> list:
        """Определить тип файла и извлечь данные"""
        db_file = Path(db_file_path)
        if not db_file.is_file():
            raise FileNotFoundError(f'Файл базы данных не найден {db_file_path}')

        if db_file_path.endswith('.db'):
            return self._fetch_data_from_sqlite(db_file_path).copy()
        elif db_file_path.endswith('.sql'):
            return self._process_sql_dump(db_file_path).copy()
        else:
            raise ValueError("Неподдерживаемый формат файла")

    def get_formatted_data(self, file: str) -> dict:
        self._data_from_file = self._fetch_data_from_file(file)
        formatted_data = self._process_data(self._data_from_file)
        return formatted_data

    @staticmethod
    def _parse_values(values: str) -> list:
        parsed_values = []
        # Используем регулярное выражение для извлечения строковых значений в скобках
        value_list = re.findall(r'\((.*?)\)', values)

        for value in value_list:
            # Замена экранированных апострофов на обычные
            value = value.replace(r"\'", "'")
            # Замена двойных кавычек на одиночные для обработки
            value = value.replace(r"\'", "'")
            # Используем регулярное выражение для разделения значений, заключенных в кавычки
            # или разделенных запятыми вне кавычек
            row = re.findall(r"'(.*?)'|([^,]+)", value)
            # Обработка значений
            row = [x[0] if x[0] else x[1] for x in row]
            parsed_values.append(tuple(v.strip().strip("'") for v in row))

        return parsed_values

    def _process_sql_dump(self, sql_dump_file: str) -> list:
        """Обработать SQL дамп и извлечь данные."""
        insert_statements = self._extract_insert_statements(sql_dump_file)
        if not insert_statements:
            raise ValueError("No INSERT INTO statements found in SQL dump")

        for table_name, values in insert_statements:
            if table_name == self._table_name:
                self._columns = self._get_column_names()

                # Обработка значений
                values = values.replace("),(", "),(")
                fetched_data = self._parse_values(values)
                self._data_from_file = self._data_from_file = self._exclude_id_column(fetched_data)

                return fetched_data

    def insert_data_in_mysql(self, file: str) -> None:
        """Вставить данные в таблицу MySQL."""
        data = self._fetch_data_from_file(file)
        self._data_from_file = [row[1:] for row in data]

        cursor = self._cnx.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{self._table_name}' AND TABLE_SCHEMA='expobank'")
        column_count = cursor.fetchone()[0] - 1

        if column_count != len(self._columns):
            raise ValueError("Количество столбцов в данных не соответствует количеству столбцов в таблице MySQL.")

        placeholders = ', '.join(['%s'] * len(self._columns))
        query = f"INSERT INTO `{self._table_name}` ({', '.join(self._columns)}) VALUES ({placeholders})"

        try:
            with self._cnx.cursor() as cursor:
                cursor.executemany(query, self._data_from_file)
                self._cnx.commit()
                print("Data inserted successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self._cnx.rollback()