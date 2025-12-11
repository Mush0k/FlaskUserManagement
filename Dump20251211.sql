-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mushok
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `parent_id` int DEFAULT NULL,
  `category_name` varchar(100) DEFAULT NULL,
  `slug` varchar(100) DEFAULT NULL,
  `order_index` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `slug_UNIQUE` (`slug`),
  KEY `fk_categories_categories1_idx` (`parent_id`),
  CONSTRAINT `fk_parent_id` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`category_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (10,NULL,'Новости','news',10),(20,NULL,'Технологии','tech',20),(30,20,'Базы Данных','databases',21),(40,20,'Программирование','programming',22),(50,10,'Спорт','sport',11);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content`
--

DROP TABLE IF EXISTS `content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `content` (
  `content_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `type_id` int NOT NULL,
  `category_id` int NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `slug` varchar(100) DEFAULT NULL,
  `excerpt` text,
  `content_body` longtext,
  `status` enum('Draft','Published','Archived') DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  PRIMARY KEY (`content_id`),
  KEY `fk_content_content_types1_idx` (`type_id`),
  KEY `fk_content_users1_idx` (`user_id`),
  KEY `fk_content_categories1_idx` (`category_id`),
  CONSTRAINT `fk_content_categories1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`),
  CONSTRAINT `fk_content_content_types1` FOREIGN KEY (`type_id`) REFERENCES `content_types` (`type_id`),
  CONSTRAINT `fk_content_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content`
--

