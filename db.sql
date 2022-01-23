CREATE DATABASE  IF NOT EXISTS `nuk_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `nuk_database`;
-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: nuk_database
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `accounts_assistantinfo`
--

DROP TABLE IF EXISTS `accounts_assistantinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_assistantinfo` (
  `info_ptr_id` bigint NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`info_ptr_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_assistantin_user_id_5b0b431c_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_participant` (`id`),
  CONSTRAINT `accounts_assistantinfo_info_ptr_id_e2198532_fk_accounts_info_id` FOREIGN KEY (`info_ptr_id`) REFERENCES `accounts_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_assistantinfo`
--

LOCK TABLES `accounts_assistantinfo` WRITE;
/*!40000 ALTER TABLE `accounts_assistantinfo` DISABLE KEYS */;
INSERT INTO `accounts_assistantinfo` VALUES (3,'0912345678',3);
/*!40000 ALTER TABLE `accounts_assistantinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_expertinfo`
--

DROP TABLE IF EXISTS `accounts_expertinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_expertinfo` (
  `info_ptr_id` bigint NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `title` varchar(20) NOT NULL,
  `address` varchar(100) NOT NULL,
  `bank_account` varchar(14) NOT NULL,
  `company` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`info_ptr_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_expertinfo_info_ptr_id_b9c9afa1_fk_accounts_info_id` FOREIGN KEY (`info_ptr_id`) REFERENCES `accounts_info` (`id`),
  CONSTRAINT `accounts_expertinfo_user_id_3b887c1a_fk_accounts_participant_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_participant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_expertinfo`
--

LOCK TABLES `accounts_expertinfo` WRITE;
/*!40000 ALTER TABLE `accounts_expertinfo` DISABLE KEYS */;
INSERT INTO `accounts_expertinfo` VALUES (1,'','','','','',1);
/*!40000 ALTER TABLE `accounts_expertinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_info`
--

DROP TABLE IF EXISTS `accounts_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_info`
--

LOCK TABLES `accounts_info` WRITE;
/*!40000 ALTER TABLE `accounts_info` DISABLE KEYS */;
INSERT INTO `accounts_info` VALUES (1),(2),(3),(4),(7),(8),(9),(10),(11),(12);
/*!40000 ALTER TABLE `accounts_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_participant`
--

DROP TABLE IF EXISTS `accounts_participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_participant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `identity` int NOT NULL,
  `sex` int NOT NULL,
  `phone` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_participant`
--

LOCK TABLES `accounts_participant` WRITE;
/*!40000 ALTER TABLE `accounts_participant` DISABLE KEYS */;
INSERT INTO `accounts_participant` VALUES (1,'pbkdf2_sha256$260000$PI1Le2oIwRHA132kDCPARA$QUlaKzIt2tAWuhimvxMaIphLuaSlyemOBc76kic/wiM=','2022-01-23 10:20:39.265325',1,'admin','admin','admin',1,1,'2021-12-31 16:15:56.000000','admin@gmail.com',3,2,''),(2,'pbkdf2_sha256$260000$xqzVzeBiZ0P9XDDMKE1VZt$91NZIE334c8kgIvlUf3Q5z/GjNb9kNCLoLFnRjbLkxM=','2021-12-31 16:26:34.000000',0,'test','1','test',0,1,'2021-12-31 16:25:27.000000','test@gmail.com',1,2,'0912345678'),(3,'pbkdf2_sha256$260000$gcsUtaxzdxXDslRies3WpN$r3jo15e3DDbRjR32/pIQgKkXFbV0Jyyq7V6ELEiICgw=','2022-01-01 07:14:24.777441',0,'test2','2','test',0,1,'2022-01-01 07:14:16.781195','test2@gmail.com',3,2,'0912345678'),(4,'pbkdf2_sha256$260000$BEFhAB5Q8apK9Kg9x9MiXL$LnfAZU/cA5IchOTFo92FN1xCsM94NwMnA80xPHb836g=','2022-01-01 16:06:09.520259',0,'test3','3','test',0,1,'2022-01-01 07:15:16.012007','test3@gmail.com',4,2,'0912345678'),(7,'pbkdf2_sha256$260000$HQ5QnfyUtVla0DiSoXCvjT$L8Dh/CgXvJz7araxj5ZFSiB+AQbAMl6i0OFjr60Ef4k=','2022-01-22 23:18:25.686253',0,'teacher','師','老',0,1,'2022-01-22 23:18:08.213669','teacher@gmail.com',4,2,'09121231123'),(8,'pbkdf2_sha256$260000$rYZFTqurR6xpgLrGEq9EW4$5IKqY1S0wMwX+xzHxVUrDffq5Z45POFvDkiSFbBUGe4=','2022-01-22 23:50:35.719731',0,'a1085515','彥輔','曾',0,1,'2022-01-22 23:50:22.244796','a1085515@mail.nuk.edu.tw',1,2,'09123123123'),(9,'pbkdf2_sha256$260000$9jx2XMyWFlrksvyZ4jGIxs$SmwndBJJp5AqgfHai0ttySNuq0md4ZIZBQT9WYFX2nY=','2022-01-22 23:53:30.596615',0,'a1085502','佾遑','謝',0,1,'2022-01-22 23:53:21.467515','a1085502@mail.nuk.edu.tw',1,2,'09123123123'),(10,'pbkdf2_sha256$260000$BHdSSX9hqUrA7rcimbg11y$RVL514PCfSc266dLqk48wksGr5l7JIFMwr1B+KLyHTA=','2022-01-22 23:54:45.000000',0,'a1085509','聖耀','林',0,1,'2022-01-22 23:54:28.000000','a1085509@mail.nuk.edu.tw',1,2,'09123123123'),(11,'pbkdf2_sha256$260000$FW30wQSUK4udFqGH7Uy57r$6TyS0NfUkqZGwNhq77Uju07GAFm8yneWuTG9PqEkhpc=','2022-01-22 23:55:38.825978',0,'a1085504','修維','吳',0,1,'2022-01-22 23:55:18.276673','a1085504@mail.nuk.edu.tw',1,2,'09123123123'),(12,'pbkdf2_sha256$260000$zo7qTk3MjesNDJLxkBVr3w$W977qnwANF1lQvYdfGhdtuYdf/+BStSnrWhfTKBeUns=','2022-01-23 10:20:13.167505',0,'tofu1234','fu','to',0,1,'2022-01-23 10:20:07.605643','alex7008uk@gmail.com',1,2,'0912345678');
/*!40000 ALTER TABLE `accounts_participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_participant_groups`
--

DROP TABLE IF EXISTS `accounts_participant_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_participant_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `participant_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_participant_gro_participant_id_group_id_0af182db_uniq` (`participant_id`,`group_id`),
  KEY `accounts_participant_groups_group_id_de9c439b_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_participant_groups_group_id_de9c439b_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_participant_participant_id_3f5b592c_fk_accounts_` FOREIGN KEY (`participant_id`) REFERENCES `accounts_participant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_participant_groups`
