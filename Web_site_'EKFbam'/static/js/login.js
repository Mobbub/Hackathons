
// Обработка отправки формы
const form_login = () => {

    // Когда браузером прочтён весь документ
    $(document).ready(function() { 
        
  
        // Создание нового элемента div для отображения в нём сообщения с сервера
        var mes_cuc =  document.createElement('div');
        mes_cuc.className += ' flex cuc-regi messeg';
  
    
        // Тригер нажатия на кнопку формы
        $(".form").on("submit", function(event) {
    
            // Запрет на обновление страницы
            event.preventDefault();

            // Подготовка запроса для отправки на сервер
            request = $(".form").serializeArray();

            var  data = {};
            data[request[0].name] = request[0].value;
            data[request[1].name] = request[1].value;
            
           
            // Отправка пост запроса на сервер
            fetch('/log', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                  'Content-Type': 'application/json'
                }
            })
                .then((response) => response.json())
                .then((data) => {

                    // Если сообщение уже есть, удалить текущее
                    if(document.querySelector(".messeg") != null) {
                        document.querySelector(".messeg").remove();    
                    }
                
                    // Выделение элемента main, для последующей вставки в его начало сообщений
                    const main = document.querySelector(".autho-section");
                        
                    if(data['status'] == 200){

                        // Вставка полученого от сервера сообщения в созданный div
                        mes_cuc.innerHTML = "Успешная авторизация \n Перенаправление...";

                        // Вставка div в начало main
                        main.before(mes_cuc);    

                        // Перенаправление на страницу загрузки схем
                        window.setTimeout(function() { window.location = "/"; }, 1000);

                    }   else if(data['status'] == 0) {

                        // Вставка полученого от сервера сообщения в созданный div
                        mes_cuc.innerHTML = "Ошибка авторизации";

                        // Вставка div в начало main
                        main.before(mes_cuc);  
                    }    
                    
    
                });
            
    })});
  
  }

form_login();