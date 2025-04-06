-- MySQL dump 10.13  Distrib 9.2.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: hotpot_db
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `album`
--

DROP TABLE IF EXISTS `album`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `album` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `artist` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `release_date` date DEFAULT NULL,
  `genre` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cover_image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `youtube_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `album`
--

LOCK TABLES `album` WRITE;
/*!40000 ALTER TABLE `album` DISABLE KEYS */;
INSERT INTO `album` VALUES (1,'DAMN.','Kendrick Lamar','2025-04-06','rap, hip-hop','https://lastfm.freetls.fastly.net/i/u/300x300/8a59ed3a9c71cb5113325e2026889e4a.png',NULL,'2025-04-06 08:22:36'),(2,'The Fame','Lady Gaga','2025-04-06','pop, dance','https://lastfm.freetls.fastly.net/i/u/300x300/3e5b462bdb66bae536bc9372b3ca9d6b.jpg',NULL,'2025-04-06 08:22:36'),(3,'Starboy','The Weeknd','2025-04-06','rnb, lana del rey','https://lastfm.freetls.fastly.net/i/u/300x300/08e3f15aca0423b084fb49f342756f3b.png',NULL,'2025-04-06 08:22:38'),(4,'Flower Boy','Tyler, The Creator','2025-04-06','rap, tyler the creator','https://lastfm.freetls.fastly.net/i/u/300x300/52a7f32bdc99238080b0f17e859b3b4d.jpg',NULL,'2025-04-06 08:22:39'),(5,'WHEN WE ALL FALL ASLEEP, WHERE DO WE GO?','Billie Eilish','2025-04-06','electropop, pop','https://lastfm.freetls.fastly.net/i/u/300x300/c2652de4809e5b4349565518b34b85ca.jpg',NULL,'2025-04-06 08:22:39'),(6,'The Rise and Fall of a Midwest Princess','Chappell Roan','2025-04-06','2023, pop','https://lastfm.freetls.fastly.net/i/u/300x300/acd4dcd1ffdc64da01273b1e3512a708.jpg',NULL,'2025-04-06 08:22:40'),(7,'Graduation','Kanye West','2025-04-06','hip-hop, rap','https://lastfm.freetls.fastly.net/i/u/300x300/8ddd1959a2bef460a5149b3e0cf5e18a.png',NULL,'2025-04-06 08:22:40'),(8,'BRAT','Charli xcx','2025-04-06','2024, electropop','https://lastfm.freetls.fastly.net/i/u/300x300/b00527c6ae0cd1d4c9bf3706b130ad56.jpg',NULL,'2025-04-06 08:22:41');
/*!40000 ALTER TABLE `album` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlist`
--

