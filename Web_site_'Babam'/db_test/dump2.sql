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
(11, 'Юлия', 'Михайловна', 'Андреева', '1993-07-12 00:00:00', 'Челябинск', '89998887777', 'Ноутбук', 'Премиум', 'АвтоСалон11', 'Высшее', '4321', '654321', '2020-01-20 00:00:00', 'ФМС', '123456', 0, 'WXYZ', '123456789', '2021-09-01 00:00:00', 'ФМС', '654321', 'GH1234', '2345678901', '2021-09-01 00:00:00', 'ГИБДД', '123456', 700000.00, 24, 150000.00, '2022-05-01 00:00:00', 'Не замужем', 0, 'Челябинск, ул. 9 Мая, д. 3', 'Арендуемое', '2022-05-01 00:00:00', 'Работа', 'ООО Сибирь', '1234567890', 'Аналитик', 'Челябинск, ул. Степана Разина, д. 6', '89998887778', '2022-05-01 00:00:00', 4, 65000.00, 10000.00, 'Государственная служба', 'Skoda', 'Octavia', '2022', 1800000.00, 35000.00, 'Легковое', 'Новое', 'Автомат', '20000 км', 'Телевизор;Холодильник'),
(12, 'Дмитрий', 'Александрович', 'Ковалев', '1986-05-03 00:00:00', 'Самара', '89997779988', 'Холодильник', 'Эконом', 'АвтоСалон12', 'Среднее', '5678', '987654', '2014-06-10 00:00:00', 'ГУВД', '654321', 1, 'QRST', '876543210', '2016-08-01 00:00:00', 'ГУВД', '543210', 'IJ1234', '3456789012', '2016-08-01 00:00:00', 'ГИБДД', '654321', 1200000.00, 36, 250000.00, '2017-05-01 00:00:00', 'Разведен', 2, 'Самара, ул. Ставропольская, д. 25', 'Собственное', '2017-05-01 00:00:00', 'Работа', 'ООО Нова', '9876543210', 'Менеджер', 'Самара, ул. Победы, д. 4', '89997779989', '2017-05-01 00:00:00', 8, 85000.00, 20000.00, 'Пособие', 'Mazda', 'CX-5', '2020', 2200000.00, 30000.00, 'Внедорожник', 'Новое', 'Автомат', '15000 км', 'Пылесос;Микроволновка'),
(13, 'Евгений', 'Ильич', 'Николаев', '1978-03-16 00:00:00', 'Барнаул', '89993336677', 'Стиральная машина', 'Премиум', 'АвтоСалон13', 'Высшее', '6789', '543210', '2011-07-01 00:00:00', 'ФМС', '123456', 1, 'UVWX', '123456789', '2015-11-01 00:00:00', 'ФМС', '654321', 'KL2345', '4567890123', '2015-11-01 00:00:00', 'ГИБДД', '123456', 1500000.00, 24, 350000.00, '2016-10-01 00:00:00', 'Замужем', 3, 'Барнаул, ул. Мичурина, д. 10', 'Собственное', '2016-10-01 00:00:00', 'Работа', 'АО Техно', '3456789012', 'Финансист', 'Барнаул, ул. Пушкина, д. 8', '89993336678', '2016-10-01 00:00:00', 9, 90000.00, 25000.00, 'Бизнес', 'Volkswagen', 'Passat', '2020', 2500000.00, 50000.00, 'Легковое', 'Новое', 'Автомат', '20000 км', 'Холодильник;Телевизор'),
(14, 'Алена', 'Сергеевна', 'Рыкова', '1984-12-22 00:00:00', 'Омск', '89992223355', 'Телевизор', 'Стандарт', 'АвтоСалон14', 'Среднее', '1234', '678901', '2006-09-01 00:00:00', 'ГУВД', '543210', 0, 'YZAB', '987654321', '2011-03-01 00:00:00', 'ГУВД', '654321', 'MN2345', '5678901234', '2011-03-01 00:00:00', 'ГИБДД', '543210', 800000.00, 36, 150000.00, '2012-12-01 00:00:00', 'Разведена', 1, 'Омск, ул. Мира, д. 18', 'Собственное', '2012-12-01 00:00:00', 'Работа', 'ЗАО Вектор', '2345678901', 'HR-менеджер', 'Омск, ул. Калинина, д. 7', '89992223356', '2012-12-01 00:00:00', 7, 75000.00, 15000.00, 'Государственная служба', 'Honda', 'CR-V', '2019', 2000000.00, 30000.00, 'Внедорожник', 'Подержанное', 'Автомат', '30000 км', 'Пылесос;Микроволновка'),
(16, 'Оксана', 'Владимировна', 'Ларина', '1987-06-09 00:00:00', 'Рязань', '89993337788', 'Стиральная машина', 'Премиум', 'АвтоСалон16', 'Высшее', '4321', '987654', '2014-02-15 00:00:00', 'ГУВД', '123456', 0, 'STUV', '123456789', '2017-06-01 00:00:00', 'ГУВД', '654321', 'KL6789', '5678901234', '2017-06-01 00:00:00', 'ГИБДД', '123456', 2000000.00, 24, 500000.00, '2018-03-01 00:00:00', 'Замужем', 2, 'Рязань, ул. Пушкина, д. 7', 'Арендуемое', '2018-03-01 00:00:00', 'Работа', 'АО Инвест', '3456789012', 'Аудитор', 'Рязань, ул. Лермонтова, д. 5', '89993337789', '2018-03-01 00:00:00', 10, 120000.00, 30000.00, 'Пенсия', 'Hyundai', 'Sonata', '2020', 2000000.00, 35000.00, 'Легковое', 'Новый', 'Автомат', '5000 км', 'Холодильник;Пылесос'),
(17, 'Роман', 'Михайлович', 'Ильин', '1983-08-24 00:00:00', 'Ижевск', '89997778888', 'Кофемашина', 'Стандарт', 'АвтоСалон17', 'Среднее', '6789', '543210', '2012-04-10 00:00:00', 'МВД', '543210', 1, 'UVWX', '987654321', '2015-12-01 00:00:00', 'МВД', '654321', 'MN5678', '6789012345', '2015-12-01 00:00:00', 'ГИБДД', '543210', 1300000.00, 24, 300000.00, '2016-09-01 00:00:00', 'Разведен', 0, 'Ижевск, ул. Суворова, д. 4', 'Собственное', '2016-09-01 00:00:00', 'Работа', 'ООО Престиж', '9876543210', 'Секретарь', 'Ижевск, ул. Ленина, д. 8', '89997778889', '2016-09-01 00:00:00', 8, 90000.00, 15000.00, 'Доход от аренды', 'Kia', 'Soul', '2021', 2000000.00, 30000.00, 'Внедорожник', 'Новое', 'Автомат', '15000 км', 'Стиральная машина;Микроволновка'),
(18, 'Вера', 'Петровна', 'Громова', '1990-02-17 00:00:00', 'Тула', '89998885555', 'Телевизор', 'Премиум', 'АвтоСалон18', 'Высшее', '3456', '789012', '2018-11-01 00:00:00', 'ФМС', '654321', 0, 'YZAB', '123456789', '2022-01-01 00:00:00', 'ФМС', '654321', 'KL3456', '5678901234', '2022-01-01 00:00:00', 'ГИБДД', '123456', 1500000.00, 36, 250000.00, '2023-05-01 00:00:00', 'Не замужем', 2, 'Тула, ул. Советская, д. 10', 'Собственное', '2023-05-01 00:00:00', 'Работа', 'ЗАО Орбита', '2345678901', 'Дизайнер', 'Тула, ул. Красина, д. 12', '89998885556', '2023-05-01 00:00:00', 5, 100000.00, 20000.00, 'Государственная служба', 'Toyota', 'Camry', '2023', 2500000.00, 30000.00, 'Легковое', 'Новое', 'Автомат', '15000 км', 'Телевизор;Пылесос'),
(19, 'Елена', 'Павловна', 'Бурова', '1995-09-15 00:00:00', 'Ярославль', '89994445566', 'Пылесос', 'Стандарт', 'АвтоСалон19', 'Среднее', '3456', '789012', '2014-05-01 00:00:00', 'ФМС', '654321', 0, 'UVWX', '567890123', '2022-05-01 00:00:00', 'ФМС', '123456', 'QR5678', '6789012345', '2022-05-01 00:00:00', 'ГИБДД', '654321', 1100000.00, 36, 220000.00, '2023-05-01 00:00:00', 'Замужем', 2, 'Ярославль, ул. Советская, д. 20', 'Собственное', '2023-05-01 00:00:00', 'Работа', 'ЗАО Прогресс', '3456789012', 'Юрист', 'Ярославль, ул. Маяковского, д. 25', '89994445567', '2023-05-01 00:00:00', 6, 85000.00, 15000.00, 'Государственная служба', 'Hyundai', 'Tucson', '2022', 2000000.00, 35000.00, 'Внедорожник', 'Новый', 'Автомат', '10000 км', 'Телевизор;Кофемашина');
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