--

LOCK TABLES `accounts_participant_groups` WRITE;
/*!40000 ALTER TABLE `accounts_participant_groups` DISABLE KEYS */;
INSERT INTO `accounts_participant_groups` VALUES (2,2,2),(1,3,1),(3,4,2),(6,7,2),(7,8,2),(8,9,2),(9,10,2),(10,11,2),(11,12,2);
/*!40000 ALTER TABLE `accounts_participant_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_participant_user_permissions`
--

DROP TABLE IF EXISTS `accounts_participant_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_participant_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `participant_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_participant_use_participant_id_permissio_2f38aad7_uniq` (`participant_id`,`permission_id`),
  KEY `accounts_participant_permission_id_8f77b4a1_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_participant_participant_id_0b66aa07_fk_accounts_` FOREIGN KEY (`participant_id`) REFERENCES `accounts_participant` (`id`),
  CONSTRAINT `accounts_participant_permission_id_8f77b4a1_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_participant_user_permissions`
--

LOCK TABLES `accounts_participant_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_participant_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_participant_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_professorinfo`
--

DROP TABLE IF EXISTS `accounts_professorinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_professorinfo` (
  `info_ptr_id` bigint NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `title` varchar(20) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`info_ptr_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_professorin_user_id_cc33fa51_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_participant` (`id`),
  CONSTRAINT `accounts_professorinfo_info_ptr_id_23e94ec1_fk_accounts_info_id` FOREIGN KEY (`info_ptr_id`) REFERENCES `accounts_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_professorinfo`
--

LOCK TABLES `accounts_professorinfo` WRITE;
/*!40000 ALTER TABLE `accounts_professorinfo` DISABLE KEYS */;
INSERT INTO `accounts_professorinfo` VALUES (4,'0912345678','助理教授',4),(7,'(07) 591-9518','專任教師',7);
/*!40000 ALTER TABLE `accounts_professorinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_studentinfo`
--

DROP TABLE IF EXISTS `accounts_studentinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_studentinfo` (
  `info_ptr_id` bigint NOT NULL,
  `student_id` varchar(15) NOT NULL,
  `school_system` varchar(10) NOT NULL,
  `grade` varchar(10) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`info_ptr_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_studentinfo_info_ptr_id_0f8b5ae2_fk_accounts_info_id` FOREIGN KEY (`info_ptr_id`) REFERENCES `accounts_info` (`id`),
  CONSTRAINT `accounts_studentinfo_user_id_064d0795_fk_accounts_participant_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_participant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_studentinfo`
--

LOCK TABLES `accounts_studentinfo` WRITE;
/*!40000 ALTER TABLE `accounts_studentinfo` DISABLE KEYS */;
INSERT INTO `accounts_studentinfo` VALUES (2,'','','',2),(8,'a1085515','大學部','三年級',8),(9,'a1085502','大學部','三年級',9),(10,'a1085509','大學部','三年級',10),(11,'a1085504','大學部','三年級',11),(12,'A1085515','大學部','三年級',12);
/*!40000 ALTER TABLE `accounts_studentinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_teacherinfo`
--

DROP TABLE IF EXISTS `accounts_teacherinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_teacherinfo` (
  `info_ptr_id` bigint NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `title` varchar(20) NOT NULL,
  `address` varchar(100) NOT NULL,
  `bank_account` varchar(14) NOT NULL,
  `school` varchar(50) NOT NULL,
  `department` varchar(20) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`info_ptr_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_teacherinfo_info_ptr_id_0aa578a9_fk_accounts_info_id` FOREIGN KEY (`info_ptr_id`) REFERENCES `accounts_info` (`id`),
  CONSTRAINT `accounts_teacherinfo_user_id_68752682_fk_accounts_participant_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_participant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_teacherinfo`
--

LOCK TABLES `accounts_teacherinfo` WRITE;
/*!40000 ALTER TABLE `accounts_teacherinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_teacherinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'normal_users'),(1,'operators');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,21),(2,1,22),(3,1,23),(4,1,24),(5,1,25),(6,1,26),(7,1,27),(8,1,28),(9,1,29),(10,1,30),(11,1,31),(12,1,32),(13,1,33),(14,1,34),(15,1,35),(16,1,36),(17,1,37),(18,1,38),(19,1,39),(20,1,40),(21,1,41),(22,1,42),(23,1,43),(24,1,44),(25,1,45),(26,1,47),(27,1,48),(28,1,49),(29,1,50),(30,1,51),(31,1,52),(32,1,53),(33,1,54),(34,1,55),(35,1,56),(36,1,58),(37,1,59),(38,1,60),(53,2,24),(52,2,28),(39,2,32),(40,2,36),(41,2,40),(42,2,44),(43,2,45),(44,2,46),(45,2,47),(46,2,48),(47,2,50),(48,2,52),(49,2,53),(50,2,56),(51,2,57);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add attendance',6,'add_attendance'),(22,'Can change attendance',6,'change_attendance'),(23,'Can delete attendance',6,'delete_attendance'),(24,'Can view attendance',6,'view_attendance'),(25,'Can add meeting',7,'add_meeting'),(26,'Can change meeting',7,'change_meeting'),(27,'Can delete meeting',7,'delete_meeting'),(28,'Can view meeting',7,'view_meeting'),(29,'Can add extempore motion',8,'add_extemporemotion'),(30,'Can change extempore motion',8,'change_extemporemotion'),(31,'Can delete extempore motion',8,'delete_extemporemotion'),(32,'Can view extempore motion',8,'view_extemporemotion'),(33,'Can add discussion',9,'add_discussion'),(34,'Can change discussion',9,'change_discussion'),(35,'Can delete discussion',9,'delete_discussion'),(36,'Can view discussion',9,'view_discussion'),(37,'Can add appendix',10,'add_appendix'),(38,'Can change appendix',10,'change_appendix'),(39,'Can delete appendix',10,'delete_appendix'),(40,'Can view appendix',10,'view_appendix'),(41,'Can add announcement',11,'add_announcement'),(42,'Can change announcement',11,'change_announcement'),(43,'Can delete announcement',11,'delete_announcement'),(44,'Can view announcement',11,'view_announcement'),(45,'Can add edit request',12,'add_editrequest'),(46,'Can change edit request',12,'change_editrequest'),(47,'Can delete edit request',12,'delete_editrequest'),(48,'Can view edit request',12,'view_editrequest'),(49,'Can add info',13,'add_info'),(50,'Can change info',13,'change_info'),(51,'Can delete info',13,'delete_info'),(52,'Can view info',13,'view_info'),(53,'Can add participant',14,'add_participant'),(54,'Can change participant',14,'change_participant'),(55,'Can delete participant',14,'delete_participant'),(56,'Can view participant',14,'view_participant'),(57,'發出會議紀錄修改請求',14,'create_edit_request'),(58,'新增臨時動議',14,'create_extempore_motion'),(59,'寄出會議通知',14,'mail_notification'),(60,'寄出開會結果',14,'mail_result'),(61,'Can add teacher info',15,'add_teacherinfo'),(62,'Can change teacher info',15,'change_teacherinfo'),(63,'Can delete teacher info',15,'delete_teacherinfo'),(64,'Can view teacher info',15,'view_teacherinfo'),(65,'Can add student info',16,'add_studentinfo'),(66,'Can change student info',16,'change_studentinfo'),(67,'Can delete student info',16,'delete_studentinfo'),(68,'Can view student info',16,'view_studentinfo'),(69,'Can add professor info',17,'add_professorinfo'),(70,'Can change professor info',17,'change_professorinfo'),(71,'Can delete professor info',17,'delete_professorinfo'),(72,'Can view professor info',17,'view_professorinfo'),(73,'Can add expert info',18,'add_expertinfo'),(74,'Can change expert info',18,'change_expertinfo'),(75,'Can delete expert info',18,'delete_expertinfo'),(76,'Can view expert info',18,'view_expertinfo'),(77,'Can add assistant info',19,'add_assistantinfo'),(78,'Can change assistant info',19,'change_assistantinfo'),(79,'Can delete assistant info',19,'delete_assistantinfo'),(80,'Can view assistant info',19,'view_assistantinfo'),(81,'Can add source',20,'add_source'),(82,'Can change source',20,'change_source'),(83,'Can delete source',20,'delete_source'),(84,'Can view source',20,'view_source'),(85,'Can add thumbnail',21,'add_thumbnail'),(86,'Can change thumbnail',21,'change_thumbnail'),(87,'Can delete thumbnail',21,'delete_thumbnail'),(88,'Can view thumbnail',21,'view_thumbnail'),(89,'Can add thumbnail dimensions',22,'add_thumbnaildimensions'),(90,'Can change thumbnail dimensions',22,'change_thumbnaildimensions'),(91,'Can delete thumbnail dimensions',22,'delete_thumbnaildimensions'),(92,'Can view thumbnail dimensions',22,'view_thumbnaildimensions');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_participant_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_participant_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_participant` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-12-31 16:18:30.157982','1','operators',1,'[{\"added\": {}}]',3,1),(2,'2021-12-31 16:19:42.515149','2','normal_participants',1,'[{\"added\": {}}]',3,1),(3,'2021-12-31 16:20:14.521663','1','adminadmin',2,'[{\"changed\": {\"fields\": [\"\\u59d3\\u6c0f\", \"\\u540d\\u7a31\", \"\\u8eab\\u5206\"]}}]',14,1),(4,'2021-12-31 16:26:05.051327','2','normal_users',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',3,1),(5,'2022-01-01 07:14:53.618412','2','test1',2,'[{\"changed\": {\"fields\": [\"\\u8eab\\u5206\", \"Groups\"]}}]',14,1),(6,'2022-01-22 23:39:13.687444','6','曾彥輔',3,'',14,1),(7,'2022-01-22 23:52:48.924305','5','葦名一心',3,'',14,1),(8,'2022-01-23 10:07:00.733500','1','adminadmin',2,'[{\"changed\": {\"fields\": [\"\\u8eab\\u5206\"]}}]',14,1),(9,'2022-01-23 10:07:37.762706','1','adminadmin',2,'[{\"changed\": {\"fields\": [\"\\u8eab\\u5206\"]}}]',14,1),(10,'2022-01-23 10:08:15.237027','1','adminadmin',2,'[{\"changed\": {\"fields\": [\"\\u8eab\\u5206\"]}}]',14,1),(11,'2022-01-23 10:11:23.835813','1','adminadmin',2,'[{\"changed\": {\"fields\": [\"\\u8eab\\u5206\"]}}]',14,1),(12,'2022-01-23 10:11:51.871731','1','adminadmin',2,'[{\"changed\": {\"fields\": [\"\\u8eab\\u5206\"]}}]',14,1),(13,'2022-01-23 10:13:02.600598','10','林聖耀',2,'[{\"changed\": {\"fields\": [\"\\u540d\\u7a31\", \"\\u8eab\\u5206\"]}}]',14,1),(14,'2022-01-23 10:24:59.768766','8','測試會議結果',3,'',7,1),(15,'2022-01-23 10:25:54.894628','7','測試寄信',3,'',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (19,'accounts','assistantinfo'),(18,'accounts','expertinfo'),(13,'accounts','info'),(14,'accounts','participant'),(17,'accounts','professorinfo'),(16,'accounts','studentinfo'),(15,'accounts','teacherinfo'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(20,'easy_thumbnails','source'),(21,'easy_thumbnails','thumbnail'),(22,'easy_thumbnails','thumbnaildimensions'),(11,'meetings','announcement'),(10,'meetings','appendix'),(6,'meetings','attendance'),(9,'meetings','discussion'),(12,'meetings','editrequest'),(8,'meetings','extemporemotion'),(7,'meetings','meeting'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-12-31 16:12:15.361403'),(2,'contenttypes','0002_remove_content_type_name','2021-12-31 16:12:15.438869'),(3,'auth','0001_initial','2021-12-31 16:12:15.672839'),(4,'auth','0002_alter_permission_name_max_length','2021-12-31 16:12:15.767359'),(5,'auth','0003_alter_user_email_max_length','2021-12-31 16:12:15.780872'),(6,'auth','0004_alter_user_username_opts','2021-12-31 16:12:15.790818'),(7,'auth','0005_alter_user_last_login_null','2021-12-31 16:12:15.802820'),(8,'auth','0006_require_contenttypes_0002','2021-12-31 16:12:15.809822'),(9,'auth','0007_alter_validators_add_error_messages','2021-12-31 16:12:15.821858'),(10,'auth','0008_alter_user_username_max_length','2021-12-31 16:12:15.834831'),(11,'auth','0009_alter_user_last_name_max_length','2021-12-31 16:12:15.840111'),(12,'auth','0010_alter_group_name_max_length','2021-12-31 16:12:15.855816'),(13,'auth','0011_update_proxy_permissions','2021-12-31 16:12:15.861817'),(14,'auth','0012_alter_user_first_name_max_length','2021-12-31 16:12:15.867819'),(15,'accounts','0001_initial','2021-12-31 16:12:17.089920'),(16,'accounts','0002_alter_participant_options','2021-12-31 16:12:17.099967'),(17,'admin','0001_initial','2021-12-31 16:12:17.228392'),(18,'admin','0002_logentry_remove_auto_add','2021-12-31 16:12:17.238859'),(19,'admin','0003_logentry_add_action_flag_choices','2021-12-31 16:12:17.248861'),(20,'easy_thumbnails','0001_initial','2021-12-31 16:12:17.590483'),(21,'easy_thumbnails','0002_thumbnaildimensions','2021-12-31 16:12:17.755629'),(22,'meetings','0001_initial','2021-12-31 16:12:18.445729'),(23,'meetings','0002_auto_20220101_0012','2021-12-31 16:12:19.456203'),(24,'sessions','0001_initial','2021-12-31 16:12:19.499283'),(25,'accounts','0003_alter_participant_options','2022-01-01 16:09:39.574576');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('8h64eghbd1a2zohjwwy9h5dzc7r6jbzm','.eJxVjDsOwjAQBe_iGln-x6Gk5wzWrteLA8iR4qRC3B0ipYD2zcx7iQTbWtPWy5ImEmehxel3Q8iP0nZAd2i3Wea5rcuEclfkQbu8zlSel8P9O6jQ67cu7MAEy16BcyaSA01oIgyI0UUib4JH661i8jbnPARgHjXDiE4BkXh_APDuOLU:1nBSUh:IuWtV5b82sF6jgFqaZOuCyeMK0DVrq_62Hoa8q5Qwlc','2022-02-06 10:20:39.269325'),('akc9hgedt62owl1xwvmf1cna3dv6j8b2','.eJxVjDsOwjAQBe_iGln-x6Gk5wzWrteLA8iR4qRC3B0ipYD2zcx7iQTbWtPWy5ImEmehxel3Q8iP0nZAd2i3Wea5rcuEclfkQbu8zlSel8P9O6jQ67cu7MAEy16BcyaSA01oIgyI0UUib4JH661i8jbnPARgHjXDiE4BkXh_APDuOLU:1nBCSU:NsH64aqvFJLMKMcteYY_ECtKNagwYOUh4fYjqUkLXHU','2022-02-05 17:13:18.051246'),('di019xd7tkj8ij4z5i39w8e63viru5bp','.eJxVjEEOwiAQRe_C2hAHsBSX7j0DmWEGqRpISrsy3l2bdKHb_977LxVxXUpcu8xxYnVWAOrwOxKmh9SN8B3rrenU6jJPpDdF77Tra2N5Xnb376BgL98aDQNJ5pRPOYRAaEew3ooVHzAADOSPnhkcUAaLFsCRASdinODgRvX-AB_9OCY:1nBIjq:57kTzim6C3qUyuP2Q1zJg2P596TyUCodgKSs-VGgw1k','2022-02-05 23:55:38.829005'),('dwybj7qbixzqzp2jbbnt4wm6sbmjj26l','.eJxVjDsOwjAQBe_iGln-x6Gk5wzWrteLA8iR4qRC3B0ipYD2zcx7iQTbWtPWy5ImEmehxel3Q8iP0nZAd2i3Wea5rcuEclfkQbu8zlSel8P9O6jQ67cu7MAEy16BcyaSA01oIgyI0UUib4JH661i8jbnPARgHjXDiE4BkXh_APDuOLU:1nBIqt:31BPOQItivRU3JoNLLxcCKsmBi_UI4mDp-KRRspo4IA','2022-02-06 00:02:55.882881'),('zt8sx1oihcfdt9phnrkkf4nzdcje3jfq','.eJxVjDsOwjAQBe_iGln-x6Gk5wzWrteLA8iR4qRC3B0ipYD2zcx7iQTbWtPWy5ImEmehxel3Q8iP0nZAd2i3Wea5rcuEclfkQbu8zlSel8P9O6jQ67cu7MAEy16BcyaSA01oIgyI0UUib4JH661i8jbnPARgHjXDiE4BkXh_APDuOLU:1n3dVc:4ZrTI8H4FutwB-BP8e8z3hkloPaNtn74FvTk-JHFx64','2022-01-15 20:29:16.221805');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_source`
--

DROP TABLE IF EXISTS `easy_thumbnails_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easy_thumbnails_source` (
  `id` int NOT NULL AUTO_INCREMENT,
  `storage_hash` varchar(40) NOT NULL,
  `name` varchar(255) NOT NULL,
  `modified` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `easy_thumbnails_source_storage_hash_name_481ce32d_uniq` (`storage_hash`,`name`),
  KEY `easy_thumbnails_source_storage_hash_946cbcc9` (`storage_hash`),
  KEY `easy_thumbnails_source_name_5fe0edc6` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_source`
--

LOCK TABLES `easy_thumbnails_source` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_source` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_thumbnail`
--

DROP TABLE IF EXISTS `easy_thumbnails_thumbnail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easy_thumbnails_thumbnail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `storage_hash` varchar(40) NOT NULL,
  `name` varchar(255) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `source_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `easy_thumbnails_thumbnai_storage_hash_name_source_fb375270_uniq` (`storage_hash`,`name`,`source_id`),
  KEY `easy_thumbnails_thum_source_id_5b57bc77_fk_easy_thum` (`source_id`),
  KEY `easy_thumbnails_thumbnail_storage_hash_f1435f49` (`storage_hash`),
  KEY `easy_thumbnails_thumbnail_name_b5882c31` (`name`),
  CONSTRAINT `easy_thumbnails_thum_source_id_5b57bc77_fk_easy_thum` FOREIGN KEY (`source_id`) REFERENCES `easy_thumbnails_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_thumbnail`
--

LOCK TABLES `easy_thumbnails_thumbnail` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnail` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_thumbnaildimensions`
--

DROP TABLE IF EXISTS `easy_thumbnails_thumbnaildimensions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easy_thumbnails_thumbnaildimensions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `thumbnail_id` int NOT NULL,
  `width` int unsigned DEFAULT NULL,
  `height` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `thumbnail_id` (`thumbnail_id`),
  CONSTRAINT `easy_thumbnails_thum_thumbnail_id_c3a0c549_fk_easy_thum` FOREIGN KEY (`thumbnail_id`) REFERENCES `easy_thumbnails_thumbnail` (`id`),
  CONSTRAINT `easy_thumbnails_thumbnaildimensions_chk_1` CHECK ((`width` >= 0)),
  CONSTRAINT `easy_thumbnails_thumbnaildimensions_chk_2` CHECK ((`height` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_thumbnaildimensions`
--

LOCK TABLES `easy_thumbnails_thumbnaildimensions` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnaildimensions` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnaildimensions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_announcement`
--

DROP TABLE IF EXISTS `meetings_announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings_announcement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` varchar(500) NOT NULL,
  `meeting_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `meetings_announcement_meeting_id_8e2c49c7_fk_meetings_meeting_id` (`meeting_id`),
  CONSTRAINT `meetings_announcement_meeting_id_8e2c49c7_fk_meetings_meeting_id` FOREIGN KEY (`meeting_id`) REFERENCES `meetings_meeting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_announcement`
--

LOCK TABLES `meetings_announcement` WRITE;
/*!40000 ALTER TABLE `meetings_announcement` DISABLE KEYS */;
INSERT INTO `meetings_announcement` VALUES (1,'無',1),(2,'測試啦',4),(3,'ㄏ',4),(4,'事項1',5),(5,'沒啥',NULL),(6,'123',2),(7,'就是ㄍ報告事項',NULL),(8,'測試',9),(9,'123',10),(10,'安安',11),(11,'空',12);
/*!40000 ALTER TABLE `meetings_announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_appendix`
--

DROP TABLE IF EXISTS `meetings_appendix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings_appendix` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `provider` varchar(100) NOT NULL,
  `file` varchar(100) NOT NULL,
  `meeting_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `meetings_appendix_meeting_id_ca937e70_fk_meetings_meeting_id` (`meeting_id`),
  CONSTRAINT `meetings_appendix_meeting_id_ca937e70_fk_meetings_meeting_id` FOREIGN KEY (`meeting_id`) REFERENCES `meetings_meeting` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_appendix`
--

LOCK TABLES `meetings_appendix` WRITE;
/*!40000 ALTER TABLE `meetings_appendix` DISABLE KEYS */;
/*!40000 ALTER TABLE `meetings_appendix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_attendance`
--

DROP TABLE IF EXISTS `meetings_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `attend` tinyint(1) NOT NULL,
  `meeting_id` bigint DEFAULT NULL,
  `participant_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `meetings_attendance_meeting_id_296f48af_fk_meetings_meeting_id` (`meeting_id`),
  KEY `meetings_attendance_participant_id_61f55d1b_fk_accounts_` (`participant_id`),
  CONSTRAINT `meetings_attendance_meeting_id_296f48af_fk_meetings_meeting_id` FOREIGN KEY (`meeting_id`) REFERENCES `meetings_meeting` (`id`),
  CONSTRAINT `meetings_attendance_participant_id_61f55d1b_fk_accounts_` FOREIGN KEY (`participant_id`) REFERENCES `accounts_participant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_attendance`
--

LOCK TABLES `meetings_attendance` WRITE;
/*!40000 ALTER TABLE `meetings_attendance` DISABLE KEYS */;
INSERT INTO `meetings_attendance` VALUES (1,0,1,1),(2,0,2,1),(3,0,2,2),(4,0,3,1),(5,0,3,2),(6,0,3,3),(7,0,3,4),(8,0,4,2),(9,0,4,3),(10,0,5,1),(11,0,5,2),(12,0,5,3),(13,0,5,4),(14,0,6,1),(15,0,6,2),(16,0,6,3),(17,0,NULL,1),(18,0,NULL,2),(19,0,NULL,3),(20,0,NULL,4),(21,0,NULL,NULL),(22,0,NULL,1),(23,0,NULL,7),(24,0,NULL,8),(25,0,NULL,9),(26,0,NULL,11),(27,0,NULL,10),(28,0,9,8),(29,0,9,9),(30,0,9,10),(31,0,9,11),(32,0,9,12),(33,0,10,1),(34,0,10,2),(35,0,10,3),(36,0,10,4),(37,0,10,7),(38,0,10,8),(39,0,10,9),(40,0,10,10),(41,0,10,11),(42,0,10,12),(43,0,11,7),(44,0,11,8),(45,0,11,9),(46,0,11,10),(47,0,11,11),(48,0,11,12),(49,0,12,1),(50,0,12,2),(51,0,12,7),(52,0,12,8),(53,0,12,9),(54,0,12,10),(55,0,12,11),(56,0,12,12);
/*!40000 ALTER TABLE `meetings_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_discussion`
--

DROP TABLE IF EXISTS `meetings_discussion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings_discussion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `topic` varchar(25) NOT NULL,
  `description` varchar(500) NOT NULL,
  `resolution` varchar(150) NOT NULL,
  `meeting_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `meetings_discussion_meeting_id_b243ae0a_fk_meetings_meeting_id` (`meeting_id`),
  CONSTRAINT `meetings_discussion_meeting_id_b243ae0a_fk_meetings_meeting_id` FOREIGN KEY (`meeting_id`) REFERENCES `meetings_meeting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_discussion`
--

LOCK TABLES `meetings_discussion` WRITE;
/*!40000 ALTER TABLE `meetings_discussion` DISABLE KEYS */;
INSERT INTO `meetings_discussion` VALUES (1,'123','123','無',1),(2,'腳踏車壞了啦','如題','修',2),(3,'123','123','123',3),(4,'123','123','',4),(5,'456','456','456',4),(6,'就這樣','嗎','無',5),(7,'你說什麼','你懂個屁 呆子','無',5),(8,'測','試','無',6),(9,'不知道','嘻嘻','無',NULL),(10,'123','123','123',2),(11,'測試一','測試一的說明','測試一的決議',NULL),(12,'測試二','測試二的說明','測試二的決議',NULL),(13,'測試三','測試三的說明','測試三的決議',NULL),(14,'1','2','3',9),(15,'123','123','123',10),(16,'案由','說明','決議',11),(17,'案由二','說明二','決議二',11),(18,'案由三','說明三','決議三',11),(19,'123','123','123',12);
/*!40000 ALTER TABLE `meetings_discussion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_editrequest`
--

DROP TABLE IF EXISTS `meetings_editrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings_editrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `meeting_id` bigint DEFAULT NULL,
  `participant_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `meetings_editrequest_meeting_id_c6895259_fk_meetings_meeting_id` (`meeting_id`),
  KEY `meetings_editrequest_participant_id_871e6f53_fk_accounts_` (`participant_id`),
  CONSTRAINT `meetings_editrequest_meeting_id_c6895259_fk_meetings_meeting_id` FOREIGN KEY (`meeting_id`) REFERENCES `meetings_meeting` (`id`),
  CONSTRAINT `meetings_editrequest_participant_id_871e6f53_fk_accounts_` FOREIGN KEY (`participant_id`) REFERENCES `accounts_participant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_editrequest`
--

LOCK TABLES `meetings_editrequest` WRITE;
/*!40000 ALTER TABLE `meetings_editrequest` DISABLE KEYS */;
INSERT INTO `meetings_editrequest` VALUES (1,'測試 新補ㄉ',1,1),(2,'哈哈是我啦',1,2),(3,'ㄟ...試試看',2,1),(4,'測一下啦\r\n123\r\n123\r\n123',NULL,1),(5,'安安',3,1);
/*!40000 ALTER TABLE `meetings_editrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_extemporemotion`
--

DROP TABLE IF EXISTS `meetings_extemporemotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings_extemporemotion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proposer` varchar(100) NOT NULL,
  `content` varchar(500) NOT NULL,
  `meeting_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `meetings_extemporemo_meeting_id_f06ec7ec_fk_meetings_` (`meeting_id`),
  CONSTRAINT `meetings_extemporemo_meeting_id_f06ec7ec_fk_meetings_` FOREIGN KEY (`meeting_id`) REFERENCES `meetings_meeting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_extemporemotion`
--

LOCK TABLES `meetings_extemporemotion` WRITE;
/*!40000 ALTER TABLE `meetings_extemporemotion` DISABLE KEYS */;
INSERT INTO `meetings_extemporemotion` VALUES (1,'123','231',2);
/*!40000 ALTER TABLE `meetings_extemporemotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_meeting`
--

DROP TABLE IF EXISTS `meetings_meeting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings_meeting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `type` int NOT NULL,
  `date` datetime(6) NOT NULL,
  `location` varchar(100) NOT NULL,
  `chairman_id` bigint DEFAULT NULL,
  `minutes_taker_id` bigint DEFAULT NULL,
  `speech` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `meetings_meeting_chairman_id_bed8588d` (`chairman_id`),
  KEY `meetings_meeting_minutes_taker_id_d4885056` (`minutes_taker_id`),
  CONSTRAINT `meetings_meeting_chairman_id_bed8588d_fk_accounts_participant_id` FOREIGN KEY (`chairman_id`) REFERENCES `accounts_participant` (`id`),
  CONSTRAINT `meetings_meeting_minutes_taker_id_d4885056_fk_accounts_` FOREIGN KEY (`minutes_taker_id`) REFERENCES `accounts_participant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_meeting`
--

LOCK TABLES `meetings_meeting` WRITE;
/*!40000 ALTER TABLE `meetings_meeting` DISABLE KEYS */;
INSERT INTO `meetings_meeting` VALUES (1,'第一場會議',0,'2021-12-31 16:20:00.000000','高雄大學工學院',1,1,'略'),(2,'第二個會議',2,'2022-01-04 22:50:00.000000','高雄大學管理學院',2,1,'大家好'),(3,'測試',2,'2021-12-10 10:30:00.000000','高雄大學工學院',1,4,'略'),(4,'測試2',0,'2021-12-23 06:50:00.000000','高雄大學工學院',2,3,'略'),(5,'測試3',4,'2022-01-01 15:57:00.000000','某個地方',1,3,'略'),(6,'測試4',0,'2022-01-10 07:30:00.000000','法學院',2,3,'略'),(9,'測',1,'2022-01-13 10:20:00.000000','高雄大學工學院',1,7,'略'),(10,'測試寄信',2,'2022-01-23 10:25:00.000000','高雄大學工學院',1,7,'略'),(11,'測試寄信2',3,'2022-01-26 03:26:00.000000','法學院',8,9,'略'),(12,'測試寄信3',4,'2022-01-05 20:31:00.000000','管院',7,11,'略');
/*!40000 ALTER TABLE `meetings_meeting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_meeting_participants`
--

DROP TABLE IF EXISTS `meetings_meeting_participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings_meeting_participants` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `meeting_id` bigint NOT NULL,
  `participant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `meetings_meeting_partici_meeting_id_participant_i_235fa39f_uniq` (`meeting_id`,`participant_id`),
  KEY `meetings_meeting_par_participant_id_5629b5f3_fk_accounts_` (`participant_id`),
  CONSTRAINT `meetings_meeting_par_meeting_id_258b53bf_fk_meetings_` FOREIGN KEY (`meeting_id`) REFERENCES `meetings_meeting` (`id`),
  CONSTRAINT `meetings_meeting_par_participant_id_5629b5f3_fk_accounts_` FOREIGN KEY (`participant_id`) REFERENCES `accounts_participant` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_meeting_participants`
--

LOCK TABLES `meetings_meeting_participants` WRITE;
/*!40000 ALTER TABLE `meetings_meeting_participants` DISABLE KEYS */;
INSERT INTO `meetings_meeting_participants` VALUES (1,1,1),(2,2,1),(3,2,2),(4,3,1),(5,3,2),(6,3,3),(7,3,4),(8,4,2),(9,4,3),(10,5,1),(11,5,2),(12,5,3),(13,5,4),(14,6,1),(15,6,2),(16,6,3),(28,9,8),(29,9,9),(30,9,10),(31,9,11),(32,9,12),(33,10,1),(34,10,2),(35,10,3),(36,10,4),(37,10,7),(38,10,8),(39,10,9),(40,10,10),(41,10,11),(42,10,12),(43,11,7),(44,11,8),(45,11,9),(46,11,10),(47,11,11),(48,11,12),(49,12,1),(50,12,2),(51,12,7),(52,12,8),(53,12,9),(54,12,10),(55,12,11),(56,12,12);
/*!40000 ALTER TABLE `meetings_meeting_participants` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-23 10:57:14