DROP TABLE IF EXISTS `playlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `cover_image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_id` int NOT NULL,
  `is_public` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `playlist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlist`
--

LOCK TABLES `playlist` WRITE;
/*!40000 ALTER TABLE `playlist` DISABLE KEYS */;
INSERT INTO `playlist` VALUES (1,'테스트 플레이리스트','테스트용 플레이리스트입니다.',NULL,'2025-04-06 08:22:41','2025-04-06 08:22:41',1,1);
/*!40000 ALTER TABLE `playlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlist_song`
--

DROP TABLE IF EXISTS `playlist_song`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlist_song` (
  `playlist_id` int NOT NULL,
  `song_id` int NOT NULL,
  `added_at` datetime DEFAULT NULL,
  PRIMARY KEY (`playlist_id`,`song_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `playlist_song_ibfk_1` FOREIGN KEY (`playlist_id`) REFERENCES `playlist` (`id`),
  CONSTRAINT `playlist_song_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `song` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlist_song`
--

LOCK TABLES `playlist_song` WRITE;
/*!40000 ALTER TABLE `playlist_song` DISABLE KEYS */;
INSERT INTO `playlist_song` VALUES (1,1,'2025-04-06 08:22:41'),(1,2,'2025-04-06 08:22:41'),(1,3,'2025-04-06 08:22:41'),(1,4,'2025-04-06 08:22:41'),(1,5,'2025-04-06 08:22:41'),(1,6,'2025-04-06 08:22:41'),(1,7,'2025-04-06 08:22:41'),(1,8,'2025-04-06 08:22:41'),(1,9,'2025-04-06 08:22:41'),(1,10,'2025-04-06 08:22:41'),(1,11,'2025-04-06 08:22:41'),(1,12,'2025-04-06 08:22:41'),(1,13,'2025-04-06 08:22:41'),(1,14,'2025-04-06 08:22:41'),(1,15,'2025-04-06 08:22:41'),(1,16,'2025-04-06 08:22:41'),(1,17,'2025-04-06 08:22:41'),(1,18,'2025-04-06 08:22:41'),(1,19,'2025-04-06 08:22:41'),(1,20,'2025-04-06 08:22:41'),(1,21,'2025-04-06 08:22:41'),(1,22,'2025-04-06 08:22:41'),(1,23,'2025-04-06 08:22:41'),(1,24,'2025-04-06 08:22:41'),(1,25,'2025-04-06 08:22:41'),(1,26,'2025-04-06 08:22:41'),(1,27,'2025-04-06 08:22:41'),(1,28,'2025-04-06 08:22:41'),(1,29,'2025-04-06 08:22:41'),(1,30,'2025-04-06 08:22:41'),(1,31,'2025-04-06 08:22:41'),(1,32,'2025-04-06 08:22:41'),(1,33,'2025-04-06 08:22:41'),(1,34,'2025-04-06 08:22:41'),(1,35,'2025-04-06 08:22:41'),(1,36,'2025-04-06 08:22:41'),(1,37,'2025-04-06 08:22:41'),(1,38,'2025-04-06 08:22:41'),(1,39,'2025-04-06 08:22:41'),(1,40,'2025-04-06 08:22:41'),(1,41,'2025-04-06 08:22:41'),(1,42,'2025-04-06 08:22:41'),(1,43,'2025-04-06 08:22:41'),(1,44,'2025-04-06 08:22:41'),(1,45,'2025-04-06 08:22:41'),(1,46,'2025-04-06 08:22:41'),(1,47,'2025-04-06 08:22:41'),(1,48,'2025-04-06 08:22:41'),(1,49,'2025-04-06 08:22:41'),(1,50,'2025-04-06 08:22:41'),(1,51,'2025-04-06 08:22:41'),(1,52,'2025-04-06 08:22:41'),(1,53,'2025-04-06 08:22:41'),(1,54,'2025-04-06 08:22:41'),(1,55,'2025-04-06 08:22:41'),(1,56,'2025-04-06 08:22:41'),(1,57,'2025-04-06 08:22:41'),(1,58,'2025-04-06 08:22:41'),(1,59,'2025-04-06 08:22:41'),(1,60,'2025-04-06 08:22:41'),(1,61,'2025-04-06 08:22:41'),(1,62,'2025-04-06 08:22:41'),(1,63,'2025-04-06 08:22:41'),(1,64,'2025-04-06 08:22:41'),(1,65,'2025-04-06 08:22:41'),(1,66,'2025-04-06 08:22:41'),(1,67,'2025-04-06 08:22:41'),(1,68,'2025-04-06 08:22:41'),(1,69,'2025-04-06 08:22:41'),(1,70,'2025-04-06 08:22:41'),(1,71,'2025-04-06 08:22:41'),(1,72,'2025-04-06 08:22:41'),(1,73,'2025-04-06 08:22:41'),(1,74,'2025-04-06 08:22:41'),(1,75,'2025-04-06 08:22:41'),(1,76,'2025-04-06 08:22:41'),(1,77,'2025-04-06 08:22:41'),(1,78,'2025-04-06 08:22:41'),(1,79,'2025-04-06 08:22:41'),(1,80,'2025-04-06 08:22:41'),(1,81,'2025-04-06 08:22:41'),(1,82,'2025-04-06 08:22:41'),(1,83,'2025-04-06 08:22:41'),(1,84,'2025-04-06 08:22:41'),(1,85,'2025-04-06 08:22:41'),(1,86,'2025-04-06 08:22:41'),(1,87,'2025-04-06 08:22:41'),(1,88,'2025-04-06 08:22:41'),(1,89,'2025-04-06 08:22:41'),(1,90,'2025-04-06 08:22:41'),(1,91,'2025-04-06 08:22:41'),(1,92,'2025-04-06 08:22:41'),(1,93,'2025-04-06 08:22:41'),(1,94,'2025-04-06 08:22:41'),(1,95,'2025-04-06 08:22:41'),(1,96,'2025-04-06 08:22:41'),(1,97,'2025-04-06 08:22:41'),(1,98,'2025-04-06 08:22:41'),(1,99,'2025-04-06 08:22:41'),(1,100,'2025-04-06 08:22:41'),(1,101,'2025-04-06 08:22:41'),(1,102,'2025-04-06 08:22:41'),(1,103,'2025-04-06 08:22:41'),(1,104,'2025-04-06 08:22:41'),(1,105,'2025-04-06 08:22:41'),(1,106,'2025-04-06 08:22:41'),(1,107,'2025-04-06 08:22:41'),(1,108,'2025-04-06 08:22:41'),(1,109,'2025-04-06 08:22:41'),(1,110,'2025-04-06 08:22:41'),(1,111,'2025-04-06 08:22:41'),(1,112,'2025-04-06 08:22:41'),(1,113,'2025-04-06 08:22:41'),(1,114,'2025-04-06 08:22:41'),(1,115,'2025-04-06 08:22:41'),(1,116,'2025-04-06 08:22:41'),(1,117,'2025-04-06 08:22:41');
/*!40000 ALTER TABLE `playlist_song` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlist_songs`
--

DROP TABLE IF EXISTS `playlist_songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlist_songs` (
  `playlist_id` int NOT NULL,
  `song_id` int NOT NULL,
  PRIMARY KEY (`playlist_id`,`song_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `playlist_songs_ibfk_1` FOREIGN KEY (`playlist_id`) REFERENCES `playlist` (`id`),
  CONSTRAINT `playlist_songs_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `song` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlist_songs`
--

LOCK TABLES `playlist_songs` WRITE;
/*!40000 ALTER TABLE `playlist_songs` DISABLE KEYS */;
/*!40000 ALTER TABLE `playlist_songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `comment` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_id` int NOT NULL,
  `album_id` int NOT NULL,
  `is_public` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `album_id` (`album_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,4,'테스트 리뷰입니다.','2025-04-06 08:22:41','2025-04-06 08:22:41',1,1,1),(2,4,'테스트 리뷰입니다.','2025-04-06 08:22:41','2025-04-06 08:22:41',1,2,1),(3,4,'테스트 리뷰입니다.','2025-04-06 08:22:41','2025-04-06 08:22:41',1,3,1),(4,4,'테스트 리뷰입니다.','2025-04-06 08:22:41','2025-04-06 08:22:41',1,4,1),(5,4,'테스트 리뷰입니다.','2025-04-06 08:22:41','2025-04-06 08:22:41',1,5,1),(6,4,'테스트 리뷰입니다.','2025-04-06 08:22:41','2025-04-06 08:22:41',1,6,1),(7,4,'테스트 리뷰입니다.','2025-04-06 08:22:41','2025-04-06 08:22:41',1,7,1),(8,4,'테스트 리뷰입니다.','2025-04-06 08:22:41','2025-04-06 08:22:41',1,8,1);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `song`
--

DROP TABLE IF EXISTS `song`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `song` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `track_number` int DEFAULT NULL,
  `youtube_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastfm_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `album_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `album_id` (`album_id`),
  CONSTRAINT `song_ibfk_1` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `song`
--

LOCK TABLES `song` WRITE;
/*!40000 ALTER TABLE `song` DISABLE KEYS */;
INSERT INTO `song` VALUES (1,'Blood','1:58',1,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Blood',1),(2,'DNA','3:05',2,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./DNA',1),(3,'Yah','2:39',3,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Yah',1),(4,'Element','3:28',4,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Element',1),(5,'Feel','3:34',5,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Feel',1),(6,'Loyalty','3:47',6,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Loyalty',1),(7,'Pride','4:31',7,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Pride',1),(8,'HUMBLE.','2:59',8,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./HUMBLE.',1),(9,'Lust','5:08',9,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Lust',1),(10,'Love','3:31',10,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Love',1),(11,'XXX','4:14',11,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./XXX',1),(12,'Fear','6:54',12,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Fear',1),(13,'God','4:08',13,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./God',1),(14,'Duckworth','4:08',14,NULL,'https://www.last.fm/music/Kendrick+Lamar/DAMN./Duckworth',1),(15,'Just Dance','1:36',1,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Just+Dance',2),(16,'LoveGame','3:36',2,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/LoveGame',2),(17,'Paparazzi','3:28',3,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Paparazzi',2),(18,'Beautiful, Dirty, Rich','2:52',4,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Beautiful,+Dirty,+Rich',2),(19,'Eh, Eh (Nothing Else I Can Say)','2:56',5,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Eh,+Eh+(Nothing+Else+I+Can+Say)',2),(20,'Poker Face','3:58',6,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Poker+Face',2),(21,'The Fame','3:42',7,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/The+Fame',2),(22,'Money Honey','2:50',8,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Money+Honey',2),(23,'Again Again','3:05',9,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Again+Again',2),(24,'Boys Boys Boys','3:20',10,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Boys+Boys+Boys',2),(25,'Brown Eyes','4:02',11,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Brown+Eyes',2),(26,'Summerboy','4:14',12,NULL,'https://www.last.fm/music/Lady+Gaga/The+Fame/Summerboy',2),(27,'Starboy','3:49',1,NULL,'https://www.last.fm/music/The+Weeknd+Feat.+Daft+Punk/Starboy/Starboy',3),(28,'Party Monster','4:09',2,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Party+Monster',3),(29,'False Alarm','3:40',3,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/False+Alarm',3),(30,'Reminder','3:38',4,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Reminder',3),(31,'Rockin\'','3:53',5,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Rockin%27',3),(32,'Secrets','4:25',6,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Secrets',3),(33,'True Colors','3:26',7,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/True+Colors',3),(34,'Stargirl Interlude','1:53',8,NULL,'https://www.last.fm/music/The+Weeknd+feat.+Lana+Del+Rey/Starboy/Stargirl+Interlude',3),(35,'Sidewalks','3:51',9,NULL,'https://www.last.fm/music/The+Weeknd+feat.+Kendrick+Lamar/Starboy/Sidewalks',3),(36,'Six Feet Under','3:57',10,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Six+Feet+Under',3),(37,'Love to Lay','3:43',11,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Love+to+Lay',3),(38,'A Lonely Night','3:40',12,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/A+Lonely+Night',3),(39,'Attention','3:17',13,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Attention',3),(40,'Ordinary Life','3:41',14,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Ordinary+Life',3),(41,'Nothing Without You','3:18',15,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Nothing+Without+You',3),(42,'All I Know','0:59',16,NULL,'https://www.last.fm/music/The+Weeknd+Feat.+Future/Starboy/All+I+Know',3),(43,'Die for You','4:20',17,NULL,'https://www.last.fm/music/The+Weeknd/Starboy/Die+for+You',3),(44,'I Feel It Coming','3:49',18,NULL,'https://www.last.fm/music/The+Weeknd+Feat.+Daft+Punk/Starboy/I+Feel+It+Coming',3),(45,'Foreword','3:14',1,NULL,'https://www.last.fm/music/Tyler,+The+Creator+feat.+Rex+Orange+County/Flower+Boy/Foreword',4),(46,'Where This Flower Blooms','3:14',2,NULL,'https://www.last.fm/music/Tyler,+the+Creator/Flower+Boy/Where+This+Flower+Blooms',4),(47,'Sometimes...','0:36',3,NULL,'https://www.last.fm/music/Tyler,+the+Creator/Flower+Boy/Sometimes...',4),(48,'See You Again','3:00',4,NULL,'https://www.last.fm/music/Tyler,+The+Creator+Feat.+Kali+Uchis/Flower+Boy/See+You+Again',4),(49,'Who Dat Boy','1:51',5,NULL,'https://www.last.fm/music/Tyler,+The+Creator+Feat.+A$AP+Rocky/Flower+Boy/Who+Dat+Boy',4),(50,'Pothole','3:57',6,NULL,'https://www.last.fm/music/Tyler,+The+Creator+feat.+Jaden+Smith/Flower+Boy/Pothole',4),(51,'Garden Shed','3:43',7,NULL,'https://www.last.fm/music/Tyler,+The+Creator+Feat.+Estelle/Flower+Boy/Garden+Shed',4),(52,'Boredom','5:20',8,NULL,'https://www.last.fm/music/Tyler,+The+Creator+feat.+Rex+Orange+County+&+Anna+Of+the+North/Flower+Boy/Boredom',4),(53,'I Ain\'t Got Time!','0:00',9,NULL,'https://www.last.fm/music/Tyler,+the+Creator/Flower+Boy/I+Ain%27t+Got+Time!',4),(54,'911 / Mr. Lonely','4:15',10,NULL,'https://www.last.fm/music/Tyler,+The+Creator+feat.+Frank+Ocean+and+Steve+Lacy/Flower+Boy/911+%2F+Mr.+Lonely',4),(55,'Droppin\' Seeds','0:59',11,NULL,'https://www.last.fm/music/Tyler,+The+Creator+Feat.+Lil+Wayne/Flower+Boy/Droppin%27+Seeds',4),(56,'November','3:45',12,NULL,'https://www.last.fm/music/Tyler,+the+Creator/Flower+Boy/November',4),(57,'Glitter','11:30',13,NULL,'https://www.last.fm/music/Tyler,+the+Creator/Flower+Boy/Glitter',4),(58,'Enjoy Right Now, Today','3:55',14,NULL,'https://www.last.fm/music/Tyler,+the+Creator/Flower+Boy/Enjoy+Right+Now,+Today',4),(59,'!!!!!!!','0:13',1,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/!!!!!!!',5),(60,'bad guy','3:14',2,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/bad+guy',5),(61,'xanny','4:03',3,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/xanny',5),(62,'you should see me in a crown','3:00',4,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/you+should+see+me+in+a+crown',5),(63,'all the good girls go to hell','2:44',5,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/all+the+good+girls+go+to+hell',5),(64,'wish you were gay','3:41',6,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/wish+you+were+gay',5),(65,'when the party\'s over','3:19',7,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/when+the+party%27s+over',5),(66,'8','2:53',8,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/8',5),(67,'my strange addiction','2:59',9,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/my+strange+addiction',5),(68,'bury a friend','3:13',10,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/bury+a+friend',5),(69,'ilomilo','2:36',11,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/ilomilo',5),(70,'listen before i go','4:02',12,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/listen+before+i+go',5),(71,'i love you','4:51',13,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/i+love+you',5),(72,'goodbye','1:59',14,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/goodbye',5),(73,'When I Was Older (Music Inspired by the Movie Roma)','4:30',15,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/When+I+Was+Older+(Music+Inspired+by+the+Movie+Roma)',5),(74,'bitches broken hearts','2:56',16,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/bitches+broken+hearts',5),(75,'everything i wanted','4:05',17,NULL,'https://www.last.fm/music/Billie+Eilish/WHEN+WE+ALL+FALL+ASLEEP,+WHERE+DO+WE+GO%3F/everything+i+wanted',5),(76,'Femininomenon','3:39',1,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Femininomenon',6),(77,'Red Wine Supernova','3:12',2,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Red+Wine+Supernova',6),(78,'After Midnight','3:24',3,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/After+Midnight',6),(79,'Coffee','3:25',4,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Coffee',6),(80,'Casual','3:52',5,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Casual',6),(81,'Super Graphic Ultra Modern Girl','3:03',6,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Super+Graphic+Ultra+Modern+Girl',6),(82,'HOT TO GO!','3:04',7,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/HOT+TO+GO!',6),(83,'My Kink Is Karma','3:42',8,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/My+Kink+Is+Karma',6),(84,'Picture You','3:07',9,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Picture+You',6),(85,'Kaleidoscope','3:42',10,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Kaleidoscope',6),(86,'Pink Pony Club','4:18',11,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Pink+Pony+Club',6),(87,'Naked in Manhattan','3:31',12,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Naked+in+Manhattan',6),(88,'California','3:18',13,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/California',6),(89,'Guilty Pleasure','3:44',14,NULL,'https://www.last.fm/music/Chappell+Roan/The+Rise+and+Fall+of+a+Midwest+Princess/Guilty+Pleasure',6),(90,'Good Morning','3:15',1,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Good+Morning',7),(91,'Champion','2:47',2,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Champion',7),(92,'Stronger','5:11',3,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Stronger',7),(93,'I Wonder','4:04',4,NULL,'https://www.last.fm/music/Kanye+West/Graduation/I+Wonder',7),(94,'Good Life','4:30',5,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Good+Life',7),(95,'Can\'t Tell Me Nothing','4:32',6,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Can%27t+Tell+Me+Nothing',7),(96,'Barry Bonds','3:24',7,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Barry+Bonds',7),(97,'Drunk and Hot Girls','5:13',8,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Drunk+and+Hot+Girls',7),(98,'Flashing Lights','3:58',9,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Flashing+Lights',7),(99,'Everything I Am','3:47',10,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Everything+I+Am',7),(100,'The Glory','3:32',11,NULL,'https://www.last.fm/music/Kanye+West/Graduation/The+Glory',7),(101,'Homecoming','1:09',12,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Homecoming',7),(102,'Big Brother','4:47',13,NULL,'https://www.last.fm/music/Kanye+West/Graduation/Big+Brother',7),(103,'360','2:13',1,NULL,'https://www.last.fm/music/Charli+xcx/BRAT/360',8),(104,'Club classics','2:33',2,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/Club+classics',8),(105,'Sympathy is a knife','2:34',3,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/Sympathy+is+a+knife',8),(106,'I might say something stupid','4:10',4,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/I+might+say+something+stupid',8),(107,'Talk talk','2:41',5,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/Talk+talk',8),(108,'Von dutch','2:44',6,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/Von+dutch',8),(109,'Everything is romantic','3:23',7,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/Everything+is+romantic',8),(110,'Rewind','2:42',8,NULL,'https://www.last.fm/music/Charli+xcx/BRAT/Rewind',8),(111,'So I','4:39',9,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/So+I',8),(112,'Girl, so confusing','3:25',10,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/Girl,+so+confusing',8),(113,'Apple','2:31',11,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/Apple',8),(114,'B2b','2:58',12,NULL,'https://www.last.fm/music/Charli+xcx/BRAT/B2b',8),(115,'Mean girls','3:46',13,NULL,'https://www.last.fm/music/Charli+XCX/BRAT/Mean+girls',8),(116,'I think about it all the time','3:20',14,NULL,'https://www.last.fm/music/Charli+xcx/BRAT/I+think+about+it+all+the+time',8),(117,'365','2:01',15,NULL,'https://www.last.fm/music/Charli+xcx/BRAT/365',8);
/*!40000 ALTER TABLE `song` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'testuser','test@example.com','pbkdf2:sha256:260000$1UuIiazGHuEREcZC$034f62157714ea87672d6097ff1465c114c212c8978306cdc04fc670fe020e91');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-06 17:26:17
