-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: expobank
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `hackaton_client_data`
--

DROP TABLE IF EXISTS `hackaton_client_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hackaton_client_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `client_name` varchar(255) DEFAULT NULL COMMENT 'Имя клиента',
  `client_middle_name` varchar(255) DEFAULT NULL COMMENT 'Отчество клиента',
  `client_surname` varchar(255) DEFAULT NULL COMMENT 'Фамилия клиента',
  `client_birthdate` datetime DEFAULT NULL COMMENT 'Дата рождения клиента',
  `client_birthplace` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Место рождения клиента',
  `client_mobile_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Мобильный телефон клиента',
  `product` varchar(100) DEFAULT NULL COMMENT 'Продукт',
  `tariff` varchar(255) DEFAULT NULL COMMENT 'Тариф',
  `autosalon` varchar(255) DEFAULT NULL COMMENT 'Салон оформления и выдачи авто',
  `client_education` varchar(255) DEFAULT NULL COMMENT 'Образование: высшее, среднее и пр.',
  `client_passport_series` varchar(20) DEFAULT NULL COMMENT 'Серия паспорта',
  `client_passport_number` varchar(20) DEFAULT NULL COMMENT 'Номер паспорта',
  `client_passport_issue_date` datetime DEFAULT NULL COMMENT 'Дата выдачи паспорта',
  `client_passport_issue_place` varchar(200) DEFAULT NULL COMMENT 'Кем выдан паспорт',
  `client_passport_issue_code` varchar(50) DEFAULT NULL COMMENT 'Код места выдачи паспорта',
  `client_passport_no_previous` tinyint DEFAULT NULL COMMENT 'Флаг - Нет сведений о ранее выданном паспорте',
  `client_zagran_passport_series` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Загран.паспорт: Серия паспорта',
  `client_zagran_passport_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Загран.паспорт: Номер паспорта',
  `client_zagran_passport_issue_date` datetime DEFAULT NULL COMMENT 'Загран.паспорт: Дата выдачи паспорта',
  `client_zagran_passport_issue_place` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Загран.паспорт: Кем выдан паспорт',
  `client_zagran_passport_issue_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Загран.паспорт: Код места выдачи паспорта',
  `client_driver_license_series` varchar(255) DEFAULT NULL COMMENT 'Серия водительского удостоверения',
  `client_driver_license_number` varchar(255) DEFAULT NULL COMMENT 'Номер водительского удостоверения',
  `client_driver_license_issue_date` datetime DEFAULT NULL COMMENT 'Дата выдачи водительского удостоверения',
  `client_driver_license_issue_place` varchar(255) DEFAULT NULL COMMENT 'Место выдачи водительского удостоверения',
  `client_driver_license_issue_code` varchar(255) DEFAULT NULL COMMENT 'Код места выдачи водительского удостоверения',
  `credit_sum` decimal(12,2) DEFAULT NULL COMMENT 'Сумма кредита',
  `credit_term` smallint DEFAULT NULL COMMENT 'Срок кредита',
  `credit_initial` decimal(12,2) DEFAULT NULL COMMENT 'Предполагаемый первоначальный взнос',
  `credit_dog_issue_date` datetime DEFAULT NULL COMMENT 'Дата подписания кредитного договора',
  `client_family_status` varchar(255) DEFAULT NULL COMMENT 'Семейное положение: женат, холост и пр.',
  `client_children_dependents` tinyint DEFAULT NULL COMMENT 'Количество иждивенцев',
  `client_registration_address` varchar(255) DEFAULT NULL COMMENT 'Распознанный адрес регистрации',
  `client_registration_own_type` varchar(255) DEFAULT NULL COMMENT 'Тип жилья',
  `client_registration_date` datetime DEFAULT NULL COMMENT 'Дата регистрации',
  `job_type` varchar(255) DEFAULT NULL COMMENT 'Тип занятости: Найм, ИП, Самозанятый, Пенсионер, Собственное дело',
  `workplace_name` varchar(255) DEFAULT NULL COMMENT 'Место работы: название организации',
  `workplace_inn` varchar(255) DEFAULT NULL COMMENT 'Место работы: ИНН',
  `workplace_client_position` varchar(255) DEFAULT NULL COMMENT 'Место работы: должность',
  `workplace_address` varchar(255) DEFAULT NULL COMMENT 'Место работы: адрес организации',
  `workplace_phone` varchar(255) DEFAULT NULL COMMENT 'Место работы: рабочий телефон',
  `workplace_workdate` datetime DEFAULT NULL COMMENT 'Место работы: дата начала трудоустройства',
  `workplace_work_experience` tinyint DEFAULT NULL COMMENT 'Место работы: общий трудовой стаж',
  `workplace_income_amount` decimal(12,2) DEFAULT NULL COMMENT 'Место работы: доход',
  `workplace_additional_income_amount` decimal(12,2) DEFAULT NULL COMMENT 'Размер дополнительного дохода',
  `workplace_additional_income_type` varchar(255) DEFAULT NULL COMMENT 'Тип дополнительного дохода: Пенсия, Пособие, Алименты, Доход от ценных бумаг/депозитов, Аренда и пр.',
  `car_brand` varchar(255) DEFAULT NULL COMMENT 'Марка приобретаемого авто',
  `car_model` varchar(255) DEFAULT NULL COMMENT 'Модель приобретаемого авто',
  `car_year` varchar(255) DEFAULT NULL COMMENT 'Год выпуска приобретаемого авто',
  `car_price` decimal(10,2) DEFAULT NULL COMMENT 'Стоимость авто',
  `car_dop_price` decimal(10,2) DEFAULT NULL COMMENT 'Стоимость доп.оборудования',
  `car_type` varchar(255) DEFAULT NULL COMMENT 'Тип авто (легковое, коммерческое и т.п.)',
  `car_condition` varchar(255) DEFAULT NULL COMMENT 'Состояние авто (новое, подержанное и т.п.)',
  `car_transmission` varchar(255) DEFAULT NULL COMMENT 'Тип коробки передач (МТ, АТ)',
  `car_mileage` varchar(255) DEFAULT NULL COMMENT 'Пробег авто',
  `client_take_products` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hackaton_client_data`
--

LOCK TABLES `hackaton_client_data` WRITE;
/*!40000 ALTER TABLE `hackaton_client_data` DISABLE KEYS */;
INSERT INTO `hackaton_client_data` VALUES
(1,'Иван','Иванович','Иванов','1980-05-15 00:00:00','Москва','89998887766','Телевизор','Эконом','АвтоСалон1','Высшее','1234','567890','2010-01-01 00:00:00','МВД','123456',0,'ABCD','123456789','2015-01-01 00:00:00','МВД','654321','AB1234','1234567890','2015-01-01 00:00:00','ГИБДД','123456',500000.00,24,100000.00,'2019-01-01 00:00:00','Женат',2,'Москва, ул. Пушкина, д. 1','Собственное','2019-01-01 00:00:00','Работа','ООО Ромашка','1234567890','Менеджер','Москва, ул. Лермонтова, д. 2','89995554433','2019-01-01 00:00:00',5,50000.00,10000.00,'Пенсия','Toyota','Camry','2020',2500000.00,50000.00,'Легковое','Новое','Автомат','15000 км','Ноутбук;Телефон'),
(2,'Александр','Петрович','Петров','1990-08-22','Санкт-Петербург','89997775544','Ноутбук','Премиум','АвтоСалон2','Среднее','5678','123456','2015-05-15','ФМС','654321', 1,'EFGH','987654321','2020-03-01','ФМС','123456','CD1234','0987654321','2020-03-01','ГИБДД','654321',1000000.00,36,200000.00,'2021-06-01','Не женат',0,'Санкт-Петербург, ул. Ленина, д. 5','Арендуемое','2021-06-01','Другое','ООО Цветок','0987654321','Инженер','Санкт-Петербург, ул. Горького, д. 3','89997775544','2021-06-01',3,80000.00,20000.00,'Государственная служба','BMW','X5','2021',3500000.00,70000.00,'Внедорожник','Новый','Автомат','5000 км','Холодильник;Микроволновка'),
(3,'Петр','Петрович','Сидоров','1985-11-30','Новосибирск','89998885544','Кофемашина','Базовый','АвтоСалон3','Высшее','9876','543210','2012-02-01 00:00:00','ГУВД','654321',0,'IJKL','456789123','2018-06-01 00:00:00','ГУВД','123456','CD5678','4567891234','2018-06-01 00:00:00','ГИБДД','654321',800000.00,36,150000.00,'2020-01-01 00:00:00','Разведен',1,'Новосибирск, ул. Чехова, д. 10','Собственное','2020-01-01 00:00:00','Работа','ООО Дубрава','2345678901','Юрист','Новосибирск, ул. Толстого, д. 5','89998885544','2020-01-01 00:00:00',6,60000.00,15000.00,'Работа по контракту','Audi','A4','2018',2800000.00,60000.00,'Легковое','Подержанное','Механическая','30000 км','Смартфон;Планшет'),
(4,'Мария','Владимировна','Кузнецова','1992-07-15','Екатеринбург','89998886655','Микроволновка','Стандарт','АвтоСалон4','Среднее','3456','789012','2016-03-01 00:00:00','ОВД','654321',1,'LMNO','345678901','2017-07-01 00:00:00','ОВД','987654','EF5678','6789012345','2017-07-01 00:00:00','ГИБДД','987654',1200000.00,48,250000.00,'2022-01-01 00:00:00','Замужем',2,'Екатеринбург, ул. Свердлова, д. 20','Арендуемое','2022-01-01 00:00:00','ИП','ООО Снег','3456789012','Аналитик','Екатеринбург, ул. Кропоткина, д. 10','89998886655','2022-01-01 00:00:00',4,70000.00,15000.00,'Другое','Mercedes','E-Class','2022',3200000.00,80000.00,'Легковое','Новый','Автомат','1000 км','Стиральная машина;Чайник'),
(5,'Сергей','Александрович','Лебедев','1988-12-12','Казань','89997776655','Пылесос','Эконом','АвтоСалон5','Среднее','4567','890123','2014-04-01 00:00:00','МВД','654321',0,'MNOP','234567890','2015-10-01 00:00:00','МВД','543210','AB2345','6789012345','2015-10-01 00:00:00','ГИБДД','543210',1500000.00,36,300000.00,'2018-01-01 00:00:00','Не женат',1,'Казань, ул. Гагарина, д. 15','Собственное','2018-01-01 00:00:00','Работа','ООО Кристалл','4567890123','Риелтор','Казань, ул. Тимирязева, д. 30','89997776655','2018-01-01 00:00:00',7,90000.00,20000.00,'Другое','Honda','Civic','2019',2000000.00,40000.00,'Легковое','Подержанное','Автомат','20000 км','Телевизор;Пылесос'),
(6,'Ольга','Юрьевна','Смирнова','1987-03-05','Сочи','89997776666','Холодильник','Премиум','АвтоСалон6','Высшее','6789','012345','2013-11-01 00:00:00','ФМС','654321',1,'QRST','123456789','2016-12-01 00:00:00','ФМС','789012','CD3456','2345678901','2016-12-01 00:00:00','ГИБДД','789012',2000000.00,48,350000.00,'2020-05-01 00:00:00','Замужем',0,'Сочи, ул. Ленина, д. 25','Собственное','2020-05-01 00:00:00','ИП','ООО Вектор','5678901234','Менеджер','Сочи, ул. Свердлова, д. 15','89997776666','2020-05-01 00:00:00',8,100000.00,25000.00,'Государственная служба','Ford','Mustang','2020',4000000.00,90000.00,'Купе','Новый','Автомат','5000 км','Холодильник;Стиральная машина'),
(7,'Наталья','Викторовна','Федорова','1995-09-20','Воронеж','89995554455','Чайник','Базовый','АвтоСалон7','Среднее','7890','123456','2017-01-01 00:00:00','ГУВД','456789',0,'UVWX','234567890','2018-02-01 00:00:00','ГУВД','654321','EF1234','3456789012','2018-02-01 00:00:00','ГИБДД','654321',500000.00,24,100000.00,'2021-01-01 00:00:00','Не замужем',2,'Воронеж, ул. Пушкина, д. 8','Арендуемое','2021-01-01 00:00:00','Работа','ООО Лаванда','6789012345','Бухгалтер','Воронеж, ул. Гоголя, д. 4','89995554455','2021-01-01 00:00:00',3,65000.00,10000.00,'Пенсия','Kia','Sportage','2019',2300000.00,50000.00,'Внедорожник','Подержанное','Автомат','40000 км','Пылесос;Микроволновка'),
(8,'Виктор','Геннадьевич','Морозов','1983-06-12','Уфа','89998887777','Утюг','Стандарт','АвтоСалон8','Высшее','8901','234567','2011-08-01 00:00:00','ОВД','789012',0,'WXYZ','456789123','2012-09-01 00:00:00','ОВД','123456','AB5678','7890123456','2012-09-01 00:00:00','ГИБДД','123456',1800000.00,36,350000.00,'2017-01-01 00:00:00','Женат',1,'Уфа, ул. Крупской, д. 12','Собственное','2017-01-01 00:00:00','Работа','ООО Золотой','7890123456','Директор','Уфа, ул. Ленина, д. 5','89998887777','2017-01-01 00:00:00',10,80000.00,20000.00,'Пенсия','Chevrolet','Tahoe','2017',2700000.00,60000.00,'Внедорожник','Подержанное','Автомат','60000 км','Микроволновка;Холодильник'),
(9,'Ирина','Сергеевна','Попова','1991-04-10','Калуга','89995553322','Стиральная машина','Премиум','АвтоСалон9','Среднее','1234','567890','2015-07-01 00:00:00','ФМС','678901',1,'XYZW','234567890','2016-05-01 00:00:00','ФМС','345678','AB2345','6789012345','2016-05-01 00:00:00','ГИБДД','345678',1500000.00,24,250000.00,'2019-07-01 00:00:00','Замужем',1,'Калуга, ул. Гагарина, д. 25','Арендуемое','2019-07-01 00:00:00','Работа','ООО Флора','2345678901','Маркетолог','Калуга, ул. Чехова, д. 30','89995553322','2019-07-01 00:00:00',6,75000.00,15000.00,'Государственная служба','Nissan','Altima','2018',2600000.00,50000.00,'Седан','Новый','Автомат','30000 км','Стиральная машина;Холодильник'),
(10,'Светлана','Юрьевна','Крылова','1980-11-11','Тюмень','89994445566','Чайник','Эконом','АвтоСалон10','Среднее','2345','678901','2014-10-01 00:00:00','ФМС','123456',0,'ABCD','234567890','2015-09-01 00:00:00','ФМС','654321','CD6789','2345678901','2015-09-01 00:00:00','ГИБДД','654321',1200000.00,36,200000.00,'2017-09-01 00:00:00','Не замужем',2,'Тюмень, ул. Лермонтова, д. 10','Собственное','2017-09-01 00:00:00','Работа','ООО Лира','3456789012','Секретарь','Тюмень, ул. Горького, д. 20','89994445566','2017-09-01 00:00:00',5,70000.00,10000.00,'Пенсия','Hyundai','Tucson','2017',2800000.00,55000.00,'Внедорожник','Новый','Автомат','20000 км','Чайник;Телевизор');
/*!40000 ALTER TABLE `hackaton_client_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-05 11:23:52
