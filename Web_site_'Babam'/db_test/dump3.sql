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
(21, 'Алексей', 'Николаевич', 'Зимин', '1987-04-14 00:00:00', 'Курск', '89995557788', 'Телевизор', 'Премиум', 'АвтоСалон21', 'Среднее', '5678', '123456', '2015-08-01 00:00:00', 'МВД', '123456', 0, 'WXYZ', '987654321', '2021-07-01 00:00:00', 'МВД', '654321', 'PQ1234', '4567890123', '2021-07-01 00:00:00', 'ГИБДД', '123456', 1400000.00, 24, 300000.00, '2022-11-01 00:00:00', 'Разведен', 1, 'Курск, ул. Гагарина, д. 12', 'Арендуемое', '2022-11-01 00:00:00', 'Работа', 'ООО Ракета', '4567890123', 'Проектный менеджер', 'Курск, ул. Свердлова, д. 8', '89995557789', '2022-11-01 00:00:00', 8, 95000.00, 25000.00, 'Аренда', 'Nissan', 'Altima', '2021', 2100000.00, 40000.00, 'Легковое', 'Новый', 'Автомат', '8000 км', 'Кофемашина;Микроволновка'),
(22, 'Виктория', 'Юрьевна', 'Соколова', '1991-06-22 00:00:00', 'Пермь', '89996667788', 'Стиральная машина', 'Эконом', 'АвтоСалон22', 'Высшее', '2345', '678901', '2016-03-01 00:00:00', 'ФМС', '123456', 0, 'ABCD', '654321987', '2021-02-01 00:00:00', 'ФМС', '654321', 'RS3456', '5678901234', '2021-02-01 00:00:00', 'ГИБДД', '123456', 1200000.00, 36, 220000.00, '2022-08-01 00:00:00', 'Не замужем', 0, 'Пермь, ул. Ленина, д. 45', 'Собственное', '2022-08-01 00:00:00', 'Работа', 'АО Стандарт', '5678901234', 'Менеджер по продажам', 'Пермь, ул. Куйбышева, д. 23', '89996667789', '2022-08-01 00:00:00', 5, 85000.00, 15000.00, 'Пенсия', 'Skoda', 'Octavia', '2022', 2200000.00, 30000.00, 'Легковое', 'Новый', 'Автомат', '15000 км', 'Телевизор;Холодильник'),
(24, 'Светлана', 'Геннадиевна', 'Федорова', '1985-02-18 00:00:00', 'Тюмень', '89998887799', 'Телевизор', 'Стандарт', 'АвтоСалон24', 'Высшее', '4567', '890123', '2012-11-01 00:00:00', 'ГУВД', '654321', 0, 'IJKL', '987654321', '2018-12-01 00:00:00', 'ГУВД', '123456', 'EF2345', '7890123456', '2018-12-01 00:00:00', 'ГИБДД', '654321', 1700000.00, 24, 350000.00, '2019-12-01 00:00:00', 'Разведена', 1, 'Тюмень, ул. Дзержинского, д. 35', 'Собственное', '2019-12-01 00:00:00', 'Работа', 'АО Звезда', '6789012345', 'Бухгалтер', 'Тюмень, ул. Гоголя, д. 40', '89998887799', '2019-12-01 00:00:00', 7, 95000.00, 30000.00, 'Аренда', 'Toyota', 'RAV4', '2021', 2500000.00, 50000.00, 'Внедорожник', 'Новый', 'Автомат', '12000 км', 'Телевизор;Кофемашина'),
(25, 'Юлия', 'Анатольевна', 'Коваленко', '1990-07-09 00:00:00', 'Калуга', '89997775566', 'Холодильник', 'Премиум', 'АвтоСалон25', 'Среднее', '5678', '901234', '2017-04-01 00:00:00', 'ФМС', '654321', 1, 'MNOP', '123456789', '2021-06-01 00:00:00', 'ФМС', '123456', 'GH7890', '8901234567', '2021-06-01 00:00:00', 'ГИБДД', '654321', 2000000.00, 36, 400000.00, '2022-11-01 00:00:00', 'Замужем', 3, 'Калуга, ул. Пролетарская, д. 55', 'Арендуемое', '2022-11-01 00:00:00', 'Работа', 'ООО Глобус', '9012345678', 'Финансовый аналитик', 'Калуга, ул. Чехова, д. 25', '89997775567', '2022-11-01 00:00:00', 6, 105000.00, 25000.00, 'Государственная служба', 'Honda', 'CR-V', '2022', 2400000.00, 35000.00, 'Внедорожник', 'Новый', 'Автомат', '15000 км', 'Кофемашина;Микроволновка'),
(26, 'Максим', 'Владимирович', 'Лебедев', '1988-01-30 00:00:00', 'Саратов', '89995559900', 'Ноутбук', 'Стандарт', 'АвтоСалон26', 'Высшее', '6789', '012345', '2014-09-01 00:00:00', 'ФМС', '123456', 0, 'QRST', '987654321', '2019-11-01 00:00:00', 'ФМС', '654321', 'IJ5678', '6789012345', '2019-11-01 00:00:00', 'ГИБДД', '123456', 1600000.00, 24, 330000.00, '2020-11-01 00:00:00', 'Разведен', 2, 'Саратов, ул. Костромская, д. 22', 'Собственное', '2020-11-01 00:00:00', 'Работа', 'АО Энергия', '3456789012', 'Технический директор', 'Саратов, ул. Ленина, д. 15', '89995559901', '2020-11-01 00:00:00', 9, 100000.00, 27000.00, 'Аренда', 'Volkswagen', 'Passat', '2021', 2100000.00, 45000.00, 'Легковое', 'Новый', 'Автомат', '13000 км', 'Телевизор;Пылесос'),
(28, 'Станислав', 'Игоревич', 'Андреев', '1980-12-05 00:00:00', 'Воронеж', '89992223344', 'Стиральная машина', 'Премиум', 'АвтоСалон28', 'Высшее', '8901', '234567', '2016-02-01 00:00:00', 'ГУВД', '654321', 0, 'YZAB', '987654321', '2022-01-01 00:00:00', 'ГУВД', '123456', 'MN4567', '5678901234', '2022-01-01 00:00:00', 'ГИБДД', '654321', 2000000.00, 36, 350000.00, '2023-01-01 00:00:00', 'Замужем', 3, 'Воронеж, ул. Мира, д. 40', 'Собственное', '2023-01-01 00:00:00', 'Работа', 'ЗАО Союз', '7890123456', 'Финансовый директор', 'Воронеж, ул. Комиссара, д. 60', '89992223345', '2023-01-01 00:00:00', 10, 115000.00, 32000.00, 'Государственная служба', 'Renault', 'Duster', '2022', 2500000.00, 50000.00, 'Внедорожник', 'Новый', 'Автомат', '9000 км', 'Холодильник;Телевизор');
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