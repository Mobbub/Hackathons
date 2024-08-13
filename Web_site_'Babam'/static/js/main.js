


// Получаем ссылку на поле выбора файла
const fileInput = document.getElementById('input__file');

// Создание нового элемента div для отображения в нём сообщения с сервера
var mes_cuc = document.createElement('div');
mes_cuc.className += ' flex cuc-regi messeg';

var mes_eror = document.createElement('div');
mes_eror.className += ' flex errors messeg';

// Получаем ссылку на div с формой
var mainWrapper = document.querySelector(".upload-wrapper");

// Получаем ссылку на секцию
const main = document.querySelector(".section-upload");

// Получаем ссылку на общий div
const container = document.querySelector(".section-upload_container");

// Счётчик обюработанных файлов
var scors = 0;

// Добавляем обработчик события 'change' на поле ввода файла
fileInput.addEventListener('change', (event) => {

    // Готовим файл к отправки на сервер
    const formData = new FormData();
    const files = document.getElementById("input__file");
    formData.append("file", files.files[0]);

    // Создание div с отображением "загрузки"
    var loadBar = create('<div class="flex loadBar"><img class="loadBar_img" src="../static/pictures/load.gif" alt="Загрузка"><p class="loadBar_text">Обработка запроса...</p></div>');
    var nameFile = files.files[0]['name']
    // Удаляет div с формой 
    document.querySelector(".upload-wrapper").remove();

    // Установка "загрузки" на место формы
    container.prepend(loadBar);

    // Создание параметров запроса
    const requestOptions = {

        mode: "no-cors",
        method: "POST",
        files: files.files[0],
        body: formData,
    };

    // Отправление первого пост запроса на сервер для сохранение файла
    fetch("/up_db", requestOptions)
        .then((response) => response.json())
        .then((response) => {

            // Проверка что ответ корректный, иначе вывод сообщение об ошибке и выход из addEventListener
            if (response['status_result'] != 200) {

                // Вставка полученого от сервера сообщения в созданный div
                mes_eror.innerHTML = "Ошибка загрузки файла";

                // Вставка div в начало main
                main.prepend(mes_eror);

                // Удаление "загрузки"
                document.querySelector(".loadBar").remove();

                // Вставка div для загрузки пользовательского изображения и обнуление его значения
                container.prepend(mainWrapper);
                document.getElementById("input__file").value = '';

                return;
            }

            document.querySelector(".loadBar").remove();

            // Вставка div для загрузки пользовательского изображения и обнуление его значения
            container.prepend(mainWrapper);
            document.getElementById("input__file").value = '';

            var sectionResult = document.querySelector(".section-result");

            // Создание контейнера для результатов обработки и вставление его в низ секции
            var container_result = create('<div class="container-' + scors + ' ' + nameFile + '"><div class="section-result__answer section-result-' + scors + '"><h2 class="result-title">Анализ по '
                + nameFile + '</h2><div class="answer-first"><p class="buy-service-1">Пользователй в базе данных: ' +
                response['stat']['num_users'] + '</p><p class="buy-service-2">Самый популярный продукт: '
                + response['stat']['popular_product']['name'] + ' Купленно: ' +
                response['stat']['popular_product']['num_sales'] + ' Процент выкупа: ' +
                response['stat']['popular_product']['percentage_take_product'] +
                '%</p></div><h3>Топ продуктов</h3><div class="answer-first top-product"></div><h3>Пользователи</h3><div class="answer-first users"></div><div class="answer-second"><div class="answer-second__id"><h3>Найти по ID</h3><form action="" class="name-form-' + scors + ' name-form"><input type="text" placeholder="ID" name="id"><button type="submit" class="name-button">Найти</button></form></div></div></div></div>');
            // var container_result_topProduct = create('<div class="answer-third"><h3>Пользователь</h3></div>');
            // var container_result_users = create('<div class="answer-third"><h3>Пользователь</h3></div>');

            var product = response['stat']['top_10_product'];
            var users = response['users'];
            container_result = addTopProduct(container_result, product);
            container_result = addUsers(1, 10, container_result, users);
            sectionResult.append(container_result);

            scors++;
        }
        );

});


