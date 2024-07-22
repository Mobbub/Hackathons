import csv, re, mysql.connector

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


class Compositor(DataBaseManager):
    # ------------------------------------Работа-с-товарами--------------------------------------------
    class ProductData:
        def __init__(self, article: str, name: str, price: float, amount: int):
            self.article = article
            self.name = name
            self.price = price
            self.amount = amount

        def __eq__(self, other):
            if not isinstance(other, Compositor.ProductData):
                return False
            return self.name == other.name

        def __hash__(self):
            return hash(self.name)

        def get_name_for_csv(self) -> str:
            """Возвращает имя с заменой запятых на точки."""
            return self.name.replace(',', '.')

    def __init__(self):
        super().__init__()
        self.box_modules_count = 0
        self.box_module_classes = [12, 24, 36, 48, 60]

    def process_response(self, ai_response_json: dict) -> dict:
        """Обработать приходящие JSON данные и составить по ним JSON ответ и CSV файл"""

        data_json = ai_response_json

        if data_json.get('status_inferens'):
            file_name = f"static/result/{data_json.get('name_file')}.csv"
            self._save_data_to_csv(data_json, file_name)
            
            return {
                'status': 200, 
                'path_result': f'{file_name}', 
                'message': 'Успешная обработка'
            }

        return {
                'status': 0, 
                'path_result': '', 
                'message': 'Ошибка обработки'
            }

    def _process_objects(self, objects: list) -> set:
        """Берёт список объектов и возвращает информацию о товаре по описанию объектов"""
        temp_products = dict()

        for obj in objects:
            name = obj[0]
            attributes = obj[1].split(';')

            fetched_data = self._fetch_data_from_db(name, attributes)
            product = self.ProductData(*fetched_data, amount=1)

            if product in temp_products:
                temp_products[product].amount += 1
            else:
                temp_products[product] = product

        return set(temp_products.values())

    def _fetch_data_from_db(self, name: str, attributes: list[str]) -> tuple:
        """
        Составляет запрос MySQL, чтобы найти товар по описанию объекта.
        Если возвращает больше одного товара, то проблема в описании объекта
        """
        def matches_any_class(item, classes):
            for cls in classes:
                if re.match(f"^{cls}", item):
                    return True
            return False

        object_classes = [
            "QF", "QFD", 'QS', "QFU", 'WH', 'TT', 'KM', 'AVR', 'FU', 'K', 'HL', 'PA', 'PV', 'QFD', 'QFU', 'FV', 'OPS',
            'ITU', 'S', 'AUX', 'M', 'R', 'QW', 'XS', 'MX', 'Q', 'PM', 'SB', 'FR', 'QD', 'U<', 'Timer'
        ]

        attributes = [attr for attr in attributes if attr]

        if attributes and matches_any_class(attributes[0], object_classes):
            del attributes[0]

        self._count_modules_for_box(attributes)

        default_query = f"SELECT Article, Name, Basic_cost_tax FROM parts WHERE circuit_value='{name}'"
        query = default_query

        default_attributes = list()
        unwanted_attributes = list()

        # match-case для определения элементов по умолчанию (или тех которые не нужны для сужения поиска)
        match name:
            case 'QF':
                if len(attributes) == 2:
                    default_attributes.append('C')
                    default_attributes.append('6kA')
                    unwanted_attributes.append('DC')

        if attributes:
            query = self._add_attributes_to_query(attributes, query)
        if default_attributes:
            query = self._add_attributes_to_query(default_attributes, query)
        if unwanted_attributes:
            query = self._add_attributes_to_query(unwanted_attributes, query, False)

        with self.cnx.cursor() as cursor:
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) != 0:
                    return result[0]
                cursor.execute(default_query)
                result = cursor.fetchall()
                return result[0]
            except mysql.connector.DataError as e:
                print(e)

    def _count_modules_for_box(self, attributes: list[str]) -> None:
        for attr in attributes:
            if 'p' in attr:
                attr = '1p' if attr == 'Ip' else attr
                self.box_modules_count += int(attr[0])

    def _choose_box(self) -> tuple:
        final_box_modules_count = next(item for item in self.box_module_classes if self.box_modules_count <= item)
        attributes = [f'{final_box_modules_count} модул']
        with self.cnx.cursor() as cursor:
            query = f"SELECT Article, Name, Basic_cost_tax FROM parts WHERE circuit_value=%s"
            query = self._add_attributes_to_query(attributes, query)
            cursor.execute(query, ('Шкаф',))
            result = cursor.fetchall()
            return result[0]

    @staticmethod
    def _add_attributes_to_query(attributes: list, current_query: str, is_wanted_attribute: bool = True):
        """Добавляет аттрибуты, создавая новую строку запроса"""
        part = str()
        if not is_wanted_attribute:
            part = 'NOT'
        for attribute in attributes:
            attribute = '1p' if attribute == 'Ip' else attribute
            current_query += f" AND Name {part} REGEXP '{attribute}'"

        return current_query

    def _save_data_to_csv(self, data_json: dict, file_name: str) -> None:
        products = list(self._process_objects(data_json['objects']))

        box_params = self._choose_box()

        if box_params:
            box_product = Compositor.ProductData(*box_params, amount=1)
            products.insert(0, box_product)
        field_names = ['Артикул', 'Номенклатура', 'Количество', 'Цена', 'Сумма']
        csv_data = list()

        for product in products:
            product_data_list = [
                product.article,
                product.get_name_for_csv(),
                product.amount,
                product.price,
                product.amount * product.price
            ]
            csv_data.append([str(element) for element in product_data_list])

        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
            csvwriter.writerow(field_names)
            csvwriter.writerows(csv_data)


