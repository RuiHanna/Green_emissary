-- MySQL dump 10.13  Distrib 5.7.31, for Win64 (x86_64)
--
-- Host: localhost    Database: quiz_app
-- ------------------------------------------------------
-- Server version	5.7.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `options`
--

DROP TABLE IF EXISTS `options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `option_text` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `options_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `options`
--

LOCK TABLES `options` WRITE;
/*!40000 ALTER TABLE `options` DISABLE KEYS */;
INSERT INTO `options` VALUES (1,3,'小麦'),(2,3,'大豆'),(3,3,'玉米'),(4,3,'水稻'),(5,4,'氮肥、磷肥、钾肥'),(6,4,'磷肥、钾肥、氮肥'),(7,4,'钾肥、氮肥、磷肥'),(8,4,'钾肥、磷肥、氮肥'),(9,5,'民族团结'),(10,5,'扶贫'),(11,5,'环境保护'),(12,5,'资源开发'),(13,1,'A. 胞间连丝'),(14,1,'B. 纤维素'),(15,1,'C. 纤丝'),(16,1,'D. 木质'),(17,2,'A. 玉米'),(18,2,'B. 瘦肉精（盐酸克伦特罗）'),(19,2,'C. 食盐'),(20,2,'D. 维生素'),(21,6,'A. 110℃～130℃'),(22,6,'B. 135℃～150℃'),(23,6,'C. 180℃～250℃'),(24,6,'D. 200℃～250℃'),(25,7,'A. 玉米'),(26,7,'B. 马铃薯'),(27,7,'C. 蔬菜'),(28,7,'D. 棉花'),(29,8,'A. 追求时尚 保护环境'),(30,8,'B. 保护环境 崇尚自然'),(31,8,'C. 保护环境 适度消费'),(32,8,'D. 开发资源 享受生活'),(33,9,'A. 保护衣物'),(34,9,'B. 防止污染，防止水体富养化'),(35,9,'C. 保护双手'),(36,10,'A. 上胚轴'),(37,10,'B. 下胚轴'),(38,10,'C. 胚根'),(39,10,'D. 胚芽'),(40,11,'A. 喀纳斯湖保护区'),(41,11,'B. 天池保护区'),(42,11,'C. 阿尔金山保护区'),(43,11,'D. 祁连山保护区'),(44,12,'A. 科技'),(45,12,'B. 经济'),(46,12,'C. 环保'),(47,12,'D. 文化'),(48,13,'A. 叶隙'),(49,13,'B. 叶迹'),(50,13,'C. 形成层'),(51,13,'D. 离层'),(52,14,'A. 9'),(53,14,'B. 10'),(54,14,'C. 11'),(55,14,'D. 12'),(56,15,'A. 1995年'),(57,15,'B. 1996年'),(58,15,'C. 1997年'),(59,15,'D. 1998年'),(60,16,'A、200吨'),(61,16,'B、300吨'),(62,16,'C、400吨'),(63,16,'D、500吨'),(64,17,'A、农村、农业和农民'),(65,17,'B、农具、农业和农民'),(66,17,'C、农技、农业和农民'),(67,17,'D、农化、农业和农医'),(68,18,'A、给予、创收和放活'),(69,18,'B、开放、创新和综合治理'),(70,18,'C、多予，少取和开放'),(71,18,'D、多予，少取和放活'),(72,19,'A、机械化、产业化'),(73,19,'B、电气化、产业化、商品化'),(74,19,'C、机械化、电气化、产业化、商品化'),(75,19,'D、机械化、产业化、商品化'),(76,20,'A、米类、豆类和薯类'),(77,20,'B、谷类、蔬类和薯类'),(78,20,'C、谷类、豆类和薯类'),(79,21,'A、生态效益，社会效益，经济效益'),(80,21,'B、环境效益，社会效益，经济效益'),(81,21,'C、生态效益，环境效益，经济效益'),(82,22,'A、病虫害，乱砍滥伐，植树造林'),(83,22,'B、病虫害，森林火灾，偷盗伐木'),(84,22,'C、森林火灾，病虫害，乱砍滥伐'),(85,23,'A、垃圾污染'),(86,23,'B、大气污染'),(87,23,'C、土地荒漠污染'),(88,24,'A、维A'),(89,24,'B、维D'),(90,24,'C、维C'),(91,25,'A、可逆性'),(92,25,'B、可塑性'),(93,25,'C、弹性'),(94,25,'D、刚性'),(95,26,'A、21%'),(96,26,'B、31%'),(97,26,'C、41%'),(98,27,'A、配子'),(99,27,'B、孢子'),(100,27,'C、合子'),(101,27,'D、种子'),(102,28,'A、器官'),(103,28,'B、分子'),(104,28,'C、组织'),(105,28,'D、细胞');
/*!40000 ALTER TABLE `options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_text` text CHARACTER SET utf8mb4 NOT NULL,
  `type` enum('multiple','true_false') CHARACTER SET utf8mb4 NOT NULL,
  `correct_answer` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,'植物进行光合作用时需要二氧化碳吗？','true_false','正确'),(2,'害虫等于虫害？','true_false','错误'),(3,'下列哪种作物属于豆科？','multiple','大豆'),(4,'氮、磷、钾化肥对环境产生危害从高到低的顺序是？','multiple','氮肥、磷肥、钾肥'),(5,'我国确立（）为一项基本国策。','multiple','环境保护'),(6,'细胞壁上（）的存在，使多细胞植物体在结构和生理功能上成为一个统一的有机体。','multiple','A. 胞间连丝'),(7,'根据国家有关规定，以下哪一种药物是国家明文禁止添加的违禁药物，不能作为饲料添加剂使用。','multiple','B. 瘦肉精（盐酸克伦特罗）'),(8,'超高温杀菌技术，是指将流体或半流体在2.8秒内瞬间加热，然后再迅速冷却到30℃～40℃的杀菌技术。瞬间加热所需的温度是？','multiple','B. 135℃～150℃'),(9,'我市地膜覆盖面积最大的是以下那一种农作物？','multiple','A. 玉米'),(10,'随着绿色消费运动的发展，全球已逐渐形成一种（）的生活风尚。','multiple','B. 保护环境 崇尚自然'),(11,'我们生活中，选无磷洗衣粉目的是？','multiple','B. 防止污染，防止水体富养化'),(12,'大豆种子萌发形成子叶出土的幼苗，其主要原因是（）生长迅速。','multiple','B. 下胚轴'),(13,'我国面积最大的自然保护区是？','multiple','C. 阿尔金山保护区'),(14,'每个时代，都会产生一个新名词，那么21世纪是（）世纪，四个答案选一个比较正确的？','multiple','D. 文化'),(15,'从解剖结构上看，植物落叶主要是在叶柄基部产生了（）。','multiple','D. 离层'),(16,'中华人民共和国农业法第八章专门用于农业资源与农业环境保护的表述，共有多少条？','multiple','B. 10'),(17,'中华人民共和国野生植物保护条例于哪一年颁布实施？','multiple','C. 1997年'),(18,'今年省农业环保站规定，加工多少吨塑料粒子以上才能享受项目资金补贴？','multiple','C、400吨'),(19,'什么是三农问题？','multiple','A、农村、农业和农民'),(20,'解决三农问题的基本方针是什么？','multiple','D、多予，少取和放活'),(21,'现代农业的构成要素有哪些？','multiple','C、机械化、电气化、产业化、商品化'),(22,'按照植物学特征和用途，粮食作物分为哪三类？','multiple','C、谷类、豆类和薯类'),(23,'森林的三大效益是什么？','multiple','A、生态效益，社会效益，经济效益'),(24,'什么是林业的“三害”？','multiple','C、森林火灾，病虫害，乱砍滥伐'),(25,'世界十大环境污染之首是？','multiple','B、大气污染'),(26,'补充哪种维生素有利于儿童骨骼生长?','multiple','B、维D'),(27,'细胞生长时，细胞壁表现一定的？','multiple','C、弹性'),(28,'清洁的空气中含有多少氧？','multiple','A、21%'),(29,'无性生殖是植物体产生许多称为（  ）的生殖细胞不经结合而直接发育成新个体的生殖方式。','multiple','B、孢子'),(30,'生物体的基本单位是？','multiple','D、细胞');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-08 21:21:38