LOCK TABLES `content` WRITE;
/*!40000 ALTER TABLE `content` DISABLE KEYS */;
INSERT INTO `content` VALUES (1,4,1,30,'Основы чистого SQL','osnovy-chistogo-sql','Краткое введение в SQL.','Основы «чистого» SQL (Structured Query Language, языка структурированных запросов) включают изучение синтаксиса, \n операторов и примеров запросов. Важно учитывать, что SQL — декларативный язык, \n и на чистом SQL нельзя написать программу — он предназначен только для взаимодействия с базами данных: получения, \n добавления, изменения и удаления информации в них, управления доступом и так далее.','Published','2025-12-09 12:51:17'),(2,5,2,10,'Срочные новости IT','srochnye-novosti-it','Сводка последних событий.','Детальное описание событий.','Draft',NULL),(3,13,1,40,'Обзор нового фреймворка','obzor-novogo-freymvorka','Анализ PHP-фреймворка.','Анализ PHP-фреймворка — это процесс, который включает \n изучение архитектуры, функциональности и особенностей фреймворка, а также сравнение его \n с другими инструментами для веб-разработки. Цель — выбрать подходящий фреймворк для проекта, \n учитывая особенности проекта и цели разработки','Published','2025-10-15 10:00:00'),(4,4,3,20,'О проекте','o-proekte','Информация о компании.','Официальный сайт Федеральной налоговой службы (ФНС) России. \nПредоставляет открытые данные из Единого государственного реестра юридических лиц (ЕГРЮЛ) и \nЕдиного государственного реестра индивидуальных предпринимателей (ЕГРИП). \nПозволяет получить выписку из ЕГРЮЛ/ЕГРИП, содержащую ИНН, ОГРН, адрес, сведения о руководителе, учредителях, \nвидах деятельности.','Published','2025-12-09 12:51:17'),(5,5,2,50,'Чемпионат по футболу','chempionat-futbolu','Обзор главных матчей.','Впервые в финальной стадии примут участие 48 команд, разделённых на 12 групп по четыре сборные...','Archived','2024-06-20 15:00:00');
/*!40000 ALTER TABLE `content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_has_tags`
--

DROP TABLE IF EXISTS `content_has_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `content_has_tags` (
  `content_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`content_id`,`tag_id`),
  KEY `fk_content_has_tags_tags1_idx` (`tag_id`),
  KEY `fk_content_has_tags_content1_idx` (`content_id`),
  CONSTRAINT `fk_content_has_tags_content1` FOREIGN KEY (`content_id`) REFERENCES `content` (`content_id`),
  CONSTRAINT `fk_content_has_tags_tags1` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_has_tags`
--

LOCK TABLES `content_has_tags` WRITE;
/*!40000 ALTER TABLE `content_has_tags` DISABLE KEYS */;
INSERT INTO `content_has_tags` VALUES (1,1),(1,2),(3,3),(3,4),(2,5),(5,6);
/*!40000 ALTER TABLE `content_has_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_types`
--

DROP TABLE IF EXISTS `content_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `content_types` (
  `type_id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  PRIMARY KEY (`type_id`),
  UNIQUE KEY `slug_UNIQUE` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_types`
--

LOCK TABLES `content_types` WRITE;
/*!40000 ALTER TABLE `content_types` DISABLE KEYS */;
INSERT INTO `content_types` VALUES (1,'Статья','article'),(2,'Новость','news'),(3,'Страница','page');
/*!40000 ALTER TABLE `content_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `permission_id` int NOT NULL AUTO_INCREMENT COMMENT 'айди',
  `code` varchar(45) DEFAULT NULL COMMENT 'код права',
  `description` text COMMENT 'описание права',
  PRIMARY KEY (`permission_id`),
  UNIQUE KEY `code_UNIQUE` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES (101,'post.create','Создание новых публикаций'),(102,'post.publish','Публикация контента в общий доступ'),(103,'user.view_all','Просмотр списка всех пользователей'),(104,'admin.config','Доступ к настройкам системы');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permissions`
--

DROP TABLE IF EXISTS `role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permissions` (
  `role_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `fk_role_has_permission_permission1_idx` (`permission_id`),
  KEY `fk_role_has_permission_role1_idx` (`role_id`),
  CONSTRAINT `fk_role_has_permission_permission1` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`permission_id`),
  CONSTRAINT `fk_role_has_permission_role1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permissions`
--

LOCK TABLES `role_permissions` WRITE;
/*!40000 ALTER TABLE `role_permissions` DISABLE KEYS */;
INSERT INTO `role_permissions` VALUES (1,101),(2,101),(3,101),(1,102),(2,102),(1,103),(1,104);
/*!40000 ALTER TABLE `role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'administrator','Полные административные права'),(2,'editor','Редактирование и публикация контента'),(3,'author','Создание и управление собственным контентом'),(4,'viewer','Только просмотр контента');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tags` (
  `tag_id` int NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(45) NOT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE KEY `tag_name_UNIQUE` (`tag_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES (4,'Frontend'),(5,'IT-новости'),(2,'MySQL'),(3,'PHP'),(1,'SQL'),(6,'Футбол');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_roles` (
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `fk_user_has_user_role_user_role1_idx` (`role_id`),
  KEY `fk_user_has_user_role_user_idx` (`user_id`),
  CONSTRAINT `fk_user_has_user_role_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `fk_user_has_user_role_user_role1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (1,1),(11,1),(3,2),(5,2),(6,2),(8,2),(14,2),(16,2),(17,2),(4,3),(5,3),(9,3),(13,3),(15,3),(16,3),(18,3),(2,4),(10,4),(12,4),(13,4);
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `patronymic` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `registration_date` datetime NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_active` tinyint DEFAULT '1',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `phone_number_UNIQUE` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ivanov_i','ivanov@corp.ru','Иван','Иванов','Иванович','1985-05-15','+79101234567','hash1','2023-09-14 19:00:30','2025-12-07 10:30:00',0),(2,'petrov_p','petrov@corp.ru','Петр','Петров','Павлович','1990-08-20','+79102234567','hash2','2024-03-01 12:00:00',NULL,0),(3,'sidorov_s','sidorov@corp.ru','Сергей','Сидоров','Сергеевич','1995-03-01','+79103234567','hash3','2025-11-20 08:00:00','2025-12-08 15:48:15',0),(4,'koval_a','koval@corp.ru','Анна','Коваль','Андреевна','1992-11-11','+79104234567','hash4','2025-12-08 15:48:15','2025-12-05 22:15:00',1),(5,'sem_m','semyonova@corp.ru','Мария','Семенова','Владимировна','1988-01-25','+79105234567','hash5','2025-06-13 18:10:30','2025-12-08 15:48:15',1),(6,'novikov_n','novikov@corp.ru','Николай','Новиков','Александрович','1975-04-04','+79106234567','hash6','2024-02-23 18:10:30','2025-12-08 14:00:00',0),(7,'vas_l','vasilieva@corp.ru','Людмила','Васильева','Георгиевна','2000-02-10','+79107234567','hash7','2023-01-10 10:00:00','2025-12-08 15:48:15',0),(8,'sm_olga','olga@site.ru','Ольга','Смирнова','Игоревна','1991-07-27','+79108234567','hash8','2024-06-08 00:00:00','2025-12-01 09:00:00',0),(9,'v_sergei','v.sergei@mail.ru','Сергей','Волков','Михайлович','1996-12-05','+79109234567','hash9','2025-12-08 16:11:37',NULL,1),(10,'mishina_a','a.mishina@blog.com','Анастасия','Мишина','Дмитриевна','1993-02-14','+79111234567','hash10','2025-12-08 16:11:37','2025-12-08 16:11:37',0),(11,'korolev_m','m.korolev@company.com','Максим','Королев','Викторович','1984-06-03','+79112234567','hash11','2020-12-08 00:00:00','2025-12-08 16:11:37',0),(12,'zaitseva_e','zaya_e@mail.ru','Елена','Зайцева','Андреевна','1999-09-09','+79113234567','hash12','2025-12-08 16:11:37',NULL,1),(13,'kuzn_d','kuznets_d@corp.ru','Денис','Кузнецов','Евгеньевич','1988-10-10','+79114234567','hash13','2025-12-08 16:11:37','2025-12-08 08:30:00',1),(14,'litv_i','litv_i@site.net','Ирина','Литвинова','Олеговна','1997-01-20','+79115234567','hash14','2023-12-08 00:00:00',NULL,0),(15,'galkin_v','galkin_v@mail.ru','Вадим','Галкин','Русланович','2002-03-30','+79116234567','hash15','2025-12-08 16:11:37','2025-12-08 16:11:37',1),(16,'romanov_a','r.alex@blog.com','Алексей','Романов','Иванович','1994-04-14','+79117234567','hash16','2025-12-08 16:11:37','2025-12-08 15:45:00',1),(17,'m_tat','tatyana_m@company.com','Татьяна','Маслова','Сергеевна','1986-06-06','+79118234567','hash17','2024-10-08 00:00:00','2025-12-08 16:11:37',0),(18,'klimenko_e','e.klim@mail.ru','Егор','Клименко','Витальевич','2000-11-22','+79119234567','hash18','2025-12-08 16:11:37','2025-12-08 16:11:37',1),(19,'mewmew','mewmew@updated.ru','Александра','Березова','Владимировна','1990-09-09','+79120234567','hash19','2025-12-08 16:24:20','2025-12-08 16:24:20',1),(20,'legenda','legendae@old.com','Алина','Захарова','Олеговна','1989-10-10','+79121234567','hash20','2022-12-08 00:00:00','2025-12-08 16:24:20',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-11  9:42:54