class UserImageManager(DataBaseManager):
    # ------------------------------------Работа-с-пользователями--------------------------------------
    def __init__(self):
        super().__init__()

    def check_user_data(self, login: str, password_hash: str) -> bool:
        query = "SELECT * FROM users WHERE login=%s AND password_hash=%s"
        with self.cnx.cursor() as cursor:
            cursor.execute(query, (login, password_hash))
            result = cursor.fetchone()
            return result is not None

    def insert_image_name(self, login: str, image_name: str) -> None:
        query = "INSERT INTO loaded_images_names (author_login, image_name) VALUES (%s, %s)"
        with self.cnx.cursor() as cursor:
            cursor.execute(query, (login, image_name))
            self.cnx.commit()

    def get_user_image_names(self, login: str) -> list:
        query = "SELECT image_name FROM loaded_images_names WHERE author_login=%s"
        with self.cnx.cursor() as cursor:
            cursor.execute(query, (login,))
            result = cursor.fetchall()
            return [name[0] for name in result]


# ------------------------------------Тестирование-кода------------------------------------------------
if __name__ == '__main__':
    compositor = Compositor()
    data_request = {
        'status_inferens': True,
        'objects': [
            ['QFD', '2F9;/30;16 4'],
            ['QFD', 'F6;30'],
            ['QFD', '2F8;УЗО'],
            ['QFD', 'XI +;/30;1'],
            ['QFD', 'YrJ;/30;6 A'],
            ['QF', 'QF11;6 4'],
            ['QF', 'QF2;6 A'],
            ['QF', 'QF16;16 A'],
            ['QF', 'QF11;40 4'],
            ['QF', 'QF18;6 4'],
            ['QS', '1WI;Iн=100 A'],
            ['QF', 'QF1;6 4'],
            ['QF', 'QF1З;16 4'],
            ['QF', 'QF17;6 A'],
            ['QF', 'QFЗ;6 4'],
            ['QF', '2F9;/30;16 4'],
            ['Шкаф', 'QF1;6 4'],
            ['QF', 'QF15;6 4'],
            ['QF', 'ы;20 4'],
            ['QF', 'QF1З;16 4'],
            ['Шкаф', 'QF1;6 4'],
            ['QF', 'QF1;6 4']
        ],
        'name_file': 'Схема-6_дVFтNЙХJйHРмЛИRшeT9N'
    }
    response = compositor.process_response(data_request)