$('body').delegate('.name-form', 'submit', function (event) {

    console.log(event.currentTarget.className);
    // Запрет на обновление страницы
    event.preventDefault();

    var str = event.currentTarget.className.split(' ', 1)
    var str2 = "." + str[0] + "";
    // Подготовка запроса для отправки на сервер
    request = $(str2).serializeArray();
    console.log(request);

    var data = {};
    data[request[0].name] = request[0].value;
    data['index_action'] = 1;

    // Отправка пост запроса на сервер
    fetch('/stat_user', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((response) => response.json())
        .then((data) => {

            if (data['status_result'] == 200) {
                var container_user_result = create('<div class="answer-third"><h3>Пользователь ' + data['FIO'] + '</h3></div>');

                var arr = data['products']
                for (var i = 0; i < arr.length; i++) {

                    container_user_result.append(create('<p class="top-user-product-' + i + '">' + i + ': ' + arr[i] + '</p>'));
                }
                document.querySelector(".section-result-" + str2.slice(-1)).append(container_user_result);
            } else {
                // Вставка полученого от сервера сообщения в созданный div
                mes_eror.innerHTML = "Ошибка поиска пользователя";

                // Вставка div в начало main
                main.prepend(mes_eror);
            }
        });
});




// Функция для добавления продуктов
function addTopProduct(html, product) {
    var productClass = html.querySelector(".top-product");
    for (var i = 1; i <= 10; i++) {
        if ((product[i] + '1') != '1') {
            productClass.append(create('<p class="top-buy-product-' + i + '">' + i + ': ' + product[i] + '</p>'));
        }
    }
    return html;
}

// Функция для добавления пользователей
function addUsers(inc1, inc2, html, users) {

    var usersClass = html.querySelector(".users");
    for (var i = inc1; i <= inc2; i++) {
        if (users[i] != undefined) {
            var usr = users[i]['FIO'];
            var id = users[i]['id'];
            console.log(usersClass);
            usersClass.append(create('<p class="users-' + i + '">' + i + ': ' + usr + ' ID: ' + id + '</p>'));
        } else {
            return html;
        }
    }

    if ((Object.keys(users).length > 10)) {
        usersClass.append(create('<button class="user-add-btn-' + scors + '">Больше пользователей...</button>'));
        html.querySelector('.user-add-btn-' + scors).addEventListener('click', (event) => {

            document.querySelector('.' + event.currentTarget.className).remove();

            var size = Object.keys(document.querySelector(".users")).length;
            console.log(scors - 1);
            var sc = scors - 1;
            addUsers(i, (inc2 + 10), document.querySelector('.container-' + sc), users);
        });
    }

    return html;
}

// Функция для создания html объекта из строки
function create(htmlStr) {
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    temp.innerHTML = htmlStr;
    while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
    }
    return frag;
}


// Слушатель кнопки для скачивания файла
$('body').delegate('.download', 'click', function (e) {
    var id = e.currentTarget.getAttribute('id');
    var link = document.createElement('a');
    link.setAttribute('href', 'static/result/' + id);
    link.setAttribute('download', id);
    link.click();
    return false;
});

//Слушатель для кнопки выхода
$('body').delegate('.exit', 'click', function (e) {

    // Создание нового элемента div для отображения в нём сообщения с сервера
    var mes_cuc = document.createElement('div');
    mes_cuc.className += ' flex cuc-regi messeg';


    request = {};
    request['index_action'] = -1;
    console.log(request);

    fetch("/exit", {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);

            // Если сообщение уже есть, удалить текущее
            if (document.querySelector(".messeg") != null) {
                document.querySelector(".messeg").remove();
            }

            // Выделение элемента main, для последующей вставки в его начало сообщений
            const main = document.querySelector(".section-upload");

            if (data['status_result'] == 200) {

                // Вставка полученого от сервера сообщения в созданный div
                mes_cuc.innerHTML = data['message'];



                // Вставка div в начало main
                main.before(mes_cuc);
                console.log("LLLFFF");
                window.setTimeout(function () { window.location = "/authorization"; }, 1000);

            } else {

                // Вставка полученого от сервера сообщения в созданный div
                mes_cuc.innerHTML = data['message'];

                // Вставка div в начало main
                main.before(mes_cuc);
            }



        });
});

// Функция для заполнения таблицы
function createTable(url, table) {

    fetch(url)
        .then(response => response.text())
        .then(data => {
            let rows = data.split("\n");
            for (let i = 0; i < rows.length; i++) {
                let cells = rows[i].split(",");
                let row = table.insertRow();
                for (let j = 0; j < cells.length; j++) {
                    let cell = row.insertCell();
                    cell.innerText = cells[j];
                }
            }
        })
        .catch(error => console.log(error));
}




