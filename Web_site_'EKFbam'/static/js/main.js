// Получаем ссылку на поле выбора файла
const fileInput = document.getElementById('input__file');

// Создание нового элемента div для отображения в нём сообщения с сервера
var mes_cuc =  document.createElement('div');
mes_cuc.className += ' flex cuc-regi messeg';

var mes_eror =  document.createElement('div');
mes_eror.className += ' flex errors messeg';

// Получаем ссылку на div с формой
var mainWrapper = document.querySelector(".main-wrapper");

// Получаем ссылку на секцию
const main = document.querySelector(".main-section");

// Получаем ссылку на общий div
const container = document.querySelector(".main-section_container");

// Счётчик обюработанных файлов
var scors = 0;

// Добавляем обработчик события 'change' на поле ввода файла
fileInput.addEventListener('change', (event) => {

    // Готовим файл к отправки на сервер
    const formData = new FormData();
    const files = document.getElementById("input__file");
    formData.append("file", files.files[0]);
    
    // Создание div с отображением "загрузки"
    var loadBar = create('<div class="flex loadBar"><img class="loadBar_img" src="../static/pictures/load.gif" alt="Загрузка"><p class="loadBar_text comfortaa">Обработка запроса...</p></div>');
    
    // Удаляет div с формой 
    document.querySelector(".main-wrapper").remove(); 

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
    fetch("/upload", requestOptions)
        .then((response) => response.json())
        .then((response) => {
            
            // Проверка что ответ корректный, иначе вывод сообщение об ошибке и выход из addEventListener
            if(response['status'] != 200) {

                // Вставка полученого от сервера сообщения в созданный div
                mes_eror.innerHTML = response['message'];
        
                // Вставка div в начало main
                main.prepend(mes_eror);
        
                // Удаление "загрузки"
                document.querySelector(".loadBar").remove();
        
                // Вставка div для загрузки пользовательского изображения и обнуление его значения
                container.prepend(mainWrapper);
                document.getElementById("input__file").value = '';
        
                return;
            }
        
            // Создание контейнера для результатов обработки и вставление его в низ секции
            var container_result = create('<div class="container-result" id="container-result-' + scors + '"></div>');
            main.append(container_result);
        
            // Получение ссылки на контейнер для отображение результатов
            var container_result = document.getElementById("container-result-" + scors);
            
            // Подготовка второго запроса
            request = {};
            request['index_action'] = 0;

            // Отправка второго пост запроса для получения ссылки на улучшеное изображение
            fetch("/heandler_post", {
                    method: 'POST',
                    // body: new FormData(form)
                    body: JSON.stringify(request),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then((response) => response.json())
                    .then((data) => {

                        // Проверка что ответ корректный, иначе вывод сообщение об ошибке и выход из addEventListener
                        if(response['status'] != 200) {

                            // Вставка полученого от сервера сообщения в созданный div
                            mes_eror.innerHTML = response['message'];
                    
                            // Вставка div в начало main
                            main.prepend(mes_eror);
                    
                            // Удаление "загрузки"
                            document.querySelector(".loadBar").remove();
                    
                            // Вставка div для загрузки пользовательского изображения и обнуление его значения
                            container.prepend(mainWrapper);
                            document.getElementById("input__file").value = '';
                    
                            return;
                        }
                        
                        var container_img = create('<div class="container-img" id="container-img-' + scors + '"></div>');
                        container_result.append(container_img);
                        var container_img = document.getElementById("container-img-" + scors);

                        // Создание html объекта для отображения улучшенной картинки 
                        // и вставка его в низ блока для отбражения результата
                        var result_img1 = create('<div class="container_img__item"><img class="container-result_img1" id="container-result-' + scors + '_img1" src="' + data['path_result'] + '" alt="result_img1"><p class="container__par comfortaa">Улучшенное изображение</p></div>');
                        container_img.append(result_img1);

                        // Подготовка третьего запроса
                        request = {};
                        request['index_action'] = 1;
                        
                        // Отправка третьего пост запроса для получения ссылки на изображение с обнаруженными объектами
                        fetch("/heandler_post", {
                                method: 'POST',
                                // body: new FormData(form)
                                body: JSON.stringify(request),
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            })
                                .then((response) => response.json())
                                .then((data) => {
                                    
                                    // Проверка что ответ корректный, иначе вывод сообщение об ошибке и выход из addEventListener
                                    if(response['status'] != 200) {

                                        // Вставка полученого от сервера сообщения в созданный div
                                        mes_eror.innerHTML = response['message'];
                                
                                        // Вставка div в начало main
                                        main.prepend(mes_eror);
                                
                                        // Удаление "загрузки"
                                        document.querySelector(".loadBar").remove();
                                
                                        // Вставка div для загрузки пользовательского изображения и обнуление его значения
                                        container.prepend(mainWrapper);
                                        document.getElementById("input__file").value = '';
                                
                                        return;
                                    }
                                    
                                    // Создание html объекта для отображения картинки снайденными объектами
                                    // и вставка его в низ блока для отбражения результата 
                                    var result_img2 = create('<div class="container_img__item"><img class="container-result_img2" id="container-result-' + scors + '_img2" src="' + data['path_result'] + '" alt="result_img2"><p class="container__par comfortaa">Обработка нейросетью</p></div>');
                                    container_img.append(result_img2);
                                
                                    // Подготовка четвёртого запроса
                                    request = {};
                                    request['index_action'] = 2;
                                    
                                    // Отправка четвёртого пост запроса для получения ссылки на файл результата 
                                    fetch("/heandler_post", {
                                            method: 'POST',
                                            // body: new FormData(form)
                                            body: JSON.stringify(request),
                                            headers: {
                                                'Content-Type': 'application/json'
                                            }
                                        })
                                            .then((response) => response.json())
                                            .then((data) => {
                                                
                                                // Удаление "Загрузки"
                                                document.querySelector(".loadBar").remove();

                                                // Вставка div для загрузки пользовательского изображения и обнуление его значения
                                                container.prepend(mainWrapper);
                                                document.getElementById("input__file").value = '';

                                                // Если сообщение уже есть, удалить текущее
                                                if(document.querySelector(".messeg") != null) {
                                                    document.querySelector(".messeg").remove();    
                                                }
                                                
                                                
                                                    // Если статус текущего запроса 200 (всё ок)
                                                    if(data['status'] == 200) {

                                                        // Получение из пути к файлу его имени
                                                        var str = data['path_result'];
                                                        
                                                        str = str.slice(str.lastIndexOf('/') + 1);
                                                        

                                                        data['name_result'] = str;
                                                        
                                                        // Вставка полученого от сервера сообщения в созданный div
                                                        mes_cuc.innerHTML = data['message'];
                                            
                                                        // Вставка div в начало main
                                                        main.prepend(mes_cuc);  

                                                        // Подготовка ссылки на файл
                                                        let url = "../" + data['path_result'];

                                                        // Создание и вставка таблицы в конец контейнера с результатом
                                                        var table = create('<table class="table comfortaa" id="csv-data_' + scors + '"></table>');
                                                        container_result.append(table);

                                                        // Полученние ссылки на таблицу и запалнение ей содержимым .csv файла
                                                        let tab = document.getElementById("csv-data_" + scors);
                                                        createTable(url, tab);

                                                        // Создание и вставка кнопки для загрузки результирующего .csv файла
                                                        // в конец контейнера с результатом
                                                        var download = create('<button id="' + data['name_result'] + '" class="download input__file-button">Скачать ком. предложение ' + data['name_result'] + '</button>');
                                                        container_result.append(download);

                                                        var link = document.createElement('a');
                                                        link.setAttribute('href', '#container-result-' + scors );
                                                        link.click();

                                                    } else {
                                                        // Вставка полученого от сервера сообщения в созданный div
                                                        mes_eror.innerHTML = data['message'];

                                                        // Вставка div в начало main
                                                        main.prepend(mes_eror);
                                                    }   
                                                    // Увеличение счётчика обработанных картинок
                                                    scors++;
                                    });
                        });
              });
           }
    );
  
});


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
$('body').delegate('.download', 'click', function(e){
    var id = e.currentTarget.getAttribute('id');
	var link = document.createElement('a');
	link.setAttribute('href', 'static/result/' + id);
	link.setAttribute('download', id);
	link.click();
	return false;
});

// Слушатель для кнопки выхода
$('body').delegate('.exit', 'click', function(e){

    // Создание нового элемента div для отображения в нём сообщения с сервера
    var mes_cuc =  document.createElement('div');
    mes_cuc.className += ' flex cuc-regi messeg';
    

    request = {};
    request['index_action'] = -1;
    console.log(request);

    fetch("/exit", {
        method: 'POST',
        // body: new FormData(form)
        body: JSON.stringify(request),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);

            // Если сообщение уже есть, удалить текущее
            if(document.querySelector(".messeg") != null) {
                document.querySelector(".messeg").remove();    
            }
            
            // Выделение элемента main, для последующей вставки в его начало сообщений
            const main = document.querySelector(".main-section");

            if(data['status'] == 200){
  
                // Вставка полученого от сервера сообщения в созданный div
                mes_cuc.innerHTML = data['message'];

               

               // Вставка div в начало main
               main.before(mes_cuc);    

               window.setTimeout(function() { window.location = "/authorization"; }, 500);

           }   else  {

                // Вставка полученого от сервера сообщения в созданный div
                mes_eror.innerHTML = data['message'];

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



 
